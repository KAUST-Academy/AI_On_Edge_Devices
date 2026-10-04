// The four benchmark cases of kit_bench: the model, the test input, and the
// output that LiteRT gives for this input on a laptop.
// Generated file. Do not change it by hand.
//
// Credits: new file of this course. The outputs come from the reference
// models of MLPerf Tiny (github.com/mlcommons/tiny, Apache-2.0).
#ifndef BENCH_CASES_H_
#define BENCH_CASES_H_

#include "model_kws_int8.h"
#include "model_kws_float32.h"
#include "model_ic_int8.h"
#include "model_ic_float32.h"

constexpr int kNumCases = 4;
constexpr int kMaxOutputs = 12;

// The input of the int8 keyword model: real value = scale x (q - zero).
constexpr float kKwsInputScale = 0.5847029090f;
constexpr int kKwsInputZero = 83;

struct BenchCase {
  const char* task;             // kws: keyword spotting, ic: image classification
  const char* precision;        // int8 or float32
  const unsigned char* model;   // the LiteRT file
  unsigned int model_bytes;
  uint32_t seed;                // seed of the test input
  int input_values;             // number of input values
  int outputs;                  // number of classes
  int expected_class;           // class of LiteRT on the laptop
  float expected[kMaxOutputs];  // outputs of LiteRT on the laptop
};

const BenchCase kCases[kNumCases] = {
  {"kws", "int8", g_kws_int8, g_kws_int8_len, 8U, 490, 12, 8,
   {0.019531f, 0.078125f, 0.027344f, 0.007812f, 0.011719f, 0.007812f, 0.019531f, 0.023438f,
    0.789062f, 0.000000f, 0.000000f, 0.015625f}},
  {"kws", "float32", g_kws_float32, g_kws_float32_len, 8U, 490, 12, 8,
   {0.014791f, 0.083789f, 0.015625f, 0.004352f, 0.010885f, 0.005243f, 0.013453f, 0.028343f,
    0.812319f, 0.000072f, 0.000011f, 0.011116f}},
  {"ic", "int8", g_ic_int8, g_ic_int8_len, 5U, 3072, 10, 6,
   {0.000000f, 0.000000f, 0.000000f, 0.000000f, 0.000000f, 0.000000f, 0.996094f, 0.000000f,
    0.000000f, 0.000000f}},
  {"ic", "float32", g_ic_float32, g_ic_float32_len, 5U, 3072, 10, 6,
   {0.000000f, 0.000035f, 0.000291f, 0.000484f, 0.000000f, 0.000000f, 0.999046f, 0.000000f,
    0.000144f, 0.000000f}},
};

#endif  // BENCH_CASES_H_
