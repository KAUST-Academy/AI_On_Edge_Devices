# Test notes: Day 15 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `schedule.py` | new | no source | tested on the work computer (Python 3.10): 3 teams use 30 of 70 minutes; 8 teams print a warning (Part B holds 7); 6 teams with `--change 2` use 70 minutes; no team prints an error |
| `report.md`, `feedback.md` | new | the report structure of `Docs/capstone.md` | none |
| `solutions/report_example.md` | new | Example A of `Docs/capstone.md` | the values of the boards say "measure in the lab"; the other values are estimates from the lectures |

The lab has no new sketch and no new program for a board. The teams reuse
the lab folders of Days 1 to 14.

## 2. Checklist for the instructor

Run the day with a test team, or record the values of the first course.

- Date of the test: YYYY-MM-DD
- Number of teams:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Make the schedule with `schedule.py` on Day 14 | The number of teams and the minutes that the slots use | |
| 2 | Time one demonstration | Minutes for one team, with the questions | |
| 3 | Count the teams that showed a cut of the network link | Number of teams | |
| 4 | Read three reports | The time to grade one report with the rubric | |
| 5 | Collect the feedback forms | Number of forms; the mean of each rating | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 80 min | |
| B | 70 min | |
| C | 30 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured times in the lab `README.md` and in the lab deck.
2. Change the line `Hardware status:` of the `README.md` to
   `tested on hardware (YYYY-MM-DD)`.
3. Change the questions of `feedback.md` that gave no useful answer.
