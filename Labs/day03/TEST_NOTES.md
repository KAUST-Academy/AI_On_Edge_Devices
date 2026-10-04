# Test notes: Day 3 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `motion_classifier.ipynb`, `solutions/motion_classifier.ipynb` | new | The feature list and the network come from the kit chapters. The function `spectral_power` follows `welch_max_hold` of "DSP Spectral Features". | Tested on the work computer with the fallback dataset. They need no board. |
| `sketches/motion_classifier/motion_features.h` | new | The same feature list | Tested on the work computer: the C++ code and the Python code give the same 63 features for 48 windows. The largest relative difference is 0.00007. |
| `sketches/motion_classifier/motion_classifier.ino` | new | The use of the interpreter follows `Labs/hardware/HW-02/sketches/tflm_hello`. The IMU code and the display code follow `XIAOML_Kit_code/motion_class_ad_inference_oled` of XIAO-ESP32S3-Sense. | Student version. Tasks B1 to B4 are not complete. It compiles. Not tested on a board. |
| `solutions/sketches/motion_classifier/motion_classifier.ino` | new | The same sources | It compiles. Not tested on a board. |
| `model.h`, `model_settings.h`, `test_window.h` (two folders) | made by the solution notebook | The fallback dataset of Day 2 | The model learned from simulated signals. It does not work on real motions. |
| `sketches/ei_motion_inference/ei_motion_inference.ino` | changed | `XIAOML_Kit_code/motion_class_ad_inference_oled/motion_class_ad_inference_oled.ino` of XIAO-ESP32S3-Sense | New: the header comment and one comment line. Changed: `MAX_ACCEPTED_RANGE` is 16 g, not 2 g. **Not compiled:** the sketch needs the Arduino library of an Edge Impulse project, and only the Studio can make it. |
| `host/tflite_to_header.py` | copied with no change | `Labs/hardware/HW-02/tflite_to_header.py` | none |

Points that only a board can confirm:

- The complete sketch: the sampling loop, the ring buffer, the display, and
  the output lines.
- The value of `arena_used_bytes()`. A 32-bit build of the same library on
  the work computer gives 1232 bytes for the model of the repository. The
  value of the board can be different.
- The two times `features_us` and `invoke_us`. The lecture says that their
  sum must be below one sample period of 20 ms.
- The display update runs one time for each inference. It uses the I2C bus
  and can need more than one sample period. Then `late_samples` increases.
  If this occurs, the instructor decides: update the display less often, or
  accept the late samples.
- The effect of the arena in the PSRAM on the latency.
- All steps of Part D in Edge Impulse Studio, the build of its library with
  the core 3.3.12, and the menu names of the README.
- The model of the repository learned from simulated signals. The live
  demonstration needs a model from real recordings.

Compile check (no board, `arduino-cli` 1.5.1, esp32 core 3.3.12, libraries
Chirale_TensorFlowLite 2.0.0, Seeed Arduino LSM6DS3 2.0.7, U8g2 2.36.19,
2026-10-02):

| Sketch | Board name (FQBN) and option | Result | Flash (bytes) | Static RAM (bytes) |
|---|---|---|---|---|
| `sketches/motion_classifier` (student version) | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 311 297 | 26 616 |
| `solutions/sketches/motion_classifier` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 364 005 | 26 952 |
| `solutions/sketches/motion_classifier` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 369 255 | 27 428 |
| `solutions/sketches/motion_classifier` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi`, with `ARENA_IN_PSRAM 1` | compiles | 369 323 | 27 428 |

"Static RAM" is the line `Global variables use ... bytes` of the build. The
runtime and the inference code add 364 005 - 311 297 = 52 708 bytes of flash
to the student version.

Test with no board (work computer, 2026-10-02). The library
Chirale_TensorFlowLite was compiled as a 32-bit program for the work
computer. A test program then ran the files of
`solutions/sketches/motion_classifier/` with the same steps as the self-test
of the sketch:

| Check | Result |
|---|---|
| The resolver with `AddFullyConnected()` and `AddSoftmax()` | `AllocateTensors()` returns with no error |
| `arena_used_bytes()` | 1232 bytes (pointers of 4 bytes, as on the ESP32-S3) |
| Features of the test window against `kTestFeatures` | largest difference 0.0000002 |
| Output of the model against `kTestOutput` | largest difference 0.0000000, class `maritime` as expected |

This test confirms the model file, the operator list, the feature code, and
the normalization. It does not confirm the sketch on the board.

Notebook check (work computer, 2026-10-02, Python 3.10.12, `tensorflow-cpu`
2.21.0, `keras` 3.12.4, `ai-edge-litert` 2.2.0, `numpy` 2.2.6):

| Notebook | Result | Run time |
|---|---|---|
| `motion_classifier.ipynb` (student version) | Runs from the first cell to the last cell with no error. It prints `not complete` for tasks 1, 2, and 4, and it does not write the three files. | about 36 s |
| `solutions/motion_classifier.ipynb` | Runs from the first cell to the last cell with no error. It prints `complete` for tasks 1, 2, and 4. | about 43 s |

Results of the solution notebook with the fallback dataset. The signals are
simulated, so these numbers say nothing about the real kit:

- 1312 training windows and 656 test windows with the test session `s3`.
- Feature model: 1534 parameters, test accuracy 100.0 percent for each test
  session.
- Raw window model: 6274 parameters, test accuracy 100.0, 54.0, and 100.0
  percent for the test sessions `s1`, `s2`, and `s3`.
- LiteRT file: 8328 bytes, operators FULLY_CONNECTED (3 times) and SOFTMAX.
- Largest difference between Keras and LiteRT: 1.79e-07.

The notebooks come from one generator script of the course repository
(`tools/notebooks/build_day03_motion_classifier.py`). Change the script, not
the two notebooks.

## 2. Checklist for the instructor

Run the lab on the real hardware with a real Day 2 dataset. Record the
result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: XIAOML Kit, esp32 core version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run `solutions/motion_classifier.ipynb` with a real dataset | Test accuracy of the two inputs for each session. The run time. | |
| 2 | Copy the three files of the notebook into `solutions/sketches/motion_classifier/` and upload with PSRAM disabled | The time of the first build. The lines of the self-test. | |
| 3 | Read the memory lines | Sketch size, arena used, free internal heap | |
| 4 | Make each of the four motions for 10 s | The class that the display shows. The probability. | |
| 5 | Read 20 output lines | Median and maximum of `features_us` and `invoke_us`. The value of `late_samples`. | |
| 6 | Set `kTensorArenaSize` to 1024 | The message of the Serial Monitor | |
| 7 | OPI PSRAM with `ARENA_IN_PSRAM 1` | The same numbers as in steps 3 and 5 | |
| 8 | Upload the student version with no change | Does it print `Tasks B1 and B2 are not complete.`? | |
| 9 | Part D, steps 1 and 2 | The menu names, the test accuracy, the three estimates of the Studio, the time for the training | |
| 10 | Part D, step 3 with the core 3.3.12 | Does the library build? The time of the build. The two times of the output line. The sketch size. | |
| 11 | If step 10 fails: repeat with the core 2.0.17 | The result | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 45 min | |
| B | 50 min | |
| C | 30 min | |
| D | 25 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured numbers in `solutions/report_example.md` and in the
   lab deck.
2. Replace the three files `model.h`, `model_settings.h`, and `test_window.h`
   of the two sketch folders with the files of a model from a real dataset.
3. If `late_samples` increases, change the display update in the two
   sketches.
4. Correct the menu names of Part D in the `README.md`.
5. Change the line `Hardware status:` of the `README.md` to
   `tested on hardware (YYYY-MM-DD)`.
