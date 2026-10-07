# Decision Log and lab check

Each lab of Days 1 to 13 ends with a lab check of 30 minutes. Your group
shows the result to the instructor and hands in a report with a Decision
Log. The daily labs are 40 percent of the course grade.

This file gives the form of the Decision Log, the rubric, three examples,
and the check sheet that the instructor uses.

## 1. The lab check

1. Complete `report.md` of the lab folder before the check starts. The
   report has your predictions, your measured values, and the Decision Log.
2. Keep the hardware connected and the programs ready. The instructor asks
   for the live demonstration that the section "Check criterion" of the lab
   `README.md` names.
3. The instructor marks each check criterion as met or not met.
4. The instructor reads the Decision Log and asks one question about it.
   Each student of the group must be able to answer.
5. Hand in `report.md`. The instructor says on Day 1 how you hand it in.

If a lab is replaced by a backup module, the check uses the check criterion
of the module `README.md`.

Days 14 and 15 are the capstone. The capstone has its own rubric: see
`Docs/capstone.md`.

## 2. Prediction before measurement

Each report has places for a prediction. Write the number that you expect
before you measure. Then measure, and write one sentence for each prediction
that was wrong.

- A prediction is a number with a unit, not a word. Write "about 40 ms",
  not "fast".
- A wrong prediction costs no points. A prediction that you wrote after the
  measurement does: the criterion is then not met.
- The difference between the prediction and the result is often the best
  subject for the Decision Log.

## 3. The Decision Log

A Decision Log is a text of about 100 words. You state one design decision,
you give your measured numbers, and you name the trade-off. Each lab gives
the question. The section "Decision Log" of `report.md` has the place for
your text.

### Form

Write these five items in this order. One or two sentences for each item
are enough.

| Item | Content | A possible start of the sentence |
|---|---|---|
| Decision | The option that you select. One decision only. | "We select ..." |
| Options | The other options that you compared. | "The other options were ..." |
| Numbers | The measured numbers of each option, with their units. | "We measured ..." |
| Trade-off | What you gain and what you pay, with a number for each side. | "The trade-off: ..." |
| Condition | The condition that would change the decision. | "We would change the decision if ..." |

### Rules

- Use your own numbers from your report. Give each number with its unit.
- Mark a number that you did not measure as "estimate", and name its
  source.
- Name the budget that decides: flash, RAM, latency, energy, accuracy, or
  cost.
- For a time, give the method: the number of runs and the statistic (see
  Day 9).
- Do not repeat all results of the lab. Select the numbers that the
  decision needs.
- Write full sentences. A table of numbers is not a Decision Log.

### Template

Copy this form if you write a Decision Log outside a lab report, for example
in the capstone report.

```markdown
## Decision Log: <subject of the decision>

Question: <the question that the decision answers>

<About 100 words. The decision. The other options. The measured numbers of
each option, with units. The trade-off: what you gain and what you pay. The
condition that would change the decision.>
```

## 4. Rubric

The instructor asks three questions about each Decision Log.

| Question | 2 points | 1 point | 0 points |
|---|---|---|---|
| Numbers: does the text give measured numbers? | Three or more numbers from your measurements, each with its unit. | One or two numbers. | No number. Only words such as "smaller" or "faster". |
| Cause: does the text explain why? | It names the budget or the mechanism that decides, and it connects the numbers to it. | It says what occurred, but not why. | A list of observations with no explanation. |
| Trade-off: does the text say what you give up? | It names what you gain and what you pay, with a number for each side. | It names a cost or a limit, with no number. | No trade-off. |

### Points of one lab check

One lab check gives 10 points.

| Part | Points | Rule |
|---|---|---|
| Check criteria of the lab `README.md`, without the line of the Decision Log | 4 | All criteria met: 4. One criterion not met: 3. Two not met: 2. Three or more not met: 1. No demonstration and no report: 0. |
| Decision Log | 6 | The three questions of the rubric, 0 to 2 points each. |

The 13 labs have the same weight. These points are a proposal. The
instructor confirms the points on Day 1.

## 5. Three examples

The three texts answer the question of the Day 1 lab: "You must classify
images of 96 x 96 pixels on the XIAOML Kit. Which of the three models do you
select, in which data type, and with PSRAM or with no PSRAM? Which budget
decides?" The numbers come from the example report of that lab,
`Labs/day01/solutions/report_example.md`.

### Example with 6 points

> We select the small depthwise CNN in `int8` on the XIAO with no PSRAM. Its
> model size is 13.9 KB and its peak activation memory is 108.0 KB. The
> budget of the board is 3.2 MB of flash and 298.7 KB of RAM, so the RAM
> budget decides, and the model uses about one third of it. In `float32` the
> peak is 432.0 KB, which does not fit with no PSRAM. MobileNetV2 in `int8`
> needs 3.3 MB of flash and 1.4 MB of RAM. It does not fit the flash, and it
> needs the PSRAM. The trade-off: the small model has less capacity, so its
> accuracy is lower, but it leaves the PSRAM free for the camera image. We
> measure the accuracy and the latency on Day 5.

| Question | Points | Reason |
|---|---|---|
| Numbers | 2 | Seven numbers with units, for the selected model and for two other options. |
| Cause | 2 | The text names the RAM budget as the budget that decides, and it compares each peak with that budget. |
| Trade-off | 2 | The text names the gain (free PSRAM, the model fits) and the cost (less capacity). It says when the group measures the cost. |

### Example with 3 points

> We select the small depthwise CNN in `int8`. Its model size is 13.9 KB and
> its peak activation memory is 108.0 KB. The board has 3.2 MB of flash and
> 298.7 KB of RAM with no PSRAM, so the model fits. MobileNetV2 and ResNet-18
> are larger and do not fit.

| Question | Points | Reason |
|---|---|---|
| Numbers | 2 | Four numbers with units. |
| Cause | 1 | The text says that the model fits. It does not say which budget decides, and it gives no number for the other models. |
| Trade-off | 0 | The text does not say what the group gives up with the small model. |

### Example with 0 points

> We select the small CNN because it is the smallest and the fastest model.
> It fits the board with no problem. The other models are too large for a
> microcontroller.

| Question | Points | Reason |
|---|---|---|
| Numbers | 0 | No number. |
| Cause | 0 | "Too large" names no budget: flash or RAM? |
| Trade-off | 0 | No trade-off. |

## 6. The decision of each lab

The lab `README.md` has the complete question and the complete check
criterion. This table shows the subject of each Decision Log and the
results of your report that the text must use.

| Day | Lab | Check criteria | Decision | Results to use |
|---|---|---|---|---|
| 1 | Toolchain, sensor tests, and model budgets | 6 | The model, the data type, and the PSRAM setting for images on the XIAOML Kit | The table "model and device" and the memory values of the board |
| 2 | MicroPython, sensor input, and a motion dataset | 9 | More recordings in the same sessions, or a new session with a different person | The two results of the leakage experiment |
| 3 | From a trained model to the microcontroller | 7 | Your sketch with TensorFlow Lite Micro, or the library of Edge Impulse | The comparison table: flash, RAM, latency |
| 4 | Quantization | 6 | The `float32` model or the `int8` model on the board | The comparison table: flash, arena, latency, accuracy |
| 5 | Audio and vision on the microcontroller | 7 | The post-processing settings of the keyword stage, and one board for two stages | The tuning table and the measurement table |
| 6 | Pruning, distillation, and model selection | 6 | One model for the XIAO ESP32S3 and one model for the Raspberry Pi 5 | The plot and the budgets of the notebook |
| 7 | Inference runtimes on the Raspberry Pi | 7 | The runtime, the precision, and the thread count for 10 images each second | The latency table |
| 8 | Object detection on the Raspberry Pi | 7 | The runtime, the image size, and the precision for 10 frames each second | The frame-rate table and the mAP of each file |
| 9 | One benchmark report for two boards | 8 | The board, the precision, the runtime, and the threads for two products | The benchmark report, each number with its method |
| 10 | Small language models on the Raspberry Pi | 5 | The model, the quantization level, the context, and k for an offline assistant | The benchmark table and the table of Part C |
| 11 | Inference on a network video stream | 4 | The place of the detector and the stream settings for a people counter | The latency of the two settings, the bit rate, the frame rate |
| 12 | Local decisions and MQTT | 5 | The decisions that stay on the device, the messages, the QoS, and the queue size | The times of Part C and the values of the link cut in Part D |
| 13 | A monitored inference application | 5 | The metrics, the storage, and the alert rules for 20 cameras | The reference values, the threshold, and the alert times |

The column "Check criteria" gives the number of lines in the section "Check
criterion" of the lab `README.md`. The last line is the line of the Decision
Log.

## 7. Lab check sheet

The instructor uses one sheet for each group and each day. Print this
section, or copy it into a file.

Day: ......  Group: ......  Date: ......

Names: ............................................................

Check criteria. Write the criteria of the lab `README.md` in their order,
without the line of the Decision Log.

| No. | Criterion (short) | Met (yes or no) | Note |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |

Decision Log.

| Question | Points (0, 1, or 2) | Note |
|---|---|---|
| Numbers | | |
| Cause | | |
| Trade-off | | |

Result.

| Item | Value |
|---|---|
| Predictions written before the measurement (yes or no) | |
| Question of the instructor, and the student who answered | |
| Points for the check criteria (0 to 4) | |
| Points for the Decision Log (0 to 6) | |
| Total (0 to 10) | |

## 8. Course record

The instructor writes the total of each lab check in this table. Add one
row for each group.

| Group | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 | Sum (of 130) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g01 | | | | | | | | | | | | | | |
| g02 | | | | | | | | | | | | | | |
| g03 | | | | | | | | | | | | | | |


