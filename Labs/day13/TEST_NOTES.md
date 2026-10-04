# Test notes: Day 13 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `pi/monitor.py`, `solutions/pi/monitor.py` | new | Parts 1 and 2 of the Day 13 lecture; the message format of `Labs/hardware/HW-08/metrics_publisher.py` | The student version has no body in the functions `input_stats` (Task A1) and `summarize` (Task A2) |
| `pi/monitor_detect.py` | new | The Day 8 files `pi/detector.py` and `pi/live_detect.py` (imported, not copied) | none |
| `pi/reference.py`, `solutions/pi/reference.py` | new | Part 3 of the Day 13 lecture (a threshold from a history) | The student version has no body in the function `threshold_from_history` (Task C1) |
| `pi/alert.py`, `solutions/pi/alert.py` | new | Part 3 of the Day 13 lecture (window, duration, hysteresis) | The student version has no body in the method `AlertRule.update` (Task D1) |
| `dashboard/dashboard.py`, `dashboard/index.html` | changed | `Labs/hardware/HW-08/python_dashboard/` of this course | See the list of changes below |

`python3 tools/notebooks/build_day13_scripts.py` of the course repository
makes the three student files from `solutions/pi/`.

Changes of the dashboard against HW-08:

1. The CSV file has 21 columns: the fields of HW-08 and the fields of the
   summary of `pi/monitor.py`.
2. The memory keeps 15 minutes (HW-08: 10 minutes). The page draws eight
   charts of 15 minutes (HW-08: six charts of 5 minutes).
3. The dashboard has no alert rule of its own. It subscribes to
   `edgeai/<group>/pi/alert/+` and shows the state of each rule of
   `pi/alert.py`. Each chart draws the threshold of the rule for its metric.
4. The state bar becomes yellow after 25 s with no summary (HW-08: 5 s),
   because the detector sends one summary each 10 s.

### Test on the work computer of the course (2026-10-03)

An x86 processor (the detector on 4 cores), no camera, no Raspberry Pi.
Mosquitto 2.0.11 on a free port, paho-mqtt 2.1.0, `ultralytics` 8.4.171,
the Day 8 model `cupbottle_320_ncnn_model` (exported from the weights of the
Day 8 solution run), and the 100 test images of the Day 8 dataset as the
source. The test ran in a clean copy of the two lab folders. The values say
nothing about the lab hardware.

| Test | Result |
|---|---|
| `solutions/pi/`: checks of the four tasks | `Task A1: complete`, `Task A2: complete`, `Task C1: complete`, `Task D1: complete` |
| The student versions | each check prints `not complete`; `monitor_detect.py` runs and prints `None` for the values of the summary; `reference.py` and `alert.py` stop with `Complete Task ... first` |
| Run 1: reference, 330 s | 5454 frames, 32 summaries; 16.5 frames each second; latency 60.5 ms (mean) and 64.9 ms (p95); mean top score 0.538; brightness 107.4; the dashboard got all messages, 0 lost |
| `reference.py` on run 1 | the 60 s means had a standard deviation of 0.001: the WARNING; with `--min-margin 0.05` the threshold 0.488 and the clear value 0.521 |
| Run 2: frames times 0.25 from 120 s to 300 s, the confidence rule | mean top score 0.535 before and 0.497 during the event; brightness 104 and 26; the lowest 60 s mean was 0.494, so `alert.py` did not fire (`Messages 41, alerts 0, clears 0`) |
| Run 3: frames times 0.1 from 120 s to 300 s, two rules | mean top score 0.405, objects 0.79, brightness 10.3, sharpness 8.6 during the event. The brightness rule (threshold 87.4, clear 100.8) fired after 81 s, the confidence rule after 91 s; both cleared 61 s after the end. The state bar showed `ALERT: LOW BRIGHTNESS`, then `ok`. |
| The log after the three runs | `start`, one `summary` each 10 s, and `stop` for each run; a summary record has 383 to 393 bytes (mean 390): 3.21 MB each day |
| A source that fails 30 of each 100 reads | 4 ERROR records (one for each streak of failures); the summaries counted 34 and 56 failed reads; the program continued |
| `--web` | `/stats` and `/video` of the Day 8 page answered; the program stopped with the exit code 0 after `--seconds` |
| `--model yolo11n.pt --imgsz 320` (the fallback) | 18.2 frames each second, mean top score 0.77 (80 classes) |
| The port 8080 of the work computer was in use | `dashboard.py` printed the error and the option `--http-port` |

Points that only the hardware can confirm:

- The camera path of the Day 8 detector (`picamera2`) with the summaries
  and the log.
- The frame rate on the Raspberry Pi 5, and the temperature and the bits of
  `vcgencmd get_throttled` in the summary. The work computer has no
  `vcgencmd`, so `throttled` was `null`.
- The variation of the mean top score in a real scene, and the effect of a
  real dim light and of a real unknown object.
- The LED of the XIAO with `--xiao-led` and the Day 12 sketch.

## 2. Checklist for the instructor

- Date of the test:
- Model file and frame rate of the detector on the Raspberry Pi:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, steps 2 to 4 | One printed line; the size of a summary record; the WARNING records with `--slow-ms 50` | |
| 2 | Part B, steps 2 and 3 | Does the dashboard open on the laptop? Messages and lost messages after 5 minutes | |
| 3 | Part B, step 4 | Mean and standard deviation of the 60 s means of a reference of 10 minutes with people in the room | |
| 4 | Part C, step 2, dim light | Mean top score, brightness, and objects before and during the event | |
| 5 | Part C, step 2, unknown object | The same values | |
| 6 | Part D, step 2 | Seconds from the start of the event to `ALERT ON`, and from its end to `ALERT OFF`; false alerts in 10 minutes of the normal scene | |
| 7 | `--xiao-led` with the Day 12 sketch | Does the LED follow the alert? | |
| 8 | Time the complete lab with one student group, or alone | Minutes for each part | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|
| | | |
