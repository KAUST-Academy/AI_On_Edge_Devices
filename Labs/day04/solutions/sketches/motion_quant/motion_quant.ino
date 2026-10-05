// motion_quant - compare a float32 model and an int8 model on the XIAOML Kit
//
// Solution of the Day 4 lab (tasks D1 and D2 are complete).
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
// FQBN:      esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Libraries: Chirale_TensorFlowLite 2.0.0, Seeed Arduino LSM6DS3 2.0.7,
//            U8g2 2.36.19
// Serial:    115200 baud
// Files:     model_float.h, model_int8.h, model_settings.h, and test_set.h
//            come from the notebook quantization.ipynb. motion_features.h
//            has the feature code of Day 3.
//
// What the sketch does:
//   1. MODEL_INT8 selects the model: 0 is the float32 model, 1 is the int8
//      model. Only the selected model is in the program.
//   2. At the start it prints the memory numbers. Then it runs the test
//      windows of test_set.h. It prints the accuracy, the number of windows
//      with the same class as on the laptop, and the time of Invoke().
//   3. Then it classifies the motion of the kit, as the sketch of Day 3
//      does.
//
// Credits: the use of TensorFlow Lite Micro follows the example
// "hello_world" of the library Chirale_TensorFlowLite 2.0.0
// (github.com/spaziochirale/Chirale_TensorFlowLite, Apache-2.0), which comes
// from the TensorFlow Lite Micro example of the TensorFlow Authors. The IMU
// code, the display code, the four classes, and the window of 2 s follow the
// sketch XIAOML_Kit_code/motion_class_ad_inference_oled of "XIAO ESP32S3
// Sense" by Marcelo Rovai (github.com/Mjrovai/XIAO-ESP32S3-Sense,
// Apache-2.0) and the motion classification chapter of "Machine Learning
// Systems" (mlsysbook.ai, CC BY-NC-SA 4.0). The sampling loop, the feature
// code, the quantization code, the test set, and the measurements are new.

#include <Chirale_TensorFlowLite.h>
#include <LSM6DS3.h>
#include <U8g2lib.h>
#include <Wire.h>

#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

// ---- The setting of Part D ---------------------------------------------------

// 0: the float32 model. 1: the int8 model.
#ifndef MODEL_INT8
#define MODEL_INT8 0
#endif

// -----------------------------------------------------------------------------

#include "motion_features.h"
#if MODEL_INT8
#include "model_int8.h"
#else
#include "model_float.h"
#endif
#include "model_settings.h"
#include "test_set.h"

// Size of the arena. The two models need less than 2 KB.
constexpr size_t kTensorArenaSize = 4 * 1024;

constexpr int kSampleRateHz = 50;
constexpr uint32_t kPeriodUs = 1000000UL / kSampleRateHz;
constexpr int kStrideSamples = 10;            // one inference each 0.2 s
constexpr float kMinProbability = 0.6f;       // below this value: "uncertain"

LSM6DS3 myIMU(I2C_MODE, 0x6A);
U8G2_SSD1306_72X40_ER_1_HW_I2C u8g2(U8G2_R2, U8X8_PIN_NONE);

alignas(16) uint8_t tensor_arena[kTensorArenaSize];
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

unsigned long invoke_us = 0;       // time of the last call of Invoke()
long clipped_total = 0;            // input values that the clamp changed
bool task_d1_complete = true;
bool task_d2_complete = true;

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

// Make the interpreter. The two models have the same operator types.
bool setupModel() {
  const tflite::Model* model = tflite::GetModel(g_model);   // no copy
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("ERROR: the schema version of the model does not match");
    return false;
  }

  static tflite::MicroMutableOpResolver<2> resolver;
  resolver.AddFullyConnected();
  resolver.AddSoftmax();

  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;
  if (interpreter->AllocateTensors() != kTfLiteOk) {
    Serial.println("ERROR: AllocateTensors() failed. The arena is too small.");
    return false;
  }
  return true;
}

// Run the model for one feature vector.
// input_features: kNumFeatures values, before the normalization.
// output:         kNumClasses probabilities.
bool classify(const float* input_features, float* output) {
  TfLiteTensor* input = interpreter->input(0);
#if MODEL_INT8
  // Task D1: quantize the input with the scale and the zero point of the
  // input tensor.
  const float input_scale = input->params.scale;
  const long input_zero_point = input->params.zero_point;
  for (int i = 0; i < kNumFeatures; i++) {
    const float x = (input_features[i] - kFeatureMean[i]) / kFeatureStd[i];
    long q = lroundf(x / input_scale) + input_zero_point;
    if (q < -128) {
      q = -128;
      clipped_total++;
    }
    if (q > 127) {
      q = 127;
      clipped_total++;
    }
    input->data.int8[i] = (int8_t)q;
  }
#else
  for (int i = 0; i < kNumFeatures; i++) {
    input->data.f[i] = (input_features[i] - kFeatureMean[i]) / kFeatureStd[i];
  }
#endif

  const unsigned long start = micros();
  if (interpreter->Invoke() != kTfLiteOk) {
    return false;
  }
  invoke_us = micros() - start;

  const TfLiteTensor* result = interpreter->output(0);
#if MODEL_INT8
  // Task D2: dequantize the output with the scale and the zero point of the
  // output tensor.
  const float output_scale = result->params.scale;
  const long output_zero_point = result->params.zero_point;
  for (int k = 0; k < kNumClasses; k++) {
    output[k] = output_scale * (result->data.int8[k] - output_zero_point);
  }
#else
  for (int k = 0; k < kNumClasses; k++) {
    output[k] = result->data.f[k];
  }
#endif
  return true;
}

// Return the number of the class with the largest probability.
int bestClass(const float* output) {
  int best = 0;
  for (int k = 1; k < kNumClasses; k++) {
    if (output[k] > output[best]) {
      best = k;
    }
  }
  return best;
}

// Run the model for each window of test_set.h. Print the accuracy, the
// agreement with the laptop, and the time of Invoke().
bool runTestSet() {
#if MODEL_INT8
  const uint8_t* laptop_class = kTestInt8Class;
#else
  const uint8_t* laptop_class = kTestFloatClass;
#endif
  static unsigned long times[kTestCount];
  int correct = 0;
  int same = 0;
  clipped_total = 0;

  for (int n = 0; n < kTestCount; n++) {
    if (!classify(&kTestFeatures[n * kNumFeatures], probabilities)) {
      Serial.println("Test set:             Invoke() failed");
      return false;
    }
    const int best = bestClass(probabilities);
    if (best == kTestLabel[n]) {
      correct++;
    }
    if (best == laptop_class[n]) {
      same++;
    }
    // Keep the times in order, smallest first.
    int position = n;
    while (position > 0 && times[position - 1] > invoke_us) {
      times[position] = times[position - 1];
      position--;
    }
    times[position] = invoke_us;
  }

  Serial.printf("Test set:             %d windows\n", kTestCount);
  Serial.printf("Test set, correct:    %d of %d (%.1f percent)\n", correct,
                kTestCount, 100.0f * correct / kTestCount);
  Serial.printf("Test set, same class as on the laptop: %d of %d\n", same,
                kTestCount);
#if MODEL_INT8
  Serial.printf("Test set, clipped input values: %ld of %d (laptop: %d)\n",
                clipped_total, kTestCount * kNumFeatures, kTestInt8Clipped);
#endif
  Serial.printf("Test set, invoke_us:  median %lu, largest %lu\n",
                times[kTestCount / 2], times[kTestCount - 1]);

  if (!task_d1_complete || !task_d2_complete) {
    Serial.printf("Task D1: %s. Task D2: %s.\n",
                  task_d1_complete ? "complete" : "not complete",
                  task_d2_complete ? "complete" : "not complete");
    return false;
  }
  if (same != kTestCount) {
    Serial.println("The board and the laptop give different classes.");
  }
  return true;
}

void printTensor(const char* name, const TfLiteTensor* tensor) {
  Serial.printf("%s type %s, %d bytes", name, TfLiteTypeGetName(tensor->type),
                (int)tensor->bytes);
  if (tensor->type == kTfLiteInt8) {
    Serial.printf(", scale %.6f, zero point %d", tensor->params.scale,
                  (int)tensor->params.zero_point);
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }
  Serial.println("motion_quant");

  u8g2.begin();
  show("Day 4", MODEL_INT8 ? "int8" : "float32");

  if (!setupModel()) {
    stop("ERROR: the model is not ready.");
  }

  Serial.printf("Model:                %s\n", MODEL_INT8 ? "int8" : "float32");
  Serial.printf("Model size (flash):   %d bytes\n", g_model_len);
  Serial.printf("Sketch size (flash):  %lu bytes\n",
                (unsigned long)ESP.getSketchSize());
  Serial.printf("Arena size:           %u bytes\n", (unsigned)kTensorArenaSize);
  Serial.printf("Arena used:           %u bytes\n",
                (unsigned)interpreter->arena_used_bytes());
  printTensor("Input tensor: ", interpreter->input(0));
  printTensor("Output tensor:", interpreter->output(0));

  if (!runTestSet()) {
    show("test set", "FAIL");
    stop("ERROR: the test of the model failed. Check tasks D1 and D2.");
  }

  if (myIMU.begin() != 0) {
    stop("ERROR: IMU initialization failed!");
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

  // Post-process: the best class, or "uncertain" below the limit.
  const int best = bestClass(probabilities);
  const float probability = probabilities[best];
  const char* name = probability >= kMinProbability ? kClassNames[best]
                                                    : "uncertain";

  Serial.printf("%s,%.3f,%lu,%lu,%ld\n", name, probability, t1 - t0, invoke_us,
                late_total);

  char line2[16];
  snprintf(line2, sizeof(line2), "%d%%", (int)(probability * 100.0f));
  show(name, line2);
}
