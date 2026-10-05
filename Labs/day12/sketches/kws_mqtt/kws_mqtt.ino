// kws_mqtt - keyword events from the XIAOML Kit to the MQTT broker
//
// Day 12 lab, Parts B to D. The keyword model of your Day 5 lab runs on a
// sliding window. Each keyword event goes to the broker on the Raspberry Pi
// as one MQTT message. The LED follows the commands of the Raspberry Pi.
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
// FQBN:      esp32:esp32:XIAO_ESP32S3:PSRAM=opi (Tools > PSRAM > OPI PSRAM)
// Core:      esp32 by Espressif Systems 3.3.12 (see the Day 5 lab for the
//            core 2.0.17)
// Libraries: the Arduino library of your Day 5 Edge Impulse project (model
//            type "Quantized (int8)"), PubSubClient 2.8 (Nick O'Leary),
//            U8g2 2.36.19
// Broker:    Mosquitto on the Raspberry Pi of the group (port 1883)
// Serial:    115200 baud
//
// Before you compile:
//   1. Change the #include line of the library to the header of your Day 5
//      library. The name comes from the name of your project.
//   2. Write the Wi-Fi password, the address of your Raspberry Pi, and your
//      group in arduino_secrets.h.
//
// Topics (GROUP_ID is in arduino_secrets.h):
//   edgeai/<group>/xiao/status   "online" or "offline", retained, last will
//   edgeai/<group>/xiao/result   one message for each keyword event:
//                                {"seq":3,"ms":81234,"label":"yes","score":0.91}
//   edgeai/<group>/xiao/stats    one message each 10 s:
//                                {"seq":8,"ms":80000,"windows":312,"events":3,
//                                 "heap":201234}
//   edgeai/<group>/xiao/cmd      command to the board: "led=1" or "led=0"

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
#include <PubSubClient.h>
#include <U8g2lib.h>
#include <WiFi.h>
#include <Wire.h>

#include "arduino_secrets.h"
#include "postprocess.h"

// ---- Settings of the post-processing (the values of the Day 5 lab) -----------

#define STRIDE_MS 250              // time between the starts of two windows
#define SMOOTH_WINDOWS 3           // number of windows for the mean
#define THRESHOLD 0.60f            // smallest mean probability of an event
#define SUPPRESSION_MS 1000        // time after an event with no new event

// The classes with these names are not keywords.
const char* const kNotKeyword[] = {"noise", "unknown", "background"};

// ---- Settings of the network --------------------------------------------------

const char* kSsid = SECRET_SSID;
const char* kPassword = SECRET_PASS;
const char* kBroker = MQTT_BROKER;
const uint16_t kPort = 1883;

const char* kClientId = "xiao-" GROUP_ID;
const char* kTopicStatus = "edgeai/" GROUP_ID "/xiao/status";
const char* kTopicResult = "edgeai/" GROUP_ID "/xiao/result";
const char* kTopicStats = "edgeai/" GROUP_ID "/xiao/stats";
const char* kTopicCmd = "edgeai/" GROUP_ID "/xiao/cmd";

const unsigned long kRetryPeriodMs = 5000;    // one connection attempt each 5 s
const unsigned long kStatsPeriodMs = 10000;   // one stats message each 10 s

// -----------------------------------------------------------------------------

#define SAMPLE_RATE 16000U
#define LED_PIN 21                 // built-in LED, on with LOW
#define DISPLAY_DURATION_MS 1000   // time that the display shows an event

U8G2_SSD1306_72X40_ER_1_HW_I2C u8g2(U8G2_R2, U8X8_PIN_NONE);
WiFiClient espClient;
PubSubClient client(espClient);

// Ring buffer with the newest 2 s of sound. The capture task writes it.
static const uint32_t kRingSamples = 2 * SAMPLE_RATE;
static int16_t* ring = nullptr;
static volatile uint32_t ring_write = 0;      // position of the next sample
static volatile uint32_t samples_total = 0;   // samples since the start

// One window for the model, with the oldest sample first.
static int16_t* window_buffer = nullptr;

static const uint32_t kChunkSamples = 512;    // samples of one microphone read
static int16_t chunk[kChunkSamples];

PostProcess post;
bool is_keyword[kMaxClasses];
unsigned long events_total = 0;
unsigned long windows_total = 0;
unsigned long last_window_ms = 0;
unsigned long last_event_ms = 0;
unsigned long last_retry_ms = 0;
unsigned long last_stats_ms = 0;
unsigned long result_seq = 0;
unsigned long stats_seq = 0;
int last_event_class = -1;
char payload[160];

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

// ---- Microphone (from the Day 5 sketch) ---------------------------------------

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
      // The gain of 8 is the gain of the source sketch.
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

// ---- Network (from the HW-07 sketch) ------------------------------------------

// The broker calls this function for each message on the command topic.
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Command: ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
  }
  Serial.println();
  if (length == 5 && memcmp(message, "led=1", 5) == 0) {
    digitalWrite(LED_PIN, LOW);    // on
  } else if (length == 5 && memcmp(message, "led=0", 5) == 0) {
    digitalWrite(LED_PIN, HIGH);   // off
  }
}

// Try one time to connect. Return true when the connection is open.
bool connectBroker() {
  Serial.printf("MQTT: connecting to %s ... ", kBroker);
  // Last will: the broker sends "offline" when the board disappears.
  if (client.connect(kClientId, kTopicStatus, 1, true, "offline")) {
    Serial.println("connected");
    client.publish(kTopicStatus, "online", true);
    client.subscribe(kTopicCmd, 1);
    return true;
  }
  Serial.printf("failed, rc=%d\n", client.state());
  return false;
}

// Keep the connection open. The function never waits for the broker longer
// than one connection attempt.
void serviceNetwork(unsigned long now) {
  if (WiFi.status() != WL_CONNECTED) {
    return;                        // the core connects again without help
  }
  if (!client.connected()) {
    if (last_retry_ms == 0 || now - last_retry_ms >= kRetryPeriodMs) {
      last_retry_ms = now;
      connectBroker();
    }
    return;
  }
  client.loop();
}

// One message for each keyword event. QoS 0: PubSubClient sends no other.
void publishEvent(const char* label, float score) {
  result_seq++;
  snprintf(payload, sizeof(payload),
           "{\"seq\":%lu,\"ms\":%lu,\"label\":\"%s\",\"score\":%.2f}",
           result_seq, millis(), label, score);
  const bool sent = client.connected() && client.publish(kTopicResult, payload);
  Serial.printf("MQTT %s: %s\n", sent ? "sent" : "NOT SENT", payload);
}

void publishStats(unsigned long now) {
  stats_seq++;
  snprintf(payload, sizeof(payload),
           "{\"seq\":%lu,\"ms\":%lu,\"windows\":%lu,\"events\":%lu,"
           "\"heap\":%lu}",
           stats_seq, now, windows_total, events_total,
           (unsigned long)ESP.getFreeHeap());
  if (client.connected()) {
    client.publish(kTopicStats, payload);
  }
}

// ---- Setup and loop -----------------------------------------------------------

void setup() {
  Serial.begin(115200);
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }
  Serial.println("kws_mqtt");

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);   // LED off
  u8g2.begin();
  showLines("Day 12", "KWS MQTT");

  if (EI_CLASSIFIER_LABEL_COUNT > kMaxClasses) {
    stop("ERROR: the model has more classes than kMaxClasses.");
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

  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    is_keyword[ix] = true;
    for (const char* name : kNotKeyword) {
      if (strcmp(ei_classifier_inferencing_categories[ix], name) == 0) {
        is_keyword[ix] = false;
      }
    }
    Serial.printf("  class %d: %s%s\n", (int)ix,
                  ei_classifier_inferencing_categories[ix],
                  is_keyword[ix] ? " (keyword)" : "");
  }

  // The network. The loop connects to the broker.
  Serial.printf("Wi-Fi: %s ", kSsid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(kSsid, kPassword);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nWi-Fi connected. IP address: %s\n",
                WiFi.localIP().toString().c_str());
  client.setServer(kBroker, kPort);
  client.setCallback(callback);
  client.setKeepAlive(15);
  Serial.printf("Group %s, topics edgeai/%s/xiao/...\n", GROUP_ID, GROUP_ID);

  xTaskCreate(capture_samples, "CaptureSamples", 1024 * 8, nullptr, 10, nullptr);
  while (samples_total < EI_CLASSIFIER_RAW_SAMPLE_COUNT) {
    delay(10);
  }
  showLines("Listening", "");
  last_window_ms = millis();
  last_stats_ms = millis();
}

void loop() {
  const unsigned long now = millis();
  serviceNetwork(now);

  if (now - last_stats_ms >= kStatsPeriodMs) {
    last_stats_ms = now;
    publishStats(now);
  }

  // Wait for the start of the next window.
  if (now - last_window_ms < STRIDE_MS) {
    delay(1);
    return;
  }
  last_window_ms = now;

  // Pre-process and infer: the library does the two steps.
  copy_newest_window();
  signal_t signal;
  signal.total_length = EI_CLASSIFIER_RAW_SAMPLE_COUNT;
  signal.get_data = &microphone_audio_signal_get_data;
  ei_impulse_result_t result = { 0 };
  EI_IMPULSE_ERROR error = run_classifier(&signal, &result, false);
  if (error != EI_IMPULSE_OK) {
    Serial.printf("ERROR: failed to run the classifier (%d)\n", (int)error);
    return;
  }
  windows_total++;

  // Post-process: the mean of the last windows, the threshold, and the
  // suppression time of the Day 5 lab.
  float probabilities[kMaxClasses];
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    probabilities[ix] = result.classification[ix].value;
  }
  pp_add(post, probabilities, EI_CLASSIFIER_LABEL_COUNT);
  const int event = pp_event(post, is_keyword, EI_CLASSIFIER_LABEL_COUNT,
                             SMOOTH_WINDOWS, THRESHOLD, SUPPRESSION_MS,
                             millis());

  if (event >= 0) {
    events_total++;
    last_event_ms = millis();
    last_event_class = event;
    publishEvent(result.classification[event].label,
                 pp_mean(post, event, SMOOTH_WINDOWS));
    char line2[16];
    snprintf(line2, sizeof(line2), "event %lu", events_total);
    showLines(result.classification[event].label, line2);
  } else if (last_event_class >= 0 &&
             millis() - last_event_ms >= DISPLAY_DURATION_MS) {
    last_event_class = -1;
    showLines("Listening", "");
  }
}

#if !defined(EI_CLASSIFIER_SENSOR) || EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_MICROPHONE
#error "Invalid model for current sensor."
#endif
