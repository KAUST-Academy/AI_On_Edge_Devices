# Test notes: MC-5 lab

The lab needs no board. These notes are for the instructor, and for a
session that changes the notebook or the figures.

## 1. Code status

| Item | Status |
|---|---|
| `host/get_keywords.py` | Runs, downloads 139 MB, writes 960 clips |
| `mfcc_training.ipynb` | Runs from the first cell to the last cell on a laptop CPU |
| `solutions/mfcc_training.ipynb` | Runs, and its output is stored |
| Sketch | none |
| Hardware | none, so "not tested on hardware" does not apply |

Numbers of one run of the solution notebook on the work computer
(TensorFlow 2.21.0, Keras 3.15.1, numpy 2.5.3, Python 3.13.11, an x86
processor with AVX2). The accuracies say nothing about a board. The split
of the clips is random, so a clip of one speaker can be in both the
training set and the test set.

| Input | Values per clip | Parameters | Test accuracy |
|---|---|---|---|
| raw audio | 16000 | 513380 | 52.6 percent |
| log Mel spectrogram | 1600 | 4532 | 72.9 percent |
| cepstral coefficients | 650 | 3620 | 77.1 percent |

Other values of the same run:

| Item | Value |
|---|---|
| Clips of the dataset | 960, 240 of each class |
| Training clips, test clips | 768, 192 |
| Frames per clip | 50 |
| Values per clip of the cepstrum | 650 |
| Time to compute the features of 960 clips | 2.4 s |
| Parameters of the convolution 1 | 3 * 13 * 16 + 16 = 640 |
| Parameters of the convolution 2 | 3 * 16 * 32 + 32 = 1568 |
| Parameters of the dense layer | 11 * 32 * 4 + 4 = 1412 |
| Frames after the two convolutions and the two pooling layers | 11 |

## 2. Checklist for the instructor

Run the solution notebook on one lab laptop before the lab.

- Date of the test: YYYY-MM-DD
- Laptop (processor, RAM):
- Tool versions: see `Labs/VERSIONS.md`

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run `python3 host/get_keywords.py` in a clean copy of the lab folder | Does the download work on the network of the room? The time. Does it write 960 clips? | |
| 2 | Run the complete solution notebook | The run time of the first run, and the run time of the second run with the file `features.npz`. | |
| 3 | Compare the table of section 10 with the table above | Are the values, the parameters, and the accuracies equal? | |
| 4 | Read the checks of tasks 1 and 2 | Does the check of task 1 give a peak of the first filter at bin 2 and of the last one at bin 236? | |
| 5 | Run the student notebook with no change | Does it print `not complete` for tasks 1, 2, 3, and 4? Does it run to the last cell? | |
| 6 | Delete `features.npz` and run the solution notebook again | Are the numbers the same? | |
| 7 | Build the deck of the module after a change of the notebook | The build gives `BUILD OK`, 0 frames with too much content, and 0 items wider than their box. | |
| 8 | Change a number in the notebook | The figures of the deck come from the file `results.json` that the notebook writes. Do the figures and the frames of the deck show the new number? | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. If the accuracy of the cepstrum is below 70 percent on a lab laptop,
   check the number of clips that section 1 prints. It must be 960, with 240
   of each class.
2. If the download fails on the network of the room, copy the folder
   `keywords/` of one group to a USB drive before the lab, and write this
   in the README of the lab.
3. The frames of the deck that show these numbers are:
   - `LaTeX/sections/modules/MC-5/content.tex`, the frame "What each step
     does to the number of values";
   - the same file, the frame "The cepstrum against the spectrogram";
   - the frame "The cepstrum against the spectrogram" also gives the two
     ratios of 25 and 142;
   - `LaTeX/sections/modules/MC-5/lab.tex`, the frames of Parts A, B, C,
     and D.
   Correct them in the same commit when a number changes.
4. The audio pipeline of the course gives 49 frames for a clip of 1 s at
   16 kHz with frames of 20 ms. This module uses the formula
   $1 + (N - L) / S$, which gives 50 frames for the same settings. Both
   counts are used in the course. The numbers of this module are
   self-consistent, and the module names no frame of a core day.