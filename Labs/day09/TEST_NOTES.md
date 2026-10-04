# Test notes: Day 9 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `sketches/kit_bench/kit_bench.ino` | new | The example `hello_world` of Chirale_TensorFlowLite 2.0.0 for the interpreter | New: four models in one sketch, an arena for each model in the internal RAM or in the PSRAM, a fixed test input, the first inference alone, warm-up and timed runs, the statistics, the output check against LiteRT, the clock setting, and the lines `CSV`. It compiles. A 32-bit build on an x86 computer ran the four models. Not tested on the board. |
| `sketches/kit_bench/bench_stats.h`, `solutions/sketches/kit_bench/bench_stats.h` | new | The nearest-rank rule of the lecture | The student version has no body in the function `percentileUs` (Task B1). The two versions compile. |
| `sketches/kit_bench/model_kws_int8.h`, `model_kws_float32.h`, `model_ic_int8.h`, `model_ic_float32.h` | generated | The four files of `models/` | Each file is one model as a C array, with no change of a byte |
| `sketches/kit_bench/bench_cases.h` | generated | The outputs of LiteRT (built-in kernels) for the test inputs | New file |
| `models/kws_int8.tflite`, `models/ic_int8.tflite`, `models/ic_float32.tflite` | copied with no change | `github.com/mlcommons/tiny`, commit `4addd0f` | none |
| `models/kws_float32.tflite` | new | `kws_ref_model_float32.tflite` of the same repository | The five `int8` weight tensors are changed to `float32`. See `models/README.md`. |
| `pi/bench.py`, `solutions/pi/bench.py` | new | The run rules of the lecture. The power estimate follows the script `avg_temp_power.sh` of the book "Edge AI Engineering". | The student version has no body in the function `percentile` (Task C1). Tested on the work computer with LiteRT, ONNX Runtime, and NCNN. Not tested on a Raspberry Pi. |
| `pi/make_report.py`, `solutions/pi/make_report.py` | new | The energy and the duty cycle of Part 3 of the lecture | The student version has no body in the functions `energy_mj` and `mean_power_w` (Tasks D1 and D2). Tested on the work computer with result files of the work computer. |
| `power.csv` | new | The data sheet of the ESP32-S3 (version 2.2, tables 5-9 and 5-10), and the chapter "Setup" of the book "Edge AI Engineering" | Five rows. Nobody measured a power for this course. |

Points that only the XIAOML Kit can confirm:

- The sketch on the board: the output of the Serial Monitor, and the line
  `Same result as LiteRT: yes` for each model.
- The memory of each arena. The arena of the `float32` image model has
  224 KB. Nobody checked if the internal RAM has a free block of this size.
  If not, the sketch takes the PSRAM.
- All times. The lab gives no expected latency of the kit. The library has
  portable kernels and no kernels for the ESP32-S3, so the `float32` models
  can need more than 1 second for one inference.
- The functions `setCpuFrequencyMhz()` and `temperatureRead()` of the esp32
  core 3.3.12 on this board, and the Serial Monitor after a clock change.
- The time of the first build on a lab laptop. On the work computer, a
  build with 24 cores needs about 1 minute.
- The time for each part.

Points that only a Raspberry Pi 5 can confirm:

- The four functions that read the board: the temperature and the clock
  from the files of `/sys`, the throttle state from `vcgencmd get_throttled`,
  and the power from `vcgencmd pmic_read_adc`. The parser of the power ran
  only with the two example rails of the book (the sum of voltage x current
  is 0.4953 W for these two rails). Nobody ran it with the complete output
  of a board.
- The linear correction of the power estimate (1.1451 x sum + 0.5879) is a
  value of the source. Nobody compared it with a power meter for this
  course.
- The packages of the two environments. The suite `detection` needs `ncnn`
  and `ai-edge-litert` in `~/yolo`. The suites `tiny` and `classification`
  need `ai-edge-litert` and `onnxruntime` in `~/tflite_env`.
- The model files of Days 7 and 8 on the card, in `~/edgeai/day07/models/`
  and `~/edgeai/day08/models/`.
- All times, temperatures, and power values.

Compile check (work computer, 2026-10-02, `arduino-cli` 1.5.1, esp32 core
3.3.12, Chirale_TensorFlowLite 2.0.0, board `esp32:esp32:XIAO_ESP32S3`):

| Version | Build option | Flash | RAM (global variables) |
|---|---|---|---|
| Student version, Task B1 not complete | `PSRAM=opi` | 944 575 bytes | 24 692 bytes |
| Solution | `PSRAM=opi` | 944 679 bytes | 24 692 bytes |
| Solution | PSRAM disabled | 939 421 bytes | 24 208 bytes |
| Solution, `CPU_MHZ` 80 | `PSRAM=opi` | 944 671 bytes | 24 692 bytes |

The flash limit of the board is 3 342 336 bytes. The four models have
567 540 bytes of the program.

Test of the sketch on the work computer (2026-10-02): a 32-bit build with
the same library, for an x86 processor. The times are not times of the
board.

| Model | Arena use | Arena of the sketch | Class | Largest difference to LiteRT | Median in this build |
|---|---|---|---|---|---|
| Keyword spotting, `int8` | 23 012 bytes | 32 768 bytes | 8 | 0.0000 | 2762 microseconds |
| Keyword spotting, `float32` | 66 256 bytes | 98 304 bytes | 8 | 0.0000 | 4140 microseconds |
| Image classification, `int8` | 55 220 bytes | 65 536 bytes | 6 | 0.0000 | 8556 microseconds |
| Image classification, `float32` | 199 344 bytes | 229 376 bytes | 6 | 0.0000 | 12 512 microseconds |

The student version prints `Task B1: not complete`, the minimum and the
maximum of each model, and 0 for the median and for the p95 in the lines
`CSV`.

One defect of the first version: the sketch filled the input tensor one time
only. The interpreter uses the memory of the input tensor again for a later
tensor, so the second inference had a different input, and the output was
not the output of LiteRT. The sketch now fills the input before each
inference, outside the timed window.

Test of the file `models/kws_float32.tflite` (work computer, 2026-10-02):
for 200 random inputs, the file gives the same class as the published file
`kws_ref_model_float32.tflite` each time. The largest difference of an
output value is 0.267: the published file calculates with `int8` weights
and quantizes its activations for each convolution.

Test of the accuracy of the image classification files (work computer,
2026-10-02, LiteRT with the built-in kernels):

| File | 10 000 test images of CIFAR-10 | The 200 test images of MLPerf Tiny |
|---|---|---|
| `ic_float32.tflite` | 87.19 percent | 87.0 percent |
| `ic_int8.tflite` | 87.02 percent | 87.0 percent |

The two files give a different class for 268 of the 10 000 images and for 7
of the 200 images.

Test of `solutions/pi/bench.py` (work computer, 2026-10-02): an x86
processor with AVX2, cores 0 to 3, `ai-edge-litert` 2.2.0, `onnxruntime`
1.23.2, `ncnn` 1.0.20260526, `numpy` 2.2.6. Each case: 20 inferences to warm
up, then 200 timed inferences. These are not values of the board. The files
of Days 7 and 8 are the files of the solution notebooks of these labs.

| Suite | File | Runtime | Threads | Median in ms | p95 in ms | Peak RAM in MB |
|---|---|---|---|---|---|---|
| tiny | `kws_int8.tflite` | LiteRT | 1 | 0.277 | 0.292 | 39.6 |
| tiny | `kws_float32.tflite` | LiteRT | 1 | 0.126 | 0.140 | 40.0 |
| tiny | `ic_int8.tflite` | LiteRT | 1 | 0.492 | 0.578 | 39.6 |
| tiny | `ic_float32.tflite` | LiteRT | 1 | 0.401 | 0.430 | 39.8 |
| classification | `mnv2.tflite` | LiteRT | 1 | 11.329 | 11.902 | 80.5 |
| classification | `mnv2.tflite` | LiteRT | 4 | 3.253 | 3.398 | 80.2 |
| classification | `mnv2_int8.tflite` | LiteRT | 1 | 15.211 | 16.240 | 56.3 |
| classification | `mnv2_int8.tflite` | LiteRT | 4 | 4.107 | 4.247 | 56.2 |
| classification | `mnv2_static.onnx` | ONNX Runtime | 1 | 10.960 | 11.816 | 101.0 |
| classification | `mnv2_static.onnx` | ONNX Runtime | 4 | 3.348 | 3.579 | 100.8 |
| classification | `mnv2_int8.onnx` | ONNX Runtime | 1 | 12.458 | 12.775 | 69.0 |
| classification | `mnv2_int8.onnx` | ONNX Runtime | 4 | 3.939 | 4.010 | 68.9 |
| detection | `cupbottle_320_ncnn_model` | NCNN | 1 | 39.347 | 40.382 | 79.3 |
| detection | `cupbottle_320_ncnn_model` | NCNN | 4 | 14.986 | 16.151 | 82.4 |
| detection | `cupbottle_320.tflite` | LiteRT | 1 | 30.452 | 33.143 | 81.5 |
| detection | `cupbottle_320.tflite` | LiteRT | 4 | 9.122 | 9.421 | 82.0 |
| detection | `cupbottle_320_int8.tflite` | LiteRT | 1 | 30.757 | 33.012 | 61.0 |
| detection | `cupbottle_320_int8.tflite` | LiteRT | 4 | 9.938 | 10.442 | 60.5 |

The suite `tiny` printed `same as the kit sketch` for the four models. A
sustained run of 60 seconds with `cupbottle_320.tflite` and 4 threads gave a
median of 8.688 ms in the first window and 8.685 ms in the last window. The
work computer gives no throttle state and no power, so these columns were
empty, and `--idle` printed `no value on this computer` for the power.

The student version of `pi/bench.py` prints `Task C1: not complete` and
stops. The student version of `pi/make_report.py` prints
`Task D1 and Task D2: not complete` and stops. The complete version made
the four tables from the result files of the work computer. With no power
value for the Raspberry Pi, the energy cells of that board have the text
`no value`.

## 2. Checklist for the instructor

Run the lab on the real hardware. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Boards: XIAOML Kit, Raspberry Pi 5 (8 GB) with the active cooler

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Copy `solutions/sketches/kit_bench/bench_stats.h` into the sketch folder. Build with `OPI PSRAM` and upload. | The time of the first build. The two lines of the build. | |
| 2 | Open the Serial Monitor | The complete output. Is each line `Same result as LiteRT: yes`? | |
| 3 | The same output | The memory of each arena: internal RAM or PSRAM. The free internal heap. | |
| 4 | Send a character two times | The median of each model for three runs: the noise | |
| 5 | Build with PSRAM disabled | Which model prints `ERROR: no memory`? | |
| 6 | Set `CPU_MHZ` to 80 and upload | The medians. Does the Serial Monitor work after the change? | |
| 7 | With a USB power meter at the kit | The power with no load and during the run | |
| 8 | On the Raspberry Pi: `vcgencmd pmic_read_adc` | The complete output, as a text file. The script needs lines of the form `NAME_A current(n)=...A` and `NAME_V volt(n)=...V`. | |
| 9 | `python solutions/pi/bench.py --idle 30` | The temperature and the power. Compare the power with a power meter. | |
| 10 | `python solutions/pi/bench.py --suite tiny` and `--suite classification` in `~/tflite_env` | The two tables. Is each class check `same as the kit sketch`? | |
| 11 | `python solutions/pi/bench.py --suite detection` in `~/yolo` | The table. Does `ncnn` import? | |
| 12 | `python solutions/pi/bench.py --sustain 180 --model ../day08/models/cupbottle_320.tflite --threads 4` | The first and the last line. The highest temperature. The throttle state. | |
| 13 | Copy `results_pi.csv`, make `results_kit.csv`, and run `python3 solutions/pi/make_report.py` | The four tables. Are the energy values plausible? | |
| 14 | Compare the latency of the two `int8` models on the kit with the published results in `report.md` | The factor to each board | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 20 min | |
| B | 45 min | |
| C | 50 min | |
| D | 35 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured values of the two boards in
   `solutions/report_example.md` and in the lab deck.
2. If a `float32` model needs more than 5 seconds for one inference on the
   kit, decrease `TIMED_RUNS` in the sketch and in the README.
3. If the output of `vcgencmd pmic_read_adc` has a different form, correct
   the function `parse_pmic` in `pi/bench.py` and in
   `solutions/pi/bench.py`.
4. If the power estimate of the board differs much from the power meter,
   write the two values here, and change the fallback of the README.
5. Write the measured power of the kit in `power.csv`, with the method
   `USB power meter`.
6. Write the package versions of the board in `Labs/VERSIONS.md`.
