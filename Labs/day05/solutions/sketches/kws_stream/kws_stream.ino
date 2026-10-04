// kws_stream - keyword spotting on a stream with the Edge Impulse library
//
// Day 5 lab, Part A. Edge Impulse Studio trains the keyword model and makes
// an Arduino library. This sketch runs that library on a sliding window and
// makes one event for each spoken keyword. Tasks A1 and A2 of the lab are in
// the file postprocess.h, not in this file.
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
// FQBN:      esp32:esp32:XIAO_ESP32S3:PSRAM=opi (Tools > PSRAM > OPI PSRAM)
// Core:      esp32 by Espressif Systems 3.3.12. The library ESP_I2S is in
//            the core, from version 3.0. If the build of the Edge Impulse
//            library fails with this core, use the core 2.0.17: the sketch
//            then uses the microphone lines of the source sketch.
// Libraries: the Arduino library of your Edge Impulse project (model type
//            "Quantized (int8)"), U8g2 2.36.19
// Serial:    115200 baud
//
// Hardware status: changed code, not tested on hardware (prepared on
// 2026-10-02). The sketch needs the library of an Edge Impulse project.
// Only the Studio can make that library. The sketch compiles with a
// replacement for that library, which is not in this repository.
//
// Before you compile: change the first #include line to the name of the
// header of your library. The name comes from the name of your project.
//
// What the sketch does:
//   1. A task reads the microphone all the time into a ring buffer of 2 s.
//   2. Each STRIDE_MS, the loop copies the newest window and runs the
//      features and the model of the library on it.
//   3. The post-processing of postprocess.h makes events from the results.
//   4. The Serial Monitor gets one line for each window. The display shows
//      an event for one second.
//
// Credits: this sketch adapts
// XIAOML_Kit_code/xiaoml-kit_kws_oled/xiaoml-kit_kws_oled.ino of "XIAO
// ESP32S3 Sense" by Marcelo Rovai (github.com/Mjrovai/XIAO-ESP32S3-Sense,
// Apache-2.0). That sketch adapts the example "esp32_microphone" of Edge
// Impulse. The notice of Edge Impulse follows this comment.
// Changes from the source:
//   - With the core 3.x, the microphone uses the library ESP_I2S. The source
//     uses the library I2S of the core 2.0.17, which the core 3.x does not
//     have. The lines of the source are still in the sketch, for a build
//     with the core 2.0.17. The pin numbers (42 and 41), the sampling rate,
//     and the gain of 8 are the values of the source.
//   - New: the ring buffer and the sliding window. The source runs the model
//     one time for each second, on windows with no overlap.
//   - New: the post-processing, the output lines, and the settings below.
//   - The display code is shorter.

/* Edge Impulse Arduino examples
 * Copyright (c) 2022 EdgeImpulse Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

// If your target is limited in memory remove this macro to save 10K RAM
#define EIDSP_QUANTIZE_FILTERBANK   0

// Change this line to the header of the library of your project.
#include <XIAO-ESP32S3-KWS_inferencing.h>
#if ESP_ARDUINO_VERSION_MAJOR >= 3
#include <ESP_I2S.h>
I2SClass I2S;
#else
#include <I2S.h>
#endif
#include <U8g2lib.h>
#include <Wire.h>

#include "postprocess.h"

// ---- Settings of Part A ------------------------------------------------------

// Time between the starts of two windows. The work for one window must be
// shorter. If it is longer, the sketch uses the real time and prints it.
#define STRIDE_MS 250

// Number of windows for the mean, from 1 to 8 (task A1).
#define SMOOTH_WINDOWS 3

// Smallest mean probability of a keyword for an event.
#define THRESHOLD 0.60f

// Time after an event with no new event (task A2).
#define SUPPRESSION_MS 1000

// The classes with these names are not keywords.
const char* const kNotKeyword[] = {"noise", "unknown", "background"};

// -----------------------------------------------------------------------------

#define SAMPLE_RATE 16000U
#define LED_PIN 21                 // built-in LED, on with LOW
#define DISPLAY_DURATION_MS 1000   // time that the display shows an event

U8G2_SSD1306_72X40_ER_1_HW_I2C u8g2(U8G2_R2, U8X8_PIN_NONE);

// Ring buffer with the newest 2 s of sound. The capture task writes it.
static const uint32_t kRingSamples = 2 * SAMPLE_RATE;
static int16_t* ring = nullptr;
static volatile uint32_t ring_write = 0;      // position of the next sample
static volatile uint32_t samples_total = 0;   // samples since the start

// One window for the model, with the oldest sample first.
static int16_t* window_buffer = nullptr;

static const uint32_t kChunkSamples = 512;    // samples of one microphone read
static int16_t chunk[kChunkSamples];

static bool debug_nn = false;   // true: print the features of each window

PostProcess post;
bool is_keyword[kMaxClasses];
unsigned long events_total = 0;
unsigned long last_window_ms = 0;
unsigned long last_event_ms = 0;
int last_event_class = -1;

void showLines(const char* line1, const char* line2) {
  u8g2.firstPage();
  do {
    u8g2.setFont(u8g2_font_6x10_tr);
    u8g2.setCursor(2, 14);
    u8g2.print(line1);
    u8g2.setCursor(2, 30);
    u8g2.print(line2);
    u8g2.drawFrame(0, 0, 72, 40);
  } while (u8g2.nextPage());
}

void stop(const char* message) {
  Serial.println(message);
  showLines("ERROR", "see serial");
  while (true) {
    delay(1000);
  }
}

// The capture task: read the microphone and write the ring buffer.
static void capture_samples(void* arg) {
  while (true) {
#if ESP_ARDUINO_VERSION_MAJOR >= 3
    const size_t bytes_read =
        I2S.readBytes((char*)chunk, kChunkSamples * sizeof(int16_t));
#else
    size_t bytes_read = 0;
    esp_i2s::i2s_read(esp_i2s::I2S_NUM_0, (void*)chunk,
                      kChunkSamples * sizeof(int16_t), &bytes_read, 100);
#endif
    const uint32_t samples = bytes_read / sizeof(int16_t);
    uint32_t position = ring_write;
    for (uint32_t i = 0; i < samples; i++) {
      // The gain of 8 is the gain of the source sketch: the sound is too
      // quiet without it.
      int32_t value = (int32_t)chunk[i] * 8;
      if (value > 32767) {
        value = 32767;
      }
      if (value < -32768) {
        value = -32768;
      }
      ring[position] = (int16_t)value;
      position = (position + 1) % kRingSamples;
    }
    ring_write = position;
    samples_total += samples;
    if (samples == 0) {
      delay(1);
    }
  }
}

// Copy the newest window of the ring buffer, with the oldest sample first.
static void copy_newest_window() {
  const uint32_t end = ring_write;
  uint32_t position =
      (end + kRingSamples - EI_CLASSIFIER_RAW_SAMPLE_COUNT) % kRingSamples;
  for (uint32_t i = 0; i < EI_CLASSIFIER_RAW_SAMPLE_COUNT; i++) {
    window_buffer[i] = ring[position];
    position = (position + 1) % kRingSamples;
  }
}

// The library reads the window through this function.
static int microphone_audio_signal_get_data(size_t offset, size_t length,
                                            float* out_ptr) {
  numpy::int16_to_float(&window_buffer[offset], out_ptr, length);
  return 0;
}

static void* allocate(size_t bytes) {
  void* memory = nullptr;
  if (psramFound()) {
    memory = heap_caps_malloc(bytes, MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);
  }
  if (memory == nullptr) {
    memory = malloc(bytes);
  }
  return memory;
}

void setup() {
  Serial.begin(115200);
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }
  Serial.println("kws_stream");

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);   // LED off
  u8g2.begin();
  showLines("Day 5", "KWS");

  if (EI_CLASSIFIER_LABEL_COUNT > kMaxClasses) {
    stop("ERROR: the model has more classes than kMaxClasses.");
  }
  if (SMOOTH_WINDOWS < 1 || SMOOTH_WINDOWS > kMaxHistory) {
    stop("ERROR: SMOOTH_WINDOWS must be from 1 to 8.");
  }

  // The microphone: PDM clock on pin 42, PDM data on pin 41.
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  I2S.setPinsPdmRx(42, 41);
  if (!I2S.begin(I2S_MODE_PDM_RX, SAMPLE_RATE, I2S_DATA_BIT_WIDTH_16BIT,
                 I2S_SLOT_MODE_MONO)) {
    stop("ERROR: failed to initialize I2S!");
  }
#else
  I2S.setAllPins(-1, 42, 41, -1, -1);
  if (!I2S.begin(PDM_MONO_MODE, SAMPLE_RATE, 16)) {
    stop("ERROR: failed to initialize I2S!");
  }
#endif

  ring = (int16_t*)allocate(kRingSamples * sizeof(int16_t));
  window_buffer =
      (int16_t*)allocate(EI_CLASSIFIER_RAW_SAMPLE_COUNT * sizeof(int16_t));
  if (ring == nullptr || window_buffer == nullptr) {
    stop("ERROR: not enough memory for the audio buffers.");
  }
  memset(ring, 0, kRingSamples * sizeof(int16_t));

  // The settings of the model, and the classes that are keywords.
  Serial.printf("Window:       %d samples (%d ms)\n",
                (int)EI_CLASSIFIER_RAW_SAMPLE_COUNT,
                (int)(EI_CLASSIFIER_RAW_SAMPLE_COUNT * 1000 / SAMPLE_RATE));
  Serial.printf("Features:     %d values\n", (int)EI_CLASSIFIER_NN_INPUT_FRAME_SIZE);
  Serial.printf("Classes:      %d\n", (int)EI_CLASSIFIER_LABEL_COUNT);
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    is_keyword[ix] = true;
    for (const char* name : kNotKeyword) {
      if (strcmp(ei_classifier_inferencing_categories[ix], name) == 0) {
        is_keyword[ix] = false;
      }
    }
    Serial.printf("  %d: %s%s\n", (int)ix,
                  ei_classifier_inferencing_categories[ix],
                  is_keyword[ix] ? " (keyword)" : "");
  }
  Serial.printf("Stride:       %d ms\n", STRIDE_MS);
  Serial.printf("Mean of:      %d windows\n", SMOOTH_WINDOWS);
  Serial.printf("Threshold:    %.2f\n", THRESHOLD);
  Serial.printf("Suppression:  %d ms\n", SUPPRESSION_MS);
  Serial.printf("Task A1: %s. Task A2: %s.\n",
                kTaskA1Complete ? "complete" : "not complete, no mean",
                kTaskA2Complete ? "complete" : "not complete, no suppression");
  Serial.printf("PSRAM:        %s\n", psramFound() ? "active" : "not active");
  Serial.printf("Free heap:    %lu bytes\n", (unsigned long)ESP.getFreeHeap());

  xTaskCreate(capture_samples, "CaptureSamples", 1024 * 8, nullptr, 10, nullptr);

  // Wait until the ring buffer holds one complete window.
  while (samples_total < EI_CLASSIFIER_RAW_SAMPLE_COUNT) {
    delay(10);
  }

  Serial.print("stride_ms,dsp_ms,classification_ms");
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    Serial.printf(",%s", ei_classifier_inferencing_categories[ix]);
  }
  Serial.println(",event");
  showLines("Listening", "");
  last_window_ms = millis();
}

void loop() {
  // Wait for the start of the next window.
  const unsigned long now = millis();
  if (now - last_window_ms < STRIDE_MS) {
    delay(1);
    return;
  }
  const unsigned long stride_ms = now - last_window_ms;
  last_window_ms = now;

  // Pre-process and infer: the library does the two steps.
  copy_newest_window();
  signal_t signal;
  signal.total_length = EI_CLASSIFIER_RAW_SAMPLE_COUNT;
  signal.get_data = &microphone_audio_signal_get_data;
  ei_impulse_result_t result = { 0 };
  EI_IMPULSE_ERROR error = run_classifier(&signal, &result, debug_nn);
  if (error != EI_IMPULSE_OK) {
    Serial.printf("ERROR: failed to run the classifier (%d)\n", (int)error);
    return;
  }

  // Post-process: store the result and decide.
  float probabilities[kMaxClasses];
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    probabilities[ix] = result.classification[ix].value;
  }
  pp_add(post, probabilities, EI_CLASSIFIER_LABEL_COUNT);
  const int event = pp_event(post, is_keyword, EI_CLASSIFIER_LABEL_COUNT,
                             SMOOTH_WINDOWS, THRESHOLD, SUPPRESSION_MS,
                             millis());

  // One line for each window.
  Serial.printf("%lu,%d,%d", stride_ms, (int)result.timing.dsp,
                (int)result.timing.classification);
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    Serial.printf(",%.2f", probabilities[ix]);
  }
  if (event >= 0) {
    events_total++;
    last_event_ms = millis();
    last_event_class = event;
    Serial.printf(",%s (event %lu)\n", result.classification[event].label,
                  events_total);
  } else {
    Serial.println(",none");
  }

  // Act: the display and the LED show an event for one second.
  if (last_event_class >= 0 && millis() - last_event_ms < DISPLAY_DURATION_MS) {
    if (event >= 0) {
      char line2[16];
      snprintf(line2, sizeof(line2), "event %lu", events_total);
      digitalWrite(LED_PIN, LOW);
      showLines(result.classification[last_event_class].label, line2);
    }
  } else if (last_event_class >= 0) {
    last_event_class = -1;
    digitalWrite(LED_PIN, HIGH);
    showLines("Listening", "");
  }
}

#if !defined(EI_CLASSIFIER_SENSOR) || EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_MICROPHONE
#error "Invalid model for current sensor."
#endif
