# Test notes: Day 4 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `quantization.ipynb`, `solutions/quantization.ipynb` | new | The methods come from chapter 10 of "Machine Learning Systems". The data code, the feature code, and the feature model come from the Day 3 notebook. | Tested on the work computer with the fallback dataset. They need no board. |
| `sketches/motion_quant/motion_quant.ino` | new | The solution sketch `motion_classifier.ino` of the Day 3 lab: the interpreter, the sampling loop, the display code. New: the build option `MODEL_INT8`, the quantization of the input, the dequantization of the output, the test set, the time of `Invoke()`. The arena is a static array, with no PSRAM option. | Student version. Tasks D1 and D2 are not complete. It compiles for the two values of `MODEL_INT8`. Not tested on a board. |
| `solutions/sketches/motion_quant/motion_quant.ino` | new | The same sources | It compiles for the two values of `MODEL_INT8`. Not tested on a board. |
| `motion_features.h` (two folders) | copied with no change | The file `motion_features.h` of the Day 3 lab | none |
| `model_float.h`, `model_int8.h`, `model_settings.h`, `test_set.h` (two folders) | made by the solution notebook | The fallback dataset of Day 2 | The models learned from simulated signals. They do not work on real motions. The file `model_float.h` holds the same 8328 bytes as the file `model.h` of the Day 3 lab. |
| `host/tflite_to_header.py` | copied with no change | The file `host/tflite_to_header.py` of the Day 3 lab | none |

Points that only a board can confirm:

- The complete sketch on the board: the test set at the start, the sampling
  loop, the display, and the output lines.
- The two values of `arena_used_bytes()`. A 32-bit build of the same library
  on the work computer gives 1232 bytes for the `float32` model and 1028
  bytes for the `int8` model. The values of the board can be different.
- The time of `Invoke()` for the two models. Nobody knows which model is
  faster on the ESP32-S3. The chip has a circuit for float arithmetic, and
  the library Chirale_TensorFlowLite has no optimized kernels for this chip.
  The lab asks the students for a prediction and gives no expected result.
- The agreement of the classes with the laptop for the `int8` model. The
  host build gives 80 of 80. The function `lroundf` of the board and the
  function `np.round` of the laptop give different results for a value that
  is exactly between two integers. This can change one input value by one
  step.
- The model of the repository learned from simulated signals. The step with
  real motions needs a model from real recordings.

Compile check (no board, `arduino-cli` 1.5.1, esp32 core 3.3.12, libraries
Chirale_TensorFlowLite 2.0.0, Seeed Arduino LSM6DS3 2.0.7, U8g2 2.36.19,
2026-10-02):

| Sketch | Board name (FQBN) and option | Result | Flash (bytes) | Static RAM (bytes) |
|---|---|---|---|---|
| `sketches/motion_quant` (student version), `MODEL_INT8 0` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 382 785 | 31 384 |
| `sketches/motion_quant` (student version), `MODEL_INT8 1` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 378 961 | 31 384 |
| `solutions/sketches/motion_quant`, `MODEL_INT8 0` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 382 785 | 31 384 |
| `solutions/sketches/motion_quant`, `MODEL_INT8 1` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 379 701 | 31 384 |
| `solutions/sketches/motion_quant`, `MODEL_INT8 1` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 384 951 | 31 860 |

"Static RAM" is the line `Global variables use ... bytes` of the build. It
holds the arena of 4096 bytes. The compile check sets the option with
`--build-property compiler.cpp.extra_flags=-DMODEL_INT8=1`. The `int8`
sketch is 382 785 - 379 701 = 3084 bytes smaller than the `float32` sketch.
The model file is 8328 - 4960 = 3368 bytes smaller, so the code for the
`int8` model is 284 bytes larger than the code for the `float32` model.

Test with no board (work computer, 2026-10-02). The library
Chirale_TensorFlowLite was compiled as a 32-bit program for the work
computer. The sketch file ran with a replacement for the Arduino functions:
a simulated IMU, a display that shows nothing, and the clock of the work
computer.

| Check | `float32` model | `int8` model |
|---|---|---|
| `AllocateTensors()` with `AddFullyConnected()` and `AddSoftmax()` | no error | no error |
| `arena_used_bytes()` (pointers of 4 bytes, as on the ESP32-S3) | 1232 bytes | 1028 bytes |
| Input tensor | `FLOAT32`, 252 bytes | `INT8`, 63 bytes, scale 0.030194, zero point -26 |
| Output tensor | `FLOAT32`, 16 bytes | `INT8`, 4 bytes, scale 0.003906, zero point -128 |
| Test set, correct | 80 of 80 | 80 of 80 |
| Test set, same class as on the laptop | 80 of 80 | 80 of 80 |
| Clipped input values | not necessary | 42 of 5040, and 42 on the laptop |
| The loop with the simulated IMU | prints one line for each inference | prints one line for each inference |
| Student version | the same result as the solution | 20 of 80, then `Task D1: not complete. Task D2: not complete.` and the sketch stops |

This test confirms the two model files, the operator list, the quantization
code, and the test set. It does not confirm the sketch on the board, and
its times say nothing about the board.

Notebook check (work computer, 2026-10-02, Python 3.10.12, `tensorflow-cpu`
2.21.0, `keras` 3.12.4, `ai-edge-litert` 2.2.0, `numpy` 2.2.6):

| Notebook | Result | Run time |
|---|---|---|
| `quantization.ipynb` (student version) | Runs from the first cell to the last cell with no error. It prints `not complete` for tasks 1, 2, 4, 5, and 7, and it does not write the four files. | about 20 s |
| `solutions/quantization.ipynb` | Runs from the first cell to the last cell with no error. It prints `complete` for tasks 1, 2, 4, 5, and 7. | about 39 s |

Results of the solution notebook with the fallback dataset. The signals are
simulated, so these numbers say nothing about the real kit:

- 1312 training windows and 656 test windows with the test session `s3`.
- CNN: 852 parameters, `float32` file 7320 bytes, `int8` file 6008 bytes,
  test accuracy 100.0 percent for the two files.
- Calibration set with the class "idle" only: 84.9 percent, with 21.98
  percent of clipped input values.
- Weights with 2 bits: 49.8 percent with no new training, and 100.0 percent
  after quantization-aware training.
- Feature model: 1534 parameters, `float32` file 8328 bytes, `int8` file
  4960 bytes, test accuracy 100.0 percent for the two files.

The results for 4 bits and for 2 bits change much with a small change of
the model: one changed weight can move a complete class of the simulated
signals. With a real dataset, the tables of Part C look different.

The notebooks come from one generator script of the course repository
(`tools/notebooks/build_day04_quantization.py`). Change the script, not
the two notebooks.

## 2. Checklist for the instructor

Run the lab on the real hardware with a real Day 2 dataset. Record the
result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: XIAOML Kit, esp32 core version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run `solutions/quantization.ipynb` with a real dataset | The run time. The tables of sections 7, 9, 11, and 12. Does each experiment show an effect with real data? | |
| 2 | Copy the four files of the notebook into `solutions/sketches/motion_quant/` and upload with `MODEL_INT8 0` and PSRAM disabled | The build line `Sketch uses`. All lines of the Serial Monitor before the loop. | |
| 3 | Upload with `MODEL_INT8 1` | The same lines, and the line with the clipped input values | |
| 4 | Compare the two runs | Arena used, median and largest `invoke_us`, correct windows, same class as on the laptop | |
| 5 | Make each of the four motions for 10 s with the `int8` model | The class that the display shows. The value of `late_samples`. | |
| 6 | Upload the student version with `MODEL_INT8 1` and no change | Does it print `Task D1: not complete. Task D2: not complete.`? | |
| 7 | Read the build time | The time of a build after a change of `MODEL_INT8`. Part D has 30 minutes for two builds. | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 30 min | |
| B | 50 min | |
| C | 40 min | |
| D | 30 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured numbers in `solutions/report_example.md` and in the
   lab deck.
2. Replace the four files `model_float.h`, `model_int8.h`,
   `model_settings.h`, and `test_set.h` of the two sketch folders with the
   files of a model from a real dataset.
3. If an experiment of Part C shows no effect with the real dataset, change
   the numbers of bits in the generator script.
4. Write the result of the latency comparison in the README: which model is
   faster on the board.
5. Change the line `Hardware status:` of the `README.md` to
   `tested on hardware (YYYY-MM-DD)`.
