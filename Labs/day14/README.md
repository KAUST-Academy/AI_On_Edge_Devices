# Day 14 lab: capstone proposal and start of the build

Hardware status: not tested on hardware (prepared on 2026-10-03)

**Goal.** Your team writes a one-page proposal for the capstone system,
presents it in a design review, and starts the build with a first test of
its riskiest assumption.

**Deliverable.** The approved proposal (`proposal.md`) and the file
`report.md` with the budgets, the result of the review, the result of the
first test, and the Decision Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Teams: form the team and select a problem | 20 min |
| B | Proposal: requirements, boards, model, data, metrics, budgets | 50 min |
| C | Design review with the instructor | 40 min |
| D | Build: the first test of the riskiest assumption | 40 min |

`Docs/capstone.md` is the capstone brief: the five requirements, the
rubric, the review questions, and four example projects. Read it before
Part A.

## Hardware

| Item | Number for each team | Note |
|---|---|---|
| XIAOML Kit | 2 (one for each lab group) | With a USB-C cable |
| Raspberry Pi 5 with the active cooler and the camera | 2 (one for each lab group) | With the microSD card of the course |
| Power supply for the Raspberry Pi 5 | 2 | 27 W, USB-C |
| Laptop | 2 or more | In the lab network |
| The router of the lab | 1 for the class | Wi-Fi `edgeai-lab` |

Parts A to C need no board. Part D uses the boards that the first test
needs. A team is two lab groups (three or four students).

## Software

| Tool | Version | Note |
|---|---|---|
| Python | 3.8 or later | `budget.py` uses the standard library only |
| The lab folders of Days 1 to 13 | this repository | The first test reuses one of them |
| A Markdown editor | any | For `proposal.md` and `report.md` |

## Files

| File | Content |
|---|---|
| `proposal.md` | The proposal template. Copy it, fill it, hand it in. |
| `report.md` | The report of today. Fill it during the lab. |
| `budget.py` | Part B. Calculates the budgets: fit, latency, power, data, cost |
| `review_sheet.md` | Part C. The sheet of the instructor. Read it to prepare. |
| `solutions/proposal_example.md` | An example proposal (machine monitor, Example A of the brief) |
| `solutions/report_example.md` | The example report that goes with it |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

## Steps

Write each result in `report.md` when you get it.

### Part A: teams (20 min)

1. **Form the team (5 min).** Join with a second lab group. Write the names
   and the two group names in `proposal.md` and `report.md`.
2. **Select a problem (10 min).** Read Sections 2 and 7 of
   `Docs/capstone.md`. Select one of the four example projects, change one,
   or write your own problem. Write the problem, not a solution: "detect a
   failing bearing", not "run YOLO on a camera".
3. **Name the riskiest assumption (5 min).** Which part of the system has
   the largest chance to fail? Write it in `report.md`. Part D tests it.

### Part B: proposal (50 min)

1. **Problem and requirements (15 min).** Fill the first two sections of
   `proposal.md`. Each requirement has a number and a test, as in Day 14,
   Part 3 of the lecture.
2. **Boards, model, and data (15 min).** Write the split of the work
   between the XIAO and the Raspberry Pi, the model and its optimization,
   and the data: source, size, labels, and the split by session.
3. **Budgets (15 min).** Calculate the budgets with `budget.py`. Each
   command prints its result. Examples with the values of the lecture:

   ```bash
   python3 budget.py fit --flash-kb 3264 --ram-kb 298.68 --program-kb 300 \
       --params 1534 --bits 8 --peak-values 1028
   python3 budget.py latency window=2000 model=100 decision=400 mqtt=100 \
       --limit-ms 3000
   python3 budget.py power --work-mw 217 --rest-mw 19 --work-ms 50 \
       --period-ms 2000 --radio-mw 290.4 --radio-s-per-hour 3 \
       --battery-mah 1000 --days 30
   python3 budget.py data --bytes 147 --per-second 50
   python3 budget.py cost kit=40 pi=80 camera=25 other=40 --sites 100 \
       --spares 0.15
   ```

   Use your own values. Name the source of each input value in the
   proposal: a lab result, a data sheet, or "estimate".
4. **The five requirements (5 min).** Write one line for each requirement
   of the brief. If one requirement is not met, change the design now.

### Part C: design review (40 min)

The instructor reviews each team for about 8 minutes, with
`review_sheet.md`. The instructor gives the order.

1. **Prepare (while you wait).** Prepare an answer with a number for each
   of the seven review questions of `Docs/capstone.md`, Section 5. Then
   prepare the first test of Part D.
2. **Present (3 min).** The problem, the split of the work, the budgets, and
   the riskiest assumption.
3. **Answer the questions (5 min).** Answer with numbers. Write the result,
   the changes, and the weak points in `report.md`.
4. **Change the proposal.** Make the changes that the instructor asked for
   before Part D.

### Part D: build (40 min)

1. **Plan the test (5 min).** Write the test of the riskiest assumption:
   which board, which lab folder, which data, which number decides.
2. **Run the test (30 min).** Reuse the lab folder of the day that the test
   needs. Examples: record two sessions with the Day 2 logger and train the
   Day 3 model; run the Day 8 detector on the scene of your system; count
   the false starts of the Day 5 keyword model for 5 minutes.
3. **Decide and plan (5 min).** Write the result with numbers, the
   decision, and the plan for Day 15 with a time for each step.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] The proposal meets the five capstone requirements of
      `Docs/capstone.md`, Section 2.
- [ ] Each requirement of the proposal has a number and a test.
- [ ] Each budget has a value and a source, and each guess is marked as an
      estimate.
- [ ] The review sheet says "approved" or "approved with changes", and the
      proposal has the changes.
- [ ] `report.md` has the result of the first test and a plan for Day 15.

## Decision Log

Write about 100 words. State one design decision, give your numbers, and
name the trade-off.

Question of this lab: how do you split the work between the XIAO and the
Raspberry Pi in your system? Which budget numbers decided the split, and
what did you give up?

## Expected values

`budget.py` gives these values for the examples of Part B, step 3. They are
the values of Day 14, Part 3 of the lecture.

| Command | Main result |
|---|---|
| `fit` | Fits: flash 308 734 of 3 342 336 bytes, RAM 1028 of 305 848 bytes |
| `latency` | 2600 ms, margin 400 ms |
| `power` | 24.192 mW, 6.4 days; 30 days need 17.42 Wh (4708 mAh) |
| `data` | 7350 bytes each second, 19.051 GB in 30 days |
| `cost` | One site 185, 115 sets 21 275 |

The values of your system are different. The proposal of the example
project A is in `solutions/proposal_example.md`.

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The idea needs more than one new part | The scope is too large for 4 hours of build | Keep one new part. Reuse the labs for the rest. |
| No data source | The model needs data that the team cannot record in the room | Select a task with data that you can record today, or a dataset of a lab |
| Requirement 3 is not met | The decision needs the instructor broker or the internet | Move the decision to the XIAO or the Raspberry Pi |
| A budget has no source | The value is a guess | Write "estimate", and measure it in Part D or on Day 15 |
| `budget.py` says `is not name=value` | A space around `=` | Write `window=2000`, with no space |
| The first test needs more than 30 minutes | The test is too large | Test only the assumption, with the smallest data that shows it |

## Credits

This lab adapts material from these sources:

- "Machine Learning Systems" by Vijay Janapa Reddi and contributors
  (mlsysbook.ai, CC BY-NC-SA 4.0), the instructor guide (`instructors/assessment.qmd`):
  the Decision Log and its rubric, through `Docs/capstone.md`.
- "XIAO: Big Power, Small Board" by Lei Feng and Marcelo Rovai
  (github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook, GPL-3.0),
  chapter 2.1: the prototype design process, through Day 14, Part 3 of the
  lecture.
- The labs of Days 1 to 13 of this course and Day 14, Part 3 of the lecture:
  the budgets and the example project. `budget.py` is new code of this
  course.
