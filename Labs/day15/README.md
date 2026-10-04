# Day 15 lab: capstone build and demonstrations

Hardware status: not tested on hardware (prepared on 2026-10-03)

**Goal.** Your team completes the capstone system, measures it, shows it
in a demonstration of 10 minutes, and submits the report.

**Deliverable.** The demonstration and the report (`report.md`).

**Time.** 180 minutes. The lecture time after Part 1 (Parts 2 and 3, 100
minutes) is also build time.

| Part | Content | Time |
|---|---|---|
| A | Build: complete the system and the measurements | 80 min |
| B | Demonstrations: 10 minutes for each team | 70 min |
| C | Close: submit the report, give course feedback | 30 min |

`Docs/capstone.md` is the capstone brief: the five requirements, the
rubric, and the report. The instructor publishes the order of the
demonstrations on Day 14.

## Hardware

| Item | Number for each team | Note |
|---|---|---|
| XIAOML Kit | 2 (one for each lab group) | With a USB-C cable |
| Raspberry Pi 5 with the active cooler and the camera | 2 (one for each lab group) | With the microSD card of the course |
| Power supply for the Raspberry Pi 5 | 2 | 27 W, USB-C |
| Laptop | 2 or more | In the lab network |
| USB power meter | optional | For the energy of the benchmark table (Day 9) |
| Spare boards | for the class | The instructor keeps them ready |

## Software

| Tool | Version | Note |
|---|---|---|
| The lab folders of Days 1 to 14 | this repository | Your system reuses them |
| Python | 3.8 or later | `schedule.py` uses the standard library only (instructor) |
| A Markdown editor | any | For `report.md` |

## Files

| File | Content |
|---|---|
| `report.md` | The capstone report template. Fill it, hand it in. |
| `feedback.md` | The course feedback form, with no name |
| `schedule.py` | For the instructor: the order of the demonstrations |
| `solutions/report_example.md` | An example report (machine monitor, Example A of the brief) |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

## Steps

### Before Part A: the lecture time (100 min)

Build the system with the plan of your Day 14 report. The instructor visits
each team. Build the parts that the demonstration needs first.

### Part A: build and measure (80 min)

1. **Complete the system (40 min).** Connect the parts. Test each
   requirement of your proposal once.
2. **Measure (30 min).** Fill the benchmark table of `report.md` with the
   method of Day 9: warm-up runs, a fixed number of runs, the window of the
   time, and the statistic. Measure the size and the accuracy of the model
   before and after the optimization on the same test set.
3. **Rehearse (10 min).** Run the demonstration once with the clock: the
   live system, the cut of the network link, the dashboard. Prepare plan B:
   a recorded input or a short video of the working system.

### Part B: demonstrations (70 min)

Each team has 10 minutes:

| Time | Content |
|---|---|
| 1 min | The problem and the requirements |
| 4 min | The system works: live, also with the network link cut |
| 3 min | The benchmark table, and two decisions with their numbers |
| 2 min | Questions |

Watch the other teams. Write one question for each team.

### Part C: close (30 min)

1. **Report (20 min).** Complete `report.md`, at most four pages. Submit it
   in the way that the instructor names.
2. **Feedback (10 min).** Fill `feedback.md` with no name and give it to
   the instructor.

## Check criterion

The instructor grades with the rubric of `Docs/capstone.md`, Section 3:

- [ ] The system works in the demonstration (30 percent).
- [ ] Integration of the two boards, messages, and monitoring (25 percent).
- [ ] Measured results and analysis of trade-offs (25 percent).
- [ ] Report and presentation (20 percent).

## Decision Log

The report has two or three Decision Logs of about 100 words each. Each one
states a decision, gives the measured numbers, and names the trade-off.

Question of this lab: which decision of your system had the largest effect
on the result, and which measured number shows it?

## For the instructor: the demonstration schedule

Make the schedule on Day 14 with `schedule.py`, and publish it:

```bash
python3 schedule.py --start 13:00 --seed 1 \
    "Machine monitor" "Room counter" "Lab assistant"
python3 schedule.py --start 13:00 --teams-file teams.txt --change 2
```

The script prints a Markdown table and the time that the slots use. Part B
holds 7 teams with 10 minutes each, or 6 teams with 2 minutes between two
teams. With more teams, the script prints a warning: use two rooms, shorter
slots, or start some demonstrations in Part A.

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| A part does not work in Part A | Not enough time on Day 15 | Show the parts that work and plan B; write the limit in the report |
| The live demonstration fails | A board, the network, or the light of the room | Use plan B: a recorded input or a video. Explain the cause. |
| The benchmark table has gaps | No time to measure | Measure the main model first; write "not measured" in a gap, never a guess with no mark |
| The energy has no meter | No USB power meter | Use the power values of Day 9 and say "estimate" |
| The demonstration takes more than 10 minutes | Too much content | Rehearse with the clock in Part A, step 3 |

## Credits

This lab adapts material from these sources:

- "Machine Learning Systems" by Vijay Janapa Reddi and contributors
  (mlsysbook.ai, CC BY-NC-SA 4.0), the instructor guide
  (`instructors/assessment.qmd`): the structure of the design report
  (problem, approach, results, trade-offs) and the robustness test, through
  `Docs/capstone.md`.
- The labs of Days 1 to 14 of this course. `schedule.py` is new code of
  this course.
