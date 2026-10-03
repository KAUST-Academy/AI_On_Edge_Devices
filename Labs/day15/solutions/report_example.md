# Capstone report: machine monitor (example)

Team: example   Groups: g07, g08   Date: Day 15

This example shows the form of a good report. It follows the example
proposal of the Day 14 lab (`../../day14/solutions/proposal_example.md`).
A value that only the boards can give says "measure in the lab". A value
from the lectures says "estimate" and names its source.

## 1. Problem and requirements

A workshop wants an alarm at a machine with a failing bearing, a warning
when a person is near a machine with an alarm, and a dashboard for the
technician. The lab model of a machine is a small fan with a weight on one
blade.

| No. | Requirement | Number | Test result | Met? |
|---|---|---|---|---|
| R1 | Classify the vibration | Recall of "abnormal" at least 0.9 | measure in the lab (session 3) | |
| R2 | Alarm at the machine | Within 3 s | measure in the lab (10 timed events) | |
| R3 | Alarm with no network | Works with the router off | measure in the lab | |
| R4 | Person warning | Within 2 s | measure in the lab (5 walks) | |
| R5 | Dashboard | Each 10 s | measure in the lab | |

## 2. The system

- XIAO: IMU at 50 Hz, windows of 2 s with a stride of 0.2 s, the feature
  block of Day 3, a model with 63, 20, 10, and 2 neurons in `int8`, the
  alarm on the display after 3 windows in a row.
- Raspberry Pi 5: YOLO11n at 320 pixels (NCNN) for persons, the Mosquitto
  broker, the logic program, the log, and the dashboard of Day 13.
- Topics: `edgeai/g07/xiao/event` (alarm, clear), `edgeai/g07/xiao/cmd`
  (`led=1`), `edgeai/g07/pi/metrics` (one summary each 10 s).

## 3. The five capstone requirements

| No. | Requirement | How the system meets it | Shown in the demonstration? |
|---|---|---|---|
| 1 | XIAOML Kit and Raspberry Pi | The XIAO detects the vibration; the Pi sees persons and runs the dashboard | measure in the lab |
| 2 | Optimized model | The XIAO model in `float32` and `int8` (Section 4) | measure in the lab |
| 3 | Local decision, no internet | The alarm on the XIAO, tested with the router off | measure in the lab |
| 4 | MQTT to a dashboard | The summaries of the Pi on the dashboard of Day 13 | measure in the lab |
| 5 | Benchmark table | Section 5 | measure in the lab |

## 4. Optimized model

| Model | Format | File size (bytes) | Accuracy (test set, number of samples) |
|---|---|---|---|
| Vibration model, 1512 parameters | `float32` | measure in the lab (estimate: about 8300, the Day 4 model with 4 classes has 8328) | measure in the lab (session 3) |
| Vibration model, 1512 parameters | `int8` | measure in the lab (estimate: about 5000, the Day 4 model has 4960) | measure in the lab (session 3) |

## 5. Benchmark table

| Model | Board | Format | Latency median (ms) | Latency p95 (ms) | Memory | Energy for each inference |
|---|---|---|---|---|---|---|
| Vibration model | XIAO ESP32S3 | `int8` | measure in the lab | measure in the lab | arena: measure in the lab (estimate 1028 bytes, Day 4, 32-bit build) | latency x 217 mW (Day 9 data sheet value) |
| YOLO11n, 320 pixels | Raspberry Pi 5 | NCNN | measure in the lab (published: about 80 ms) | measure in the lab | resident memory: measure in the lab | latency x the power estimate of Day 9 |

Method: 20 warm-up runs, then 200 timed runs. The window is the model only
(XIAO: `micros()` around `Invoke()`; Pi: the time of the network in the
detector of Day 8). Memory: the arena size of the sketch and the resident
memory of the Python process. Energy: an estimate from the power values of
Day 9, not a meter.

## 6. Robustness

| Test | What changed | Effect |
|---|---|---|
| Network | Router off for 2 minutes | measure in the lab: the alarm continues; the dashboard shows the gap |
| Position | The kit on a different side of the fan | measure in the lab: recall of "abnormal" |
| Light | The room light at half | measure in the lab: person count against a manual count |

## 7. Decision Log

### Decision 1: the alarm on the XIAO

The alarm decision runs on the XIAO, not on the Pi. The budget of the alarm
path is 2.6 s of the 3.0 s requirement, and the window takes 2.0 s of it.
A network step in the path adds a risk with no gain: the XIAO decides alone
and keeps working with the router off. The measured latency of the model
(measure in the lab) replaces the budget value of 100 ms. We give up a
central rule for all machines: each XIAO has its own threshold.

### Decision 2: a USB cable in place of a battery

The power budget gives 24.2 mW and 6.4 days on 1000 mAh with light sleep
and Wi-Fi 3 s each hour, and at most 22 h with Wi-Fi always connected.
Neither reaches 30 days. The demonstration uses a USB cable. We give up a
sensor with no cable, which was requirement R6 of the lecture example.

## 8. Limits and next steps

- The model learned one fan with one weight. A real bearing fault has
  other frequencies: record real machines before a product.
- The energy values are estimates from the data sheet, not a meter.
- Next: a USB power meter on the XIAO, and a test session on a second day.
