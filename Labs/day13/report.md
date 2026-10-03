# Day 13 report: a monitored inference application

Group: gNN. Names:

Date:

Model file: . Address of the Raspberry Pi:

## Part A: instrument

| Value | Result |
|---|---|
| Output of `python monitor.py` | `Task A1: complete`, `Task A2: complete` |
| Frames each second (a printed line) | |
| Latency mean and p95 of a frame | ms |
| Mean top score with the cup and the bottle in view | |
| Brightness and sharpness | |
| CPU temperature and memory of the detector (`rss`) | |

The log (step 4):

| Value | Result |
|---|---|
| Records in `logs/detector.jsonl` after 2 minutes (`wc -l`) | |
| Size of the file after 2 minutes (`wc -c`) | bytes |
| Bytes of one summary record | bytes |
| WARNING records with `--slow-ms 50` in 1 minute (`grep -c slow_frame`) | |

Question A1. Calculate the size of the log for one day with one summary
each 10 s. How many days does the rotation (1 MB and 5 old files) keep?

Answer:

Question A2. The detector writes one WARNING for each slow frame. What
happens to the log when the board is too hot and each frame is slow? Which
rule of Part 2 of the lecture protects the disk?

Answer:

## Part B: dashboard

| Value | Result |
|---|---|
| Messages and lost messages in the state bar after 5 minutes | |
| Age of the last message in the state bar | s |
| Name of the CSV file in `dashboard/metrics_log/` | |

Reference period (step 4):

| Value | Result |
|---|---|
| Start and end (local time) | |
| What happened in the room during the period | |
| Panels that changed during the period | |
| Panels that stayed flat | |

## Part C: drift

Threshold from the reference period (step 1), the output of
`reference.py`:

```
Rows:
Means of 6 rows:
Threshold:
```

| Value | Result |
|---|---|
| Did `reference.py` print the WARNING? Did you use `--min-margin`? | |
| Threshold and clear value of the confidence | |
| Threshold of the brightness (`--metric brightness`) | |

Drift events (step 2). Read the values of the printed lines of
`monitor_detect.py` or of the dashboard:

| Event | Start, end | Mean top score | Part below 0.5 | Objects | Brightness | Sharpness |
|---|---|---|---|---|---|---|
| Normal (reference) | | | | | | |
| Dim light | | | | | | |
| Unknown object | | | | | | |
| (Optional) lens out of focus | | | | | | |

Question C1. Which metric showed each event most clearly? Which metric
names the cause?

Answer:

Question C2. The model gave no error during the events. How would a user of
the application see the dim light event?

Answer:

## Part D: alert

| Value | Result |
|---|---|
| First line of `alert.py` | `Task D1: complete` |
| The command of `alert.py` (threshold, clear, window, duration) | |
| Seconds from the start of the event to `ALERT ON` | s |
| Seconds from the end of the event to `ALERT OFF` | s |
| Did the state bar of the dashboard become red? | |
| Alerts during the reference period, or a false alert | |
| (Optional) Did the LED of the XIAO follow the alert? | |

Question D1. Which part of the delay to `ALERT ON` comes from the window
(6 summaries), and which part from the duration (60 s)? How would you make
the alert faster, and what is the cost?

Answer:

## Incident report

Write the report of one drift event of Part C or Part D, as a record of what
happened (Part 3 of the lecture).

| Item | Content |
|---|---|
| Event | |
| Start of the event (time) | |
| Time of the alert, or how you found the event | |
| End of the event (time) | |
| Effect: what was wrong, and for how long | |
| Signals: values of the metrics before and during the event | |
| Cause | |
| Action | |
| What changes so that it does not happen again | |

## Decision Log

A shop uses 20 Raspberry Pi cameras to count the people at its doors. One
camera stands near a window, so its light changes with the time of day. The
shop has one person who looks at alerts. Which metrics does each device
send, how often, and where are they stored? Which alert rules do you use,
with which thresholds, windows, and durations? How many false alerts each
week do you expect, and what does the person do for each alert?

Write about 100 words with your measured numbers, and name one trade-off.

Decision:
