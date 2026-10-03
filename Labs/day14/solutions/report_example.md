# Day 14 lab report: capstone start (example)

Team: example   Groups: g07, g08   Date: Day 14

This example goes with `solutions/proposal_example.md`. A value that only
the boards can give says "measure in the lab".

## Part A: team and problem

- Problem selected: an alarm at a machine with abnormal vibration, and a
  warning when a person is near it.
- Example project used: A (machine monitor).
- Riskiest assumption: the IMU separates a normal fan from a fan with a
  weight on one blade.

## Part B: budgets

| Budget | Command | Result |
|---|---|---|
| Fit of the XIAO model | `python3 budget.py fit --flash-kb 3264 --ram-kb 298.68 --program-kb 300 --params 1512 --bits 8 --peak-values 1028` | Fits: flash 308 712 of 3 342 336 bytes (9.2 percent), RAM 1028 of 305 848 bytes (0.3 percent) |
| Latency of the main path | `python3 budget.py latency window=2000 model=100 decision=400 mqtt=100 --limit-ms 3000` | 2600 ms, margin 400 ms (met) |
| Power or energy | `python3 budget.py power --work-mw 217 --rest-mw 19 --work-ms 50 --period-ms 2000 --radio-mw 290.4 --radio-s-per-hour 3 --battery-mah 1000 --days 30` | 24.192 mW, 152.9 h = 6.4 days; 30 days need 17.42 Wh (4708 mAh) |
| Data volume | `python3 budget.py data --bytes 400 --per-second 0.1` | 3.456 MB each day |
| Cost (optional) | not used | |

## Part C: design review

- Result: approved with changes.
- Changes that the instructor asked for:
  1. R1 needs a test session on a different day or position, not only a
     different time.
  2. The benchmark table needs the latency of the XIAO model, not only the
     budget value of 100 ms.
- Weak points that the review found:
  1. The battery does not reach 30 days (6.4 days in the budget). The team
     uses a USB cable and writes this limit in the report.
  2. The person warning depends on the Wi-Fi between the Pi and the XIAO.
     The alarm itself does not.

## Part D: first test

- The test: two sessions of each state with the Day 2 logger at 50 Hz, then
  the Day 3 notebook with two classes.
- The result, with numbers: measure in the lab (the recall of "abnormal" on
  the second session).
- The decision: measure in the lab.
- The plan for Day 15: (1) record session 3 and train the final model,
  30 min; (2) convert to `int8` and deploy, 30 min; (3) connect the Day 12
  and Day 13 programs, 40 min; (4) measure the benchmark table, 40 min;
  (5) rehearse the demonstration with the router off, 20 min.

## Decision Log

We put the alarm decision on the XIAO and the person detection on the
Raspberry Pi. The alarm path needs 2.6 s of the 3.0 s budget, and 2.0 s of
it is the window, so the network must not be in the path: the XIAO decides
alone and works with the router off. The person detector needs YOLO11n: at
320 pixels its first layer alone needs 716 800 bytes of `int8` activations
(the rule of Day 1), more than the 305 848 bytes of RAM of the XIAO with no
PSRAM. We gave up the battery: with Wi-Fi each hour and light sleep the
budget gives 6.4 days on 1000 mAh, far from 30 days, so the XIAO uses a USB
cable.
