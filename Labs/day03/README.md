# Day 3 lab: from a trained model to the microcontroller


**Goal.** Your group has a motion classifier that runs on the XIAOML Kit, and
you know its flash use, its arena size, and its latency.

**Deliverable.** A live demonstration of the four motions on the kit, and the
file `report.md` with the comparison table of the two paths and the Decision
Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Train: features of the Day 2 dataset, a small classifier | 45 min |
| B | Convert and deploy: LiteRT file, C array, sketch with TensorFlow Lite Micro, class on the display | 50 min |
| C | Measure: flash use, arena size, latency, with PSRAM and with no PSRAM | 30 min |
| D | Compare: the same task in Edge Impulse Studio | 25 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| XIAOML Kit | 1 | XIAO ESP32S3 Sense with the expansion board (IMU and display). The board must run the Arduino firmware again (last step of the Day 2 lab). |
| USB-C cable | 1 | A data cable |
| Laptop | 1 | With the dataset of Day 2 in `Labs/day02/data/` |

## Software

| Tool | Version | Note |
|---|---|---|
| Arduino IDE 2 with the esp32 core | 3.3.12 | Steps 1 to 3 of `Labs/SETUP.md` |
| Chirale_TensorFlowLite (library) | 2.0.0 | New today. Install it in the Library Manager. |
| Seeed Arduino LSM6DS3, U8g2 (libraries) | 2.0.7, 2.36.19 | Installed on Day 1 |
| Python | 3.10 or later | The notebook ran with Python 3.10.12 |
| `tensorflow-cpu`, `ai-edge-litert`, `numpy`, `matplotlib`, `jupyterlab` | see `Labs/VERSIONS.md` | `Labs/requirements.txt` |
| Edge Impulse account | no version | The project of Day 2 with your data |

Install the two new Python packages in the virtual environment of Day 1. Run
the command from the root of this repository:

```bash
.venv/bin/pip install tensorflow-cpu ai-edge-litert
```

Run all other commands of this lab from the folder `Labs/day03/`.

## Files

| File | Content |
|---|---|
| `motion_classifier.ipynb` | Parts A and B. The student notebook. It has five tasks. |
| `sketches/motion_classifier/motion_classifier.ino` | Parts B and C. The sketch for the board. **Tasks B1 to B4** are in this file. |
| `sketches/motion_classifier/motion_features.h` | The feature code in C++. You do not change it. |
| `sketches/motion_classifier/model.h`, `model_settings.h`, `test_window.h` | The model, its settings, and one test window. The notebook writes these files. The files in the repository come from the fallback dataset. |
| `sketches/ei_motion_inference/` | Part D. The sketch of the kit lab for the library of Edge Impulse. |
| `host/tflite_to_header.py` | Converts a LiteRT file to a C array. The notebook uses it. |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/` | The notebook with all tasks complete and with its output, the complete sketch, and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

## Steps

Write each result in `report.md` when you get it.

### Part A: train (45 min)

1. **Start (5 min).** Start Jupyter and run sections 0 and 1 of the
   notebook:

   ```bash
   ../../.venv/bin/jupyter lab motion_classifier.ipynb
   ```

   You see the versions, the data folder, and the number of training
   windows and test windows. The notebook uses `Labs/day02/data/` and its
   file `split.json`. If the folder has no recordings, the notebook uses the
   fallback dataset. Its signals are simulated. A model that learns from
   them does not work on the real kit.

2. **Task 1: features (12 min).** Write the function
   `remove_mean_and_rms` in section 2. Read the other feature functions.
   Look at the plot of the spectral power: which axis and which frequency
   separate your classes?

3. **Normalize (2 min).** Run section 3. The mean and the standard
   deviation of each feature come from the training set.

4. **Task 2: the model (8 min).** Add the two hidden layers in section 4.

   You see: `parameters: 1534 (expected: 1534)` and `Task 2: complete`.

5. **Train and test (8 min).** Run section 5. Write the training accuracy,
   the test accuracy, and the confusion matrix in the report.

6. **Task 3: features against the raw window (10 min).** Write your
   prediction in section 6 before you run the experiment. Then run it and
   answer the three questions in the report.

### Part B: convert and deploy (50 min)

1. **Task 4: convert (5 min).** Write the two lines of the converter in
   section 7 of the notebook.

   You see: `Task 4: complete`, the size of the LiteRT file, the operator
   types, and the largest difference between Keras and LiteRT. The
   difference must be smaller than 0.00001. Write the file size and the
   operator types in the report.

2. **Write the files (3 min).** Run section 8. It writes `model.h`,
   `model_settings.h`, and `test_window.h` into
   `sketches/motion_classifier/`.

3. **Task 5: estimate the arena (2 min).** Use the table of the last code
   cell. Write the peak of the activations and the arena size that you try
   first in the report.

4. **The library (5 min).** In the Arduino IDE, open the Library Manager,
   enter `Chirale_TensorFlowLite`, and install version 2.0.0.

5. **First build (5 min).** Open
   `sketches/motion_classifier/motion_classifier.ino`. Select the board
   `XIAO_ESP32S3` and the port. Set `Tools` > `PSRAM` > `Disabled`. Click
   Upload. The first build of the library needs some minutes.

   You see in the Serial Monitor at 115200 baud:
   `Tasks B1 and B2 are not complete.` Write the line
   `Sketch uses ... bytes` of the build output in the report. This is the
   flash use with no runtime in the program.

6. **Tasks B1 to B4: the inference code (20 min).** Complete the four
   places with the mark `TODO (student)`:

   - Task B1: the operator resolver.
   - Task B2: the interpreter and `AllocateTensors()`.
   - Task B3: the function `classify`: normalize the features, write the
     input tensor, call `Invoke()`, read the output tensor.
   - Task B4: the function `bestClass`.

   Upload again. You see the memory numbers and then the self-test:

   ```
   Self-test, features:  largest difference ...
   Self-test, model:     largest difference ...
   Self-test, class:     ... (expected: ...)
   Self-test:            PASS
   ```

   The self-test calculates the features of the window of `test_window.h`
   on the board and runs the model. It compares the results with the
   results of the notebook. `FAIL` shows an error in task B3 or B4, or
   files that do not come from the same run of the notebook.

7. **Demonstration (10 min).** Make each of the four motions for some
   seconds. The display shows the class and its probability. The Serial
   Monitor prints one line for each inference:

   ```
   class,probability,features_us,invoke_us,late_samples
   ```

   Write in the report, for each motion, the class that the board shows
   most of the time.

### Part C: measure (30 min)

1. **Prediction (3 min).** Write in the report before you measure: is the
   inference faster, slower, or equal when the arena is in the PSRAM?

2. **Flash (5 min).** Write the line `Sketch uses ... bytes` of the build
   output of the complete sketch in the report, and the line
   `Model size (flash)` of the Serial Monitor. Calculate the difference to
   the first build of Part B: this is the flash that the runtime and the
   inference code add.

3. **Arena (8 min).** Write the value `Arena used` in the report. Compare
   it with your estimate of task 5. Then set `kTensorArenaSize` to 1024
   and upload: write the message of the Serial Monitor in the report. Set
   `kTensorArenaSize` to the used value plus 256 bytes, upload, and check
   that the self-test passes.

4. **Latency (6 min).** Copy 20 lines of the Serial Monitor. Write the
   median and the maximum of `features_us` and of `invoke_us` in the
   report, and the last value of `late_samples`. The sum of the two times
   must be below 20 000 microseconds: one sample period.

5. **With PSRAM (8 min).** Set `Tools` > `PSRAM` > `OPI PSRAM`. Change the
   line `#define ARENA_IN_PSRAM 0` to `#define ARENA_IN_PSRAM 1`. Upload.
   The Serial Monitor prints `Arena location: PSRAM`. Write the same
   numbers in the second column of the table: flash, arena, and latency.

### Part D: compare with Edge Impulse (25 min)

1. **The impulse (5 min).** Open your project of Day 2 in Edge Impulse
   Studio. In `Create impulse`, set a window size of 2000 ms and a window
   increase of 200 ms. Add the processing block `Spectral Analysis` and
   the learning block `Classification`. Save the impulse.

2. **Features and training (7 min).** In `Spectral features`, set the FFT
   length to 32 and generate the features. In `Classifier`, use two dense
   layers with 20 and 10 neurons and 30 training cycles. Start the
   training. Then run `Model testing` with your test data.

   Write in the report: the test accuracy, and the three estimates of the
   Studio for the device: the inferencing time, the peak RAM, and the
   flash use.

3. **The library (8 min).** In `Deployment`, select `Arduino library` and
   build. Add the ZIP file in the Arduino IDE: `Sketch` >
   `Include Library` > `Add .ZIP Library`. Open
   `sketches/ei_motion_inference/ei_motion_inference.ino`. Change the
   first `#include` line to the header of your library. Upload. The first
   build needs some minutes.

   You see one result each three seconds, with a line of this form:
   `Predictions (DSP: ... ms, Classification: ... ms, Anomaly: ... ms):`.
   Write the two times and the line `Sketch uses ... bytes` in the report.

   If the build is not complete in time, use the estimates of the Studio
   and write "estimate" in the table.

4. **The comparison table (5 min).** Complete the table in the report:
   your sketch against the library of Edge Impulse. Write the Decision
   Log.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] The notebook prints `complete` for tasks 1, 2, and 4.
- [ ] The Serial Monitor shows `Self-test: PASS`.
- [ ] The board shows the correct class for each of the four motions.
- [ ] The report has the three predictions: task 3, the arena estimate of
      task 5, and the PSRAM question of Part C. The predictions were
      written before the measurement.
- [ ] The comparison table has measured numbers for your sketch: flash,
      arena, and latency, with PSRAM and with no PSRAM.
- [ ] The comparison table has numbers for the path of Edge Impulse. Each
      number says if it is a measurement or an estimate of the Studio.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: a product must classify the motion of a package for one
year with a battery. Which path do you select for the firmware: your own
sketch with TensorFlow Lite Micro, or the library of Edge Impulse? Use your
numbers for the flash, the RAM, and the latency.

## If a part does not work

| Problem | Fallback |
|---|---|
| Your group has no dataset of Day 2 | Copy the folder `data/` of a different group into `Labs/day02/`, and write this in the report. With no real data, the notebook uses the simulated fallback dataset. The sketch then passes the self-test, but it does not classify real motions. |
| The inference code does not work in time | Use `solutions/sketches/motion_classifier/motion_classifier.ino`, copy your three files of the notebook into its folder, and continue with Part C. Write this in the report. |
| Edge Impulse Studio is not available | Complete only the column of your sketch, and write the reason in the report. |
| The build of the Edge Impulse library fails with the core 3.3.12 | Use the estimates of the Studio. The kit chapter names the core 2.0.17 for this library. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The notebook prints `No module named 'tensorflow'` | The package is not in the virtual environment, or Jupyter does not use the environment | Install the packages (see "Software"). Start Jupyter with `../../.venv/bin/jupyter lab`. |
| The notebook says that it uses the fallback dataset | `Labs/day02/data/` has no recordings | Copy your Day 2 recordings into this folder |
| The upload fails after Day 2 | MicroPython is on the board | Start bootloader mode: hold the `B` button, connect the cable, release the button. Upload again. |
| The build prints `Chirale_TensorFlowLite.h: No such file or directory` | The library is not installed | Install Chirale_TensorFlowLite 2.0.0 in the Library Manager |
| The Serial Monitor prints `Didn't find op for builtin opcode` | The resolver does not name an operator of the model | Add the `Add...()` call for this operator (task B1) |
| The Serial Monitor prints `AllocateTensors() failed` or `Failed to resize buffer` | The arena is too small | Increase `kTensorArenaSize` |
| The self-test prints `FAIL` for the model | The normalization is missing in task B3, or the three files come from different runs of the notebook | Check task B3. Run section 8 of the notebook again. |
| The board shows `uncertain` | The largest probability is below 0.6 | Make the motion as in your Day 2 recordings. Hold the kit with the display up. |
| The board shows the wrong class for all motions | The model learned from the fallback dataset, or from a different position of the kit | Train with your own recordings |
| `late_samples` increases | The features, the inference, and the display need more than one sample period | Write the value in the report. Part C measures the two times. |
| `ERROR: ARENA_IN_PSRAM is 1, but PSRAM is not active` | The PSRAM setting is `Disabled` | Set `Tools` > `PSRAM` > `OPI PSRAM` |

## Credits

This lab adapts material from these sources:

- The chapters "Motion Classification and Anomaly Detection" and "DSP
  Spectral Features" of the XIAOML Kit in "Machine Learning Systems" by Vijay
  Janapa Reddi and contributors, written by Marcelo Rovai (mlsysbook.ai,
  CC BY-NC-SA 4.0): the four motion classes, the window of 2 s with a stride
  of 0.2 s, the feature list, the network with 20 and 10 neurons, and the
  steps in Edge Impulse Studio.
- The repository XIAO-ESP32S3-Sense by Marcelo Rovai
  (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0): the sketch
  `motion_class_ad_inference_oled`, which is the sketch
  `sketches/ei_motion_inference/` with two changes, and the IMU code and
  the display code of `sketches/motion_classifier/`.
- The library Chirale_TensorFlowLite by Chirale and the TensorFlow Authors
  (github.com/spaziochirale/Chirale_TensorFlowLite, Apache-2.0): the use of
  the interpreter in `sketches/motion_classifier/`, from its example
  `hello_world`.

The notebook, the feature code in C++, the self-test, and the measurements
are new code of this course.
