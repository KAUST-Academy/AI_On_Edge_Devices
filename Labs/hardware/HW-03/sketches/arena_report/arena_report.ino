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

// arena_report - find the tensor arena size of a model on the XIAO ESP32S3
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense), FQBN esp32:esp32:XIAO_ESP32S3
// Core:      esp32 by Espressif Systems 3.3.12
// Libraries: Chirale_TensorFlowLite 2.0.0
// Model:     model.h, the "hello world" sine model (int8, 2488 bytes).
//            Replace model.h with your model (see Labs/hardware/HW-02).
//
// Hardware status: not tested on hardware (prepared on 2026-10-01).
// The sketch compiles for the board with PSRAM disabled and with OPI PSRAM.
//
// What the sketch does:
//   1. It reserves the arena in the internal RAM or in the PSRAM.
//   2. It prints the free memory before and after.
//   3. It prints how many bytes of the arena the model uses.
//   4. It prints the latency of the model.
//
// Credits: the interpreter code adapts the example "hello_world" of the
// library Chirale_TensorFlowLite 2.0.0
// (github.com/spaziochirale/Chirale_TensorFlowLite, Apache-2.0).
// The memory report and the arena on the heap are new.

#include <Chirale_TensorFlowLite.h>

#include "model.h"

#include "esp_heap_caps.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

// ---- Settings for the experiment -------------------------------------------

// Size of the arena to try. Start large, then decrease.
constexpr size_t kTensorArenaSize = 16 * 1024;

// 0: arena in the internal RAM.
// 1: arena in the PSRAM. Needs Tools > PSRAM > OPI PSRAM.
#define ARENA_IN_PSRAM 0

// Number of inferences for the latency.
constexpr int kRuns = 100;

// -----------------------------------------------------------------------------

uint8_t* tensor_arena = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;

void stop(const char* message) {
  Serial.println(message);
  while (true) {
    delay(1000);
  }
}

void printFree(const char* when) {
  Serial.printf("%-28s internal free %7lu, largest block %7lu",
                when, (unsigned long)ESP.getFreeHeap(),
                (unsigned long)ESP.getMaxAllocHeap());
  if (psramFound()) {
    Serial.printf(", PSRAM free %8lu", (unsigned long)ESP.getFreePsram());
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  const unsigned long start = millis();
  while (!Serial && millis() - start < 3000) {
    delay(10);
  }

  Serial.println("arena_report");
  Serial.printf("PSRAM: %s\n", psramFound() ? "active" : "not active");
  printFree("Before the arena:");

  // Reserve the arena with an alignment of 16 bytes.
#if ARENA_IN_PSRAM
  if (!psramFound()) {
    stop("ERROR: ARENA_IN_PSRAM is 1, but PSRAM is not active.");
  }
  const uint32_t caps = MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT;
  Serial.println("Arena location: PSRAM");
#else
  const uint32_t caps = MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT;
  Serial.println("Arena location: internal RAM");
#endif
  tensor_arena =
      static_cast<uint8_t*>(heap_caps_aligned_alloc(16, kTensorArenaSize, caps));
  if (tensor_arena == nullptr) {
    stop("ERROR: not enough memory for the arena. Decrease kTensorArenaSize.");
  }
  printFree("After the arena:");

  const tflite::Model* model = tflite::GetModel(g_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    stop("ERROR: the schema version of the model does not match the library");
  }

  // Register the operators of your model here.
  static tflite::MicroMutableOpResolver<1> resolver;
  resolver.AddFullyConnected();

  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;

  if (interpreter->AllocateTensors() != kTfLiteOk) {
    stop("ERROR: AllocateTensors() failed. The arena is too small.");
  }

  const size_t used = interpreter->arena_used_bytes();
  Serial.println();
  Serial.printf("Model size:        %7d bytes (flash)\n", g_model_len);
  Serial.printf("Arena size:        %7u bytes\n", (unsigned)kTensorArenaSize);
  Serial.printf("Arena used:        %7u bytes\n", (unsigned)used);
  Serial.printf("Arena not used:    %7u bytes\n", (unsigned)(kTensorArenaSize - used));
  Serial.printf("Sketch size:       %7lu bytes (flash)\n",
                (unsigned long)ESP.getSketchSize());
  Serial.println();
}

void loop() {
  // Fill the input with zeros. The latency does not depend on the values.
  TfLiteTensor* input = interpreter->input(0);
  memset(input->data.raw, 0, input->bytes);

  unsigned long total = 0;
  unsigned long slowest = 0;
  for (int i = 0; i < kRuns; i++) {
    const unsigned long t0 = micros();
    if (interpreter->Invoke() != kTfLiteOk) {
      stop("ERROR: Invoke() failed");
    }
    const unsigned long dt = micros() - t0;
    total += dt;
    if (dt > slowest) {
      slowest = dt;
    }
  }
  Serial.printf("Latency of %d runs: mean %lu us, maximum %lu us\n", kRuns,
                total / kRuns, slowest);
  printFree("During inference:");
  delay(5000);
}
