# Day 13 lab: a monitored inference application


**Goal.** Your group adds measurements and a log to the Day 8 detector on
the Raspberry Pi 5. The detector sends one summary each 10 s with MQTT to a
live dashboard. You record a normal reference period, cause drift events
(less light, an unknown object), find them in the metrics, and test one
alert rule.

**Deliverable.** The live dashboard during a drift event, and the file
`report.md` with the measured values, a short incident report of one drift
event, and the Decision Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Instrument: measurements, summary, and a JSON log with rotation | 40 min |
| B | Dashboard: summaries with MQTT, the live dashboard, a reference period | 45 min |
| C | Drift: a threshold from the reference, two drift events | 40 min |
| D | Alert: one rule with a window, a duration, and hysteresis | 25 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| Raspberry Pi 5 with the active cooler and the camera | 1 | With the microSD card of the course |
| Power supply for the Raspberry Pi 5 | 1 | 27 W, USB-C |
| Laptop | 1 | In the lab network, with an SSH client and a browser |
| A cup and a bottle | 1 each | The classes of the Day 8 model |
| An object that the model does not know | 1 | For example a phone, a box, or a book |
| A desk lamp, or the light of the room | 1 | For the dim light event |
| XIAOML Kit with the Day 12 sketch `kws_mqtt` | 1 | Optional: its LED shows the alert |

## Software

| Tool | Version | Note |
|---|---|---|
| The environment `~/yolo` on the Raspberry Pi | `ultralytics` 8.4.171, `ncnn`, `paho-mqtt` 2.1, `psutil`, `flask` | `Labs/hardware/HW-04/setup_pi.sh` installs them. |
| Mosquitto broker on the Raspberry Pi | the card of the course | The broker of the Day 12 lab, port 1883 |
| The Day 8 lab folder on the Raspberry Pi | `~/edgeai/day08/` | `../day08/pi/detector.py`, `../day08/pi/live_detect.py`, and the model `models/cupbottle_320_ncnn_model` of Day 8 Part C |
| Mosquitto clients on the laptop | any version 2 | Optional: `mosquitto_sub` |

`NN` is the number of your group, and `gNN` is its group name (for example
`g07`). Your Raspberry Pi has the name `pi-NN`. The examples use the group
`g07`. Run the commands on the Raspberry Pi in `~/edgeai/day13/pi/`, unless
a step names a different folder. `PY` is `~/yolo/bin/python`.

## Topics

| Topic | From | To | Payload | QoS, retained |
|---|---|---|---|---|
| `edgeai/gNN/pi/metrics` | `pi/monitor_detect.py` | dashboard, `pi/alert.py` | one summary each 10 s | 0, no |
| `edgeai/gNN/pi/status` | `pi/monitor_detect.py` | all | `online`, or `offline` (last will) | 1, yes |
| `edgeai/gNN/pi/alert/<metric>` | `pi/alert.py` (one topic for each rule) | dashboard | the state of the rule: `firing` or `ok` | 1, yes |
| `edgeai/gNN/xiao/cmd` | `pi/alert.py` with `--xiao-led` | XIAO (Day 12 sketch) | `led=1` or `led=0` | 1, no |

A summary has the fields of the HW-08 dashboard (`seq`, `ts`, `latency_ms`,
`fps`, `confidence`, `cpu_temp_c`, `cpu_percent`, `ram_used_mb`) and more:
`frames`, `latency_p95_ms`, `latency_max_ms`, `low_conf`, `objects`,
`brightness`, `sharpness`, `throttled`, `rss_mb`, `disk_free_pct`, `errors`,
and `dimmed`. Here `confidence` is the mean of the top score of each frame:
the largest box score of the frame, or 0 when the frame has no box above
0.05.

## Files

| File | Content |
|---|---|
| `report.md` | The report to hand in. Fill it during the lab. |
| `pi/monitor.py` | Part A. Measurements, summary, system metrics, the log, and the MQTT sender. **Task A1** and **Task A2** are in this file. |
| `pi/monitor_detect.py` | Parts A to D. The Day 8 detector with the measurements of `pi/monitor.py` |
| `pi/reference.py` | Part C. A threshold from a reference period. **Task C1** is in this file. |
| `pi/alert.py` | Part D. One alert rule on the summaries. **Task D1** is in this file. |
| `dashboard/dashboard.py`, `dashboard/index.html` | Part B. The live dashboard: the Python dashboard of HW-08 with eight charts and the state of the alert |
| `solutions/` | The complete task files and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

The programs write into two folders that git ignores: `logs/` (the JSON log
of the detector) and `dashboard/metrics_log/` (one CSV file each day).

## Steps

Write each result in `report.md` when you get it.

### Part A: instrument (40 min)

1. **Copy the lab folder (5 min).** On the laptop, in `Labs/`:
   `scp -r day13 edge@pi-07.local:edgeai/`. On the Raspberry Pi, check that
   the Day 8 folder and its model are there:

   ```bash
   ls ~/edgeai/day08/pi/detector.py ~/edgeai/day08/models/cupbottle_320_ncnn_model
   ```

2. **Task A1 and Task A2 (15 min).** Open `pi/monitor.py`. Complete the two
   functions `input_stats` (brightness and sharpness of a frame) and
   `summarize` (one summary of the frames of 10 s). The docstrings give the
   formulas. Copy the file to the Raspberry Pi and check it:

   ```bash
   cd ~/edgeai/day13/pi
   ~/yolo/bin/python monitor.py
   ```

   You see `Task A1: complete` and `Task A2: complete`.

3. **Run the detector with the log (10 min).** Put the cup and the bottle in
   front of the camera. Run the detector for 2 minutes with no MQTT:

   ```bash
   ~/yolo/bin/python monitor_detect.py \
       --model ../../day08/models/cupbottle_320_ncnn_model \
       --group g07 --no-mqtt --seconds 120
   ```

   Each 10 s, one line shows the frame rate, the latency (mean and p95), the
   mean top score, the part of the frames below 0.5, the objects, the
   brightness, the sharpness, the temperature, and the memory of the
   detector. Write one line in the report. Cover the lens with a hand for
   10 s: write which values change.

4. **Read the log (10 min).**

   ```bash
   wc -l -c ../logs/detector.jsonl
   tail -n 1 ../logs/detector.jsonl | python3 -m json.tool
   ```

   The first record is `start`, then one `summary` each 10 s, then `stop`.
   Write the number of records and the size. Run step 3 again for 1 minute
   with `--slow-ms 50 --seconds 60`, and count the WARNING records:
   `grep -c slow_frame ../logs/detector.jsonl`. Answer questions A1 and A2.

### Part B: dashboard (45 min)

1. **Check the broker (5 min).** `systemctl is-active mosquitto` prints
   `active` (Day 12).

2. **Start the dashboard (10 min).** In a second SSH terminal:

   ```bash
   cd ~/edgeai/day13/dashboard
   ~/yolo/bin/python dashboard.py --group g07
   ```

   Open `http://pi-07.local:8080` in the browser of the laptop. The state
   bar says `Waiting for data ...`, then `no alert program`.

3. **Start the detector with MQTT (10 min).** In the first terminal:

   ```bash
   ~/yolo/bin/python monitor_detect.py \
       --model ../../day08/models/cupbottle_320_ncnn_model --group g07
   ```

   The eight charts of the dashboard get one point each 10 s. On the laptop,
   `mosquitto_sub -h pi-07.local -t 'edgeai/g07/pi/#' -v` shows the
   messages. Write the values of the state bar after 5 minutes.

4. **Reference period (20 min).** Keep the scene normal for 10 minutes: the
   cup and the bottle in view, the normal light. People can move in the
   room as usual. Write the start and the end time. Do not stop the
   detector. During this time, complete **Task C1** in `pi/reference.py`
   (the means of 6 summaries, then mean - 3 sd), and copy the file to the
   Raspberry Pi. Write which panels move and which stay flat.

### Part C: drift (40 min)

Keep the dashboard and the detector running.

1. **Threshold (10 min).** In a third SSH terminal, with the date of today
   and the times of your reference period:

   ```bash
   cd ~/edgeai/day13/pi
   ~/yolo/bin/python reference.py \
       --csv ../dashboard/metrics_log/metrics_2026-10-05.csv \
       --start 10:20 --end 10:30 --group g07
   ```

   It prints `Task C1: complete`, the mean and the standard deviation, the
   threshold, the clear value, and the command for `pi/alert.py`. If it prints
   `WARNING: the reference has almost no variation`, run it again with
   `--min-margin 0.05`. Run it also with `--metric brightness`. Write the
   values.

2. **Drift events (20 min).** Make two events of 3 minutes each, with 3
   minutes of the normal scene between them. Write the start and the end
   time of each event.
   - **Dim light**: switch off the light of the room or turn the lamp away.
   - **Unknown object**: put your unknown object in place of the cup.

   Watch the dashboard. For each event, write the values of the table of the
   report (from the printed lines of `pi/monitor_detect.py`).

3. **Analysis (10 min).** Answer questions C1 and C2.

### Part D: alert (25 min)

1. **Task D1 (10 min).** Open `pi/alert.py`. Complete the method `update`
   of the class `AlertRule`: the mean of the last 6 values, a duration, and
   hysteresis. Copy the file to the Raspberry Pi.

2. **Test the alert (15 min).** In the third terminal, start the command
   that `pi/reference.py` printed, for example:

   ```bash
   ~/yolo/bin/python alert.py --group g07 --metric confidence \
       --threshold 0.488 --clear 0.521 --window 6
   ```

   It prints `Task D1: complete` and the rule. Make the dim light event
   again for 3 minutes. Write the time from the start of the event to
   `ALERT ON`, and from the end of the event to `ALERT OFF`. The state bar of
   the dashboard is red during the alert. With the XIAO of Day 12, add
   `--xiao-led`: its LED is on during the alert. Then write the incident
   report and answer question D1.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] `pi/monitor_detect.py` prints `Task A1: complete` and `Task A2:
      complete`, and the log has `start`, `summary`, and `stop` records.
- [ ] The dashboard shows the live system and model metrics, and the state
      bar shows no lost message.
- [ ] `pi/reference.py` prints `Task C1: complete` and a threshold from your
      reference period.
- [ ] Live demonstration: during a dim light event, `pi/alert.py` (with `Task
      D1: complete`) prints `ALERT ON` and the state bar becomes red. After
      the event, the alert clears.
- [ ] The report has the incident report and a Decision Log with numbers
      and one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured
numbers, and name the trade-off.

Question of this lab: a shop uses 20 Raspberry Pi cameras to count the
people at its doors. One camera stands near a window, so its light changes
with the time of day. The shop has one person who looks at alerts. Which
metrics does each device send, how often, and where are they stored? Which
alert rules do you use, with which thresholds, windows, and durations? How
many false alerts each week do you expect, and what does the person do for
each alert?

## Expected values

The values come from a test on an x86 processor with 4 cores: the Day 8
model in NCNN at 320 pixels, and the 100 test images of the Day 8 dataset
in place of the camera. They say nothing about the Raspberry Pi. The
values of your camera scene are different.

- Part A: 16.5 frames each second, a latency of 60.5 ms (mean) and 64.9 ms
  (p95) for one frame on that machine. The Raspberry Pi 5 is slower:
  the companion book gives about 80 ms for the inference of a custom
  YOLO11n model in NCNN at 320 pixels. A summary record of the log has about
  390 bytes. One summary each 10 s gives 3.21 MB each day, so the rotation
  (6 files of 1 MB) keeps about 1.9 days.
- Part C: with the test images, the 60 s means of the reference had almost
  no variation (standard deviation 0.001), because the same 100 images came
  again and again. `pi/reference.py` printed the WARNING, and `--min-margin
  0.05` gave the threshold 0.488 and the clear value 0.521 (mean 0.538).
  A camera scene with people in the room gives more variation.
- Part C: frames times 0.25 (simulated dim light): the mean top score went
  from 0.535 to 0.497, the brightness from 104 to 26. Frames times 0.1: the
  mean top score went to 0.405, the objects from 1.25 to 0.79, the
  brightness to 10.3, and the sharpness from about 700 to 8.6.
- Part D: with the frames times 0.25, the confidence rule did not fire: the
  lowest 60 s mean was 0.494, above 0.488. The brightness showed the event
  clearly. With the frames times 0.1, the confidence rule fired 91 s after
  the start of the event, and a brightness rule (threshold 87.4 with
  `--min-margin 20`) fired after 81 s. Both cleared 61 s after the end. The
  delay is the time until the mean of 6 summaries passes the threshold (2
  or 3 summaries of the event), plus the duration of 60 s.

## If a part does not work

| Problem | Fallback |
|---|---|
| A task is not complete in time | Use the file of the folder `solutions/pi/`, and write this in the report |
| The Day 8 model is not on the card | Download the pre-trained model of the package once: `~/yolo/bin/python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"`. Then use `--model yolo11n.pt --imgsz 320`. It has the classes `cup` and `bottle` in its 80 classes, and `objects` counts all classes. |
| The camera does not work | Use image files: `--source <folder with images>`. The values change with each image. |
| The light of the room cannot change | Simulate the event: `--dim-after 60 --dim-gain 0.1 --dim-seconds 180` multiplies each frame by 0.1 for 3 minutes. In the test, the factor 0.25 did not fire the confidence rule. |
| The broker does not run | `sudo systemctl start mosquitto`, or run `pi/monitor_detect.py` with `--no-mqtt` and read the log |
| The port 8080 is in use | `dashboard.py --http-port 8081` |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| `ERROR: the Day 8 file pi/detector.py is not found` | The Day 8 folder is not at `~/edgeai/day08/` | Copy it from the laptop: `scp -r day08 edge@pi-07.local:edgeai/` |
| The charts stay empty | The detector runs with `--no-mqtt`, or with a different group | Start it with `--group g07` and no `--no-mqtt` |
| The state bar is yellow | No summary for 25 s: the detector stopped | Look at the terminal of the detector |
| `pi/reference.py` says `only N rows in the period` | Wrong times, or a different date of the file | Use the times of the printed lines and the CSV file of today |
| The alert fires during the normal scene | The threshold is too near the mean | Record a longer reference period, or use `--min-margin 0.05` |
| The alert does not fire during the event | The event is too short for the window and the duration | Make the event longer than 2 minutes, or use `--for-seconds 30` |
| `Task A2: not complete` with a sum that looks right | A key is missing, or a value is not rounded | Compare the keys with the docstring; round each float to 3 decimals |

## Credits

This lab adapts material from these sources:

- The Day 8 lab of this course: the detector (`../day08/pi/detector.py`), the web
  page, and the model. Its camera code follows `object_detection_app.py` of
  "EdgeML with Raspberry Pi" by Marcelo Rovai
  (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0).
- The Python dashboard of `Labs/hardware/HW-08/` of this course. Its CSV log
  follows `data_logger.py` of "EdgeML with Raspberry Pi" by Marcelo Rovai
  (GPL-3.0).
- "Machine Learning Systems" by Vijay Janapa Reddi and contributors
  (mlsysbook.ai, CC BY-NC-SA 4.0), chapter "ML Operations": the monitoring
  method, through the Day 13 lecture.
- Ultralytics YOLO (github.com/ultralytics/ultralytics, AGPL-3.0): the
  package that runs the model.
- Eclipse Mosquitto (mosquitto.org, EPL-2.0 or EDL-1.0) and Eclipse Paho
  Python client (eclipse.dev/paho, EPL-2.0 or BSD-3-Clause): the broker and
  the MQTT client.

The programs `pi/monitor.py`, `pi/monitor_detect.py`, `pi/reference.py`, and
`pi/alert.py`, the changes of the dashboard, the steps, and the report are
new work of this course.
