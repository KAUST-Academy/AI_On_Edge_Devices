# Capstone proposal: machine monitor

Team: example   Groups: g07, g08   Date: Day 14

This is an example for the instructor and for teams that need a model of a
good proposal. It is Example A of `Docs/capstone.md`. The values are
estimates from the lectures and the labs; the team measures them on Day 15.

## Problem and user

A workshop has machines with fans and motors. A bearing that fails makes
the machine vibrate, and today a technician hears it too late. The
technician wants an alarm at the machine and a dashboard of all machines.
Nobody should stand near a machine that has an alarm.

## Requirements with numbers

| No. | Requirement | Number | Test |
|---|---|---|---|
| R1 | Classify the vibration as normal or abnormal | Recall of "abnormal" at least 0.9 on the test sessions | Test set: one session for each state that the training does not see |
| R2 | Alarm at the machine | Within 3 s of the start of the abnormal vibration | 10 timed events, median and largest value |
| R3 | Alarm with no network | The alarm works with the router off | Switch off the Wi-Fi during the demonstration |
| R4 | Warn when a person is near a machine with an alarm | Warning within 2 s | 5 timed walks into the camera view |
| R5 | Dashboard | State of each machine each 10 s | Read the dashboard during the demonstration |

## Boards and split of the work

- XIAO on the machine (a small fan in the lab): IMU at 50 Hz, the feature
  block of Day 3, the small model, and the alarm on the display. The alarm
  path stays on the XIAO, so it needs no network (R2, R3).
- Raspberry Pi 5 with the camera: YOLO11n detects persons (Day 8), the
  broker and the logic (Day 12), the log and the dashboard (Day 13). A
  camera model needs more memory than the XIAO has.

## Model and optimization

| Model | Board | Task | Optimization | Size before / after (estimate) |
|---|---|---|---|---|
| Features and dense 63, 20, 10, 2 (1512 parameters) | XIAO | Vibration: normal, abnormal | `float32` to full `int8` (Day 4) | about 8.3 KB / 5.0 KB (the Day 4 model with 4 classes: 8328 and 4960 bytes) |
| YOLO11n, 320 pixels, NCNN | Raspberry Pi 5 | Person | none (pre-trained) | 2 616 248 parameters |

## Data

A small desk fan. "Normal": the fan as it is. "Abnormal": a small weight
taped to one blade. Three sessions on three positions of the kit, 10
recordings of 10 s for each state in each session: 60 recordings in the
Day 2 format. Training: sessions 1 and 2. Test: session 3. The team labels
each recording when it records it.

## Local decision and telemetry

- XIAO: alarm when 3 windows in a row (stride 0.2 s) are "abnormal". It
  publishes `edgeai/g07/xiao/event` (`alarm` and `clear`, QoS 1, a sequence
  number).
- Raspberry Pi: when the alarm is on and the camera sees a person, it sends
  `led=1` to `edgeai/g07/xiao/cmd`. It publishes one summary each 10 s to
  `edgeai/g07/pi/metrics` for the dashboard.

## Budgets

| Budget | Value | Source or method |
|---|---|---|
| Latency of the alarm path | 2.6 s of 3.0 s: window 2.0 s, model 0.1 s, two more windows 0.4 s, MQTT 0.1 s | `budget.py latency`; window and stride of Day 2; model and MQTT are budget values to measure |
| Flash and RAM of the XIAO model | 308 712 of 3 342 336 bytes of flash; arena about 1028 bytes of 305 848 bytes | `budget.py fit` with a program of 300 KB (estimate) and the arena of the Day 4 model (32-bit build on the work computer) |
| Power | XIAO on a battery of 1000 mAh: 24.2 mW and 6.4 days with light sleep and Wi-Fi 3 s each hour. Decision: a USB cable for the demonstration. Raspberry Pi: 5 to 7 W, mains supply | `budget.py power`; Day 9 values (data sheet and Seeed); Pi range of *Edge AI Engineering* |
| Data to the dashboard | 3.5 MB each day with a summary of about 400 bytes each 10 s | `budget.py data` (estimate of the message size) |

## The five requirements

1. XIAOML Kit and Raspberry Pi: the XIAO detects the vibration, the Pi sees
   the persons and runs the dashboard.
2. Optimized model: the XIAO model in `float32` and `int8`, with the file
   size and the recall on session 3.
3. Local decision: the alarm on the XIAO. Test: the router off.
4. Telemetry: MQTT to the broker on the Pi, the dashboard of Day 13.
5. Benchmark table: the XIAO model (arena, flash, latency, energy from the
   Day 9 values) and YOLO11n on the Pi (latency, memory, power estimate).

## Riskiest assumption and first test

- Assumption: the IMU separates the two states of the fan.
- First test (Day 14, Part D): record two sessions of each state with the
  Day 2 logger, and train the Day 3 model in the notebook.
- Plan B: the RMS of the acceleration and one threshold, with no model; or
  a larger weight on the blade.
