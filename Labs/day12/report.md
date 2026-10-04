# Day 12 report: local decisions and MQTT

Group: gNN. Names:

Date:

Address of the Raspberry Pi: . Address of the cloud broker:

## Part A: broker

| Value | Result |
|---|---|
| `systemctl is-active mosquitto` | |
| The line of `ss -tln` with the port 1883 | |

Wildcards (step 2). Write which of the three messages each filter received:

| Filter | `edgeai/g07/test/a` | `edgeai/g07/test/b/c` | `edgeai/g08/test/a` |
|---|---|---|---|
| `edgeai/gNN/#` | | | |
| `edgeai/+/test/a` | | | |

QoS, retained message, last will (step 3):

| Value | Result |
|---|---|
| Packets that `-d` shows for QoS 0 (after CONNACK, before DISCONNECT) | |
| Packets for QoS 1 | |
| Packets for QoS 2 | |
| Did the new subscriber get the retained message at once? | |
| Did a subscriber get it after the empty retained message? | |
| Time from `kill -9` to the message `offline` | |

Question A1. Your group has the XIAO, the Raspberry Pi, and the laptop.
Write your topic tree for the lab, and the filter that each program uses.

Answer:

## Part B: telemetry

IMU readings with MicroPython (step 1), `mqtt_check.py` for 30 s:

| Value | Result |
|---|---|
| Messages | |
| Lost messages | |
| Rate (messages each second) | |
| Gap in `seq` after 10 s with no USB cable | |

Keyword events with the Arduino sketch (step 2):

| Spoken word, 10 times | Events on `.../xiao/result` | Labels and scores (some examples) |
|---|---|---|
| "yes" | | |
| "no" | | |

| Value | Result |
|---|---|
| `stats` message: `windows` and `events` after 1 minute | |
| Does the LED follow `led=1` and `led=0` sent by hand? | |

Question B1. The sketch sends one message for each event, and MicroPython
sends one message for each IMU reading. Calculate the bytes each hour for
each design (Part 2 of the lecture: 147 bytes for one IMU message with the
headers). Which design would you use for a battery device?

Answer:

## Part C: local decision

| Value | Result |
|---|---|
| First line of `decide.py` | `Task C1: complete` |
| Local time from the event to the command (some values) | ms |
| Delay from the spoken word to the LED, as you see it | s |
| Does the LED go off 60 s after the last "yes"? | |
| Seconds from the removed USB cable to `-> FAULT` | s |

Question C1. The delay from the word to the LED is much longer than the
local time of `decide.py`. Name the parts of the delay (Day 5 and Part 1 of
the lecture).

Answer:

Question C2. Which state is the safe state of this light? Would your
answer change for a heater, or for the lock of a door?

Answer:

## Part D: offline operation

| Value | Result |
|---|---|
| First line of `cloud_check.py` | `Task D1: complete` |
| Duration of the cut | s |
| Seconds from `link.sh down` to `link lost` of the forwarder | s |
| Queue length after 1, 2, and 3 minutes of the cut | |
| Did the LED follow each word during the cut? | |
| Seconds from `link.sh up` to `connected` | s |
| Seconds from `connected` to the queue length 0 | s |
| The largest `late` value of `cloud_check.py` | s |

Table of `cloud_check.py` (copy the lines):

```
topic                          received   unique   lost double
```

Result line:

Question D1. The forwarder found the cut only after some seconds. Which
setting sets this time (Part 2 of the lecture)? What happened to the
messages of that time?

Answer:

Question D2. Your queue must survive a cut of 2 hours. Calculate its size
with the message rate of your system and 150 bytes for each message.

Answer:

## Decision Log

A cold store has five temperature sensors, a door contact, and a fan. The
cloud is behind a mobile modem, which loses the link for up to 2 hours each
day. Which decisions stay on the device? What does each device send, how
often, with which QoS, and which messages are retained? How large must the
queue of the forwarder be, and what happens when it is full?

Write about 100 words with your measured numbers, and name one trade-off.

Decision:
