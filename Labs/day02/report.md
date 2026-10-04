# Day 2 lab report

Group:

Names:

Date:

## Part A: MicroPython start

| Item | Your result |
|---|---|
| MicroPython version (`sys.implementation`) | |
| Clock frequency (`machine.freq()`) in Hz | |
| Free memory (`gc.mem_free()`) in bytes | |
| Timer events of `blink_timer.py` in 10 s | |
| I2C addresses of the scan | |

## Part B: sensor input

The six values of `imu.read()` with the kit flat on the table:

| ax (g) | ay (g) | az (g) | gx (dps) | gy (dps) | gz (dps) |
|---|---|---|---|---|---|
| | | | | | |

Prediction before the measurement. The first version of `imu_stream.py`
waits 20 ms after each sample. Is the real rate equal to 50 Hz, lower, or
higher? By how much?

- Your prediction:

Results of `host/check_rate.py`:

| Version | Connection | Mean rate (Hz) | Minimum period (us) | Maximum period (us) | Lost lines | Result |
|---|---|---|---|---|---|---|
| Fixed wait of 20 ms | Serial port | | | | | |
| Deadline (task B1) | Serial port | | | | | |
| Deadline (`imu_wifi.py`) | Wi-Fi | | | | | |

One sentence for each question:

- Why is the rate of the first version not 50 Hz?
- Which connection loses samples, and why?

## Part C: dataset

### The collection protocol

Write this part before the first recording.

| Class | Definition of the motion (one sentence) |
|---|---|
| `idle` | |
| `terrestrial` | |
| `lift` | |
| `maritime` | |

| Session | Person | What is different from the other sessions |
|---|---|---|
| `s1` | | |
| `s2` | | |
| `s3` | | |

### The leakage experiment (task 4 of the notebook)

Write the prediction before you run section 6 of the notebook.

| Question | Your prediction | Result |
|---|---|---|
| The procedure with the higher test accuracy (A, B, or equal) | | |
| Test accuracy of procedure A in percent | | |
| Lowest test accuracy of procedure B in percent | | |

Your answers:

1. Compare the result with your prediction.
2. Why is the result of procedure A too high? Use the words "overlap" and
   "session".
3. The results of procedure B are different for each test session. Which
   number do you give to a customer, and why?

### The data card

| Field | Your dataset |
|---|---|
| Name and version | |
| Classes | |
| Sensor and settings | |
| Sampling rate, nominal and measured | |
| Duration of each class | |
| Sessions and persons | |
| Split: training sessions and test sessions | |
| Number of recordings and of windows in each set | |
| Checks and their results | |
| Known limits | |

## Part D: Edge Impulse

| Item | Your result |
|---|---|
| Name of the project | |
| Duration of the training data | |
| Duration of the test data | |
| Ratio between training and test data that the Studio shows | |
| Do the four labels agree with your file names? | |

## Decision Log

About 100 words. Your group has 10 more minutes to record data. Do you add
more recordings to the three sessions that you have, or do you record a new
session with a different person? State the decision, give the two results
of your leakage experiment, and name the trade-off.

## Problems

Write each problem that you had, and how you solved it.
