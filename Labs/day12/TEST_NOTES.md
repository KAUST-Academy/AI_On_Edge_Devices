# Test notes: Day 12 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `sketches/kws_mqtt/kws_mqtt.ino` | changed | `Labs/day05/sketches/kws_stream` (solution) and `Labs/hardware/HW-07/sketches/mqtt_imu` of this course | See the list of changes below |
| `sketches/kws_mqtt/postprocess.h` | copy | `Labs/day05/solutions/sketches/kws_stream/postprocess.h` | Only the comment at the top |
| `sketches/kws_mqtt/arduino_secrets.h` | copy | `Labs/hardware/HW-07/sketches/mqtt_imu/arduino_secrets.h` | none |
| `pi/decide.py`, `solutions/pi/decide.py` | new | Part 1 of the Day 12 lecture (the state machine) | The student version has no body in the function `next_state` (Task C1) |
| `pi/forwarder.py` | new | Part 3 of the Day 12 lecture and the rules of the course plan | none |
| `pi/link.sh` | new | no source | Not run: the work computer has no `sudo` |
| `cloud_check.py`, `solutions/cloud_check.py` | new | The counter of `Labs/hardware/HW-07/host/mqtt_check.py` | The student version has no body in the function `count_sequence` (Task D1) |

`python3 tools/notebooks/build_day12_scripts.py` of the course repository
makes the two student files from `solutions/`.

Changes of the sketch against the two source sketches. Each changed line is
not tested on the board:

1. The network code of HW-07: Wi-Fi, one connection attempt each 5 s, the
   last will `offline` (retained), the status `online`, the command topic
   with QoS 1, and a keep-alive of 15 s. The loop calls `client.loop()` at
   each pass, before it waits for the next window.
2. One message on `edgeai/<group>/xiao/result` for each keyword event, with
   `seq`, `ms`, the label, and the mean score of the event. The Serial
   Monitor prints `MQTT sent` or `MQTT NOT SENT`.
3. One message on `edgeai/<group>/xiao/stats` each 10 s: windows, events,
   free memory.
4. The LED shows the command of the Raspberry Pi (`led=1`, `led=0`), not the
   event. The display still shows each event for one second.
5. The Serial Monitor prints no line for each window (Day 5 printed one).
6. The post-processing values are the values of the Day 5 lab: stride
   250 ms, the mean of 3 windows, threshold 0.60, suppression 1000 ms.

### Compile results (arduino-cli 1.5.1, esp32 core 3.3.12, 2026-10-03)

| Sketch | Board name | Result |
|---|---|---|
| `kws_mqtt` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles with a replacement for the Edge Impulse library, no warning with `--warnings all`. No size: the real library is larger. |

The replacement library has the constants, the types, and the functions
that the sketch uses (classes `no`, `noise`, `unknown`, `yes`; 16 000
samples). It is not in a repository.

### Test on the work computer of the course (2026-10-03)

An x86 processor, no board, no Wi-Fi, no Raspberry Pi. Two Mosquitto 2.0.11
brokers ("local" and "cloud"), paho-mqtt 2.1.0, and a proxy between the
forwarder and the cloud broker that can cut the link. A Python program
played the XIAO: the status with the last will, 8 keyword events, a `stats`
message each 2 s, and the command topic. `decide.py` ran with
`--on-seconds 5 --summary-seconds 2`. The test ran in a clean copy of the
lab folder. The values say nothing about the lab hardware.

| Test | Result |
|---|---|
| Part A commands (`mosquitto_sub`, `mosquitto_pub`) against the test broker | `edgeai/g07/#` got `test/a` and `test/b/c`; `edgeai/+/test/a` got `g07` and `g08`. `-d` showed PUBLISH, PUBACK for QoS 1 and PUBLISH, PUBREC, PUBREL, PUBCOMP for QoS 2. The retained message came at once and not after the empty retained message. `kill -9` of a client with a will gave `offline` at once. |
| `solutions/pi/decide.py`, check of Task C1 | `Task C1: complete` |
| Events "yes" 0.91, "no" 0.88, "yes" 0.55, "yes" 0.93 | commands `led=1`, `led=0`, nothing, `led=1`; `led=0` 5.1 s after the last "yes" |
| Local time from the event to the command | 0.08 ms to 0.31 ms |
| The simulated XIAO closed its connection with no DISCONNECT | `ON -> FAULT status offline`, command `led=0` |
| Cut of the link from 20 s to 45 s, events "yes", "no", "yes" during the cut | the commands came as before; the forwarder queue grew to 30 messages and went to 0 after the link came back |
| `solutions/cloud_check.py` after 75 s | decision 11, summary 37, stats 27 messages, 0 lost, 0 double, `RESULT: PASS - no lost message`; the queued messages came with `late 7 s` to `late 27 s` |
| A silent cut (the proxy dropped all data and kept the connection), three runs | `link lost` after 18.6 s each time (keep-alive 10 s); after a restore at 40 s, 149 of 149 messages, 0 double |
| The student versions | `Task C1: not complete. The state never changes.` and no command; `Task D1: not complete` and `RESULT: not valid - Task D1 is not complete` |

Points that only the hardware can confirm:

- The sketch on the XIAO with a real Edge Impulse library: the Wi-Fi, the
  broker connection, the events, the `stats` message, and the LED command.
  The time of `client.connect()` when the broker is away: it can stop the
  inference for some seconds.
- `mqtt_imu.py` of HW-07 with the real `umqtt.simple`.
- `link.sh` with `sudo ip route add blackhole` on Raspberry Pi OS.
- The time from the removed USB cable to the last will (about 22 s
  expected).
- The cloud broker on the instructor laptop with all groups at the same
  time.

## 2. Checklist for the instructor

- Date of the test:
- Mosquitto version on the Raspberry Pi (`mosquitto -h`) and on the
  instructor laptop:
- Edge Impulse project and library of the test:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, steps 1 to 3 | The line of `ss`, the packets of `-d` for QoS 2, the time of the last will | |
| 2 | Part B, step 1 | The `mqtt_check.py` table for 30 s, the gap after 10 s with no cable | |
| 3 | Part B, step 2 | Does the sketch compile with the real library? Flash and RAM. Events for 10 "yes" and 10 "no". | |
| 4 | Part C, step 2 | The local times, the delay from the word to the LED, the LED off after 60 s | |
| 5 | Part C, step 3 | Seconds from the removed cable to FAULT | |
| 6 | Part D, steps 2 to 4 | Seconds until `link lost`, queue length each minute, seconds until the queue is 0, the table of `cloud_check.py` | |
| 7 | Part D with three groups at the same time | Does each group see only its own topics on the cloud broker? | |
| 8 | Time the complete lab with one student group, or alone | Minutes for each part | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|
| | | |
