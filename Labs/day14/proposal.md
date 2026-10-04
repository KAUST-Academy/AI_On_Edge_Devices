# Capstone proposal: <name of the system>

Team: <names>   Groups: gNN, gNN   Date: <date>

Fill each field. Write numbers where the template asks for numbers. Mark a
value that you did not measure as "estimate". Keep the proposal to one page.
`Docs/capstone.md` gives the five requirements and four example projects.

## Problem and user

<For whom, where, what, which benefit. Two to four sentences. Write the
problem, not a solution.>

## Requirements with numbers

| No. | Requirement | Number | Test |
|---|---|---|---|
| R1 | | | |
| R2 | | | |
| R3 | | | |

## Boards and split of the work

<What runs on the XIAO, what runs on the Raspberry Pi, and why.>

## Model and optimization

| Model | Board | Task | Optimization | Size before / after (estimate) |
|---|---|---|---|---|
| | | | | |

## Data

<Source, number of samples or recordings, classes, who labels, the split
between training and test.>

## Local decision and telemetry

<The decision rule, the MQTT topics (`edgeai/gNN/<device>/<channel>`), the
values on the dashboard.>

## Budgets

Calculate the values with `budget.py`. Name the source of each input value.

| Budget | Value | Source or method |
|---|---|---|
| Latency of the main path | | |
| Flash and RAM of the XIAO model | | |
| Power or energy | | |

## The five requirements

1. XIAOML Kit and Raspberry Pi: <how>
2. Optimized model, size and accuracy before and after: <how>
3. Local decision, works without the internet: <how>
4. Telemetry with MQTT to a dashboard: <how>
5. Benchmark table with latency, memory, and energy: <how>

## Riskiest assumption and first test

<The assumption, the first test (Part D of today), plan B.>
