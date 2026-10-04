# Test notes: Day 6 lab

This lab needs no board. So this file has no hardware test. Part 1 gives the
code status. Part 2 is the checklist for the instructor on a lab laptop.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `compression.ipynb`, `solutions/compression.ipynb` | new | The methods come from chapter 10 of "Machine Learning Systems". The method of the distillation follows the script `kd_mnist.py` of EdgeML-with-Raspberry-Pi. | Tested on the work computer. They need no board. |
| `models/baseline.keras` | new | A training of this course: 16, 32, and 64 filters, 20 epochs, Fashion-MNIST | 23 946 parameters, 89.1 percent on the test set |
| `models/teacher.keras` | new | A training of this course: 32, 64, and 128 filters, 20 epochs, Fashion-MNIST | 93 962 parameters, 90.3 percent on the test set |

Notebook check (work computer, 2026-10-02, Python 3.10.12, `tensorflow-cpu`
2.21.0, `keras` 3.12.4, `ai-edge-litert` 2.2.0, `numpy` 2.2.6):

| Notebook | Result | Run time |
|---|---|---|
| `compression.ipynb` (student version) | Runs from the first cell to the last cell with no error. It prints `not complete` for tasks 1, 3, 4, 5, and 7. The three experiments do not run. The plot has one model. | about 17 s |
| `solutions/compression.ipynb` | Runs from the first cell to the last cell with no error. It prints `complete` for tasks 1, 3, 4, 5, and 7. The plot has 7 models. | about 275 s |

Results of the solution notebook. The accuracy values and the file sizes are
the same in each run. The latency is the latency of the work computer with
one thread. It changes by some microseconds between two runs:

- Unstructured pruning with a sparsity of 50, 70, 80, and 90 percent: 90.0,
  88.8, 85.7, and 76.4 percent after 2 epochs of fine-tuning. The file has
  99 320 bytes for each sparsity.
- Structured pruning to 12-24-48, 8-16-32, and 4-8-16 filters: 88.8, 85.6,
  and 76.2 percent, with files of 58 104, 28 408, and 10 232 bytes.
- The student with 6218 parameters: 76.5 percent with 1000 labels, 78.8
  percent with distillation on the same images, 85.1 percent with the
  outputs of the teacher for 60 000 images with no label, and 87.1 percent
  with all labels.
- The `int8` files: 31 280 bytes for the baseline, 20 216 bytes for
  12-24-48, 12 040 bytes for 8-16-32, and 6736 bytes for 4-8-16.
- The selection of the solution: the student with all labels in `int8` for
  the XIAO ESP32S3 (12 040 bytes, peak 7840 bytes, 87.3 percent), and the
  model with 12-24-48 filters in `float32` for the Raspberry Pi 5 (88.8
  percent).

Points that the instructor must know:

- The numbers above agree with the numbers of the Day 6 lecture. The lecture
  and the lab use the same baseline model and the same code.
- The results of the distillation are for one seed. With three seeds, the
  gain of run 2 against run 1 is 1.5 points (the lecture gives this mean
  value). The notebook shows 2.3 points for its seed.
- With all 60 000 labels, distillation gives no clear gain for this small
  student. The lab does not have this run. The lecture shows the result.
- On the work computer, the `int8` files are slower than the `float32`
  files. This is a property of the kernels for this processor. On the
  Raspberry Pi the result can be different. Day 9 measures it.
- The two budgets of section 10 are example budgets of this lab. They are
  not limits of the real boards: each model of this lab fits the two boards.
- The check of task 7 accepts each file that meets the budget when no file
  is clearly better. For the Raspberry Pi 5, the baseline in `float32` and
  the model with 12-24-48 filters in `float32` can pass, because their
  latency values are close.
- The notebooks come from one generator script of the course repository
  (`tools/notebooks/build_day06_compression.py`). Change the script, not the
  two notebooks.

## 2. Checklist for the instructor

Run the solution notebook on one lab laptop before the lab. Record the
result here.

- Date of the test: YYYY-MM-DD
- Laptop (processor, RAM):
- Tool versions: see `Labs/VERSIONS.md`

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run section 0 with no dataset in the home folder | Does the download work in the classroom network? The time. | |
| 2 | Run the complete solution notebook | The run time. The lab plan needs less than 15 minutes. | |
| 3 | Compare the tables with `solutions/compression.ipynb` | Are the accuracy values and the file sizes equal? | |
| 4 | Read the latency column of section 8 | Is `int8` slower or faster than `float32` on this laptop? | |
| 5 | Run the student notebook with no change | Does it print `not complete` for tasks 1, 3, 4, 5, and 7? | |
| 6 | Copy the folder `fashion-mnist` of `.keras/datasets/` to a USB drive | The fallback for a group with no download | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| Quiz | 20 min | |
| A | 45 min | |
| B | 45 min | |
| C | 40 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. If the notebook needs more than 15 minutes on a lab laptop, decrease the
   number of epochs of runs 3 and 4 in the generator script.
2. If a table of the solution is different on the lab laptop, write the
   difference here. The accuracy can change with a different version of
   TensorFlow.
3. After the hardware test of Day 9, write in the README of this lab which
   format is faster on the Raspberry Pi.
