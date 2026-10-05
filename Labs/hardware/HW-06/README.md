# HW-06: RTSP from the Raspberry Pi camera


Needed by: the Day 11 lab (RTSP server, inference on the stream, latency).

## Decision

| Topic | Decision |
|---|---|
| RTSP server | MediaMTX v1.21.1, one program with no installation, in `~/mediamtx` |
| Camera source | The source `rpiCamera` of MediaMTX. It reads the Raspberry Pi camera directly. |
| Stream address | `rtsp://pi-NN.local:8554/cam` |
| Start values | 1280 × 720, 30 frames per second, 2 Mbit/s, one keyframe each second |
| Reader | `rtsp_reader.py`: OpenCV with the FFmpeg backend. A thread keeps only the newest frame. |
| Transport | RTP over TCP as the default. UDP is the second setting of the lab. |
| Latency method | A clock on the screen and the stream side by side (`latency_clock.py`). The median of 10 images. |

## Reason

- MediaMTX is one file. It needs no package and no administrator right. The
  release has a build for the 64-bit Raspberry Pi.
- The source `rpiCamera` needs no second program. The other method (a camera
  program that sends to FFmpeg, and FFmpeg that sends to the server) has more
  parts that can fail.
- One configuration file sets the resolution, the frame rate, and the bit
  rate. Part C of the lab changes these values.
- OpenCV is the library of the Day 8 lab. The reader gives the same frame
  type (a NumPy array) as the Day 8 code, so the detector needs no change.
- A slow model reads fewer frames than the stream sends. OpenCV then keeps
  old frames in a buffer, and the delay grows with time. A thread that always
  reads, and keeps only the newest frame, prevents this.
- TCP loses no packet, so the image has no errors on Wi-Fi. UDP can have a
  smaller delay. The comparison is a lab measurement.
- The clock method measures the complete path: camera, encoder, network,
  decoder, and display. It needs no synchronized clocks on two computers,
  because one screen shows both times.

**Facts that the lab must know:**

- The Raspberry Pi 5 has no hardware H.264 encoder. The setting
  `rpiCameraCodec: auto` then selects the software encoder (the file
  `mediamtx.yml` of the release describes this rule). The encoder uses CPU
  time. A detector on the same Raspberry Pi has less CPU time.
- Only one program can use the camera. While MediaMTX runs, a `picamera2`
  script cannot open the camera. Stop MediaMTX before you run the Day 8 code
  with the camera.

## Sources

| Item | Source |
|---|---|
| Server, settings, camera source | MediaMTX documentation (`mediamtx.org/docs`) and the file `mediamtx.yml` of the release v1.21.1 (`github.com/bluenviron/mediamtx`, MIT) |
| Checksums | File `checksums.sha256` of the release v1.21.1 (read on 2026-10-01) |
| Reader options | OpenCV documentation, video I/O with the FFmpeg backend (`OPENCV_FFMPEG_CAPTURE_OPTIONS`) |

No source repository of the course has RTSP material. All code of this folder
is new.

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

## Result of the test on the work computer

The work computer has no Raspberry Pi camera. The test used MediaMTX v1.21.1
for x86, the path `test`, and a Python program that sent a clock image
through FFmpeg (640 × 480, 30 frames per second, `libx264`).

- `install_mediamtx.sh`: the download, the checksum, and the start pass.
- `mediamtx_cam.yml`: the server loads the file. On x86, the path `cam`
  reports "server was compiled without support for the Raspberry Pi Camera".
  This is correct for a computer that is not a Raspberry Pi.
- `rtsp_reader.py`: 194 frames in 7 seconds, 30.0 frames per second, 0 frames
  skipped. A wrong address gives the error "cannot open the stream".
- `latency_clock.py --no-window`: three images saved. Both clocks are easy to
  read. Two images gave 544 ms and 548 ms. This number includes the delay of
  the test program that sent the stream. **It is not a number for the lab.**
- Correction of 2026-10-03: most of the 544 ms came from the decoder of
  the reader. OpenCV used 16 decoder threads on the 24 cores of
  the work computer, and each thread holds one frame (33 ms). With one
  decoder thread, the age of a frame was 40 ms on the same computer.
  `rtsp_reader.py` now opens the stream with one decoder thread
  (`cv2.CAP_PROP_N_THREADS`). An experiment of this course measured this
  (Part 3 of the Day 11 lecture).

## Code status

| File | State | Source | Change |
|---|---|---|---|
| `install_mediamtx.sh` | new | no source | tested on the work computer (x86). Not tested on a Raspberry Pi. |
| `mediamtx_cam.yml` | new | Key names from `mediamtx.yml` of the release | The file loads on x86. The camera keys are not tested. |
| `rtsp_reader.py` | new | no source | tested with a synthetic stream. Not tested with the camera, a model, or `--show`. |
| `latency_clock.py` | new | no source | The mode `--no-window` was tested. The window mode was not tested. |

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

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the MediaMTX version in `Labs/VERSIONS.md`.
3. Write the measured latency of two settings in the Day 11 lab deck as the
   expected result.
4. Install MediaMTX on the master card (`HW-04`, step 4).

## Credits

MediaMTX is a program of the bluenviron project
(github.com/bluenviron/mediamtx, MIT licence). The scripts of this folder are
new.
