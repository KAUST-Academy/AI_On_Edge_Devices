# Day 13 report: a monitored inference application (example)

This example comes from a test on an x86 processor with 4 cores: the Day 8
model `cupbottle_320_ncnn_model`, and the 100 test images of the Day 8
dataset in place of the camera. A value that only the Raspberry Pi and its
camera can give is "measure in the lab".

Group: g07 (example). Model file: `cupbottle_320_ncnn_model`.

## Part A: instrument

| Value | Result |
|---|---|
| Output of `python monitor.py` | `Task A1: complete`, `Task A2: complete` |
| Frames each second (a printed line) | 16.5 in the example; measure in the lab |
| Latency mean and p95 of a frame | 60.5 ms and 64.9 ms in the example; measure in the lab |
| Mean top score with the cup and the bottle in view | 0.538 with the test images; measure in the lab |
| Brightness and sharpness | 107.4 and about 730 with the test images; measure in the lab |
| CPU temperature and memory of the detector (`rss`) | about 400 MB of memory; measure the temperature in the lab |

The log:

| Value | Result |
|---|---|
| Records after 2 minutes | about 14: `start`, 11 or 12 summaries, `stop` (calculation: one summary each 10 s) |
| Size of the file after 2 minutes | about 5 KB (calculation: 12 x 390 bytes and two short records) |
| Bytes of one summary record | 383 to 393, mean 390 |
| WARNING records with `--slow-ms 50` in 1 minute | measure in the lab |

Question A1. One summary each 10 s gives 8640 records each day. With 390
bytes each, that is 3 369 600 bytes, or 3.21 MB. The rotation keeps 6 files
of 1 MB: about 1.9 days.

Question A2. A hot board makes each frame slow, so the detector writes one
WARNING for each frame: about 10 records each second. The log then fills
its 6 MB in a few hours and loses the older summaries. The rotation
protects the disk. A count of the slow frames in the summary, in place of
one record for each frame, would also keep the old summaries (Part 2 of the
lecture: keep each rare event, and summarize the frequent ones).

## Part B: dashboard

| Value | Result |
|---|---|
| Messages and lost messages after 5 minutes | about 30 messages, 0 lost |
| Age of the last message | 0 s to 10 s |
| Name of the CSV file | `metrics_2026-10-03.csv` (the date of the test) |

| Value | Result |
|---|---|
| Start and end of the reference (local time) | 15:49 to 15:54 in the test (5 minutes; the lab uses 10 minutes) |
| What happened in the room during the period | nothing: the source was the 100 image files |
| Panels that changed | the mean top score and the objects moved a little from summary to summary |
| Panels that stayed flat | memory of the detector, brightness, temperature |

## Part C: drift

Output of `reference.py --min-margin 0.05`:

```
Rows:      mean 0.538  sd 0.014  min 0.515  max 0.560
Means of 6 rows: 23 means, mean 0.538  sd 0.001
Threshold: 0.488   clear: 0.521   (mean - 0.050, mean - 0.017)
```

| Value | Result |
|---|---|
| Did `reference.py` print the WARNING? Did you use `--min-margin`? | yes, 3 sd was only 0.0025; yes, 0.05 |
| Threshold and clear value of the confidence | 0.488 and 0.521 |
| Threshold of the brightness (`--metric brightness --min-margin 20`) | 87.4 (clear 100.8) |

Drift events. The test simulated the dim light with `--dim-gain`. It could
not show an unknown object.

| Event | Start, end | Mean top score | Part below 0.5 | Objects | Brightness | Sharpness |
|---|---|---|---|---|---|---|
| Normal (reference) | 15:49 to 15:54 | 0.538 | 0.42 | 1.27 | 107.4 | 731 |
| Dim light, frames x 0.25 | 3 minutes | 0.497 | 0.48 | 1.15 | 26.5 | 47 |
| Dim light, frames x 0.1 | 16:05:36 to 16:08:36 | 0.405 | 0.59 | 0.79 | 10.3 | 8.6 |
| Unknown object | | measure in the lab | | | | |

Question C1. The brightness showed each dim event most clearly: it fell
from 107 to 26 and to 10. It also names the cause. The mean top score fell
only from 0.538 to 0.497 for the frames x 0.25: this detector is robust to
a small change of the light. The sharpness also fell, because a dark image
has small differences between its pixels.

Question C2. The program gave no error. The user sees fewer counted objects:
0.79 in place of 1.25 objects in each frame for the frames x 0.1. A counter
of cups would count too few cups and give no message.

## Part D: alert

| Value | Result |
|---|---|
| First line of `alert.py` | `Task D1: complete` |
| The command of `alert.py` | `--threshold 0.488 --clear 0.521 --window 6`, duration 60 s |
| Seconds from the start of the event to `ALERT ON` | frames x 0.1: 91 s (the brightness rule: 81 s); frames x 0.25: no alert |
| Seconds from the end of the event to `ALERT OFF` | 61 s for the two rules |
| Did the state bar of the dashboard become red? | yes, `ALERT: LOW BRIGHTNESS`, then `ok` |
| Alerts during the reference period, or a false alert | none in the test |
| Did the LED of the XIAO follow the alert? | measure in the lab |

Question D1. The mean of 6 summaries passes the threshold after 2 or 3
summaries of the event: 20 s to 30 s. Then the rule waits for the duration
of 60 s. A shorter window or a shorter duration gives a faster alert. The
cost is more false alerts for short normal changes, for example a person who
stands in front of the camera for 30 s (Part 3 of the lecture).

## Incident report

| Item | Content |
|---|---|
| Event | The light of the scene fell to one tenth (simulated, frames x 0.1) |
| Start of the event (time) | 16:05:36 |
| Time of the alert, or how you found the event | `ALERT ON` of the brightness rule at 16:06:57, of the confidence rule at 16:07:07 |
| End of the event (time) | 16:08:36 |
| Effect: what was wrong, and for how long | 3 minutes with fewer counted objects (0.79 in place of 1.25 in each frame); 81 s of it before the first alert |
| Signals: values of the metrics before and during the event | mean top score 0.533 and 0.405; brightness 103.7 and 10.3; sharpness 702 and 8.6 |
| Cause | Less light on the scene |
| Action | The light came back; the alerts cleared at 16:09:37 |
| What changes so that it does not happen again | A lamp on a fixed switch; the brightness rule stays active as the first signal |

## Decision Log

Example: each camera sends one summary each 10 s (390 bytes, 3.21 MB each
day) to a broker in the shop; a dashboard stores one CSV file each day. Two
rules for each camera: the 60 s mean top score below its reference mean
minus the larger of 3 sd and 0.05, for 60 s; and the brightness below the
reference minus 20, for 60 s, as the name of the cause. The camera near the
window needs a reference for each hour of the day, else the evening fires
each day. In the test, the confidence rule missed the small light change
and fired after 91 s for the large one. Trade-off: a shorter window and
duration give a faster alert and more false alerts for the one person who
reads them.
