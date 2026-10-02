# Day 6 lab: pruning, distillation, and model selection

Hardware status: no board is necessary. The notebook ran on the work computer of the course (prepared on 2026-10-02)

**Goal.** Your group has a trade-off curve for one task, and a model
selection for the two boards of the course.

**Deliverable.** The plot `tradeoff.png` with at least six models, and the
file `report.md` with your selection and the Decision Log.

**Time.** 20 minutes for the quiz, 130 minutes of work, then 30 minutes for
the check by the instructor.

| Part | Content | Time |
|---|---|---|
| Quiz | The quiz of Week 1 | 20 min |
| A | Pruning: prune a CNN at several sparsity levels and fine-tune it | 45 min |
| B | Distillation: distill a teacher model into a smaller student model | 45 min |
| C | Selection: quantize the best candidates, plot the accuracy against the size and against the latency, select one model for each board | 40 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| Laptop | 1 | No board is necessary. Use spare time for the hardware labs of Week 1. |

## Software

| Tool | Version | Note |
|---|---|---|
| Python | 3.10 or later | The notebook ran with Python 3.10.12 |
| `tensorflow-cpu`, `ai-edge-litert`, `numpy`, `matplotlib`, `jupyterlab` | see `Labs/VERSIONS.md` | Installed on Days 1 and 3. `Labs/requirements.txt` has the list. |

The lab needs no new package.

The first run of the notebook downloads the dataset Fashion-MNIST: about
30 MB. The notebook stores it in the folder `.keras/datasets/` of your home
folder.

Run all commands of this lab from the folder `Labs/day06/`.

## Files

| File | Content |
|---|---|
| `compression.ipynb` | Parts A, B, and C. The student notebook. It has seven tasks. |
| `models/baseline.keras` | The trained CNN of the lecture: 16, 32, and 64 filters, 23 946 parameters |
| `models/teacher.keras` | The trained teacher: 32, 64, and 128 filters, 93 962 parameters |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/` | The notebook with all tasks complete and with its output, and an example report |
| `TEST_NOTES.md` | The code status and the checklist for the instructor |

The notebook writes the file `tradeoff.png` into this folder.

## Steps

Write each result in `report.md` when you get it.

### Quiz (20 min)

The instructor gives the quiz of Week 1. Close the laptop for the quiz.

### Part A: pruning (45 min)

1. **Start (5 min).** Start Jupyter and run section 0 of the notebook:

   ```bash
   ../../.venv/bin/jupyter lab compression.ipynb
   ```

   You see the versions, the size of the dataset, and the two trained
   models with their accuracy. Then you see the four numbers of the
   baseline: the file size, the accuracy, the latency on your laptop, and
   the peak of the activations. Write them in the report.

2. **Task 1: the magnitude mask (10 min).** Complete the function
   `magnitude_mask` in section 1.

   You see: `Task 1: complete`, and the threshold for a sparsity of 0.5
   and of 0.8.

3. **Task 2: unstructured pruning (15 min).** Write your prediction in
   section 2 before you run the experiment. Then run it. The experiment
   prunes the baseline to a sparsity of 50, 70, 80, and 90 percent, and it
   fine-tunes each model for 2 epochs. It needs about one minute.

   Write the table in the report.

4. **Task 3: structured pruning (10 min).** Complete the function
   `filter_scores` in section 3. Then the experiment removes a quarter, a
   half, and three quarters of the filters.

   You see: `Task 3: complete`, and one row for each model. Write the table
   in the report.

5. **Compare (5 min).** Answer the three questions of section 4 in the
   report.

### Part B: knowledge distillation (45 min)

1. **Task 4: soft targets (10 min).** Complete the function `soft_targets`
   in section 5.

   You see: `Task 4: complete`, and the soft targets of the teacher for one
   test image at three temperatures. Write in the report which classes get
   a probability above 0.05 at a temperature of 4.

2. **Task 5: the loss (10 min).** Write the three lines of the soft part of
   the function `distillation_loss` in section 6.

   You see: `Task 5: complete`, and two values that agree with the expected
   values.

3. **Task 6: train the student (20 min).** Write your prediction in section
   7 before you run the experiment. Then run it. The experiment trains the
   student four times. It needs about three minutes.

   Write the four accuracy values and the two gains in the report.

4. **Questions (5 min).** Answer the three questions at the end of section
   7 in the report.

### Part C: selection (40 min)

1. **Quantize (10 min).** Run section 8. It converts each candidate to a
   `float32` file and to an `int8` file, and it measures each file. It
   needs about one minute.

   Write the table in the report.

2. **The plot (10 min).** Run section 9. It writes the file `tradeoff.png`.
   Mark in the report the models on the upper left border of each plot.

3. **Task 7: select (15 min).** Read the two budgets in section 10. Write
   your selection in the cell of task 7, and run the check.

   You see, for each product: the numbers of your file, if it meets the
   budget, and if a better file exists. The target is `Task 7: complete`.

4. **Decision Log (5 min).** Write the Decision Log in the report.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] The notebook prints `complete` for tasks 1, 3, 4, 5, and 7.
- [ ] The report has the two predictions: task 2 and task 6. The predictions
      were written before the experiments.
- [ ] The plot `tradeoff.png` has at least six models.
- [ ] The report names one model for the XIAO ESP32S3 and one model for the
      Raspberry Pi 5, with the numbers of each model.
- [ ] The selection states the constraint that decides for each product.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: which model do you select for the XIAO ESP32S3, and
which model for the Raspberry Pi 5? Use the budgets of section 10 of the
notebook. Name the constraint that decides for each product, and say what
the product loses with your selection.

## If a part does not work

| Problem | Fallback |
|---|---|
| The download of the dataset fails | The instructor gives the folder `fashion-mnist` on a USB drive. Copy it into the folder `.keras/datasets/` of your home folder. |
| A task is not complete in time | Copy the function from `solutions/compression.ipynb`, and write this in the report. Each experiment needs its task. |
| The experiments are too slow on your laptop | Work with a second group on one laptop, or use the tables of `solutions/compression.ipynb` and write this in the report. The selection of Part C is still your work. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The notebook prints `No module named 'tensorflow'` | Jupyter does not use the virtual environment | Start Jupyter with `../../.venv/bin/jupyter lab` |
| The first cell stops with a download error | No connection to the internet | See the fallback for the dataset |
| An experiment prints `Task ... is not complete. The experiment does not run.` | The check of the task before it failed | Complete the task, run its check cell again, then run the experiment |
| `Task 1: not complete` after your change | The mask has a wrong type, or it uses `>=` | The mask is `float32`. A weight stays only if its magnitude is above the threshold. |
| `Task 5: not complete`, and the first value is not 0 | The student or the teacher is not divided by `T`, or the softmax is missing | Use `ops.softmax(z_teacher / T)` and `ops.log_softmax(z_student / T)` |
| Section 8 has fewer than six models | An experiment of Part A or Part B did not run | Complete tasks 1, 3, and 5, and run the three experiments again |
| The latency values change from run to run | Other programs use the processor | Close other programs. Differences of some microseconds are noise. |
| `Task 7: not complete` | The file does not meet the budget, a better file exists, or a field still has `?` | Read the two lines that the check prints for each product |

## Credits

This lab adapts material from these sources:

- Chapter 10 "Model Compression" of "Machine Learning Systems" by Vijay
  Janapa Reddi and contributors (mlsysbook.ai, CC BY-NC-SA 4.0): magnitude
  pruning, structured pruning, knowledge distillation with soft targets and
  a temperature, and the selection of a technique from a constraint.
- The repository EdgeML-with-Raspberry-Pi by Marcelo Rovai
  (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0): the method of its
  distillation script for MNIST. The teacher runs one time over the training
  set, and the loss has a hard part and a soft part.
- The dataset Fashion-MNIST by Zalando Research (MIT licence). The notebook
  downloads it. It is not in this repository.

The notebook, the two trained models, the experiments, and the selection
task are new work of this course.
