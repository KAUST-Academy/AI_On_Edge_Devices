# Test notes: Day 14 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `budget.py` | new | no source; the method of Day 9, Part 3 and Day 14, Part 3 | tested on the work computer (Python 3.10): each example of the README gives the values of the lecture; a wrong argument prints an error |
| `proposal.md`, `report.md`, `review_sheet.md` | new | the template of `Docs/capstone.md` | none |
| `solutions/proposal_example.md`, `solutions/report_example.md` | new | Example A of `Docs/capstone.md` | the values are estimates from the lectures and the labs; the values of the boards say "measure in the lab" |

The lab has no new sketch and no new program for a board. Part D reuses
the lab folders of Days 1 to 13.

Run on the work computer (2026-10-03), with the commands of Part B,
step 3 of the README:

| Command | Result | Value of the lecture |
|---|---|---|
| `fit` | flash 308 734 of 3 342 336 bytes, RAM 1028 of 305 848 bytes, fits | the program of 300 KB is an estimate |
| `latency` | 2600 ms, margin 400 ms | 2.6 s against 3.0 s |
| `power` | 24.192 mW, 152.9 h = 6.4 days, 17.42 Wh for 30 days | 24.2 mW, 6.4 days, 17.4 Wh |
| `data` | 19.051 GB in 30 days | 19.1 GB |
| `cost` | 185 and 21 275 | 185 USD and 21 275 USD |

## 2. Checklist for the instructor

Run the lab with a test team. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Python version of the lab laptops:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run the five commands of Part B, step 3 on a lab laptop | The results against the table above | |
| 2 | Time a review with `review_sheet.md` | Minutes for one team | |
| 3 | Count the teams that one instructor can review in the 40 minutes of Part C | Number of teams | |
| 4 | Check that each example project of `Docs/capstone.md` has the boards and the lab folders it needs | The missing items | |
| 5 | Run the first test of Example A (two sessions of a fan, the Day 3 notebook) | The recall of "abnormal" on the second session | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 20 min | |
| B | 50 min | |
| C | 40 min | |
| D | 40 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured numbers in the lab `README.md` and in the lab deck.
2. Change the line `Hardware status:` of the `README.md` to
   `tested on hardware (YYYY-MM-DD)`.
3. If one instructor cannot review all teams in 40 minutes, change the time
   of a review or start the reviews during Part B.
