# Test notes: Day 1 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `sketches/blink/blink.ino` | changed | Code block "Testing the board with BLINK" of the XIAOML Kit setup chapter of "Machine Learning Systems" | New: the header comment, `Serial.begin`, and two `Serial.println` lines. The pin name is `LED_PIN`. |
| `sketches/imu_test/imu_test.ino` | changed | `XIAOML_Kit_code/imu_test/imu_test.ino` of XIAO-ESP32S3-Sense | New: the header comment. Changed: the two lines that print the sensor range. The source prints 2 g and 250 dps. The library sets 16 g and 2000 dps. |
| `sketches/oled_test/oled_test.ino` | copied with no change of the code | `XIAOML_Kit_code/oled_test/oled_test.ino` of XIAO-ESP32S3-Sense | New: the header comment |
| `sketches/mic_test/mic_test.ino` | copied with no change of the code | `XIAOML_Kit_code/XIAOML_Kit_Mic_Test/XIAOML_Kit_Mic_Test.ino` of XIAO-ESP32S3-Sense | New: the header comment. The folder name is new. |
| `sketches/camera_test/camera_test.ino` | new | Pin numbers and camera settings from the example `CameraWebServer` of the esp32 core 3.3.12 | not tested |
| `sketches/memory_report/memory_report.ino` | copied with no change | `Labs/hardware/HW-03/sketches/memory_report/memory_report.ino` | none. `HW-03` says that this sketch is new and not tested. |
| `model_budgets.ipynb`, `solutions/model_budgets.ipynb` | new | no source | Tested on the work computer. It needs no board. |

Points that only a board can confirm:

- `camera_test` uses the pixel format `PIXFORMAT_GRAYSCALE`. Nobody checked
  that the camera of the kit gives this format with the frame size QVGA.
- `camera_test` puts two frame buffers in the PSRAM. Nobody measured the
  capture time.
- The README gives the steps for bootloader mode from `Labs/hardware/HW-01/`.
- The README says that the Z value is near 1.0 g with the kit flat. This
  statement comes from the setup chapter.

Compile check (no board, `arduino-cli` 1.5.1, esp32 core 3.3.12, 2026-10-01):

| Sketch | Board name (FQBN) | Result | Flash (bytes) | Static RAM (bytes) |
|---|---|---|---|---|
| `blink` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 271 701 | 21 824 |
| `blink` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 276 935 | 22 300 |
| `imu_test` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 303 021 | 23 352 |
| `imu_test` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 308 239 | 23 812 |
| `oled_test` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 304 165 | 23 544 |
| `oled_test` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 309 383 | 24 012 |
| `mic_test` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 301 981 | 21 944 |
| `mic_test` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 307 215 | 22 436 |
| `camera_test` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles, no compiler warning in the sketch | 353 535 | 33 472 |
| `camera_test` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles. On the board it prints the PSRAM error and stops. | 348 301 | 32 996 |
| `memory_report` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 274 217 | 21 832 |
| `memory_report` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 279 435 | 22 308 |
| Example `WiFiScan` of the core | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 839 740 | 44 672 |
| Example `CameraWebServer` of the core, model `CAMERA_MODEL_XIAO_ESP32S3` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 997 538 | 68 504 |

"Static RAM" is the line `Global variables use ... bytes` of the build.

Notebook check (work computer, 2026-10-01, Python 3.10.12, `torch` 2.14.1
for CPU, `torchvision` 0.29.1, `numpy` 2.2.6, `matplotlib` 3.10.9):

| Notebook | Result | Run time |
|---|---|---|
| `model_budgets.ipynb` (student version) | Runs from the first cell to the last cell with no error. It prints `Task 1: not complete`, and `?` in the table. | about 9 s |
| `solutions/model_budgets.ipynb` | Runs from the first cell to the last cell with no error. It prints `Task 1: complete`. | about 9 s |

The profiler of the notebook gives the same numbers as the theory deck:
24 234 parameters, 6 304 384 MACs, and a peak of 64 512 values for the example
network, and a peak of 1 505 280 values for MobileNetV2.

The solution keeps two RAM budgets that nobody measured: 305 848 bytes for
the XIAO with no PSRAM (result of the compiler) and 8 MB for the XIAO with
PSRAM (size of the chip). Steps 9 and 10 below replace them.

## 2. Checklist for the instructor

Run the lab on the real hardware. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: XIAOML Kit, esp32 core version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A on a lab computer with no tools installed | The time for the install. The versions. | |
| 2 | Upload `blink` | Does the LED blink? The two lines of the build output. | |
| 3 | Upload `imu_test` | Z value with the kit flat. Do the values change when you move the kit? | |
| 4 | Upload `oled_test` | Is the text readable and in the correct orientation? | |
| 5 | Upload `mic_test`, open the Serial Plotter | Does the line follow your voice? | |
| 6 | Upload `camera_test` with OPI PSRAM | The printed line. The capture time. Does the mean brightness decrease when you cover the lens? | |
| 7 | `CameraWebServer` with the lab Wi-Fi | Does the browser show the image? The time that the students need for the two changes. | |
| 8 | `WiFiScan` | Number of networks. Does the lab network appear? | |
| 9 | `memory_report` with the two PSRAM settings | Heap size, free heap, largest block, PSRAM size, free PSRAM | |
| 10 | Put the two measured budgets in task 3 of the solution notebook and run it | Does a result of the table change? | |
| 11 | Start bootloader mode with the steps of the README | Do the steps work? | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 50 min | |
| B | 45 min | |
| C | 55 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured numbers in the lab `README.md`, in
   `solutions/report_example.md`, and in the lab deck.
2. Put the two measured RAM budgets in `solutions/model_budgets.ipynb` and
   run the notebook again.
3. Change the line `Hardware status:` of the `README.md` to
   `tested on hardware (YYYY-MM-DD)`.
4. Write the fixed tool versions in `Labs/VERSIONS.md`.
