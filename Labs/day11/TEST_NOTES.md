# Test notes: Day 11 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `stream_detect.py`, `solutions/stream_detect.py` | new | The reader thread and the clock method of `Labs/hardware/HW-06/` of this course. The detector of `Labs/day08/pi/detector.py`. | New: one decoder thread (`cv2.CAP_PROP_N_THREADS`), the reader in order for the comparison with the value `behind`, a warm-up of the model, the clock window with the stream and the boxes, the `RESULT` line, and `results.csv`. The student version has no body in the method `_store` (Task C1). |
| `mjpeg_rate.py`, `solutions/mjpeg_rate.py` | new | The stream format of `Streeming_Video.ino` | The student version has no body in the function `stream_stats` (Task D1) |
| `sketches/xiao_mjpeg_stream/xiao_mjpeg_stream.ino` | changed | `Streeming_Video/Streeming_Video.ino` of the repository XIAO-ESP32S3-Sense (Apache-2.0) | See the list of changes below |
| `../hardware/HW-06/rtsp_reader.py` | changed | this course | The stream opens with one decoder thread (2026-10-03) |

Changes of the sketch against the source. Each changed line is not tested on
the board:

1. The Wi-Fi name `edgeai-lab` and a password placeholder, as build options
   `WIFI_SSID` and `WIFI_PASSWORD`.
2. The frame size `FRAMESIZE_VGA` (640 x 480) in place of `FRAMESIZE_UXGA`
   (1600 x 1200), as the build option `FRAME_SIZE`. `JPEG_QUALITY` (12, the
   value of the source) is also a build option.
3. The sketch waits for the Serial Monitor for 3 seconds at most. The
   source waits with no limit, so it did not start with no USB connection to
   a computer.
4. The pin numbers are in the sketch (the values of `camera_pins.h` of the
   example `CameraWebServer` of the core, model `CAMERA_MODEL_XIAO_ESP32S3`).
5. The names `pin_sccb_sda` and `pin_sccb_scl` of the core 3.x in place of
   `pin_sscb_sda` and `pin_sscb_scl`.
6. The boundary line comes before each part, as in the example
   `CameraWebServer`. The source sends the boundary after each part, so its
   stream starts with a part header. FFmpeg, and so OpenCV, cannot open such
   a stream: `ffprobe` reports "Invalid data found when processing input"
   (test below). A browser shows both forms.
7. A status line each 5 seconds: the frames sent, the frame rate, the mean
   JPEG size, and the RSSI. The handler counts with `std::atomic`.
8. The conversion branch for a frame that is not JPEG is removed: the camera
   sends JPEG (`PIXFORMAT_JPEG`).

### Compile results (arduino-cli 1.5.1, esp32 core 3.3.12, 2026-10-03)

| Sketch | Board name | Result | Flash (bytes) | RAM (bytes) |
|---|---|---|---|---|
| `xiao_mjpeg_stream` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles, no warning in the sketch with `--warnings all` | 955 438 | 56 328 |
| `xiao_mjpeg_stream` with `-DFRAME_SIZE=FRAMESIZE_QVGA -DJPEG_QUALITY=20` | the same | compiles | 955 442 | not recorded |

### Test on the work computer of the course (2026-10-03)

An x86 processor with 24 cores, no camera, and no Wi-Fi. The stream did not
leave the computer. MediaMTX v1.21.1 for x86 (path `cam` with the source
`publisher`, port 18554). FFmpeg 4.4 sent a test stream: the image
`bus.jpg` of the package `ultralytics` with a slow movement, 1280 x 720, 30
frames each second, H.264 at 2 Mbit/s with a keyframe each 30 frames. The
scripts ran in an environment with `ultralytics` 8.4.171 and OpenCV
5.0.0, on four cores (`taskset -c 0-3`), with the model `yolo11n.pt`. The
values say nothing about a laptop of the lab or a Raspberry Pi.

| Command | Result |
|---|---|
| `solutions/stream_detect.py rtsp://... --seconds 10` | `Task C1: complete`. 29.8 frames/s from the stream, 29.7 processed |
| the same with `--model yolo11n.pt --imgsz 320` | 19.6 frames/s processed, 123 frames skipped in 12 s, model 46.9 ms, 3 objects |
| the same with `--imgsz 640` | 14.3 frames/s processed, 187 frames skipped, model 65.4 ms |
| the same with `--imgsz 640 --in-order` | 14.0 frames/s, 0 skipped, `behind` 1.2, 2.2, 3.3, 4.3, 5.4 s in the lines of the first 10 s |
| the same with `--clock --no-window --count 3` | 3 images saved: the clock on the left, the stream with the boxes on the right |
| `RTSP_TRANSPORT=udp` with no model | 29.7 frames/s from the stream |
| `--threads 4` with no model | 29.2 frames/s from the stream |
| `../hardware/HW-06/rtsp_reader.py` with one decoder thread | 178 frames in 6 s |
| `solutions/mjpeg_rate.py` on a test server in the format of the course sketch (640 x 480, 15 frames/s, chunked HTTP answer) | `Task D1: complete`, 15.1 frames/s, mean 87.2 KB, 10.78 Mbit/s. The saved file is a JPEG image. |
| `solutions/stream_detect.py` on the same test server, with the model at 320 | 15.1 frames/s from the stream, 14.9 processed, model 49.5 ms |
| `solutions/mjpeg_rate.py` on an MJPEG stream of FFmpeg (`-f mpjpeg`, 10 frames/s) | 10.0 frames/s, 66.4 KB, 5.45 Mbit/s |
| OpenCV and `ffprobe` on a test server in the format of the source sketch (part before boundary) | cannot open the stream: "Invalid data found when processing input" |
| `ss -tln` while MediaMTX runs | `LISTEN 0 4096 0.0.0.0:18554 0.0.0.0:*` |
| `../hardware/HW-09/net_check.py 127.0.0.1 --need 22 --iperf` and `--scan 127.0.0.0/29` | `RESULT: PASS`, 6 devices found |
| The two student scripts | `Task C1: not complete` and `Task D1: not complete`, exit code 1 |

Points that only the hardware can confirm:

- The camera source `rpiCamera` of MediaMTX, the CPU load of the software
  encoder, and the frame rate of the stream on the Raspberry Pi 5.
- All latency values with the clock method, and the time of each part.
- The throughput, the jitter, and the loss of the lab network.
- The sketch on the XIAO: the camera start, the Wi-Fi connection, the frame
  rate at VGA, the JPEG size, and the status line.
- One reader at a time on the XIAO: the HTTP server of the ESP32 runs the
  stream handler, which never returns, in its task. Nobody tested a second
  reader.
- The window mode of `stream_detect.py --clock` (the work computer has no
  screen).

## 2. Checklist for the instructor

- Date of the test:
- Router, Wi-Fi band of the Raspberry Pi, distance to the router:
- Processor of the laptop, version of OpenCV in `~/day08_env`:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, steps 1 to 3 | The scan count, the TCP rates in both directions, the UDP jitter and loss, the `ping` lines | |
| 2 | Part B, steps 1 and 2 | The log lines of MediaMTX for the camera, the line of `ss`, the CPU load of `mediamtx` | |
| 3 | Part B, steps 3 and 5 | Seconds until the first image in `ffplay`. The `RESULT` line with no model. | |
| 4 | Part C, step 1 | Processed frames/s and model time for the two models | |
| 5 | Part C, step 2 | 10 latency values with no model and 10 with the detector | |
| 6 | Part C, step 3 | 10 latency values at 640 x 480 and 0.5 Mbit/s | |
| 7 | Part C, step 4 | The value `behind` after 30 s | |
| 8 | Part D: upload the sketch, open the stream in a browser | The status line of the Serial Monitor. Does the image show? | |
| 9 | Part D: `mjpeg_rate.py` and `stream_detect.py` on the XIAO stream | The `RESULT` lines, 10 latency values | |
| 10 | Part D: open a second reader while the browser shows the stream | Does the second reader get frames? Correct the README if it does. | |
| 11 | Time the complete lab with one student group, or alone | Minutes for each part | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|
| | | |
