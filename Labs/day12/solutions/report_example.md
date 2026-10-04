# Day 12 report: example

This example gives the parts that need no board, and the values of a test
on the work computer of the course. The work computer had two Mosquitto
2.0.11 brokers, a simulated XIAO, and a proxy for the cut of the link: no
board, no Wi-Fi, and no Raspberry Pi. Write "measure in the lab" values from
your own system.

Group: g07. Address of the Raspberry Pi: 192.168.8.107. Address of the
cloud broker: 192.168.8.10.

## Part A: broker

| Value | Result |
|---|---|
| `systemctl is-active mosquitto` | `active` (measure in the lab) |
| The line of `ss -tln` with the port 1883 | a line with `0.0.0.0:1883` (measure in the lab) |

| Filter | `edgeai/g07/test/a` | `edgeai/g07/test/b/c` | `edgeai/g08/test/a` |
|---|---|---|---|
| `edgeai/g07/#` | yes | yes | no |
| `edgeai/+/test/a` | yes | no | yes |

| Value | Result |
|---|---|
| Packets for QoS 0 | PUBLISH |
| Packets for QoS 1 | PUBLISH, PUBACK |
| Packets for QoS 2 | PUBLISH, PUBREC, PUBREL, PUBCOMP |
| Did the new subscriber get the retained message at once? | yes |
| Did a subscriber get it after the empty retained message? | no |
| Time from `kill -9` to the message `offline` | at once: the process closed its TCP connection with no DISCONNECT packet |

Question A1. Tree `edgeai/g07/<device>/<channel>`. The XIAO publishes
`xiao/imu`, `xiao/result`, `xiao/stats`, `xiao/status`, and subscribes to
`edgeai/g07/xiao/cmd`. `decide.py` subscribes to `edgeai/g07/xiao/result`
and `edgeai/g07/xiao/status`, and publishes `xiao/cmd`, `pi/decision`,
`pi/summary`, `pi/status`. The forwarder subscribes to
`edgeai/g07/pi/decision`, `edgeai/g07/pi/summary`, `edgeai/g07/xiao/stats`.
The laptop subscribes to `edgeai/g07/#`.

## Part B: telemetry

| Value | Result |
|---|---|
| Messages, lost, rate of `mqtt_imu.py` in 30 s | about 150, 0, 5.00 each second (HW-07 test with simulated modules: 21 messages in 4 s, no gap) |
| Gap in `seq` after 10 s with no USB cable | measure in the lab |
| Events for 10 "yes" and 10 "no" | measure in the lab |

Question B1. 5 IMU messages each second: 5 x 147 x 3600 = 2 646 000 bytes
each hour. Keyword events: one message of about 120 bytes for each event;
with 50 events each hour, 6000 bytes. For a battery device, send events:
the radio stays off for longer.

## Part C: local decision

| Value | Result |
|---|---|
| First line of `decide.py` | `Task C1: complete` |
| Local time from the event to the command | 0.08 ms to 0.31 ms on the work computer; measure in the lab |
| Delay from the spoken word to the LED | measure in the lab |
| Does the LED go off 60 s after the last "yes"? | yes, in the test with `--on-seconds 5`: the command `led=0` came 5.1 s after the last "yes" |
| Seconds from the removed USB cable to `-> FAULT` | measure in the lab; about 22 s expected (1.5 x 15 s) |

Question C1. The word must end, the model needs the window of 1 s, the mean
of 3 windows adds about 0.5 s (stride 250 ms), then the Wi-Fi to the broker,
the broker, `decide.py`, the broker again, and the Wi-Fi to the XIAO. The
program itself needs less than 1 ms.

Question C2. Off is the safe state of this light. A heater is also safe when
off. For the lock of a door, the safe state depends on the door: a fire exit
must open, a store room must stay locked (Part 1 of the lecture).

## Part D: offline operation

Test on the work computer: a cut of 25 s with a summary and a `stats`
message each 2 s (the lab uses 10 s). The proxy closed the connection and
refused new connections during the cut.

| Value | Result |
|---|---|
| First line of `cloud_check.py` | `Task D1: complete` |
| Duration of the cut | 25 s |
| Seconds from the cut to `link lost` | at once (the proxy closed the connection). In a second test with a silent cut (the effect of `link.sh`), 18.6 s in three runs |
| Largest queue length | 30 messages |
| Did the decisions continue during the cut? | yes: the simulated XIAO got `led=1` and `led=0` for each word |
| Seconds from the restore to the queue length 0 | below 5 s (the next line of the forwarder) |
| The largest `late` value | 27 s |

```
topic                          received   unique   lost double
edgeai/g07/pi/decision               11       11      0      0
edgeai/g07/pi/summary                37       37      0      0
edgeai/g07/xiao/stats                27       27      0      0
RESULT: PASS - no lost message
```

Question D1. The keep-alive of the forwarder (10 s). When nothing comes
back from the broker, paho sends a PINGREQ, waits for the PINGRESP, and then
closes the connection: 18.6 s after a silent cut on the work computer. The
messages of that time stay in the queue, because the forwarder deletes a
message only after its PUBACK. Messages in flight with no PUBACK are sent
again: the receiver can get a second copy. The test with the silent cut
lost no message and had no double copy (149 of 149).

Question D2. In the lab, about 12 messages each minute: 12 x 120 = 1440
messages in 2 hours, x 150 bytes = 216 000 bytes. The microSD card holds
this with no problem.
