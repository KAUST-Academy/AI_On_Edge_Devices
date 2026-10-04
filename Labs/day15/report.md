# Capstone report: <name of the system>

Team: <names>   Groups: gNN, gNN   Date: <date>

At most four pages. Write numbers with their unit and their method. Mark a
value that you did not measure as "estimate". `Docs/capstone.md` gives the
rubric.

## 1. Problem and requirements

<The problem and the user, in two to four sentences. Then the requirements
of your approved proposal, with the result of each test.>

| No. | Requirement | Number | Test result | Met? |
|---|---|---|---|---|
| R1 | | | | |
| R2 | | | | |
| R3 | | | | |

## 2. The system

<What runs on the XIAO, what runs on the Raspberry Pi, the MQTT topics, the
local decision, and the dashboard. A diagram helps.>

## 3. The five capstone requirements

| No. | Requirement | How the system meets it | Shown in the demonstration? |
|---|---|---|---|
| 1 | XIAOML Kit and Raspberry Pi | | |
| 2 | One optimized model, size and accuracy before and after | | |
| 3 | One local decision, works without the internet | | |
| 4 | Telemetry with MQTT to a dashboard | | |
| 5 | Benchmark table with latency, memory, and energy | | |

## 4. Optimized model

| Model | Format | File size (bytes) | Accuracy (test set, number of samples) |
|---|---|---|---|
| | before | | |
| | after | | |

## 5. Benchmark table

| Model | Board | Format | Latency median (ms) | Latency p95 (ms) | Memory | Energy for each inference |
|---|---|---|---|---|---|---|
| | | | | | | |

Method: <warm-up runs, number of runs, the window of the time (model only
or end to end), how you got the memory and the energy (meter, data sheet,
or estimate of Day 9)>.

## 6. Robustness

<One change of the input (less light, noise, a different person or object),
the cut of the network link, and the effect on the system, with numbers.>

| Test | What changed | Effect |
|---|---|---|
| | | |

## 7. Decision Log

Two or three decisions, about 100 words each. For each one: the decision,
the measured numbers, the trade-off (what you gained and what you gave up).

### Decision 1

### Decision 2

## 8. Limits and next steps

<What does not work yet, what you did not measure, and what you would
change with more time.>
