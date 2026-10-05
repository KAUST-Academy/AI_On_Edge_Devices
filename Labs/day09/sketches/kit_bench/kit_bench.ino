// kit_bench - benchmark four models on the XIAOML Kit
//
// Day 9 lab, Part B. The sketch has no task. Task B1 is in bench_stats.h.
//
// Board:     XIAOML Kit (XIAO ESP32S3 Sense). The sketch uses no sensor and
//            no display.
// FQBN:      esp32:esp32:XIAO_ESP32S3:PSRAM=opi
// Core:      esp32 by Espressif Systems 3.3.12
// Library:   Chirale_TensorFlowLite 2.0.0
// Serial:    115200 baud
// Files:     bench_cases.h and the four files model_*.h are generated files.
//            bench_stats.h has the sort and the percentile.
//
// What the sketch does, for each of the four models:
//   1. It makes an interpreter of TensorFlow Lite Micro with its own arena.
//      The arena is in the internal RAM if it fits, and in the PSRAM if not.
//   2. It fills the input with a fixed test input (bench_input()) before
//      each inference. The interpreter can use the memory of the input
//      tensor again for a later tensor, so the values do not stay.
//   3. It measures the first inference alone. Then it does more inferences
//      to warm up, with no measurement.
//   4. It measures kTimedRuns inferences with micros(), one after the other.
//   5. It prints the minimum, the median, the 95th percentile, and the
//      maximum, and compares the output with the output of LiteRT.
//   6. It prints one line that starts with "CSV". Copy these lines into the
//      file results_kit.csv.
// The timed window is the call of Invoke(): the model only. The input is in
// the input tensor before the clock starts.

#include <Chirale_TensorFlowLite.h>
#include <esp_heap_caps.h>

#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

#include "bench_cases.h"
#include "bench_stats.h"

// ---- The settings of your protocol (Part A) ---------------------------------

// Inferences before the timed runs. The first one is measured alone.
#ifndef WARMUP_RUNS
#define WARMUP_RUNS 3
#endif

// Timed inferences for each model. The largest value is kMaxTimedRuns.
#ifndef TIMED_RUNS
#define TIMED_RUNS 20
#endif

// Clock of the processor in MHz: 240, 160, or 80.
#ifndef CPU_MHZ
#define CPU_MHZ 240
#endif

// -----------------------------------------------------------------------------

constexpr int kWarmupRuns = WARMUP_RUNS;
constexpr int kTimedRuns = TIMED_RUNS;
constexpr int kMaxTimedRuns = 200;

// Arena for each model, in bytes. The values are the arena use of a 32-bit
// build on an x86 computer, plus a reserve. See TEST_NOTES.md.
const size_t kArenaBytes[kNumCases] = {
    32 * 1024,     // kws int8
    96 * 1024,     // kws float32
    64 * 1024,     // ic int8
    224 * 1024,    // ic float32
};

// Largest difference between an output of the kit and the output of LiteRT
// that counts as the same result.
constexpr float kToleranceInt8 = 0.02f;       // 5 steps of 1/256
constexpr float kToleranceFloat = 0.001f;

uint32_t times_us[kMaxTimedRuns];
bool task_b1_complete = false;

// The test input: a small random number generator with a fixed seed. Each
// call gives the next byte, from 0 to 255. The tool that made bench_cases.h
// has the same generator.
uint32_t input_state = 0;
uint8_t nextByte() {
  input_state = input_state * 1664525UL + 1013904223UL;
  return (uint8_t)(input_state >> 24);
}

// Fill the input tensor of one case.
// Keyword spotting: 49 frames of 10 coefficients, near the zero point of the
// int8 input. The first coefficient of each frame is lower.
// Image classification: one image of 32 x 32 pixels with 3 colours.
void bench_input(const BenchCase& bench, TfLiteTensor* input) {
  input_state = bench.seed;
  const bool is_kws = bench.task[0] == 'k';
  for (int i = 0; i < bench.input_values; i++) {
    const int byte_value = nextByte();
    int q = byte_value - 128;                  // image: pixel - 128
    if (is_kws) {
      q = kKwsInputZero + (byte_value - 128) / 12;
      if (i % 10 == 0) {
        q -= 60;
      }
      if (q < -128) {
        q = -128;
      }
      if (q > 127) {
        q = 127;
      }
    }
    if (input->type == kTfLiteInt8) {
      input->data.int8[i] = (int8_t)q;
    } else if (is_kws) {
      input->data.f[i] = kKwsInputScale * (float)(q - kKwsInputZero);
    } else {
      input->data.f[i] = (float)byte_value;    // image: pixel from 0 to 255
    }
  }
}

// Read one output as a real value.
float outputValue(const TfLiteTensor* output, int k) {
  if (output->type == kTfLiteInt8) {
    return output->params.scale * (float)(output->data.int8[k] - output->params.zero_point);
  }
  return output->data.f[k];
}

// Measure one model. Return false if the model does not run.
bool runCase(int index) {
  const BenchCase& bench = kCases[index];
  Serial.printf("--- %s %s ---\n", bench.task, bench.precision);
  Serial.printf("model: %u bytes\n", bench.model_bytes);

  // The arena: internal RAM first, then PSRAM.
  const size_t arena_bytes = kArenaBytes[index];
  const char* arena_memory = "internal";
  uint8_t* arena = (uint8_t*)heap_caps_aligned_alloc(
      16, arena_bytes, MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT);
  if (arena == nullptr) {
    arena_memory = "psram";
    arena = (uint8_t*)heap_caps_aligned_alloc(16, arena_bytes,
                                              MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);
  }
  if (arena == nullptr) {
    Serial.printf("ERROR: no memory for an arena of %u bytes. Set Tools > PSRAM > "
                  "OPI PSRAM.\n", (unsigned)arena_bytes);
    Serial.printf("CSV,kit,%s,%s,%u,0,none,%d,%d,%d,0,0,0,0,0,no_memory,0.0\n",
                  bench.task, bench.precision, bench.model_bytes, CPU_MHZ, kWarmupRuns,
                  kTimedRuns);
    return false;
  }

  bool ok = false;
  {
    const tflite::Model* model = tflite::GetModel(bench.model);   // no copy
    tflite::MicroMutableOpResolver<7> resolver;
    resolver.AddConv2D();
    resolver.AddDepthwiseConv2D();
    resolver.AddAdd();
    resolver.AddAveragePool2D();
    resolver.AddReshape();
    resolver.AddFullyConnected();
    resolver.AddSoftmax();
    tflite::MicroInterpreter interpreter(model, resolver, arena, arena_bytes);

    if (model->version() != TFLITE_SCHEMA_VERSION) {
      Serial.println("ERROR: the schema version of the model does not match");
    } else if (interpreter.AllocateTensors() != kTfLiteOk) {
      Serial.println("ERROR: AllocateTensors() failed. The arena is too small.");
    } else {
      const size_t arena_used = interpreter.arena_used_bytes();
      Serial.printf("arena: %u bytes used of %u, in the %s RAM\n", (unsigned)arena_used,
                    (unsigned)arena_bytes, arena_memory);
      TfLiteTensor* input = interpreter.input(0);

      // The first inference, alone.
      bench_input(bench, input);
      unsigned long start = micros();
      ok = interpreter.Invoke() == kTfLiteOk;
      const unsigned long first_us = micros() - start;

      // The other warm-up inferences: no measurement.
      for (int i = 1; ok && i < kWarmupRuns; i++) {
        bench_input(bench, input);
        ok = interpreter.Invoke() == kTfLiteOk;
      }

      // The timed inferences. The clock starts after the input is ready.
      const int runs = kTimedRuns < kMaxTimedRuns ? kTimedRuns : kMaxTimedRuns;
      for (int i = 0; ok && i < runs; i++) {
        bench_input(bench, input);
        start = micros();
        ok = interpreter.Invoke() == kTfLiteOk;
        times_us[i] = (uint32_t)(micros() - start);
      }

      if (!ok) {
        Serial.println("ERROR: Invoke() failed");
      } else {
        sortTimes(times_us, runs);
        const uint32_t min_us = times_us[0];
        const uint32_t max_us = times_us[runs - 1];
        const uint32_t median_us = task_b1_complete ? percentileUs(times_us, runs, 50) : 0;
        const uint32_t p95_us = task_b1_complete ? percentileUs(times_us, runs, 95) : 0;

        // Compare the output with the output of LiteRT on the laptop.
        const TfLiteTensor* output = interpreter.output(0);
        int best = 0;
        float largest_difference = 0.0f;
        for (int k = 0; k < bench.outputs; k++) {
          const float value = outputValue(output, k);
          if (value > outputValue(output, best)) {
            best = k;
          }
          const float difference = fabsf(value - bench.expected[k]);
          if (difference > largest_difference) {
            largest_difference = difference;
          }
        }
        const float tolerance =
            output->type == kTfLiteInt8 ? kToleranceInt8 : kToleranceFloat;
        const bool same = best == bench.expected_class && largest_difference <= tolerance;
        const float degrees = temperatureRead();

        Serial.printf("first inference: %lu us\n", first_us);
        Serial.printf("timed runs: %d, after %d inferences to warm up\n", runs, kWarmupRuns);
        if (task_b1_complete) {
          Serial.printf("min %lu us, median %lu us, p95 %lu us, max %lu us\n",
                        (unsigned long)min_us, (unsigned long)median_us,
                        (unsigned long)p95_us, (unsigned long)max_us);
        } else {
          Serial.printf("min %lu us, max %lu us. Task B1 is not complete: no median, "
                        "no p95.\n", (unsigned long)min_us, (unsigned long)max_us);
        }
        Serial.printf("output: class %d (LiteRT: %d), largest difference %.4f. Same result "
                      "as LiteRT: %s\n", best, bench.expected_class, largest_difference,
                      same ? "yes" : "NO");
        Serial.printf("chip temperature: %.1f C\n", degrees);
        Serial.printf("CSV,kit,%s,%s,%u,%u,%s,%d,%d,%d,%lu,%lu,%lu,%lu,%lu,%s,%.1f\n",
                      bench.task, bench.precision, bench.model_bytes, (unsigned)arena_used,
                      arena_memory, CPU_MHZ, kWarmupRuns, runs, first_us,
                      (unsigned long)min_us, (unsigned long)median_us,
                      (unsigned long)p95_us, (unsigned long)max_us, same ? "yes" : "no",
                      degrees);
      }
    }
  }
  heap_caps_free(arena);
  return ok;
}

void runAll() {
  Serial.println();
  Serial.println("kit_bench: four models with TensorFlow Lite Micro");
  Serial.printf("clock: %lu MHz (setting %d). Free internal heap: %u bytes. PSRAM: %u "
                "bytes.\n", (unsigned long)getCpuFrequencyMhz(), CPU_MHZ,
                (unsigned)heap_caps_get_free_size(MALLOC_CAP_INTERNAL),
                (unsigned)ESP.getPsramSize());
  task_b1_complete = taskB1Complete();
  Serial.println(task_b1_complete ? "Task B1: complete"
                                  : "Task B1: not complete. Write percentileUs() in "
                                    "bench_stats.h.");
  Serial.println("CSV,device,task,precision,model_bytes,arena_bytes,arena_memory,cpu_mhz,"
                 "warmup,runs,first_us,min_us,median_us,p95_us,max_us,same_as_litert,temp_c");
  int passed = 0;
  for (int i = 0; i < kNumCases; i++) {
    if (runCase(i)) {
      passed++;
    }
  }
  Serial.printf("--- complete: %d of %d models ran. Send a character to measure again. "
                "---\n", passed, kNumCases);
}

void setup() {
  Serial.begin(115200);
  const unsigned long wait_start = millis();
  while (!Serial && millis() - wait_start < 5000) {
    delay(10);
  }
  setCpuFrequencyMhz(CPU_MHZ);
  delay(2000);          // time to open the Serial Monitor
  runAll();
}

void loop() {
  if (Serial.available() > 0) {
    while (Serial.available() > 0) {
      Serial.read();
    }
    runAll();
  }
  delay(100);
}
