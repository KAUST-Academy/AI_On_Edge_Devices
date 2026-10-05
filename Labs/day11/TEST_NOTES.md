# Test notes: Day 11 lab

## 1. Checklist for the instructor

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
