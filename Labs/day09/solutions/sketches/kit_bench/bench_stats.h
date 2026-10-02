// bench_stats.h - the statistics of the benchmark sketch kit_bench
//
// Solution of the Day 9 lab (Task B1 is complete). Copy this file into the
// folder sketches/kit_bench/ to use it.
//
// Credits: new code of this course. The percentile follows the nearest-rank
// rule of Parts 1 and 2 of the Day 9 lecture, and the measurement rules
// (warm-up, repetitions, percentiles) follow chapter 12 "Benchmarking" of
// "Machine Learning Systems" by Vijay Janapa Reddi and contributors
// (mlsysbook.ai, CC BY-NC-SA 4.0).
#ifndef BENCH_STATS_H_
#define BENCH_STATS_H_

#include <stdint.h>

// Sort n values from the smallest to the largest (insertion sort). The
// benchmark has 200 values or fewer, so a simple sort is fast enough.
inline void sortTimes(uint32_t* values, int n) {
  for (int i = 1; i < n; i++) {
    const uint32_t value = values[i];
    int k = i - 1;
    while (k >= 0 && values[k] > value) {
      values[k + 1] = values[k];
      k--;
    }
    values[k + 1] = value;
  }
}

// Task B1. Return the percentile of n sorted values with the nearest-rank
// rule: the smallest value with at least `percent` percent of the values at
// or below it.
//
// sorted:  n values, from the smallest to the largest
// percent: 1 to 100. The median is the percentile 50.
//
// rank = percent x n / 100, rounded up. The result is the value with this
// rank. The first value has the rank 1.
// Examples: n = 20, percent = 50: rank 10. n = 20, percent = 95: rank 19.
//           n = 7, percent = 50: rank 4 (3.5 rounded up).
inline uint32_t percentileUs(const uint32_t* sorted, int n, int percent) {
  int rank = (percent * n + 99) / 100;     // integer division rounds up
  if (rank < 1) {
    rank = 1;
  }
  if (rank > n) {
    rank = n;
  }
  return sorted[rank - 1];
}

// The sketch calls this test at the start. It returns true if percentileUs
// gives the correct value for four examples.
inline bool taskB1Complete() {
  uint32_t twenty[20];
  for (int i = 0; i < 20; i++) {
    twenty[i] = 10U * (uint32_t)(i + 1);          // 10, 20, ..., 200
  }
  const uint32_t seven[7] = {3, 5, 8, 13, 21, 34, 55};
  return percentileUs(twenty, 20, 50) == 100U && percentileUs(twenty, 20, 95) == 190U &&
         percentileUs(seven, 7, 50) == 13U && percentileUs(seven, 7, 100) == 55U;
}

#endif  // BENCH_STATS_H_
