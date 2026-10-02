// Test of postprocess.h with the example of Part 3 of the Day 5 lecture.
#include <cstdio>
#include "postprocess.h"
int main() {
  const float yes[15] = {0.03f,0.05f,0.72f,0.04f,0.06f,0.10f,0.55f,0.93f,0.96f,0.88f,0.31f,0.05f,0.04f,0.08f,0.03f};
  const bool is_keyword[2] = {false, true};   // class 0: noise, class 1: yes
  PostProcess pp;
  int events = 0;
  printf("tasks: A1 %d A2 %d\n", kTaskA1Complete, kTaskA2Complete);
  for (int w = 0; w < 15; w++) {
    const float p[2] = {1.0f - yes[w], yes[w]};
    pp_add(pp, p, 2);
    const float mean = pp_mean(pp, 1, 3);
    const int event = pp_event(pp, is_keyword, 2, 3, 0.6f, 1000, 250u * (w + 1));
    printf("window %2d  p %.2f  mean %.2f  event %d\n", w + 1, yes[w], mean, event);
    if (event >= 0) events++;
  }
  printf("events: %d\n", events);
  return 0;
}
