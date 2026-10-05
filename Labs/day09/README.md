# Day 9 lab: one benchmark report for two boards


**Goal.** Your group has one benchmark report for the XIAOML Kit and the
Raspberry Pi 5. Each number of the report has a method, and the report
compares the same model file on the two boards.

**Deliverable.** The file `report.md` with the protocol, the result tables,
and the Decision Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Protocol: write the method of each measurement before you measure | 20 min |
| B | Microcontroller: keyword spotting and image classification on the kit, in `float32` and in `int8` | 45 min |
| C | Raspberry Pi: image classification and object detection for two runtimes and two thread counts, with the temperature | 50 min |
| D | Report: latency, RAM, flash, accuracy, and estimated energy | 35 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| XIAOML Kit | 1 | XIAO ESP32S3 Sense. This lab uses no sensor and no display. |
| USB-C cable | 1 | A data cable |
| Raspberry Pi 5 (8 GB) with the active cooler | 1 | With the microSD card of the course and the model files of Days 7 and 8 |
| Power supply for the Raspberry Pi 5 | 1 | 27 W, USB-C |
| Laptop | 1 | With the Arduino IDE, in the same network as the Raspberry Pi |
| USB power meter | 1, if the classroom has it | Between the power supply and the board. Without the meter, you estimate the energy. |

## Software

| Tool | Version | Note |
|---|---|---|
| Arduino IDE 2 with the esp32 core | 3.3.12 | Steps 1 to 3 of `Labs/SETUP.md` |
| Chirale_TensorFlowLite (library) | 2.0.0 | Installed on Day 3 |
| Raspberry Pi OS (64-bit) with the environments `~/tflite_env` and `~/yolo` | the card of the course | `Labs/hardware/HW-04/` prepares the card. `~/tflite_env` has `ai-edge-litert` and `onnxruntime`. `~/yolo` has `ai-edge-litert` and `ncnn`. |
| SSH client on the laptop | no version | The commands `ssh` and `scp` |
| Python on the laptop | 3.8 or later | Only for `pi/make_report.py`. It needs no package. |

Run all commands of this lab from the folder `Labs/day09/` on the laptop,
and from the folder `~/edgeai/day09/` on the Raspberry Pi. `NN` is the number
of your group.

## Files

| File | Content |
|---|---|
| `report.md` | The report to hand in. Part A is the protocol. Fill it during the lab. |
| `sketches/kit_bench/kit_bench.ino` | Part B. The benchmark sketch for the kit. It has no task. |
| `sketches/kit_bench/bench_stats.h` | Part B. The sort and the percentile. **Task B1** is in this file. |
| `sketches/kit_bench/bench_cases.h`, `sketches/kit_bench/model_kws_int8.h`, `sketches/kit_bench/model_kws_float32.h`, `sketches/kit_bench/model_ic_int8.h`, `sketches/kit_bench/model_ic_float32.h` | Generated files: the four models as C arrays, the test input, and the output of LiteRT |
| `models/kws_int8.tflite`, `models/kws_float32.tflite`, `models/ic_int8.tflite`, `models/ic_float32.tflite` | The same four models as files, for the Raspberry Pi. `models/README.md` gives the source and the licence. |
| `pi/bench.py` | Part C. The benchmark harness for the Raspberry Pi. **Task C1** is in this file. |
| `pi/make_report.py` | Part D. Makes the tables of the report. **Tasks D1 and D2** are in this file. |
| `power.csv` | Part D. The power of each board. It has data sheet values at the start. |
| `solutions/` | The complete files `bench_stats.h`, `pi/bench.py`, and `pi/make_report.py`, and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

The scripts write the files `results_pi.csv`, `sustain.csv`,
`report_tables.md`, and the folder `raw/`. You make the file
`results_kit.csv`. Git ignores these files.

## The models

Part B uses the reference models of the benchmark suite MLPerf Tiny for
keyword spotting and for image classification (Part 1 of the lecture). Each
model has an `int8` file and a `float32` file. Part C runs the same four
files on the Raspberry Pi, the MobileNetV2 files of Day 7, and your detector
of Day 8.

You do not measure the accuracy today. Use these values in the report, and
give the source of each value:

| Model | Accuracy | Test set | Source |
|---|---|---|---|
| Image classification of MLPerf Tiny, `float32` | 87.2 percent | 10 000 test images of CIFAR-10 | An experiment of this course with LiteRT |
| Image classification of MLPerf Tiny, `int8` | 87.0 percent | 10 000 test images of CIFAR-10 | An experiment of this course with LiteRT |
| The two files of that model | 87.0 percent each | The 200 test images of MLPerf Tiny | An experiment of this course. The published results of MLPerf Tiny v1.2 give the same value. |
| Keyword spotting of MLPerf Tiny, `int8` | 91.6 percent | The test set of Speech Commands | Published: Banbury et al., "MLPerf Tiny Benchmark", 2021 |
| Keyword spotting, `float32` file of this lab | not measured | none | `models/README.md` |
| MobileNetV2, `float32`, `int8` for LiteRT, `int8` for ONNX Runtime | 77.4, 75.2, and 74.4 percent | 500 images of Imagenette | The Day 7 lab |
| Your detector | your values | The 100 test images of Day 8 | Your notebook of Day 8 |

The two image classification files give a different class for 268 of the
10 000 images, and for 7 of the 200 images.

## Steps

Write each result in `report.md` when you get it.

### Part A: protocol (20 min)

1. **Read the plan (5 min).** The lab has three groups of measurements:
   four models on the kit (Part B), the same four models on the Raspberry Pi,
   and the models of Days 7 and 8 on the Raspberry Pi (Part C). Read the
   tables of Parts B and C in `report.md`.

2. **Write the protocol (10 min).** Fill the table of Part A in `report.md`.
   It has the seven parts of a benchmark of the lecture. Decide these
   values:

   - The number of inferences to warm up, and the number of timed
     inferences. On the kit, one inference can need more than 1 second: the
     sketch has 3 and 20 at the start. On the Raspberry Pi, the script has
     20 and 200 at the start.
   - The statistic that you report: the median and the 95th percentile.
   - The timed window. The sketch and the script measure the model only.
   - The input. The sketch and the script use one fixed input for each
     model.

3. **Predict (5 min).** Write your prediction for each question of the
   prediction table. Give a number or a factor, and one reason.

### Part B: microcontroller (45 min)

1. **Build (10 min).** Open `sketches/kit_bench/kit_bench.ino` in the
   Arduino IDE. Select the board `XIAO_ESP32S3` and the port. Set `Tools` >
   `PSRAM` > `OPI PSRAM`. Set `WARMUP_RUNS` and `TIMED_RUNS` at the top of
   the sketch to the values of your protocol. Click Upload. The first build
   needs some minutes. Do step 2 during the build.

   Write in the report the two lines `Sketch uses ... bytes` and
   `Global variables use ... bytes` of the build.

2. **Task B1 (10 min).** Open the tab `bench_stats.h`. Complete the function
   `percentileUs` at the mark `TODO (student)`: the nearest-rank rule of the
   lecture, with integer arithmetic. Upload again.

3. **Measure (10 min).** Open the Serial Monitor at 115200 baud. You see
   `Task B1: complete`, and then for each of the four models:

   ```
   --- kws int8 ---
   model: 53936 bytes
   arena: ... bytes used of 32768, in the internal RAM
   first inference: ... us
   timed runs: 20, after 3 inferences to warm up
   min ... us, median ... us, p95 ... us, max ... us
   output: class 8 (LiteRT: 8), largest difference ... Same result as LiteRT: yes
   chip temperature: ... C
   CSV,kit,kws,int8,53936,...
   ```

   Make the file `results_kit.csv` in the folder `Labs/day09/`. Copy each
   line that starts with `CSV` into this file. Fill the table of the four
   models in the report.

   Send a character in the Serial Monitor. The sketch measures again. Write
   the two medians of the second table: the difference is the noise of your
   measurement.

4. **Change the clock (10 min).** Set `CPU_MHZ` at the top of the sketch to
   80. Upload, and copy the new `CSV` lines into `results_kit.csv`, after
   the first lines. Fill the clock table of the report. Then set `CPU_MHZ`
   to 240 again.

5. **Compare (5 min).** The report has the published results of MLPerf Tiny
   for the same two `int8` models on three boards. Write your values in the
   last row. If you have your report of Day 5, write the two times of your
   own keyword model. Answer the three questions of Part B.

### Part C: Raspberry Pi (50 min)

1. **Copy and connect (5 min).** On the laptop, in the folder `Labs/`:

   ```bash
   scp -r day09 edge@pi-NN.local:~/edgeai/
   ssh edge@pi-NN.local
   ```

   On the Raspberry Pi:

   ```bash
   cd ~/edgeai/day09
   source ~/tflite_env/bin/activate
   ls ../day07/models ../day08/models
   ```

   You must see the files `mnv2.tflite` and `mnv2_static.onnx` of Day 7,
   and the files `cupbottle_320_ncnn_model`, `cupbottle_320.tflite`, and
   `cupbottle_320_int8.tflite` of Day 8.

2. **Task C1 (5 min).** Open `pi/bench.py` with `nano`. Complete the
   function `percentile` at the mark `TODO (student)`: the same rule as in
   Task B1.

3. **Idle (5 min).** Close each other program on the Raspberry Pi. Read the
   temperature and the estimated power with no load:

   ```bash
   python pi/bench.py --idle 30
   ```

   Write the two values in the report.

4. **The kit models and MobileNetV2 (10 min).** Run two suites. Use the
   options `--warmup` and `--runs` if your protocol has other values than 20
   and 200.

   ```bash
   python pi/bench.py --suite tiny
   python pi/bench.py --suite classification
   ```

   The script prints one line for each case: the first inference, the
   median, the 95th percentile, and the maximum in ms, the peak RAM of the
   process, the highest temperature, and the estimated power. The suite
   `tiny` also checks the class of each model with the test input of the
   kit sketch. Each case adds one row to the file `results_pi.csv`.

5. **The detector (10 min).** The runtime NCNN is in the second
   environment:

   ```bash
   deactivate
   source ~/yolo/bin/activate
   python pi/bench.py --suite detection
   ```

6. **A sustained run (10 min).** Run the detector with 4 threads for 180
   seconds:

   ```bash
   python pi/bench.py --sustain 180 --threads 4 \
       --model ../day08/models/cupbottle_320.tflite
   ```

   The script prints one line for each 10 seconds: the median latency, the
   temperature, the clock of the processor, and the throttle state. Fill
   the table of the sustained run in the report.

7. **Copy the results (5 min).** On the laptop, in the folder `Labs/day09/`:

   ```bash
   scp edge@pi-NN.local:~/edgeai/day09/results_pi.csv .
   scp edge@pi-NN.local:~/edgeai/day09/sustain.csv .
   ```

   Fill the tables of Part C in the report, and answer the three questions.

### Part D: report (35 min)

1. **Power (10 min).** The file `power.csv` has one row for each board and
   state. Open it in a text editor.

   - With a USB power meter: connect the meter between the power supply and
     the board. Read the power with no load, and during a run of the sketch
     or of `pi/bench.py --sustain 60`. Write your values and the method
     `USB power meter` in `power.csv`.
   - Without the meter, for the kit: keep the data sheet values of the file.
   - Without the meter, for the Raspberry Pi: keep the row `pi,active`
     empty. The script then uses the estimate of the board in the column
     `power_w` of `results_pi.csv`. Write your idle value of Part C in the
     row `pi,idle`.

2. **Tasks D1 and D2 (5 min).** Open `pi/make_report.py`. Complete the two
   functions `energy_mj` and `mean_power_w` at the marks `TODO (student)`.

3. **Make the tables (5 min).** On the laptop, in the folder `Labs/day09/`:

   ```bash
   python3 pi/make_report.py
   ```

   You see four tables: the kit, the Raspberry Pi, the same model file on
   the two boards, and a battery estimate for one keyword inference in each
   second. The script also writes the file `report_tables.md`. Copy the
   tables into the report.

4. **Complete the report (15 min).** Fill the accuracy table with the
   values of the section "The models" above and with your values of Day 8.
   Answer the four questions of Part D. Compare each result with your
   prediction of Part A. Write the Decision Log.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] Part A of the report has the protocol and the predictions, and no
      prediction looks like a result.
- [ ] The Serial Monitor shows `Task B1: complete`, and the line
      `Same result as LiteRT: yes` for each of the four models.
- [ ] `python pi/bench.py --suite tiny` prints `Task C1: complete` and
      `same as the kit sketch` for each of the four models.
- [ ] `python3 pi/make_report.py` prints `Tasks D1 and D2: complete`.
- [ ] Each number of the report has a method: the warm-up runs, the timed
      runs, the input, the statistic, and the window.
- [ ] The report compares the same model file on the two boards: the
      latency and the energy.
- [ ] The report has the temperature of the sustained run.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: a company wants a keyword detector that runs from a
battery for one month, and a camera that counts cups on a desk with 10
frames in each second. You have the two boards of this course. Which board
do you select for each product? Which precision, which runtime, and how many
threads? Give each number with its method.

## If a part does not work

| Problem | Fallback |
|---|---|
| The build of the sketch is not complete in time | Do Task B1 and the protocol during the build. The second build is faster. |
| Task B1, C1, D1, or D2 is not complete in time | Use the file of the folder `solutions/`, and write this in the report |
| A model prints `ERROR: no memory for an arena` | Set `Tools` > `PSRAM` > `OPI PSRAM` and upload again. If the error stays, write "does not fit" for this model: this is also a result. |
| The model files of Day 7 or Day 8 are not on the Raspberry Pi | The script prints `not found` for these files and measures the other files. The instructor gives the files. |
| The script prints no power value | The estimate needs a Raspberry Pi 5. Write a value in the row `pi,active` of `power.csv`: your meter value, or the published range of 5 to 7 W for a moderate load, with the source "published range". |
| The Raspberry Pi is not available | Run `pi/bench.py --suite tiny` on the laptop in an environment with `ai-edge-litert`, and write the name of the processor in the report |
| No USB power meter | Use the data sheet values for the kit and the estimate of the board for the Raspberry Pi |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The build prints `Chirale_TensorFlowLite.h: No such file or directory` | The library is not installed | Install `Chirale_TensorFlowLite` 2.0.0 with the Library Manager |
| The Serial Monitor shows nothing | The sketch ran before the monitor was open | Send a character: the sketch measures again |
| `Same result as LiteRT: NO` | A file of the sketch folder was changed, or the library has a different version | Copy the sketch folder again. Write the library version in the report. |
| The median and the p95 are 0 | Task B1 is not complete | Complete `percentileUs` in `bench_stats.h` |
| The arena of a model is in the PSRAM | The internal RAM has no free block of this size | This is correct. Write the memory in the report: the PSRAM is slower. |
| `ModuleNotFoundError: No module named 'ncnn'` | The environment `~/tflite_env` is active | `deactivate`, then `source ~/yolo/bin/activate` |
| `pi/bench.py` prints `not found` | The file is not in the folder of Day 7 or Day 8 | Copy it with `scp`, or give the file with `--model` |
| The column `watt` is empty | The command `vcgencmd pmic_read_adc` gives no value on this computer | See the table above |
| The throttle state is not `0x0` | The supply voltage was too low, or the firmware limited the clock | Use the 27 W power supply. Check the cooler. Write the value in the report. |
| `pi/make_report.py` prints `0 rows of the kit` | The file `results_kit.csv` is not in the folder, or it has no line with `CSV` | Copy the `CSV` lines of the Serial Monitor into `results_kit.csv` |
| Two runs give different medians | Noise, a second program, or the temperature | Report the two values. More timed runs give a more stable median. |

## Published values for the energy estimate

Use these values only if you have no power meter. Write the source in the
report.

| Board | State | Value | Source |
|---|---|---|---|
| ESP32-S3 chip | Active at 240 MHz, one core runs, the other core waits | 65.9 mA at 3.3 V: 0.217 W | Data sheet of the ESP32-S3 (version 2.2), table 5-9, with the clocks of the peripherals on |
| ESP32-S3 chip | Active at 80 MHz, one core runs | 42.6 mA at 3.3 V: 0.141 W | The same table |
| ESP32-S3 chip | The two cores wait, at 240 MHz | 47.6 mA at 3.3 V: 0.157 W | The same table |
| ESP32-S3 chip | Light sleep | 240 microamperes at 3.3 V: 0.00079 W | Data sheet, table 5-10 |
| ESP32-S3 chip | Deep sleep | 8 microamperes at 3.3 V | Data sheet, table 5-10 |
| Raspberry Pi 5 | No load, with the active cooler | 3.0 to 3.5 W | Book "Edge AI Engineering", chapter "Setup" |
| Raspberry Pi 5 | Moderate processor load | 5 to 7 W | The same chapter |
| Raspberry Pi 5 | Heavy load | 7 to 10 W | The same chapter |

The data sheet values are for the chip only. The board also has the PSRAM,
the flash memory, a voltage regulator, and a light. A power meter at the USB
connector shows a larger value.

## Credits

This lab adapts material from these sources:

- Chapter 12 "Benchmarking" of "Machine Learning Systems" by Vijay Janapa
  Reddi and contributors (mlsysbook.ai, CC BY-NC-SA 4.0): the parts of a
  benchmark, the run rules (warm-up, repetitions, percentiles), the timed
  window, and the energy of a duty cycle.
- The repository `github.com/mlcommons/tiny` of MLCommons (Apache-2.0): the
  four model files. `models/README.md` gives the details. The published
  results in `report.md` are results of MLPerf Tiny v1.2, closed division
  (`github.com/mlcommons/tiny_results_v1.2`, Apache-2.0).
- The paper "MLPerf Tiny Benchmark" by Banbury et al., 2021: the run rules
  of the benchmark (the median of repeated runs, the model as the timed
  window) and the published accuracy of the keyword model.
- The chapter "Setup" of "Edge AI Engineering: Raspberry Pi" by Marcelo
  Rovai (mjrovai.github.io/EdgeML_Made_Ease_ebook): the commands for the
  temperature, the power estimate from the command `vcgencmd pmic_read_adc`
  with its correction, and the published power ranges of the Raspberry Pi 5.
- The example "hello_world" of the library Chirale_TensorFlowLite 2.0.0
  (github.com/spaziochirale/Chirale_TensorFlowLite, Apache-2.0): the use of
  TensorFlow Lite Micro in the sketch.
- The data sheet of the ESP32-S3 by Espressif Systems (version 2.2): the
  current values of the energy estimate.

The benchmark sketch, the harness for the Raspberry Pi, the report script,
the test inputs, and the `float32` keyword file are new work of this course.
The MLPerf name and logo are trademarks of MLCommons Association. A time
that you measure in this lab is not an MLPerf result.
