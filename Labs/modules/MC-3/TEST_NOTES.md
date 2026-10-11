# Test notes: MC-3 lab

The lab needs no board. These notes are for the instructor, and for a
session that changes the notebook or the figures.

## 1. Code status

| Item | Status |
|---|---|
| `spectral_features.ipynb` | Runs from the first cell to the last cell on a laptop CPU |
| `solutions/spectral_features.ipynb` | Runs, and its output is stored |
| `host/motion_sim.py` | Runs, imported by the notebook and by `host/make_dataset.py` |
| `host/make_dataset.py` | Runs, writes 48 files |
| Sketch | none |
| Hardware | none, so "not tested on hardware" does not apply |



| Input | Values | Parameters | Test accuracy |
|---|---|---|---|
| raw window | 300 | 6274 | 58.5 percent |
| time-domain features | 9 | 454 | 100.0 percent |
| spectral features, FFT 128 | 201 | 4294 | 98.8 percent |
| spectral features, FFT 32 | 57 | 1414 | 99.2 percent |
| spectral features, FFT 64 | 105 | 2374 | 100.0 percent |

## 2. Checklist for the instructor

Run the solution notebook on one lab laptop before the lab.

- Date of the test: YYYY-MM-DD
- Laptop (processor, RAM):
- Tool versions: see `Labs/VERSIONS.md`

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run `python3 host/make_dataset.py` in a clean copy of the lab folder | Does it write 48 files? The time. | |
| 2 | Run the complete solution notebook | The run time. The lab plan is 45 minutes, so the notebook must run in less than 10 minutes. | |
| 3 | Compare the table of section 8 with the table above | Are the values and the accuracies equal? | |
| 4 | Read the plot of section 3 | Does the power of `lift` sit in a different bin from the power of `maritime`? | |
| 5 | Run the student notebook with no change | Does it print `not complete` for tasks 1, 2, 3, and 4? Does it run to the last cell? | |
| 6 | Put three recordings of your group into `data/` and run the notebook again | Does the notebook read `data/` and skip the fallback dataset? | |
| 7 | Build the deck of the module after a change of the notebook | The build gives `BUILD OK`, 0 frames with too much content, and 0 items wider than their box. | |
| 8 | Change a number in the notebook | The figures of the deck come from the file `results.json` that the notebook writes. Do the figures and the frames of the deck show the new number? | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. If the accuracy of the raw window is above 90 percent on a lab laptop,
   the student version of the dataset is not the one of the report. Check
   the number of training windows in section 1.
2. If a table of the solution differs on the lab laptop, write the
   difference here. The accuracy can change with a different version of
   TensorFlow, and the model has 4294 parameters, so a small change is
   possible.
3. The frames of the deck that show these numbers are:
   - `LaTeX/sections/modules/MC-3/content.tex`, frame "The choice of the FFT
     length": the columns "Values, 3 axes" and "Parameters";
   - the same file, frame "What the module measures";
   - `LaTeX/sections/modules/MC-3/lab.tex`, the frames of Parts C and D.
   Correct them in the same commit when a number changes.