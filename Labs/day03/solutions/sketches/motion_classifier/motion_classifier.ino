// motion_classifier - classify four motions on the XIAOML Kit
//
// Solution of the Day 3 lab (tasks B1 to B4 are complete).
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
// FQBN:      esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Libraries: Chirale_TensorFlowLite 2.0.0, Seeed Arduino LSM6DS3 2.0.7,
//            U8g2 2.36.19
// Serial:    115200 baud
// Files:     model.h, model_settings.h, and test_window.h come from the
//            notebook motion_classifier.ipynb. motion_features.h has the
//            feature code.
//
// What the sketch does:
//   1. At the start it tests the feature code and the model with the window
//      of test_window.h, and it prints the memory numbers.
//   2. It reads the IMU 50 times each second into a ring buffer of 2 s.
//   3. After each 10 samples (0.2 s) it calculates the 63 features of the
//      newest window, runs the model, and shows the class on the display.

#include <Chirale_TensorFlowLite.h>
#include <LSM6DS3.h>
#include <U8g2lib.h>
#include <Wire.h>

#include "esp_heap_caps.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

#include "motion_features.h"
#include "model.h"
#include "model_settings.h"
#include "test_window.h"

// ---- Settings for the measurements of Part C --------------------------------

// Size of the arena. Start large. Then use the value "Arena used" of the
// Serial Monitor plus a small margin.
constexpr size_t kTensorArenaSize = 4 * 1024;

// 0: arena in the internal RAM.
// 1: arena in the PSRAM. Needs Tools > PSRAM > OPI PSRAM.
#ifndef ARENA_IN_PSRAM
#define ARENA_IN_PSRAM 0
#endif

// -----------------------------------------------------------------------------

constexpr int kSampleRateHz = 50;
constexpr uint32_t kPeriodUs = 1000000UL / kSampleRateHz;
constexpr int kStrideSamples = 10;            // one inference each 0.2 s
constexpr float kMinProbability = 0.6f;       // below this value: "uncertain"

LSM6DS3 myIMU(I2C_MODE, 0x6A);
U8G2_SSD1306_72X40_ER_1_HW_I2C u8g2(U8G2_R2, U8X8_PIN_NONE);

uint8_t* tensor_arena = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;

// Ring buffer with the newest window: kWindowSamples samples of 3 axes.
float ring[kWindowSamples * kAxes];
int ring_head = 0;                 // position of the next sample
long samples_total = 0;
long late_total = 0;
uint32_t deadline_us = 0;

float window_buffer[kWindowSamples * kAxes];
float features[kNumFeatures];
float probabilities[kNumClasses];

void stop(const char* message) {
  Serial.println(message);
  while (true) {
    delay(1000);
  }
}

void show(const char* line1, const char* line2) {
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

// Task B1 and task B2: make the interpreter.
bool setupModel() {
  const tflite::Model* model = tflite::GetModel(g_model);   // no copy
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("ERROR: the schema version of the model does not match");
    return false;
  }

  // Task B1: the operator types of the model. The notebook prints them.
  static tflite::MicroMutableOpResolver<2> resolver;
  resolver.AddFullyConnected();
  resolver.AddSoftmax();

  // Task B2: the interpreter and the memory plan.
  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;
  if (interpreter->AllocateTensors() != kTfLiteOk) {
    Serial.println("ERROR: AllocateTensors() failed. The arena is too small.");
    return false;
  }
  return true;
}

// Task B3: run the model for one feature vector.
// input_features: kNumFeatures values, before the normalization.
// output:         kNumClasses probabilities.
bool classify(const float* input_features, float* output) {
  TfLiteTensor* input = interpreter->input(0);
  for (int i = 0; i < kNumFeatures; i++) {
    input->data.f[i] = (input_features[i] - kFeatureMean[i]) / kFeatureStd[i];
  }
  if (interpreter->Invoke() != kTfLiteOk) {
    return false;
  }
  const TfLiteTensor* result = interpreter->output(0);
  for (int k = 0; k < kNumClasses; k++) {
    output[k] = result->data.f[k];
  }
  return true;
}

// Task B4: return the number of the class with the largest probability.
int bestClass(const float* output) {
  int best = 0;
  for (int k = 1; k < kNumClasses; k++) {
    if (output[k] > output[best]) {
      best = k;
    }
  }
  return best;
}

// Compare the board with the notebook for the window of test_window.h.
bool selfTest() {
  bool pass = true;

  extract_features(kTestWindow, features);
  float worst = 0.0f;
  for (int i = 0; i < kNumFeatures; i++) {
    const float limit = 0.001f + 0.001f * fabsf(kTestFeatures[i]);
    const float difference = fabsf(features[i] - kTestFeatures[i]);
    if (difference > limit) {
      pass = false;
    }
    if (difference > worst) {
      worst = difference;
    }
  }
  Serial.printf("Self-test, features:  largest difference %.6f\n", worst);

  if (!classify(kTestFeatures, probabilities)) {
    Serial.println("Self-test, model:     Invoke() failed");
    return false;
  }
  worst = 0.0f;
  for (int k = 0; k < kNumClasses; k++) {
    const float difference = fabsf(probabilities[k] - kTestOutput[k]);
    if (difference > worst) {
      worst = difference;
    }
  }
  if (worst > 0.001f) {
    pass = false;
  }
  Serial.printf("Self-test, model:     largest difference %.6f\n", worst);
  Serial.printf("Self-test, class:     %s (expected: %s)\n",
                kClassNames[bestClass(probabilities)], kClassNames[kTestClass]);
  if (bestClass(probabilities) != kTestClass) {
    pass = false;
  }
  Serial.printf("Self-test:            %s\n", pass ? "PASS" : "FAIL");
  return pass;
}

void setup() {
  Serial.begin(115200);
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }
  Serial.println("motion_classifier");

  u8g2.begin();
  show("Day 3", "start");

  if (myIMU.begin() != 0) {
    stop("ERROR: IMU initialization failed!");
  }

  // Reserve the arena with an alignment of 16 bytes.
#if ARENA_IN_PSRAM
  if (!psramFound()) {
    stop("ERROR: ARENA_IN_PSRAM is 1, but PSRAM is not active.");
  }
  const uint32_t caps = MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT;
  Serial.println("Arena location:       PSRAM");
#else
  const uint32_t caps = MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT;
  Serial.println("Arena location:       internal RAM");
#endif
  tensor_arena =
      static_cast<uint8_t*>(heap_caps_aligned_alloc(16, kTensorArenaSize, caps));
  if (tensor_arena == nullptr) {
    stop("ERROR: not enough memory for the arena.");
  }

  if (!setupModel()) {
    stop("ERROR: the model is not ready.");
  }

  Serial.printf("Model size (flash):   %d bytes\n", g_model_len);
  Serial.printf("Sketch size (flash):  %lu bytes\n",
                (unsigned long)ESP.getSketchSize());
  Serial.printf("Arena size:           %u bytes\n", (unsigned)kTensorArenaSize);
  Serial.printf("Arena used:           %u bytes\n",
                (unsigned)interpreter->arena_used_bytes());
  Serial.printf("Free internal heap:   %lu bytes\n",
                (unsigned long)ESP.getFreeHeap());
  Serial.printf("PSRAM:                %s\n",
                psramFound() ? "active" : "not active");

  if (!selfTest()) {
    show("self-test", "FAIL");
    stop("ERROR: the self-test failed. Check the model files.");
  }

  Serial.println();
  Serial.println("class,probability,features_us,invoke_us,late_samples");
  deadline_us = micros();
}

void loop() {
  // Wait for the deadline of the next sample.
  const uint32_t now = micros();
  if ((int32_t)(now - deadline_us) < 0) {
    return;
  }
  deadline_us += kPeriodUs;
  if ((int32_t)(now - deadline_us) > 0) {
    deadline_us = now + kPeriodUs;   // the loop was too slow: new time base
    late_total++;
  }

  // Read one sample, in g, into the ring buffer.
  ring[ring_head * kAxes + 0] = myIMU.readFloatAccelX();
  ring[ring_head * kAxes + 1] = myIMU.readFloatAccelY();
  ring[ring_head * kAxes + 2] = myIMU.readFloatAccelZ();
  ring_head = (ring_head + 1) % kWindowSamples;
  samples_total++;

  // One inference each 10 samples, when the buffer holds a complete window.
  if (samples_total < kWindowSamples || samples_total % kStrideSamples != 0) {
    return;
  }

  // Pre-process: copy the window with the oldest sample first, then
  // calculate the features.
  const unsigned long t0 = micros();
  for (int i = 0; i < kWindowSamples; i++) {
    const int source = (ring_head + i) % kWindowSamples;
    for (int k = 0; k < kAxes; k++) {
      window_buffer[i * kAxes + k] = ring[source * kAxes + k];
    }
  }
  extract_features(window_buffer, features);
  const unsigned long t1 = micros();

  // Infer.
  if (!classify(features, probabilities)) {
    Serial.println("ERROR: Invoke() failed");
    return;
  }
  const unsigned long t2 = micros();

  // Post-process: the best class, or "uncertain" below the limit.
  const int best = bestClass(probabilities);
  const float probability = probabilities[best];
  const char* name = probability >= kMinProbability ? kClassNames[best]
                                                    : "uncertain";

  Serial.printf("%s,%.3f,%lu,%lu,%ld\n", name, probability, t1 - t0, t2 - t1,
                late_total);

  char line2[16];
  snprintf(line2, sizeof(line2), "%d%%", (int)(probability * 100.0f));
  show(name, line2);
}
