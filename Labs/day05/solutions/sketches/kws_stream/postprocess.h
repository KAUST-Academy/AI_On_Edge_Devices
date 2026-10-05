// postprocess.h - from the results of many windows to one event
//
// Solution of the Day 5 lab (tasks A1 and A2 are complete).
//
// The model gives one probability for each class and each window. The
// post-processing keeps the newest results. It calculates the mean of the
// last N results, compares it with a threshold, and accepts no second event
// during the suppression time. Part 3 of the Day 5 lecture gives the method.
//
// The file uses only standard C++. It runs on the board and on a laptop.

#ifndef POSTPROCESS_H_
#define POSTPROCESS_H_

#include <stdint.h>

// Set a flag to true when its task is complete. The sketch prints the flags.
constexpr bool kTaskA1Complete = true;
constexpr bool kTaskA2Complete = true;

constexpr int kMaxClasses = 8;    // the largest number of classes of a model
constexpr int kMaxHistory = 8;    // the largest value of N

struct PostProcess {
  float history[kMaxHistory][kMaxClasses];  // the newest results
  int count = 0;                 // number of results in the history
  int next = 0;                  // position of the next result
  bool had_event = false;        // true after the first event
  uint32_t last_event_ms = 0;    // time of the last event
};

// Store the probabilities of one window.
inline void pp_add(PostProcess& pp, const float* probabilities, int classes) {
  for (int k = 0; k < classes && k < kMaxClasses; k++) {
    pp.history[pp.next][k] = probabilities[k];
  }
  pp.next = (pp.next + 1) % kMaxHistory;
  if (pp.count < kMaxHistory) {
    pp.count++;
  }
}

// Return the probability of one class in the result number "back":
// back = 0 is the newest result, back = 1 is the result before it.
inline float pp_value(const PostProcess& pp, int class_index, int back) {
  const int position = (pp.next - 1 - back + 2 * kMaxHistory) % kMaxHistory;
  return pp.history[position][class_index];
}

// Task A1: return the mean of the last n results for one class.
// A window that the history does not hold counts as 0.
inline float pp_mean(const PostProcess& pp, int class_index, int n) {
  float sum = 0.0f;
  for (int back = 0; back < n && back < pp.count; back++) {
    sum += pp_value(pp, class_index, back);
  }
  return sum / n;
}

// Task A2: decide if the newest result gives an event.
//   is_keyword:     for each class, true if the class is a keyword
//   n:              number of windows for the mean
//   threshold:      smallest mean for an event
//   suppression_ms: time after an event with no new event
//   now_ms:         the time now
// Return the number of the keyword class of the event, or -1 for no event.
inline int pp_event(PostProcess& pp, const bool* is_keyword, int classes,
                    int n, float threshold, uint32_t suppression_ms,
                    uint32_t now_ms) {
  // Rule 1: no event during the suppression time.
  if (pp.had_event && now_ms - pp.last_event_ms < suppression_ms) {
    return -1;
  }
  // Rule 2: the keyword class with the largest mean.
  int best = -1;
  float best_mean = 0.0f;
  for (int k = 0; k < classes; k++) {
    if (!is_keyword[k]) {
      continue;
    }
    const float mean = pp_mean(pp, k, n);
    if (best < 0 || mean > best_mean) {
      best = k;
      best_mean = mean;
    }
  }
  // Rule 3: the mean must reach the threshold.
  if (best < 0 || best_mean < threshold) {
    return -1;
  }
  pp.had_event = true;
  pp.last_event_ms = now_ms;
  return best;
}

#endif  // POSTPROCESS_H_
