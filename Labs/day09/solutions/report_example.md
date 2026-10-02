# Day 9 lab report: example

This example has the parts of the report that need no board: the protocol,
the sizes of the models, the accuracy table, and the method of each
calculation. Nobody measured a time, a temperature, or a power on the two
boards for this course. These cells have the text "measure in the lab".

## Part A: the protocol

| Part | XIAOML Kit | Raspberry Pi 5 |
|---|---|---|
| Task | Keyword spotting and image classification | The same two tasks, image classification with MobileNetV2, and object detection |
| Dataset: the input of each run | One fixed test input for each model, from the generator of the sketch. The same values each time. | The same test input for the four kit models. One fixed random tensor (seed 0) for MobileNetV2 and for the detector. |
| Model: the files | The four reference models of MLPerf Tiny, as C arrays in the sketch | The same four files, 4 files of MobileNetV2 (Day 7), 3 files of the detector (Day 8) |
| Metrics, with their units | Latency in ms (median, p95), flash in bytes, arena in bytes, energy in mJ | Latency in ms (median, p95), peak RAM in MB, temperature in C, power in W, energy in mJ |
| Harness: the program that reads the clock | The sketch `kit_bench`, with `micros()` | The script `pi/bench.py`, with `time.perf_counter_ns()`, one new process for each case |
| System description: board, clock, runtime, threads | XIAO ESP32S3 Sense, 240 MHz, esp32 core 3.3.12, Chirale_TensorFlowLite 2.0.0, one core | Raspberry Pi 5 (8 GB) with the active cooler, LiteRT, ONNX Runtime, and NCNN, 1 and 4 threads |
| Run rules: warm-up runs | 3. The first one is measured alone. | 20. The first one is measured alone. |
| Run rules: timed runs | 20 | 200, or 30 seconds |
| Run rules: the statistic that you report | The median and the p95. With 20 runs, the p95 is the value with the rank 19. | The median and the p95. With 200 runs, the p95 is the value with the rank 190. |
| The timed window | The call of `Invoke()`: the model only | The call of the runtime: the model only |
| What your benchmark does not include | The microphone, the camera, the features, the display, and Wi-Fi | The camera, the pre-processing, and the post-processing of the detector. A second program on the board. |
| Changes of the method, with the reason | none | none |

The predictions are your own work. An example of a prediction with a
reason: "The `int8` model is faster on the kit, by a factor of 2 to 4,
because the processor has no fast kernels for `float32` in this library."
The result can be different. Write it in the column "Result".

## Part B: the microcontroller

The values of the build are from the work computer of the course, with the
setting `OPI PSRAM` and the complete file `bench_stats.h`.

| Item | Result |
|---|---|
| Version of the esp32 core | 3.3.12 |
| Setting of `Tools` > `PSRAM` | OPI PSRAM |
| `WARMUP_RUNS` and `TIMED_RUNS` | 3 and 20 |
| The line `Sketch uses ... bytes` of the build | `Sketch uses 944679 bytes (28%) of program storage space. Maximum is 3342336 bytes.` |
| The line `Global variables use ... bytes` of the build | `Global variables use 24692 bytes (7%) of dynamic memory, leaving 302988 bytes for local variables. Maximum is 327680 bytes.` |
| Free internal heap and PSRAM (second line of the Serial Monitor) | measure in the lab |
| The line of Task B1 in the Serial Monitor | `Task B1: complete` |

The arena values of this table are from a 32-bit build of the sketch on an
x86 computer. The value on the kit can be a little different.

| Model | Model bytes (flash) | Arena bytes (RAM) | Arena memory | First inference in ms | Median in ms | p95 in ms | Maximum in ms | Same result as LiteRT |
|---|---|---|---|---|---|---|---|---|
| Keyword spotting, `int8` | 53 936 | 23 012 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | yes |
| Keyword spotting, `float32` | 96 964 | 66 256 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | yes |
| Image classification, `int8` | 98 496 | 55 220 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | yes |
| Image classification, `float32` | 318 144 | 199 344 | measure in the lab | measure in the lab | measure in the lab | measure in the lab | measure in the lab | yes |

The `float32` file is 1.8 times the `int8` file for the keyword model, and
3.2 times for the image model. The arena is 2.9 times and 3.6 times as
large. A file also holds the graph and the quantization values, so the
factor between the two files is smaller than 4.

Answers:

1. The arena of the `float32` image model needs 224 KB in one block. The
   internal RAM of the board has about 300 KB in total, in more than one
   block. If no block is large enough, the sketch takes the PSRAM. Write
   what your Serial Monitor shows.
2. Two possible reasons. (1) The software: the three published boards use
   an inference tool of their vendor with kernels for their processor. The
   library of this lab has portable C kernels and no kernels for the
   ESP32-S3. (2) The memory: an arena in the PSRAM is slower than an arena
   in the internal RAM, and the model weights are in the flash memory.
3. The Day 5 measurement had no fixed input, no separate warm-up, 10 runs
   only, no percentile, and no statement of the window. Its times were the
   times of a live signal with the display active.

## Part C: the Raspberry Pi

All times, temperatures, and power values: measure in the lab.

The class check of the suite `tiny` must print `same as the kit sketch` for
the four models: class 8 for the two keyword files, and class 6 for the two
image files.

Answers:

1. The frame rate of Day 8 is end to end: capture, pre-processing, model,
   and post-processing. The value of today is the model only, with a random
   input. So 1000 divided by the median of today is higher than the frame
   rate of Day 8. The difference is the time of the other steps.
2. Measure in the lab. A case with 4 threads often has the larger ratio:
   the operating system can give one of the 4 cores to a different program
   for a short time.
3. Measure in the lab. With the active cooler, the processor of the
   Raspberry Pi 5 usually stays below the temperature at which the firmware
   limits the clock (about 80 degrees Celsius). Then the two latencies are
   almost the same.

## Part D: the report

| Board and state | Power in W | Method: power meter, estimate of the board, or data sheet |
|---|---|---|
| Kit, active | 0.217 | Data sheet of the ESP32-S3: 65.9 mA at 3.3 V |
| Kit, idle | 0.157 | Data sheet: 47.6 mA at 3.3 V |
| Kit, sleep | 0.00079 | Data sheet: light sleep, 240 microamperes at 3.3 V |
| Raspberry Pi, active | measure in the lab | The estimate of the board (`power_w`), or the power meter |
| Raspberry Pi, idle | measure in the lab | `python pi/bench.py --idle 30`, or the power meter |

The method of each calculated value:

- Energy of one inference in mJ: power in W x median latency in ms.
- Duty cycle: median latency divided by the period, and not more than 1.
- Mean power: duty cycle x active power + (1 - duty cycle) x rest power.
- Battery life in hours: capacity in Wh divided by the mean power in W. A
  battery of 1000 mAh at 3.7 V has 3.7 Wh.

One calculation that needs no board: a device that sleeps all the time with
0.00079 W gets 3.7 / 0.00079 = 4684 hours from this battery: 195 days. A
device that waits all the time with 0.157 W gets 23.6 hours. So the rest
state decides the battery life of a keyword detector, not the inference.

| Model | Accuracy | Test set | Source of the value |
|---|---|---|---|
| Keyword spotting, `int8` | 91.6 percent | The test set of Speech Commands | Published: Banbury et al., 2021 |
| Keyword spotting, `float32` | not measured | none | `models/README.md` |
| Image classification, `int8` | 87.0 percent | 10 000 test images of CIFAR-10 | An experiment of this course |
| Image classification, `float32` | 87.2 percent | 10 000 test images of CIFAR-10 | An experiment of this course |
| MobileNetV2, `float32` | 77.4 percent | 500 images of Imagenette | The Day 7 lab |
| MobileNetV2, `int8` (LiteRT) | 75.2 percent | 500 images of Imagenette | The Day 7 lab |
| Your detector, `float32`: mAP50-95 | your value of Day 8 | The 100 test images of Day 8 | Your notebook of Day 8 |
| Your detector, `int8`: mAP50-95 | your value of Day 8 | The 100 test images of Day 8 | Your notebook of Day 8 |

Answers:

1. Measure in the lab.
2. Measure in the lab. The Raspberry Pi is faster. It also uses more than
   10 times the power of the kit, so the energy for one inference depends
   on the two factors.
3. The 95 percent interval of an accuracy of 87.0 percent with 200 images is
   plus and minus 4.7 points. With 10 000 images it is plus and minus 0.7
   points. So 200 images show only a difference of about 5 points or more.
   The two files differ by 0.2 points on the 10 000 images.
4. Examples: the power of the kit (a data sheet value of the chip, not a
   measurement of the board: use a power meter); the accuracy of the
   `float32` keyword file (not measured: run the test set of Speech
   Commands); the p95 of the kit (20 runs only: use 200 runs).

## Decision Log

An example of the form. Replace each text in brackets with your numbers.

Decision: the keyword detector uses the XIAOML Kit with the `int8` model,
and the board sleeps between two inferences. The cup counter uses the
Raspberry Pi 5 with [runtime], [precision], and [threads] threads.

Numbers that support the decision, each with its method: the keyword model
needs [median] ms on the kit ([warm-up] + [runs] runs, the model only). With
one inference in each second and light sleep, the mean power is [value] W,
and a battery of [capacity] gives [hours] hours. The detector needs
[median] ms for the model on the Raspberry Pi, and the frame rate of Day 8
was [value] frames in each second, end to end.

Trade-off: the kit cannot run the detector at 10 frames in each second, and
the Raspberry Pi cannot run for one month from a small battery. The sleep
power of the kit is a data sheet value for the chip: a measurement of the
board is necessary before the product decision.
