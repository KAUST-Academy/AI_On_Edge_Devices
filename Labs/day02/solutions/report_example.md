# Day 2 lab report: example

This example has the parts of the report that need no board. The numbers of
Part C come from the solution notebook with the fallback dataset. The
signals of the fallback dataset are simulated. Nobody recorded them. The
parts that need a board say "measure in the lab".

Group: example

## Part A: MicroPython start

| Item | Your result |
|---|---|
| MicroPython version (`sys.implementation`) | measure in the lab. The firmware file has the version v1.29.0. |
| Clock frequency (`machine.freq()`) in Hz | measure in the lab |
| Free memory (`gc.mem_free()`) in bytes | measure in the lab |
| Timer events of `blink_timer.py` in 10 s | 20. The timer has a frequency of 2 Hz. |
| I2C addresses of the scan | `0x3C` (display) and `0x6A` (IMU) |

## Part B: sensor input

The six values of `imu.read()` with the kit flat on the table: measure in
the lab. The kit chapter says: the z axis is near 1.0 g, the x axis and the
y axis are near 0, and the three gyroscope values are near 0.

Prediction. The first version of `imu_stream.py` waits 20 ms after each
sample.

- An example of a prediction: the rate is lower than 50 Hz. One period is
  20 ms plus the time for the read and for the print. With 1 ms for this
  work, the period is 21 ms, and the rate is 1000 / 21 = 47.6 Hz.

Results of `host/check_rate.py`: measure in the lab.

| Version | Connection | Mean rate (Hz) | Minimum period (us) | Maximum period (us) | Lost lines | Result |
|---|---|---|---|---|---|---|
| Fixed wait of 20 ms | Serial port | measure in the lab | | | | |
| Deadline (task B1) | Serial port | measure in the lab | | | | PASS is necessary for the check |
| Deadline (`imu_wifi.py`) | Wi-Fi | measure in the lab | | | | |

- Why is the rate of the first version not 50 Hz? The wait of 20 ms starts
  after the work of the loop. The time for the read and for the print adds
  to each period.
- Which connection loses samples, and why? Only Wi-Fi can lose samples. The
  script sends UDP packets, and UDP does not repeat a packet that the
  network loses. One lost packet is 5 lost samples.

## Part C: dataset

### The collection protocol

| Class | Definition of the motion (one sentence) |
|---|---|
| `idle` | The kit lies on the table with the display up, and nobody touches it. |
| `terrestrial` | The hand moves the kit left and right in a horizontal line, about one cycle each second. |
| `lift` | The hand moves the kit up and down, about one cycle each second. |
| `maritime` | The hand moves the kit slowly on all three axes and turns it, as a boat on waves. |

| Session | Person | What is different from the other sessions |
|---|---|---|
| `s1` | A | medium speed |
| `s2` | B | a different person, slow motion |
| `s3` | A | fast motion, after a pause |

### The leakage experiment (task 4 of the notebook)

| Question | Your prediction | Result |
|---|---|---|
| The procedure with the higher test accuracy (A, B, or equal) | A | A |
| Test accuracy of procedure A in percent | 99 | 100.0 |
| Lowest test accuracy of procedure B in percent | 85 | 75.6 |

Answers:

1. The prediction was correct for the direction. Procedure A gives 100.0
   percent. Procedure B gives 100.0, 75.6, and 100.0 percent for the test
   sessions `s1`, `s2`, and `s3`. The mean is 91.9 percent.
2. In procedure A, adjacent windows of one recording have an overlap of 90
   percent, and one of them is in the training set. All recordings of each
   session are also in the two sets. The classifier finds an almost equal
   window in the training set.
3. The mean of procedure B, with the lowest value next to it. The device
   will meet new sessions and new persons. Three sessions are a small
   sample, so the estimate is not exact.

### The data card

| Field | Your dataset |
|---|---|
| Name and version | Motion of a package, fallback dataset, v1 |
| Classes | `idle`: no motion. `terrestrial`: motion in the horizontal plane. `lift`: motion up and down. `maritime`: slow motion on all axes. |
| Sensor and settings | Simulated signals in the format of the LSM6DS3TR-C: range 16 g and 2000 dps, three acceleration axes and three gyroscope axes |
| Sampling rate, nominal and measured | 50 Hz nominal. 50.00 Hz in each file (simulated time stamps). |
| Duration of each class | 120 s for each class, 480 s in total |
| Sessions and persons | `s1`, `s2`, `s3`. No person: the signals are simulated. |
| Split: training sessions and test sessions | Training: `s1` and `s2`. Test: `s3`. |
| Number of recordings and of windows in each set | 32 recordings and 1312 windows for the training. 16 recordings and 656 windows for the test. |
| Checks and their results | 48 recordings checked. 500 rows in each recording. No lost sample, no clipped sample, no recording with a problem. |
| Known limits | The signals are simulated. A model that learns from this data does not work on the real kit. Three sessions only. The classifier with six features fails for the class `lift` in session `s2`, because the tilt of the kit is different in that session. |

## Part D: Edge Impulse

Measure in the lab. The program `host/to_edge_impulse.py` writes 32 files
into `ei_upload/training/` and 16 files into `ei_upload/testing/` for the
fallback dataset. The Studio then shows a ratio near 67 percent to 33
percent.

## Decision Log

An example with the numbers of the fallback dataset:

We record a new session with a different person. Procedure A gave 100.0
percent, but this number comes from overlapping windows. Procedure B gave
between 75.6 and 100.0 percent for a new session, so the model depends on
the session. More recordings in the same three sessions give more windows
that are almost equal to the windows that we have. They do not show the
model a new person or a new angle of the kit. A new session adds variation.
The trade-off: a new person needs time for the instructions, so we get
fewer recordings in the 10 minutes, and the classes of the new session can
have less data than the classes of the first sessions.
