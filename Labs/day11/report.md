# Day 11 report: inference on a network video stream

Group: gNN. Names:

Date:

Connection of the Raspberry Pi (Wi-Fi 2.4 GHz, Wi-Fi 5 GHz, or Ethernet):

## Part A: network tools

Addresses (step 1):

| Device | Name | Address | Router (`default via`) |
|---|---|---|---|
| Laptop | | | |
| Raspberry Pi | `pi-NN` | | |

Scan and check (step 2):

| Value | Result |
|---|---|
| Devices that answer in the scan | |
| `net_check.py pi-NN.local --need 22` | `RESULT: PASS` or `FAIL` |

Throughput, jitter, and loss (step 3):

| Test | Bit rate (receiver) | Jitter | Lost datagrams |
|---|---|---|---|
| TCP, laptop to Raspberry Pi | Mbit/s | none | none |
| TCP, Raspberry Pi to laptop (`-R`) | Mbit/s | none | none |
| UDP at 20 Mbit/s | Mbit/s | ms | of |

| `ping`, 100 requests | min | avg | max | mdev | loss |
|---|---|---|---|---|---|
| Laptop to Raspberry Pi | ms | ms | ms | ms | % |

Question A1. The stream of Part B has 2 Mbit/s. How many such streams fit
into the throughput that you measured from the Raspberry Pi to the laptop?
Why can the real number be smaller?

Answer:

## Part B: RTSP server

| Value | Result |
|---|---|
| The line of `ss -tln` with the port 8554 | |
| CPU load of `mediamtx` in `top` | % |
| Seconds until the first image in `ffplay` or VLC | s |
| `stream_detect.py` with no model: `stream_fps` and `processed_fps` of the `RESULT` line | |

## Part C: inference on the stream

The detector (step 1), with the start setting 1280 x 720 at 2 Mbit/s:

| Model | Image size | Processed frames/s | Skipped frames each second | Model time |
|---|---|---|---|---|
| `yolo11n.pt` | 320 | | | ms |
| Your Day 8 model: | | | | ms |

Processor of the laptop:

Latency (steps 2 and 3). Write the 10 values in ms, then the median, the
minimum, and the maximum:

| Setting | 10 values (ms) | Median | Min | Max |
|---|---|---|---|---|
| `hd_nomodel`: 1280 x 720, 2 Mbit/s, no model | | | | |
| `hd_yolo`: 1280 x 720, 2 Mbit/s, `yolo11n.pt` at 320 | | | | |
| `sd_yolo`: 640 x 480, 0.5 Mbit/s, `yolo11n.pt` at 320 | | | | |

The reader in order (step 4): `behind` after 30 s: s. Processed frames/s:

Question C1. How many ms does the detector add to the latency
(`hd_yolo` against `hd_nomodel`)? Compare with the model time of step 1.

Answer:

Question C2. Which setting has the lower latency? Name two parts of the
pipeline that changed with the setting.

Answer:

Question C3. In step 4, the reader fell behind the live stream. Calculate the
growth for each second from the processed frame rate and the 30 frames each
second of the stream (Part 3 of the lecture). Does it agree with the value
`behind` after 30 s?

Answer:

## Part D: microcontroller camera

| Value | Result |
|---|---|
| Frame size and `JPEG_QUALITY` of the sketch | VGA, 12 |
| `mjpeg_rate.py`: frames/s | |
| `mjpeg_rate.py`: mean JPEG size | KB |
| `mjpeg_rate.py`: bit rate | Mbit/s |
| Serial Monitor: `sent ... frames in 5 s`, mean JPEG, RSSI | |
| `stream_detect.py` on the XIAO stream: processed frames/s | |
| Latency `xiao_yolo`: 10 values (ms) | |
| Latency `xiao_yolo`: median, min, max | |

Question D1. Calculate the bit rate of the XIAO stream from the frame rate
and the mean JPEG size (Part 2 of the lecture). Does it agree with the value
of `mjpeg_rate.py`?

Answer:

Question D2. Compare the XIAO stream (MJPEG) with the stream of the
Raspberry Pi (H.264, setting 1): the bit rate for each frame, the frame
rate, the latency, and the work of the processor on each board.

Answer:

## Decision Log

A shop wants to count the people at its entrance. One camera hangs at the
door. A Raspberry Pi 5 stands in the back office, 15 m away, on Wi-Fi. The
count must change within 1 second after a person enters, and no image may
leave the shop. Where do you run the detector? Which stream settings do you
select? What leaves the camera, and what leaves the shop?

Write about 100 words with your measured numbers, and name one trade-off.

Decision:
