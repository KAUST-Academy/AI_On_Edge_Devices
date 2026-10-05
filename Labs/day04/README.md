# Day 4 lab: quantization


**Goal.** Your group has a measured comparison of a `float32` model and an
`int8` model: size, accuracy, and latency, on the laptop and on the XIAOML
Kit.

**Deliverable.** The file `report.md` with the comparison table of Part D
and the Decision Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | By hand: quantize tensors in NumPy, measure the rounding error and the clipping error | 30 min |
| B | Post-training quantization: quantize a small CNN, change the calibration set | 50 min |
| C | Quantization-aware training: train the same CNN with simulated quantization | 40 min |
| D | On the board: the float model and the `int8` model of Day 3 | 30 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| XIAOML Kit | 1 | XIAO ESP32S3 Sense with the expansion board (IMU and display). Only Part D needs the kit. |
| USB-C cable | 1 | A data cable |
| Laptop | 1 | With the dataset of Day 2 in `Labs/day02/data/` |

## Software

| Tool | Version | Note |
|---|---|---|
| Arduino IDE 2 with the esp32 core | 3.3.12 | Steps 1 to 3 of `Labs/SETUP.md` |
| Chirale_TensorFlowLite (library) | 2.0.0 | Installed on Day 3 |
| Seeed Arduino LSM6DS3, U8g2 (libraries) | 2.0.7, 2.36.19 | Installed on Day 1 |
| Python | 3.10 or later | The notebook ran with Python 3.10.12 |
| `tensorflow-cpu`, `ai-edge-litert`, `numpy`, `matplotlib`, `jupyterlab` | see `Labs/VERSIONS.md` | Installed on Day 3. `Labs/requirements.txt` has the list. |

The lab needs no new package and no new library.

Run all commands of this lab from the folder `Labs/day04/`.

## Files

| File | Content |
|---|---|
| `quantization.ipynb` | Parts A, B, and C, and the first step of Part D. The student notebook. It has eight tasks. |
| `sketches/motion_quant/motion_quant.ino` | Part D. The sketch for the board. **Tasks D1 and D2** are in this file. |
| `sketches/motion_quant/motion_features.h` | The feature code of Day 3. You do not change it. |
| `sketches/motion_quant/model_float.h`, `model_int8.h`, `model_settings.h`, `test_set.h` | The two models, their settings, and 80 test windows. The notebook writes these files. The files in the repository come from the fallback dataset. |
| `host/tflite_to_header.py` | Converts a LiteRT file to a C array. The notebook uses it. |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/` | The notebook with all tasks complete and with its output, the complete sketch, and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

## Steps

Write each result in `report.md` when you get it.

### Part A: quantize by hand (30 min)

1. **Start (2 min).** Start Jupyter and run sections 0 and 1 of the
   notebook:

   ```bash
   ../../.venv/bin/jupyter lab quantization.ipynb
   ```

   You see the versions, the data folder, the number of training windows
   and test windows, and the range of the values of each class. The
   notebook uses `Labs/day02/data/`. If the folder has no recordings, the
   notebook uses the fallback dataset. Its signals are simulated.

2. **Tasks 1 and 2: the affine mapping (10 min).** Write the function
   `scale_zero_point` and the functions `quantize` and `dequantize` in
   section 2.

   You see: `Task 1: complete`, `Task 2: complete`, and the table of the
   lecture exercise with the scale 0.01 and the zero point -28.

3. **The rounding error (6 min).** Run section 3. The code quantizes all
   acceleration values of the training set. Write the scale, the zero
   point, the largest error, and the typical error in the report. Compare
   them with the two rules of the lecture: `S / 2` and `S / sqrt(12)`.
   Then run the cell with fewer bits.

4. **Task 3: the clipping error (12 min).** Write your prediction in
   section 4 before you run the experiment. Then run it and answer the
   two questions in the report.

### Part B: post-training quantization (50 min)

1. **The float baseline (5 min).** Run section 5. The notebook trains a
   small CNN for the raw window. Write the number of parameters, the size
   of the `float32` LiteRT file, and the test accuracy in the report.

2. **Task 4: convert (10 min).** Complete the function `convert_int8` in
   section 6: the generator `representative_dataset` and the five
   settings of the converter.

   You see: `Task 4: complete` and the sizes of the two LiteRT files.

3. **Task 5: test the `int8` model (10 min).** Complete the function
   `quantize_input` in section 7.

   You see: `Task 5: complete` and a table with one row for each model:
   the file size, the accuracy, the accuracy of each class, and the
   percent of clipped input values. Write the two rows in the report.

4. **Look into the model (8 min).** Run section 8. Answer in the report:
   how many scales has the weight tensor of each convolution, which zero
   point have the weights, and which type have the biases?

5. **Task 6: change the calibration set (17 min).** Write your
   prediction in section 9 before you run the experiment. Then run it.
   Write the table of experiment 1 in the report and answer the three
   questions.

### Part C: quantization-aware training (40 min)

1. **Task 7: the straight-through estimator (10 min).** Replace the last
   line of the function `fake_quant` in section 10. Then read the layers
   of the next cell and run it.

   You see: `Task 7: complete`, a gradient of 1 for each value, and the
   accuracy of the model with simulated quantization. This accuracy must
   be near the accuracy of the `int8` LiteRT model of Part B.

2. **Task 8: train with simulated quantization (12 min).** Write your
   prediction in section 11 before you run the experiment. Then run it.
   The code trains the model four times: with weights of 8, 4, 3, and 2
   bits. Write the table in the report and answer the two questions.

3. **Find the layer (8 min).** Run section 12. Write the two tables in
   the report and answer the two questions.

4. **The real `int8` model (10 min).** Run section 13. Write the three
   rows of the table in the report: the float model, the `int8` model of
   Part B, and the `int8` model after quantization-aware training.

### Part D: on the board (30 min)

1. **The two models (5 min).** Run sections 14 and 15 of the notebook.
   The notebook trains the feature model of Day 3 again, converts it to
   `float32` and to `int8`, and writes four files into
   `sketches/motion_quant/`. Write the two file sizes, the two
   accuracies, and the two peaks of the activations in the report.

2. **Prediction (2 min).** Write in the report before you measure: by
   which factor does the `int8` model change the flash use of the sketch,
   the arena, and the time of `Invoke()`? The ESP32-S3 has a circuit for
   float arithmetic, and the library of this course has no optimized
   kernels for this chip.

3. **The float model (6 min).** Open
   `sketches/motion_quant/motion_quant.ino` in the Arduino IDE. Select
   the board `XIAO_ESP32S3` and the port. Set `Tools` > `PSRAM` >
   `Disabled`. Keep the line `#define MODEL_INT8 0`. Click Upload.

   You see in the Serial Monitor at 115200 baud:

   ```
   Model:                float32
   Model size (flash):   ... bytes
   Sketch size (flash):  ... bytes
   Arena size:           4096 bytes
   Arena used:           ... bytes
   Input tensor:  type FLOAT32, 252 bytes
   Output tensor: type FLOAT32, 16 bytes
   Test set:             80 windows
   Test set, correct:    ... of 80 (... percent)
   Test set, same class as on the laptop: ... of 80
   Test set, invoke_us:  median ..., largest ...
   ```

   Write these numbers and the line `Sketch uses ... bytes` of the build
   output in the first column of the comparison table.

4. **Tasks D1 and D2: the `int8` model (8 min).** Change the line to
   `#define MODEL_INT8 1`. Complete the two places with the mark
   `TODO (student)` in the function `classify`:

   - Task D1: quantize the input with the scale and the zero point of
     the input tensor.
   - Task D2: dequantize the output with the scale and the zero point of
     the output tensor.

   Upload. The Serial Monitor prints the same lines for the `int8` model,
   the scale and the zero point of the two tensors, and one more line:
   `Test set, clipped input values: ... of 5040 (laptop: ...)`. Write the
   numbers in the second column of the table.

   The number of windows with the same class as on the laptop must be 80
   of 80. If it is not, check tasks D1 and D2.

5. **Real motions (4 min).** Make each of the four motions for some
   seconds with the `int8` model on the board. Write in the report, for
   each motion, the class that the display shows most of the time.
   Compare with your result of Day 3.

6. **The table and the Decision Log (5 min).** Complete the comparison
   table. Calculate the change of each number. Write the Decision Log.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] The notebook prints `complete` for tasks 1, 2, 4, 5, and 7.
- [ ] The report has the four predictions: task 3, task 6, task 8, and
      the prediction of Part D. The predictions were written before the
      measurement.
- [ ] The report has the table of the calibration experiment, with the
      accuracy of each class and the clipped input values.
- [ ] The Serial Monitor shows `Test set, same class as on the laptop: 80
      of 80` for the `int8` model.
- [ ] The comparison table has a `float32` column and an `int8` column
      with measured numbers of the board: flash, arena, latency, and
      accuracy.
- [ ] The Decision Log gives numbers and explains the change of the
      accuracy.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: the motion classifier of Day 3 goes into a product with
the XIAO ESP32S3. Which model do you put on the board: the `float32` model
or the `int8` model? Use your numbers for the flash, the arena, the latency,
and the accuracy. Explain the change of the accuracy, or explain why the
accuracy does not change.

## If a part does not work

| Problem | Fallback |
|---|---|
| Your group has no dataset of Day 2 | Copy the folder `data/` of a different group into `Labs/day02/`, and write this in the report. With no real data, the notebook uses the simulated fallback dataset. The numbers of the notebook are then the numbers of `solutions/report_example.md`. |
| Task 4 or task 5 is not complete in time | Copy the two functions from `solutions/quantization.ipynb`, and write this in the report. Parts C and D need the two functions. |
| The notebook did not write the four files | Use the files in `sketches/motion_quant/` of the repository. They come from the fallback dataset: the test set of the sketch works, but the board does not classify real motions. |
| Tasks D1 and D2 are not complete in time | Use `solutions/sketches/motion_quant/motion_quant.ino`, copy your four files of the notebook into its folder, and write this in the report. |
| The kit is not available | Complete Parts A, B, and C. In the table of Part D, write the numbers of the notebook, and write "no board" in the other rows. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The notebook prints `No module named 'tensorflow'` | Jupyter does not use the virtual environment | Start Jupyter with `../../.venv/bin/jupyter lab` |
| The notebook says that it uses the fallback dataset | `Labs/day02/data/` has no recordings | Copy your Day 2 recordings into this folder |
| `Task 4: not complete` after your change | The model still has `float32` input: one of the five settings is missing, or the generator gives no input | Compare with the frame "Full integer quantization" of the lecture. The generator must use `yield`. |
| The conversion stops with an error about the shape of the input | The generator gives an array with no batch dimension | Give `[calibration[i:i + 1]]`, not `[calibration[i]]` |
| The `int8` model has an accuracy near 25 percent | The test code gives float values or zeros to the `int8` model | Check task 5 |
| `Task 7: not complete`, and the gradient is `None` | The function returns `x_q`. The round function gives no gradient. | Return `x + ops.stop_gradient(x_q - x)` |
| The upload fails | The port is not correct, or the board does not answer | Start bootloader mode: hold the `B` button, connect the cable, release the button. Upload again. |
| The build prints `model_int8.h: No such file or directory` | The folder of the sketch has no model files | Run section 15 of the notebook, or use the files of the repository |
| The Serial Monitor prints `Task D1: not complete` | The line `task_d1_complete = false;` is still in the code | Remove the line when the task is complete. The same rule applies to task D2. |
| The `int8` model gives the correct class for 20 of 80 windows | The output is 0 for each class: task D2 is not complete | Complete task D2 |
| `Test set, same class as on the laptop` is below 80 | An error in the scale or in the zero point, or the files come from different runs of the notebook | Check tasks D1 and D2. Run section 15 of the notebook again. |
| The board shows the wrong class for all real motions | The model learned from the fallback dataset | Train with your own recordings |

## Credits

This lab adapts material from these sources:

- The section "Quantization and Precision" of chapter 10 of "Machine
  Learning Systems" by Vijay Janapa Reddi and contributors (mlsysbook.ai,
  CC BY-NC-SA 4.0): the affine mapping, post-training quantization with a
  calibration set, per-channel scales, and quantization-aware training with
  the straight-through estimator.
- The chapters "Motion Classification and Anomaly Detection" and "DSP
  Spectral Features" of the XIAOML Kit in the same book, written by Marcelo
  Rovai: the four motion classes, the window of 2 s, the feature list, and
  the network with 20 and 10 neurons.
- The repository EdgeML-with-Raspberry-Pi by Marcelo Rovai
  (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0): its script for
  calibration images, which makes a calibration set with the same number of
  inputs for each class.
- The repository XIAO-ESP32S3-Sense by Marcelo Rovai
  (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0): the IMU code and the
  display code of the sketch.
- The library Chirale_TensorFlowLite by Chirale and the TensorFlow Authors
  (github.com/spaziochirale/Chirale_TensorFlowLite, Apache-2.0): the use of
  the interpreter in the sketch, from its example `hello_world`.

The notebook, the layers for simulated quantization, the quantization code of
the sketch, the test set for the board, and the measurements are new code of
this course.
