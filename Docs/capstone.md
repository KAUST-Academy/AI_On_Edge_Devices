# Capstone project

The capstone joins the parts of the course into one edge AI system. Your
team proposes the system on Day 14, builds it on Days 14 and 15, and shows
it on Day 15. The capstone is 40 percent of the course grade.

## 1. Teams and timeline

- A team has three or four students: two lab groups. The team can use the
  boards of both groups: two XIAOML Kits and two Raspberry Pi 5 boards.
- Keep the scope small. Reuse the labs of Days 1 to 13 and add one new
  part. A small system that works scores more than a large system that does
  not.

| When | What | Time |
|---|---|---|
| Day 14, lab Part A | Form the team. Select a problem. | 20 min |
| Day 14, lab Part B | Write the proposal (Section 4). | 50 min |
| Day 14, lab Part C | Design review with the instructor (Section 5). | 40 min |
| Day 14, lab Part D | Start the build: the riskiest part first. | 40 min |
| Day 15, lecture Parts 2 and 3 | Build. The instructor visits each team. | 100 min |
| Day 15, lab Part A | Complete the build and the measurements. | 80 min |
| Day 15, lab Part B | Demonstration: 10 minutes for each team. | 70 min |
| Day 15, lab Part C | Submit the report. Give course feedback. | 30 min |

The instructor publishes the order of the demonstrations on Day 14.

## 2. The five requirements

Your system must meet all five requirements. The proposal says how, and the
demonstration shows it.

| No. | Requirement | How you show it |
|---|---|---|
| 1 | Use the XIAOML Kit and the Raspberry Pi. | Each board has a task that the other board cannot do as well. |
| 2 | Run at least one optimized model, with the size and the accuracy before and after the optimization. | A table: the model before and after (for example `float32` and `int8`), with the file size and the accuracy on the same test set. |
| 3 | Make one decision locally, and continue to work without the internet. | Cut the link to the instructor broker during the demonstration. The local decision continues. |
| 4 | Send telemetry with MQTT to a dashboard. | The dashboard of Day 13 shows the values of your system during the demonstration. |
| 5 | Include a benchmark table with latency, memory, and energy. | The table of Section 6 for each model on its board, with the method of Day 9. |

## 3. Rubric

The instructor grades the demonstration and the report on Day 15.

| Criterion | Weight | Excellent | Adequate | Insufficient |
|---|---|---|---|---|
| The system works in the demonstration | 30% | All five requirements work live, also with the link cut. | The system works, but one requirement needs a recorded input or a second try. | The main function does not work live. |
| Integration of the two boards, messages, and monitoring | 25% | Both boards have a clear task. The messages have a topic tree and a sequence number. The dashboard shows live values. | The boards and the messages work, but one part is weak (for example, no sequence number, or a dashboard with old values). | One board, or no MQTT, or no dashboard. |
| Measured results and analysis of trade-offs | 25% | The benchmark table is complete, with the method. The report explains each main decision with at least two measured numbers and names what the team gave up. | The table has gaps, or the report gives numbers with no trade-off. | No measured numbers, or numbers with no method. |
| Report and presentation | 20% | The report follows the template, is short and clear, and the team answers the questions with numbers. | The report is complete but long or unclear. | The report is missing or incomplete. |

The levels of the third criterion follow the Decision Log rubric of the
instructor guide of *Machine Learning Systems*: quantitative evidence,
causal reasoning, and constraint awareness.

## 4. Proposal template

Write one page. Copy this template into `proposal.md` of your team and
fill each field. Write numbers where the template asks for numbers. Mark a
value that you did not measure as "estimate".

```markdown
# Capstone proposal: <name of the system>

Team: <names>   Groups: gNN, gNN   Date: <date>

## Problem and user
<For whom, where, what, which benefit. Two to four sentences.>

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

## Data
<Source, number of samples or recordings, classes, who labels, the split
between training and test.>

## Local decision and telemetry
<The decision rule, the MQTT topics, the values on the dashboard.>

## Budgets
| Budget | Value | Source or method |
|---|---|---|
| Latency of the main path | | |
| Flash and RAM of the XIAO model | | |
| Power or energy | | |

## The five requirements
<One line for each requirement: how the system meets it.>

## Riskiest assumption and first test
<The assumption, the first test, plan B.>
```

## 5. Design review

On Day 14, Part C, the instructor reviews each proposal with these
questions. Prepare an answer with a number for each one.

1. Does each requirement have a number and a test?
2. Does each budget have a value and a source? Is each guess marked?
3. Does the model fit the board: flash, RAM, and time?
4. Where does the data come from? How many samples? Who labels them? Is the
   test set separate from the training set?
5. What happens with no network, a failed sensor, or a bad update?
6. Which data leaves the device? Who can read it or send a command?
7. What is the riskiest assumption, and what is its first test?

The proposal is approved when it meets the five requirements of Section 2
and the team has a first test for its riskiest assumption.

## 6. Report and benchmark table

The Day 15 lab gives the report template. The report has at most four
pages: the problem, the system, the benchmark table, the Decision Log of
the two or three main decisions, the robustness tests, and the limits.

The benchmark table has one row for each model on its board:

| Model | Board | Format | File size | Accuracy | Latency (median, p95) | Memory | Energy for each inference |
|---|---|---|---|---|---|---|---|

- Use the method of Day 9: warm-up runs, a fixed number of runs, the
  window of the time, and the statistic.
- XIAO: arena size and flash use from the build, latency with `micros()`,
  energy from a USB power meter or from the data sheet values of Day 9
  (say which).
- Raspberry Pi: latency of the full pipeline and of the model only, the
  resident memory of the process, and the power estimate of Day 9.
- Robustness: test the system with one change of the input (less light,
  noise, a different person or object) and report the effect, as in Day 13.

## 7. Example projects

Use one of these projects if your team has no idea, or change one. Each
example meets the five requirements and reuses the labs.

### Example A: machine monitor

A XIAO on a machine detects abnormal vibration and sounds a local alarm. A
Raspberry Pi with a camera warns when a person is near a machine with an
alarm. Day 14, Part 3 of the lecture uses this example.

| Item | Plan |
|---|---|
| XIAO | IMU at 50 Hz, the feature block and the small model of Day 3, retrained for "normal" and "abnormal" vibration. Alarm on the display after 3 windows in a row. |
| Raspberry Pi | YOLO11n (pre-trained, class "person") on the camera, Day 8. Broker, logic, log, and dashboard, Days 12 and 13. |
| Optimized model | The XIAO model in `float32` and in `int8` (Day 4). |
| Data | Record a small fan: normal, and with a small weight taped to one blade for "abnormal". Split by session (Day 2). |
| Local decision | The alarm on the XIAO. It works with no network. |
| Telemetry | Vibration state each 10 s, person count, alarm events. |
| Riskiest assumption | The IMU separates the two states of the fan. First test: record two sessions of each state and train. |

### Example B: voice-controlled camera

A keyword on the XIAO wakes the detector on the Raspberry Pi. The Pi counts
objects for 30 s and then goes back to a low load. This is the cascade of
Day 5, Part 3.

| Item | Plan |
|---|---|
| XIAO | The keyword model of Day 5 (Edge Impulse). The keyword "yes" sends a start event with MQTT. |
| Raspberry Pi | The detector of Day 8 (cups and bottles) on the camera, active for 30 s after each start event. |
| Optimized model | The detector in `float32` and in `int8` (Day 8): size and mAP on the test images. |
| Data | The keyword data of Day 5 and the dataset of Day 8. |
| Local decision | Start and stop of the detector on the Pi, and the LED of the XIAO, with no network. |
| Telemetry | Start events, counts, the frame rate, and the CPU temperature. |
| Riskiest assumption | False starts in a noisy room. First test: 5 minutes of normal speech, count the false starts (Day 5). |

### Example C: room counter with privacy

A XIAO at the door sees if a person is there. It wakes a Raspberry Pi that
counts the persons in the room. No image leaves the Raspberry Pi.

| Item | Plan |
|---|---|
| XIAO | An image classifier "person" or "no person" (MobileNetV2 0.35, 96 x 96 pixels, Day 5). It sends an event with MQTT. |
| Raspberry Pi | YOLO11n at 320 pixels counts the persons (Day 8). It shows "room full" on the display of the XIAO above a limit. |
| Optimized model | The XIAO model in `float32` and in `int8`, or YOLO11n at 640 and 320 pixels (Day 8). |
| Data | Photos of the door area with and without a person, taken by the team (Day 5 method). |
| Local decision | "Room full" on the XIAO display, with no network. |
| Telemetry | The count each 10 s and the events of the door. No image. |
| Riskiest assumption | The XIAO model works in the light of the room. First test: 20 photos at two times of the day. |

### Example D: offline lab assistant

A gesture on the XIAO selects a question. A small language model on the
Raspberry Pi answers from a local file of lab notes, with no internet.

| Item | Plan |
|---|---|
| XIAO | The motion model of Days 3 and 4, retrained for three gestures. Each gesture sends a question number with MQTT. The answer appears on the display. |
| Raspberry Pi | `llama3.2:1b` with Ollama and the retrieval of Day 10, Part 3: the two most similar notes go into the prompt. |
| Optimized model | The XIAO gesture model in `float32` and in `int8` (Day 4). |
| Data | Gesture recordings of the team (Day 2 method) and a file of 10 to 20 lab notes. |
| Local decision | The Pi answers only from the notes. With no matching note, it says so. |
| Telemetry | Gesture events, the time to the first token, tokens each second. |
| Riskiest assumption | The answer is short enough for the display and comes fast enough. First test: 10 questions, measure the time and the length (Day 10). |


