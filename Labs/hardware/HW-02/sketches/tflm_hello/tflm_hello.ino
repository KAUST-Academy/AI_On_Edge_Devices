/* Copyright 2024 Chirale, TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

// tflm_hello - minimal TensorFlow Lite Micro sketch for the XIAO ESP32S3
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense), FQBN esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Libraries: Chirale_TensorFlowLite 2.0.0
// Model:     model.h, the "hello world" sine model (int8, 2488 bytes)

#include <Chirale_TensorFlowLite.h>

#include "model.h"

#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;

// The tensor arena holds the input, the output, and the intermediate tensors.
// The value comes from the example. The sketch prints how much the model uses.
constexpr int kTensorArenaSize = 2000;
alignas(16) uint8_t tensor_arena[kTensorArenaSize];

// One period of the sine wave in 20 steps.
constexpr int kSteps = 20;
constexpr float kTwoPi = 6.2831853f;
int step = 0;

void stop(const char* message) {
  Serial.println(message);
  while (true) {
    delay(1000);
  }
}

void setup() {
  Serial.begin(115200);
  // Wait for the Serial Monitor, but not for more than 3 seconds.
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }

  Serial.println("tflm_hello: sine model with TensorFlow Lite Micro");

  // Map the model. This does not copy the model.
  model = tflite::GetModel(g_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    stop("ERROR: the schema version of the model does not match the library");
  }

  // Register the operators that the model uses. This model has three
  // fully connected layers and no other operator.
  static tflite::MicroMutableOpResolver<1> resolver;
  if (resolver.AddFullyConnected() != kTfLiteOk) {
    stop("ERROR: AddFullyConnected() failed");
  }

  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;

  if (interpreter->AllocateTensors() != kTfLiteOk) {
    stop("ERROR: AllocateTensors() failed. The arena is too small.");
  }

  input = interpreter->input(0);
  output = interpreter->output(0);

  Serial.print("Model size (bytes):      ");
  Serial.println(g_model_len);
  Serial.print("Arena size (bytes):      ");
  Serial.println(kTensorArenaSize);
  Serial.print("Arena used (bytes):      ");
  Serial.println(interpreter->arena_used_bytes());
  Serial.print("Free internal heap:      ");
  Serial.println(ESP.getFreeHeap());
  Serial.println();
  Serial.println("x,y_model,y_true,error,latency_us");
}

void loop() {
  const float x = kTwoPi * step / kSteps;
  step = (step + 1) % kSteps;

  // The model has int8 input and int8 output. Convert the input value.
  const int8_t x_quantized = x / input->params.scale + input->params.zero_point;
  input->data.int8[0] = x_quantized;

  const unsigned long t0 = micros();
  const TfLiteStatus status = interpreter->Invoke();
  const unsigned long latency = micros() - t0;

  if (status != kTfLiteOk) {
    Serial.println("ERROR: Invoke() failed");
    delay(1000);
    return;
  }

  const int8_t y_quantized = output->data.int8[0];
  const float y = (y_quantized - output->params.zero_point) * output->params.scale;
  const float y_true = sin(x);

  Serial.print(x, 3);
  Serial.print(",");
  Serial.print(y, 3);
  Serial.print(",");
  Serial.print(y_true, 3);
  Serial.print(",");
  Serial.print(y - y_true, 3);
  Serial.print(",");
  Serial.println(latency);

  delay(500);
}
