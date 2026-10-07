# Day 11 lab report: example

This example has the parts of the report that need no board and no lab
network: the settings, the method, the calculations, and the form of the
answers. Each value of the network, the camera, the latency, and the frame
rate depends on the room, the router, the laptop, and the boards. These cells
have the text "measure in the lab". The text says so at each such value.

Connection of the Raspberry Pi: measure in the lab.

## Part A: network tools

| Device | Name | Address | Router (`default via`) |
|---|---|---|---|
| Laptop | the name of the laptop | an address from `X.150` to `X.250` | `X.1` |
| Raspberry Pi | `pi-NN` | `X.(100+NN)`, for example `192.168.8.107` for group 07 | `X.1` |

| Value | Result |
|---|---|
| Devices that answer in the scan | measure in the lab |
| `net_check.py pi-NN.local --need 22` | `RESULT: PASS` |

| Test | Bit rate (receiver) | Jitter | Lost datagrams |
|---|---|---|---|
| TCP, laptop to Raspberry Pi | measure in the lab | none | none |
| TCP, Raspberry Pi to laptop (`-R`) | measure in the lab | none | none |
| UDP at 20 Mbit/s | measure in the lab | measure in the lab | measure in the lab |

| `ping`, 100 requests | min | avg | max | mdev | loss |
|---|---|---|---|---|---|
| Laptop to Raspberry Pi | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab |

Question A1. Divide the measured TCP throughput from the Raspberry Pi to the
laptop by 2 Mbit/s. Example: 40 Mbit/s / 2 Mbit/s = 20 streams. The real
number is smaller: the groups share one Wi-Fi channel, each keyframe is a
burst (a keyframe of 64 KB needs 0.26 s at 2 Mbit/s, Part 2 of the lecture),
a device far from the router uses a slow rate and takes more time of the
channel, and `iperf3` measured one moment only.

## Part B: RTSP server

| Value | Result |
|---|---|
| The line of `ss -tln` with the port 8554 | `LISTEN 0 4096 0.0.0.0:8554 0.0.0.0:*` (MediaMTX on the machine that runs the server; `*:8554` is also correct) |
| CPU load of `mediamtx` in `top` | measure in the lab |
| Seconds until the first image in `ffplay` or VLC | measure in the lab |
| `stream_detect.py` with no model: `stream_fps` and `processed_fps` | about 30 and about 30. A run with a test stream of 30 frames/s gave 29.8 and 29.7. |

## Part C: inference on the stream

| Model | Image size | Processed frames/s | Skipped frames each second | Model time |
|---|---|---|---|---|
| `yolo11n.pt` | 320 | measure in the lab | measure in the lab | measure in the lab |
| Day 8 model `cupbottle_320_ncnn_model` | 320 | measure in the lab | measure in the lab | measure in the lab |

The rates depend on the processor of the laptop. On an x86 server
processor with four cores, `yolo11n.pt` at 320 pixels needed 46.9 ms and
took 19.6 of the 30 frames each second. At 640 pixels it needed 65.4 ms
and took 14.3 frames each second. These values say nothing about your
laptop.

| Setting | 10 values (ms) | Median | Min | Max |
|---|---|---|---|---|
| `hd_nomodel`: 1280 x 720, 2 Mbit/s, no model | measure in the lab | measure in the lab | measure in the lab | measure in the lab |
| `hd_yolo`: 1280 x 720, 2 Mbit/s, `yolo11n.pt` at 320 | measure in the lab | measure in the lab | measure in the lab | measure in the lab |
| `sd_yolo`: 640 x 480, 0.5 Mbit/s, `yolo11n.pt` at 320 | measure in the lab | measure in the lab | measure in the lab | measure in the lab |

The reader in order: `behind` after 30 s: measure in the lab.

Question C1. The detector adds the median of `hd_yolo` minus the median of
`hd_nomodel`. Expect a value near the model time of step 1, and up to one
more frame time (33 ms): a frame that arrives during a model run waits for
the end of that run. The error of one clock reading is about 50 ms, so a
difference below about 30 ms is not clear with 10 readings.

Question C2. Expect the lower latency for `sd_yolo`. Parts that change with
the setting: the camera and the encoder of the Raspberry Pi (fewer pixels to
encode in software), the transfer of each frame on the Wi-Fi (fewer bits),
and the decoder and the scaling on the laptop. The model input stays 320
pixels, so the model time changes little.

Question C3. The stream brings 30 frames each second. A reader that takes
each frame in order and processes F frames each second falls behind by
1 - F/30 seconds each second. Example from the solution scripts: F = 14.0,
so 1 - 14.0/30 = 0.53 s each second. The script printed `behind 5.4 s`
after 10 s. After 30 s, the same rate gives about 16 s. Your F comes from
your laptop.

## Part D: microcontroller camera

| Value | Result |
|---|---|
| Frame size and `JPEG_QUALITY` of the sketch | VGA (640 x 480), 12 |
| `mjpeg_rate.py`: frames/s | measure in the lab |
| `mjpeg_rate.py`: mean JPEG size | measure in the lab |
| `mjpeg_rate.py`: bit rate | measure in the lab |
| Serial Monitor: `sent ... frames in 5 s`, mean JPEG, RSSI | measure in the lab |
| `stream_detect.py` on the XIAO stream: processed frames/s | measure in the lab |
| Latency `xiao_yolo`: 10 values (ms) | measure in the lab |
| Latency `xiao_yolo`: median, min, max | measure in the lab |

Question D1. Bit rate = frames each second x mean JPEG size x 1024 x 8.
Example: 10 frames/s with a mean JPEG of 24 KB give 10 x 24 x 1024 x 8 =
1 966 080 bits each second, about 1.97 Mbit/s (the exercise of Part 2 of the
lecture). The value of `mjpeg_rate.py` uses the same formula with all images
of the measurement, so the two values must agree within the rounding.

Question D2. Divide each bit rate by its frame rate to get the bits for each
frame. MJPEG sends each frame as a complete JPEG image, so it needs more bits
for each frame than H.264. In the experiment of the lecture, MJPEG needed 4.2
times the bits of H.264 for a moving camera and 10.5 times for a fixed
camera, at the same image quality. The camera module of the XIAO makes the
JPEG, so the processor of the XIAO only sends the data. The Raspberry Pi 5
encodes H.264 on its CPU. Compare the frame rates and the latency with your
measured values.

## Decision Log

Example of the form (use your own numbers):

The camera at the door is a camera node with no model, and the Raspberry Pi
in the back office is the central node: it runs the detector on an RTSP
stream at 640 x 480 and 0.5 Mbit/s. In our lab, this setting gave a median
latency of ... ms with the detector, below the limit of 1 s, and the
detector took ... frames each second. The camera sends only the stream, and
only on the Wi-Fi of the shop. Only the counts leave the shop. The trade-off: the stream uses ... percent of the measured
throughput of the Wi-Fi, and an image on the network is a privacy risk. A
model on the camera node would send only the counts, but it needs a
processor at the door.
