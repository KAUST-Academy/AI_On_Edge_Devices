# MC-3 lab: spectral features for motion data



**Goal.** You compute the features of a motion signal, train a small
classifier on them, and compare five inputs for the same task: the raw
window, the time-domain features, and the spectral features with three FFT
lengths.

**Deliverable.** The table of section 8 of the notebook, copied into
`report.md`, the answers of its three questions, and the Decision Log.

**Time.** 45 minutes of work.

| Part | Content | Time |
|---|---|---|
| A | The data, the windows, and the three time-domain features | 12 min |
| B | The FFT and the spectral power of one axis | 13 min |
| C | The classifier, and its number of parameters | 8 min |
| D | Five inputs for the same task, and the FFT length | 12 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| Laptop | 1 | A CPU of any class. No board, no camera, no network. |
| XIAOML Kit | 0 | The recordings come from a kit lab of another day. The lab runs with the simulated signals when the group has no recording. |

## Software

| Tool | Version | Note |
|---|---|---|
| Python | 3.10 or later | The notebook ran with Python 3.13.11 |
| `tensorflow-cpu`, `keras` | see `Labs/VERSIONS.md` | In the virtual environment of the course |
| `numpy`, `matplotlib` | see `Labs/VERSIONS.md` | In the same environment |
| `jupyterlab` | see `Labs/VERSIONS.md` | To run the notebook |

The notebook needs no other package. It reads the WAV-free text files of the
clips, so it needs no audio library.

## Files

| File | Content |
|---|---|
| `spectral_features.ipynb` | Parts A to D. The student notebook. It has four tasks. |
| `host/motion_sim.py` | The simulated signals of the four motion classes. |
| `host/make_dataset.py` | Makes the fallback dataset in `fallback_data/`. |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/` | The notebook with all four tasks complete and with its output, and an example report |
| `TEST_NOTES.md` | The code status and the steps to run the lab |

## Steps

Write each result in `report.md` when you get it. Run all the commands from
the folder `Labs/modules/MC-3/`.

### Part A: the data and the time features (12 min)

1. Start Jupyter:

   ```bash
   ../../../.venv/bin/jupyter lab spectral_features.ipynb
   ```

2. Run section 1. It loads the recordings, cuts them into windows of 2 s
   with a stride of 0.2 s, and prints the number of windows of each class.
   The last session is the test session. Write the two numbers in the
   report.

3. **Task 1.** Write `time_features(window)`: the RMS, the skewness, and the
   kurtosis of one axis of one window, after the removal of the mean. The
   functions that do each step are in the cell above.

   You see `Task 1: complete`. The three values that the check prints are
   for the first window, which is an idle window, so they are small.

4. Look at the plot of section 3. It draws the power of one window of each
   class on the z axis, from 0 to 4 Hz. Write in the report which frequency
   holds the power of `lift`, and which one holds the power of `maritime`.
   Two of the curves stay near zero: `idle` does not move, and the motion of
   a truck sits on the axes x and y, not on z.

### Part B: the FFT and the spectral power (13 min)

1. **Task 2.** Write `axis_features(window, nfft)`: the three time-domain
   features first, then the power of bins 1 to `nfft // 2`.

   You see `Task 2: complete` and the number of values of one axis. It must
   be `3 + 128 / 2 = 67`.

2. Run section 4. It normalizes each feature with the mean and the standard
   deviation of the training windows. Write the mean and the standard
   deviation of the first nine features in the report. The first three
   values are the RMS, the skewness, and the kurtosis of the axis `x`, and
   the next six are power values.

### Part C: the classifier (8 min)

1. **Task 3.** Write `make_model(n_inputs)`: an input of `n_inputs` values, a
   dense layer of 20 units with ReLU, a dense layer of 10 units with ReLU,
   and 4 outputs with softmax. Give the layers the names `dense`,
   `dense_1`, and `dense_2`, and the input the name `keras_tensor`.

   You see `Task 3: complete`, the number of parameters, and then the test
   accuracy of the model.

2. Write the number of parameters and the test accuracy in the report. The
   number of parameters is `n_inputs * 20 + 20 + 20 * 10 + 10 + 10 * 4 + 4`.

### Part D: five inputs for the same task (12 min)

1. Run section 6. It trains the same network three times: on the raw
   window, on the time-domain features only, and on the spectral features.
   Write the three lines of output in the report.

2. **Task 4.** Before you run the next cell, complete `feature_count` in
   section 7 with the number of values of one axis for the FFT lengths 32,
   64, and 128. Then write in `best_fft_length` the length that you expect
   to give the best test accuracy, and one sentence in `best_fft_reason`.

3. Run section 7 and section 8. Copy the table into the report, then answer
   the three questions of the notebook.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] The notebook prints `complete` for tasks 1, 2, 3, and 4.
- [ ] The table of the report has five rows: the raw window, the
      time-domain features, the spectral features with the FFT length of the
      notebook, and the two other FFT lengths.
- [ ] Each row has the number of values, the number of parameters, and a
      measured test accuracy.
- [ ] The three questions of the report have answers with numbers from your
      own run.
- [ ] The Decision Log names one decision, one number, and one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured
numbers, and name the trade-off.

Question of this lab: a device must classify the motion of a pallet for one
year on a battery. Which feature set do you put in the firmware, and which
number of your table decides it?

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The notebook says that it uses the fallback dataset | The folder `data/` has no recording | Copy the recordings of your group into `Labs/modules/MC-3/data/`. With the simulated signals, the model does not classify real motions. |
| The notebook prints `No module named 'tensorflow'` | The package is not in the virtual environment, or Jupyter does not use it | Install the packages of `Labs/requirements.txt` in the virtual environment of the course, and start Jupyter with `../../../.venv/bin/jupyter lab`. |
| `Task 1` prints `not complete` | The answer does not have three values, or the mean was not removed | The check compares your answer with its own calculation. Read the code of the three given functions. |
| `Task 2` prints that the table needs 67 values | Your answer has a different number | Return three time-domain features and then one value for each bin from 1 to `nfft // 2`. |
| `Task 3` prints that the model raises an error | A layer is missing, or a layer was added to the model with a tensor | Build the layers on top of the input, one after the other, and return a model with that input and that output. |
| The accuracies change between two runs | The run is not reproducible | Write `keras.utils.set_random_seed(0)` before each `model.fit`, and run the same cells in the same order. |
| The plot of section 3 is empty | The window has no power above the noise | Check that `FFT_LENGTH` is 128 and that the file of the plot has been written in the working folder. |
| The notebook is slow | The virtual environment is on a network drive | Copy the virtual environment to the local disk of the laptop. |