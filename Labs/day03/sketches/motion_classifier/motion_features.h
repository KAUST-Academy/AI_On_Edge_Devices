// motion_features.h - features of one motion window, for the Day 3 lab
//
// The functions of this file calculate the 63 features that the notebook
// motion_classifier.ipynb calculates in Python. The two results must be
// equal for the same window. The sketch checks this at the start with the
// window of test_window.h.
//
// One window has 100 samples of 3 axes (2 s at 50 Hz), in g. For each axis,
// the code removes the mean and then calculates 21 features:
//   0      RMS
//   1      skewness
//   2      kurtosis (the value 0 is the kurtosis of a normal distribution)
//   3      skewness of the 16 power values
//   4      kurtosis of the 16 power values
//   5..20  spectral power of the frequency bins 1 to 16 (FFT length 32)
//
// The file uses only standard C++. It runs on the board and on a laptop.
//
// Hardware status: new code, not tested on hardware (prepared on
// 2026-10-02). It was compared with the Python code on a laptop.
//
// Credits: the feature list and the method of the spectral power (frames
// of the FFT length, and the largest power of each bin over the frames)
// follow the chapter "DSP Spectral Features" of "Machine Learning Systems"
// by Vijay Janapa Reddi and contributors, written by Marcelo Rovai
// (mlsysbook.ai, CC BY-NC-SA 4.0). The code is new.

#ifndef MOTION_FEATURES_H_
#define MOTION_FEATURES_H_

#include <math.h>

constexpr int kWindowSamples = 100;                    // 2 s at 50 Hz
constexpr int kAxes = 3;                               // ax, ay, az
constexpr int kFftLength = 32;
constexpr int kPowerBins = kFftLength / 2;             // bins 1 to 16
constexpr int kFeaturesPerAxis = 5 + kPowerBins;       // 21
constexpr int kNumFeatures = kAxes * kFeaturesPerAxis; // 63

// Skewness and kurtosis of n values. The two results are 0 for a constant
// signal.
inline void moments(const float* x, int n, float* skewness, float* kurtosis) {
  float mean = 0.0f;
  for (int i = 0; i < n; i++) {
    mean += x[i];
  }
  mean /= n;
  float m2 = 0.0f, m3 = 0.0f, m4 = 0.0f;
  for (int i = 0; i < n; i++) {
    const float d = x[i] - mean;
    const float d2 = d * d;
    m2 += d2;
    m3 += d2 * d;
    m4 += d2 * d2;
  }
  m2 /= n;
  m3 /= n;
  m4 /= n;
  if (m2 < 1e-12f) {
    *skewness = 0.0f;
    *kurtosis = 0.0f;
    return;
  }
  *skewness = m3 / (m2 * sqrtf(m2));
  *kurtosis = m4 / (m2 * m2) - 3.0f;
}

// Spectral power of the bins 1 to 16. The window is cut into frames of 32
// samples. The last frame is short, and zeros fill it. For each bin, the
// result is the largest power over the frames.
inline void spectral_power(const float* x, int n, float* power) {
  static float cos_table[kFftLength];
  static float sin_table[kFftLength];
  static bool table_ready = false;
  if (!table_ready) {
    for (int i = 0; i < kFftLength; i++) {
      const float angle = 2.0f * (float)M_PI * i / kFftLength;
      cos_table[i] = cosf(angle);
      sin_table[i] = sinf(angle);
    }
    table_ready = true;
  }
  for (int k = 0; k < kPowerBins; k++) {
    power[k] = 0.0f;
  }
  for (int start = 0; start < n; start += kFftLength) {
    for (int k = 1; k <= kPowerBins; k++) {
      float re = 0.0f, im = 0.0f;
      for (int i = 0; i < kFftLength && start + i < n; i++) {
        const int index = (k * i) % kFftLength;
        re += x[start + i] * cos_table[index];
        im -= x[start + i] * sin_table[index];
      }
      const float p = (re * re + im * im) / kFftLength;
      if (p > power[k - 1]) {
        power[k - 1] = p;
      }
    }
  }
}

// Calculate the 63 features of one window.
//   window:   kWindowSamples * kAxes values. The value of sample i and axis
//             k is window[i * kAxes + k].
//   features: kNumFeatures values, 21 for each axis.
inline void extract_features(const float* window, float* features) {
  float x[kWindowSamples];
  for (int axis = 0; axis < kAxes; axis++) {
    float* out = features + axis * kFeaturesPerAxis;

    // Copy the axis and remove its mean.
    float mean = 0.0f;
    for (int i = 0; i < kWindowSamples; i++) {
      x[i] = window[i * kAxes + axis];
      mean += x[i];
    }
    mean /= kWindowSamples;
    float sum_of_squares = 0.0f;
    for (int i = 0; i < kWindowSamples; i++) {
      x[i] -= mean;
      sum_of_squares += x[i] * x[i];
    }

    out[0] = sqrtf(sum_of_squares / kWindowSamples);   // RMS
    moments(x, kWindowSamples, &out[1], &out[2]);
    spectral_power(x, kWindowSamples, &out[5]);
    moments(&out[5], kPowerBins, &out[3], &out[4]);
  }
}

#endif  // MOTION_FEATURES_H_
