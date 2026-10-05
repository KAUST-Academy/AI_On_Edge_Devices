# Day 11 lab: inference on a network video stream


**Goal.** Your group measures the lab network, publishes the camera of the
Raspberry Pi 5 as an RTSP stream, runs the Day 8 detector on the stream, and
measures the end-to-end latency. Then you stream the camera of the XIAOML
Kit as MJPEG and compare the two streams.

**Deliverable.** A live demonstration of the detector on the network stream,
and the file `report.md` with the network values, the latency for two stream
settings, the values of the XIAO stream, and the Decision Log.

**Time.** The quiz of Week 2 (20 minutes), then 130 minutes of work, then 30
minutes for the check by the instructor.

| Part | Content | Time |
|---|---|---|
| Quiz | The quiz of Week 2 (Days 6 to 10) | 20 min |
| A | Network tools: find the devices, measure the throughput | 20 min |
| B | RTSP server: publish the camera with MediaMTX, open the stream | 40 min |
| C | Inference on the stream: the detector, the latency, two settings | 45 min |
| D | Microcontroller camera: an MJPEG stream of the XIAO, a comparison | 25 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| Raspberry Pi 5 with the active cooler and the camera of Day 8 | 1 | With the microSD card of the course |
| Power supply for the Raspberry Pi 5 | 1 | 27 W, USB-C |
| XIAOML Kit with its camera | 1 | With a USB-C cable for the laptop |
| Laptop | 1 | In the lab network, with an SSH client |
| The router of the lab | 1 for the class | Wi-Fi `edgeai-lab` with 2.4 GHz (`Labs/hardware/HW-09/`) |
| Ethernet cable and a switch | optional | Write in the report which connection the Raspberry Pi used |

## Software

| Tool | Version | Note |
|---|---|---|
| MediaMTX on the Raspberry Pi | v1.21.1 in `~/mediamtx` with `mediamtx_cam.yml` | `Labs/hardware/HW-06/` installs it on the card |
| `iperf3`, `ffmpeg`, `avahi-utils` on the Raspberry Pi | the card of the course | `Labs/hardware/HW-04/setup_pi.sh` installs them |
| The Day 8 environment on the laptop, `~/day08_env` | `ultralytics` 8.4.171 with `opencv-python` | `Labs/day08/requirements.txt`. It runs `stream_detect.py`. |
| The Day 8 lab folder on the laptop | `day08/pi/detector.py`, `day08/models/yolo11n.pt`, and your exported models | The detector of the Day 8 lab |
| `iperf3` on the laptop | any version 3 | Linux: package `iperf3`. macOS: `brew install iperf3`. Windows: the build of `iperf.fr`. |
| `ffplay` (FFmpeg) or VLC on the laptop | any | To see the stream |
| Arduino IDE with the esp32 core | core 3.3.12 | `Labs/SETUP.md` |

`NN` is the number of your group. Your Raspberry Pi has the name `pi-NN` and
the address `X.(100+NN)`. The examples use the network `192.168.8` of
`Labs/hardware/HW-09/`. Use the network of your router. Run the laptop
commands in the folder `Labs/day11/`.

## Files

| File | Content |
|---|---|
| `report.md` | The report to hand in. Fill it during the lab. |
| `stream_detect.py` | Parts B, C, and D. Reads an RTSP or an MJPEG stream, runs the Day 8 detector, shows a clock for the latency. **Task C1** is in this file. |
| `mjpeg_rate.py` | Part D. Measures the frame rate, the JPEG size, and the bit rate of an MJPEG stream. **Task D1** is in this file. |
| `sketches/xiao_mjpeg_stream/` | Part D. The sketch that sends the camera of the XIAO as MJPEG over HTTP |
| `solutions/` | The complete scripts and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

The lab also uses these files of other folders:

| File | Part |
|---|---|
| `../hardware/HW-09/net_check.py` | A: the scan and the check of the Raspberry Pi |
| `~/mediamtx/mediamtx_cam.yml` on the Raspberry Pi (a copy of `../hardware/HW-06/mediamtx_cam.yml`) | B and C: the settings of the stream |
| `../day08/pi/detector.py` | C and D: `stream_detect.py` imports it |

`stream_detect.py` adds one row to `results.csv` for each run, and it saves
the images of the clock as `latency_<label>_NN.png`. Git ignores these files.

## Steps

Write each result in `report.md` when you get it.

### Quiz (20 min)

The instructor gives the quiz of Week 2. It covers Days 6 to 10.

### Part A: network tools (20 min)

1. **Addresses (5 min).** Connect the laptop to `edgeai-lab`. Start the
   Raspberry Pi. On the laptop and on the Raspberry Pi
   (`ssh edge@pi-NN.local`), run:

   ```bash
   ip -br addr
   ip route
   ```

   Write the address of each device and the router (`default via`) in the
   report. macOS: `ifconfig` and `netstat -rn`. Windows: `ipconfig`.

2. **Find the devices (5 min).** On the laptop:

   ```bash
   python3 ../hardware/HW-09/net_check.py --scan 192.168.8.0/24
   python3 ../hardware/HW-09/net_check.py pi-NN.local --need 22
   ```

   The scan prints one line for each device that answers, and the number of
   devices. The check prints `RESULT: PASS` when the name, `ping`, and SSH
   work.

3. **Throughput, jitter, and loss (10 min).** On the Raspberry Pi, start
   the server: `iperf3 -s`. On the laptop:

   ```bash
   iperf3 -c pi-NN.local -t 10          # laptop to Raspberry Pi
   iperf3 -c pi-NN.local -t 10 -R       # Raspberry Pi to laptop
   iperf3 -c pi-NN.local -t 10 -u -b 20M
   ping -c 100 -i 0.2 pi-NN.local
   ```

   With `-R`, the data goes in the direction of the video. Write the bit rate of the `receiver` lines, the jitter and the lost
   datagrams of the UDP test, and the last two lines of `ping`. Stop the
   server with `Ctrl-C`.

### Part B: RTSP server (40 min)

1. **Start the server (10 min).** On the Raspberry Pi:

   ```bash
   cd ~/mediamtx
   cp mediamtx_cam.yml mediamtx_cam.yml.orig
   ./mediamtx mediamtx_cam.yml
   ```

   The log shows `[RTSP] started with listeners on :8554 (TCP/RTSP)` and,
   when the camera works, `[path cam] stream is available and online`. Keep
   this terminal open.

2. **Check the port (5 min).** In a second SSH terminal:

   ```bash
   ss -tln | grep 8554
   top -b -n 1 | grep mediamtx
   ```

   `ss` must show `*:8554` or `0.0.0.0:8554`, not `127.0.0.1:8554`. Write the
   CPU load of `mediamtx`. The Raspberry Pi 5 encodes H.264 in software.

3. **Open the stream (10 min).** On the laptop:

   ```bash
   ffplay -fflags nobuffer -flags low_delay -rtsp_transport tcp \
       rtsp://pi-NN.local:8554/cam
   ```

   VLC also works: `Media`, then `Open Network Stream`, then the same
   address. Write the seconds until the first image. Close the window.

4. **Task C1 (5 min).** Open `stream_detect.py`. Complete the method
   `_store` of the class `NewestFrameReader`. It keeps only the newest
   frame: no list, no queue.

5. **Read the stream in Python (10 min).** On the laptop, set two shell
   variables for the rest of the lab: the Python of the Day 8 environment and
   the address of the stream. Then run the script:

   ```bash
   PY=~/day08_env/bin/python
   URL=rtsp://pi-NN.local:8554/cam
   $PY stream_detect.py $URL --seconds 20
   ```

   The script prints `Task C1: complete`, then one line each 2 seconds:

   ```
   1280x720  stream 30.0 frames/s  processed 30.0 frames/s  skipped 0
   ```

   and at the end one line that starts with `RESULT`. With no model, the
   two rates must be almost the same.

### Part C: inference on the stream (45 min)

1. **The detector (10 min).** Run the pre-trained model and your model of
   Day 8:

   ```bash
   $PY stream_detect.py $URL --seconds 30 --show \
       --model ../day08/models/yolo11n.pt --imgsz 320
   $PY stream_detect.py $URL --seconds 30 --show \
       --model ../day08/models/cupbottle_320_ncnn_model
   ```

   The window shows the boxes. Each line now also gives `model` (the time
   of the detector in ms) and `objects`. Write the processed frame rate,
   the skipped frames each second, and the model time.

2. **Latency of setting 1 (15 min).** Run the clock, first with no model,
   then with the detector:

   ```bash
   $PY stream_detect.py $URL --clock --label hd_nomodel
   $PY stream_detect.py $URL --clock --label hd_yolo \
       --model ../day08/models/yolo11n.pt --imgsz 320
   ```

   A window shows a clock on the left and the stream on the right. Point
   the camera of the Raspberry Pi at the clock. Press `s` 10 times, with
   about 1 second between two presses, then `q`. In each image
   `latency_<label>_NN.png`, read the clock on the left and the clock in the
   stream. The difference is the end-to-end latency. Write the 10 values,
   the median, the minimum, and the maximum.

3. **Setting 2 (15 min).** Stop MediaMTX with `Ctrl-C`. In
   `~/mediamtx/mediamtx_cam.yml`, set `rpiCameraWidth: 640`,
   `rpiCameraHeight: 480`, and `rpiCameraBitrate: 500000`. Start MediaMTX
   again. Repeat step 2 with the detector and `--label sd_yolo`.

4. **In order (5 min).** Read each frame in order, with a slow model:

   ```bash
   $PY stream_detect.py $URL --seconds 30 --in-order \
       --model ../day08/models/yolo11n.pt --imgsz 640
   ```

   Each line ends with `behind ... s`: the time that the reader is behind
   the live stream. Write the value after 30 s. Then restore the settings:
   `cp mediamtx_cam.yml.orig mediamtx_cam.yml`, and start MediaMTX again.

### Part D: microcontroller camera (25 min)

1. **Upload the sketch (8 min).** In the Arduino IDE, open
   `sketches/xiao_mjpeg_stream/xiao_mjpeg_stream.ino`. Write the Wi-Fi
   password of the lab in `WIFI_PASSWORD`. Select the board
   `XIAO_ESP32S3` and `Tools > PSRAM > OPI PSRAM`. Upload. The Serial
   Monitor (115200 baud) prints the address, for example
   `Camera Stream Ready! Go to: http://192.168.8.163/`.

2. **See the stream (2 min).** Open the address in a browser. Close the
   browser tab again: the sketch serves one reader at a time.

3. **Task D1 and the bit rate (7 min).** Open `mjpeg_rate.py`. Complete
   the function `stream_stats`. Then run:

   ```bash
   python3 mjpeg_rate.py http://192.168.8.163/ --seconds 10 --save xiao.jpg
   ```

   The script prints `Task D1: complete`, then
   `RESULT ... fps=... mean_kb=... mbit_s=...`. Compare with the line of the
   Serial Monitor (`sent ... frames in 5 s`).

4. **Detector and latency (8 min).** Point the XIAO camera at the clock:

   ```bash
   $PY stream_detect.py http://192.168.8.163/ --clock --label xiao_yolo \
       --model ../day08/models/yolo11n.pt --imgsz 320
   ```

   Write the processed frame rate and the 10 latency values. Compare with
   the stream of the Raspberry Pi.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] `stream_detect.py` prints `Task C1: complete`, and `mjpeg_rate.py`
      prints `Task D1: complete`.
- [ ] Live demonstration: the detector draws boxes on the RTSP stream of the
      Raspberry Pi, on the laptop.
- [ ] The report gives the latency (10 values and the median) for two
      settings of the RTSP stream with the detector, and the bit rate and
      the frame rate of the XIAO stream.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured
numbers, and name the trade-off.

Question of this lab: a shop wants to count the people at its entrance. One
camera hangs at the door. A Raspberry Pi 5 stands in the back office, 15 m
away, on Wi-Fi. The count must change within 1 second after a person
enters, and no image may leave the shop. Where do you run the detector?
Which stream settings do you select? What leaves the camera, and what leaves
the shop?

## Expected values

The start values of the stream are 1280 x 720, 30 frames each second,
2 Mbit/s, and one keyframe each second (`mediamtx_cam.yml`). With no model,
`stream_detect.py` must show about 30 frames/s. Measure the latency on the
hardware of the lab. The clock method has an error of about 50 ms
for one reading: use the median of 10. A run on one computer, with no
network and no camera, gave a frame age of 40 ms with one decoder thread
(Part 3 of the lecture). Your latency also includes the camera, the
encoder of the Raspberry Pi, the Wi-Fi, and the screen.

## If a part does not work

| Problem | Fallback |
|---|---|
| A task is not complete in time | Use the file of the folder `solutions/`, and write this in the report |
| The camera of the Raspberry Pi does not work | Send a test image: step 8 of `Labs/hardware/HW-06/README.md`, path `test`. The latency then has no camera part. |
| MediaMTX is not on the card | `bash Labs/hardware/HW-06/install_mediamtx.sh` on the Raspberry Pi (needs the internet) |
| The laptop has no Day 8 environment | Run Parts B and D with no `--model`. For Part C, run `stream_detect.py` on the Raspberry Pi in `~/yolo` with `rtsp://localhost:8554/cam`, and write this in the report. |
| The XIAO does not connect to the Wi-Fi | The router must send on 2.4 GHz. Check the password and the antenna. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| `ERROR: cannot open the stream` | MediaMTX does not run, or it listens only on `127.0.0.1`, or the name does not resolve | Check the log of MediaMTX and `ss -tln` on the Raspberry Pi. Use the address in place of `pi-NN.local`. |
| MediaMTX or a Day 8 script reports an error for the camera | A second program uses the camera, for example a `picamera2` script of Day 8 | Stop the other program. Only one program can use the camera. |
| `ERROR: no file detector.py` | The Day 8 folder is not next to `day11/` | Give the folder: `--day08 <path>/day08/pi` |
| `ModuleNotFoundError: No module named 'ultralytics'` | The script does not run in the Day 8 environment | Start it with `~/day08_env/bin/python` |
| The image has grey areas for a short time | Lost packets with UDP | This is the effect of UDP. Use TCP, or write it in the report. |
| The stream in VLC is one second late | VLC adds a buffer | Use `ffplay` with the options of Part B, or `stream_detect.py` |
| The latency grows during a run | The reader reads each frame in order, or the decoder uses many threads | Use the reader of the lab (no `--in-order`). It opens the stream with one decoder thread. |
| The browser shows the XIAO stream, but `mjpeg_rate.py` waits | The sketch serves one reader at a time | Close the browser tab, then run the script |
| The XIAO prints `Camera init failed` | The PSRAM setting, or the camera cable | Select `OPI PSRAM`. Check the camera connector. |
| The window of `--clock` does not open on the laptop | The OpenCV package has no window support (`opencv-python-headless`) | Install `opencv-python` in the environment |

## Credits

This lab adapts material from these sources:

- The sketch `Streeming_Video.ino` of "XIAO ESP32S3 Sense" by Marcelo Rovai
  (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0), based on the
  ESP32-CAM project of Rui Santos: the MJPEG stream of the XIAO. The changes
  are in `TEST_NOTES.md`.
- Chapter 3.4 of "XIAO: Big Power, Small Board" by Lei Feng and Marcelo
  Rovai (github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook, GPL-3.0): the
  network commands and `ping`.
- MediaMTX by the bluenviron project (github.com/bluenviron/mediamtx, MIT):
  the RTSP server and its settings.
- The detector of the Day 8 lab with the package `ultralytics`
  (AGPL-3.0).

The scripts `stream_detect.py` and `mjpeg_rate.py`, the steps, and the report
are new work of this course. The tools of `Labs/hardware/HW-06/` and
`Labs/hardware/HW-09/` are new work of this course.
