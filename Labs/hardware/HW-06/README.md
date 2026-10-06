# HW-06: RTSP from the Raspberry Pi camera

Needed by: the Day 11 lab (RTSP server, inference on the stream, latency).

## Files

| File | Runs on | Content |
|---|---|---|
| `install_mediamtx.sh` | Raspberry Pi | Downloads MediaMTX, checks the SHA-256, unpacks it in `~/mediamtx` |
| `mediamtx_cam.yml` | Raspberry Pi | The settings of the course: RTSP only, path `cam` from the camera, path `test` for a program |
| `rtsp_reader.py` | laptop or Raspberry Pi | Reads the stream, reports the frame rate, has the function `process()` for a model |
| `latency_clock.py` | laptop with a screen | Shows a clock and the stream. Saves images for the latency. |

## Steps

### 1. Install the server (on the Raspberry Pi)

```bash
scp -r Labs/hardware/HW-06 edge@pi-NN.local:~/
ssh edge@pi-NN.local
bash ~/HW-06/install_mediamtx.sh
```

You see `mediamtx_v1.21.1_linux_arm64.tar.gz: OK` and `Installed: v1.21.1`.

### 2. Start the stream

```bash
cd ~/mediamtx
./mediamtx mediamtx_cam.yml
```

You see `[RTSP] started with listeners on :8554` and a line that says that
the path `cam` is ready. Press `Ctrl-C` to stop the server.

### 3. Open the stream on the laptop

```bash
ffplay -fflags nobuffer -flags low_delay -rtsp_transport tcp rtsp://pi-NN.local:8554/cam
```

VLC also works: `Media` > `Open Network Stream`, then the same address. VLC
adds a buffer of about 1 second. Use `ffplay` for a latency test.

### 4. Read the stream in Python

```bash
python3 rtsp_reader.py rtsp://pi-NN.local:8554/cam --seconds 20 --save frame.jpg
```

Each 2 seconds, the script prints one line:

```
1280x720  stream 30.0 frames/s  processed 30.0 frames/s  skipped 0
```

- `stream` is the rate that arrives.
- `processed` is the rate of the function `process()`.
- `skipped` is the number of frames that the model did not see.

For UDP:

```bash
RTSP_TRANSPORT=udp python3 rtsp_reader.py rtsp://pi-NN.local:8554/cam
```

### 5. Add the detector

In `rtsp_reader.py`, change the function `process()`:

```python
from ultralytics import YOLO
model = YOLO("yolo11n.pt")          # or your Day 8 model

def process(frame):
    results = model(frame, verbose=False)
    return results[0].plot()
```

Run the script with `--show` to see the boxes.

### 6. Measure the end-to-end latency

1. Run on the laptop:

   ```bash
   python3 latency_clock.py rtsp://pi-NN.local:8554/cam
   ```

2. A window opens. The left side shows a clock with milliseconds. The right
   side shows the stream.
3. Point the camera at the clock on the laptop screen. The stream now shows
   the clock of the past.
4. Press `s` 10 times, with about 1 second between two presses. The script
   saves `latency_01.png` to `latency_10.png`.
5. In each image, read the left clock and the clock in the stream. The
   difference is the latency.
6. Report the median, the minimum, and the maximum.

The error of one reading is about 50 ms: the screen shows a new image each
16.7 ms, and the camera makes a new frame each 33 ms. For this reason the
method uses the median of 10 images.

### 7. Change the settings (Part C of the lab)

Stop MediaMTX. Change `mediamtx_cam.yml`. Start MediaMTX again.

| Setting | Key | Values to compare |
|---|---|---|
| Resolution | `rpiCameraWidth`, `rpiCameraHeight` | 1280 × 720 and 640 × 480 |
| Bit rate | `rpiCameraBitrate` | 2000000 and 500000 |
| Frame rate | `rpiCameraFPS` | 30 and 15 |
| Keyframe period | `rpiCameraIDRPeriod` | 30 and 120 |
| Transport | `RTSP_TRANSPORT` of the reader | `tcp` and `udp` |

Measure the latency again for each setting (step 6). Measure the CPU load of
MediaMTX with `htop` on the Raspberry Pi.

### 8. Test with no camera

The path `test` accepts a stream from a program. This command sends a test
image from the Raspberry Pi or from a laptop:

```bash
ffmpeg -re -f lavfi -i testsrc=size=640x480:rate=30 -c:v libx264 \
  -tune zerolatency -g 30 -f rtsp rtsp://localhost:8554/test
```

Then read `rtsp://localhost:8554/test`. Use this to test the reader when the
camera does not work.

## Test steps for the instructor

- Date of the test:
- MediaMTX version, OpenCV version on the laptop:
- Network: router model, Wi-Fi band, distance:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run steps 1 and 2 | The log lines of the path `cam`. Which codec does the log name? | |
| 2 | Run `htop` on the Raspberry Pi with one reader connected | CPU load of `mediamtx` in percent | |
| 3 | Run step 3 | Does `ffplay` show the image? Seconds until the first image. | |
| 4 | Run step 4 with TCP and with UDP | Stream frame rate. Image errors with UDP. | |
| 5 | Run step 6 with 1280 × 720 and 2 Mbit/s | 10 latency values, the median | |
| 6 | Run step 6 with 640 × 480 and 500 kbit/s | 10 latency values, the median | |
| 7 | Run step 5 with the Day 8 model on the laptop | Processed frame rate, skipped frames, latency | |
| 8 | Run the reader with the model on the Raspberry Pi itself (`rtsp://localhost:8554/cam`) | Processed frame rate with the encoder active | |
| 9 | Start a `picamera2` script while MediaMTX runs | The error text. The lab names it in "Common problems". | |
| 10 | Connect 5 readers at the same time | CPU load, frame rate of each reader | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Write the MediaMTX version in `Labs/VERSIONS.md`.
2. Write the measured latency of two settings in the Day 11 lab deck as the
   expected result.
3. Install MediaMTX on the master card (`HW-04`, step 4).
