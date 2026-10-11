# MC-5 lab: keyword spotting features and training in Python

**Goal.** You compute the Mel-frequency cepstral coefficients of a clip of
one second with numpy only, and you train a small classifier on them, with
no tool of Edge Impulse Studio.

**Deliverable.** The table of section 10 of the notebook, copied into
`report.md`, the answers of its three questions, and the Decision Log.

**Time.** 45 minutes of work, plus the download of the dataset one time.

| Part | Content | Time |
|---|---|---|
| A | The clips, and the triangular filters of the Mel scale | 12 min |
| B | The cepstral coefficients, and the plot of one clip | 13 min |
| C | The classifier, and its number of parameters | 8 min |
| D | Three inputs for the same task | 12 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| Laptop | 1 | A CPU of any class. No board, no microphone, no sound card. |
| XIAOML Kit | 0 | The clips come from a public dataset. The lab has no part on the kit. |

## Software

| Tool | Version | Note |
|---|---|---|
| Python | 3.10 or later | The notebook ran with Python 3.13.11 |
| `tensorflow-cpu`, `keras` | see `Labs/VERSIONS.md` | In the virtual environment of the course |
| `numpy`, `matplotlib` | see `Labs/VERSIONS.md` | In the same environment |
| `jupyterlab` | see `Labs/VERSIONS.md` | To run the notebook |

The notebook needs no other package: the Mel filters, the FFT, and the
cosine transform are written with numpy, and the clips are read from text
files, so no audio library is needed.

## Files

| File | Content |
|---|---|
| `mfcc_training.ipynb` | Parts A to D. The student notebook. It has four tasks. |
| `host/get_keywords.py` | Downloads the dataset and writes the clips as text files. |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/` | The notebook with all four tasks complete and with its output, and an example report |
| `TEST_NOTES.md` | The code status and the steps to run the lab |

## Steps

Write each result in `report.md` when you get it. Run all the commands from
the folder `Labs/modules/MC-5/`.

### Before the lab: the dataset

One time for the whole group, or one time for each group:

```bash
python3 host/get_keywords.py
```

The script downloads the file `keywords2.zip` (139 MB) into the folder
`downloads/` and then writes 240 clips of each of the four classes into
`keywords/clips/`. Each clip is one second of audio at 16 kHz, written as
one amplitude per line.

The classroom needs a network with 139 MB of traffic per group. Copy the
folder `keywords/` from a USB drive when the network of the room is small.

### Part A: the clips and the filter bank (12 min)

1. Start Jupyter:

   ```bash
   ../../../.venv/bin/jupyter lab mfcc_training.ipynb
   ```

2. Run sections 0, 1, and 2. Section 2 gives the functions of the pipeline
   that need no decision from you. Read them: two of the four tasks use
   them.

3. **Task 1.** Write `mel_filters(n_filters, n_bins, f_min, f_max,
   sample_rate)`: the matrix of the triangular filters of the Mel scale.
   Each filter rises from 0 to 1 over its left half and falls from 1 to 0
   over its right half.

   You see `Task 1: complete`, the peak of the first filter at bin 2 and of
   the last one at bin 236, and the width of each of them. Write the two
   widths in the report.

### Part B: the cepstral coefficients (13 min)

1. **Task 2.** Write `mfcc(clip, filters=None)`: the pre-emphasis, the
   framing, the Hamming window, the FFT, the power of each bin, the energy
   of each Mel filter, the logarithm, and the cosine transform. The
   function `log_mel` of section 2 does the middle of the list.

   You see `Task 2: complete`, the number of rows and of columns, and the
   mean of the first coefficient and of the last one.

2. Run section 5. The cell draws the waveform, the log Mel energies, and
   the cepstral coefficients of one clip of the class `yes`. Write in the
   report what the middle panel shows and what the bottom panel shows.

3. Run section 6. It computes the features of the 960 clips and writes them
   into the file `features.npz`. Write the run time in the report.

### Part C: the classifier (8 min)

1. **Task 3.** Write `make_model(n_frames, n_features)`: a `Conv1D` layer
   with 16 filters of 3 frames and ReLU, a max pooling of 2, a `Conv1D`
   layer with 32 filters of 3 frames and ReLU, the same max pooling, and a
   `Dense` layer with 4 outputs and softmax.

   You see `Task 3: complete`, the number of frames after the two
   convolutions and the two pooling layers, and the number of parameters.
   Write both in the report.

2. Run the next cell to train the model. Write the test accuracy in the
   report.

### Part D: three inputs for the same task (12 min)

1. **Task 4.** Before you run the next cell, complete `values_per_clip`
   with the number of values that one clip gives for each of the three
   inputs, and write in `best_input` the input that you expect to give the
   best test accuracy.

2. Run the next cell and section 10. Copy the table into the report, then
   answer the three questions of the notebook.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] The notebook prints `complete` for tasks 1, 2, 3, and 4.
- [ ] The table of the report has three rows: the raw audio, the log Mel
      spectrogram, and the cepstral coefficients.
- [ ] Each row has the number of values, the number of parameters, and a
      measured test accuracy.
- [ ] The three questions of the report have answers with numbers from your
      own run.
- [ ] The Decision Log names one decision, one number, and one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured
numbers, and name the trade-off.

Question of this lab: the device must say one word every 500 ms on a
battery. Which of the three inputs do you put in the firmware, and which
number of your table decides it?

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The notebook stops with `No clip in the folder keywords/clips/` | The dataset is not there | Run `python3 host/get_keywords.py`. The download is 139 MB. |
| The download stops | The network of the room | Copy the folder `keywords/` of another group on a USB drive. |
| The notebook prints `No module named 'tensorflow'` | The package is not in the virtual environment, or Jupyter does not use it | Install the packages of `Labs/requirements.txt` in the virtual environment of the course, and start Jupyter with `../../../.venv/bin/jupyter lab`. |
| `Task 1` says that the last filter must reach bin 205 | The bin index of a frequency is `frequency * nfft / sample_rate`, and `nfft` is `2 * (n_bins - 1)` | The last filter must sit near 8000 Hz, which is bin 256. |
| `Task 1` says that every filter must have a maximum of 1 | The peak of a triangle is 1 at its centre | Divide each row by its own maximum. |
| `Task 2` says that the answer needs 50 rows | A clip of 16000 samples with a frame and a stride of 320 gives 50 frames | Return one row for each frame, and no padding row. |
| `Task 3` says that the model raises an error | A layer is missing, or a layer was added with a tensor instead of with its input | Build the layers on top of the input, one after the other, and return a model with that input and that output. |
| The plot of section 5 is empty | The file `features.npz` holds features of another run | Delete `features.npz` and run section 6 again. |
| The accuracies change between two runs | The run is not reproducible | Keep the seed 0 in the two cells that call `keras.utils.set_random_seed`, and run the cells in the same order. |
| The first run of the notebook takes more than 3 minutes | It computes the features of 960 clips in Python | Wait for it. The file `features.npz` makes the next run fast. |