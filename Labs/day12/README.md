# Day 12 lab: local decisions and MQTT


**Goal.** Your group builds a system of two boards. The XIAOML Kit sends
keyword events with MQTT to a broker on the Raspberry Pi 5. A program on the
Raspberry Pi decides locally and sends a command back to the XIAO. A second
program sends the decisions to the "cloud" broker on the instructor laptop.
Then you cut the link to the cloud and show that the local system continues
to work and that no message is lost.

**Deliverable.** A live demonstration with the link to the cloud connected
and cut, and the file `report.md` with the topic tree, the measured values,
and the Decision Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Broker: Mosquitto on the Raspberry Pi, publish and subscribe from the command line | 30 min |
| B | Telemetry: IMU readings with MicroPython, keyword events with the Arduino sketch | 45 min |
| C | Local decision: a state machine on the Raspberry Pi, a command back to the XIAO | 40 min |
| D | Offline operation: store and forward to the cloud, a cut of the link | 35 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| XIAOML Kit | 1 | With a USB-C cable for the laptop |
| Raspberry Pi 5 with the active cooler | 1 | With the microSD card of the course |
| Power supply for the Raspberry Pi 5 | 1 | 27 W, USB-C |
| Laptop | 1 | In the lab network, with an SSH client and the Arduino IDE |
| The router of the lab | 1 for the class | Wi-Fi `edgeai-lab` with 2.4 GHz (`Labs/hardware/HW-09/`) |
| The instructor laptop with a Mosquitto broker | 1 for the class | The "cloud" of Part D, address `X.10` |

## Software

| Tool | Version | Note |
|---|---|---|
| Mosquitto broker and clients on the Raspberry Pi | the card of the course (Debian package) | `Labs/hardware/HW-04/setup_pi.sh` installs them. `Labs/hardware/HW-07/mosquitto_lab.conf` opens port 1883 to the lab network. |
| The environment `~/yolo` on the Raspberry Pi | `paho-mqtt` 2.1 | `Labs/hardware/HW-04/setup_pi.sh` installs it. It runs `pi/decide.py` and `pi/forwarder.py`. |
| Python 3 with `paho-mqtt` 2.x on the laptop | `pip install paho-mqtt` | `cloud_check.py` and `../hardware/HW-07/host/mqtt_check.py` |
| Mosquitto clients on the laptop | any version 2 | Optional: `mosquitto_pub` and `mosquitto_sub` |
| MicroPython for the XIAO, `esptool`, `mpremote` | MicroPython v1.29.0 | `Labs/hardware/HW-01/`, as in the Day 2 lab |
| Arduino IDE with the esp32 core | core 3.3.12 | `Labs/SETUP.md` |
| Arduino libraries | PubSubClient 2.8, U8g2 2.36.19, the library of your Day 5 Edge Impulse project | Library Manager. The Day 5 library is the ZIP file of your group. |

`NN` is the number of your group, and `gNN` is its group name (for example
`g07`). Your Raspberry Pi has the name `pi-NN` and the address `X.(100+NN)`.
The instructor laptop has the address `X.10`. The examples use the network
`192.168.8` and the group `g07` of `Labs/hardware/HW-09/`. Use the network
of your router and your group. Run the laptop commands in the folder
`Labs/day12/`.

## Topic tree

| Topic | From | To | Payload | QoS, retained |
|---|---|---|---|---|
| `edgeai/gNN/xiao/imu` | XIAO (MicroPython) | Raspberry Pi | one IMU reading each 200 ms | 0, no |
| `edgeai/gNN/xiao/result` | XIAO (Arduino) | Raspberry Pi | one keyword event: `{"seq":3,"ms":81234,"label":"yes","score":0.91}` | 0, no |
| `edgeai/gNN/xiao/stats` | XIAO (Arduino) | Raspberry Pi, cloud | each 10 s: windows, events, free memory | 0, no |
| `edgeai/gNN/xiao/status` | XIAO | all | `online`, or `offline` (last will) | 1, yes |
| `edgeai/gNN/xiao/cmd` | Raspberry Pi | XIAO | `led=1` or `led=0` | 1, no |
| `edgeai/gNN/pi/decision` | Raspberry Pi | cloud | one change of state: `{"seq":5,"t":...,"state":"ON","reason":"yes 0.91","source_seq":3}` | 1, no |
| `edgeai/gNN/pi/summary` | Raspberry Pi | cloud | each 10 s: the state and the counts | 1, no |
| `edgeai/gNN/pi/status` | Raspberry Pi | all | `online`, or `offline` (last will) | 1, yes |

## Files

| File | Content |
|---|---|
| `report.md` | The report to hand in. Fill it during the lab. |
| `sketches/kws_mqtt/` | Part B. The keyword model of your Day 5 lab with MQTT: one message for each keyword event, the LED from the command |
| `pi/decide.py` | Part C. The local decision on the Raspberry Pi. **Task C1** is in this file. |
| `pi/forwarder.py` | Part D. Store and forward from the local broker to the cloud broker |
| `pi/link.sh` | Part D. Cuts and restores the link from the Raspberry Pi to the cloud broker |
| `cloud_check.py` | Part D. Counts the messages of the group on the cloud broker. **Task D1** is in this file. |
| `solutions/` | The complete task files and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

The lab also uses these files of other folders:

| File | Part |
|---|---|
| `../hardware/HW-07/mosquitto_lab.conf` | A: the settings of the broker |
| `../hardware/HW-07/micropython/mqtt_imu.py` and `config.py` | B: the IMU telemetry with MicroPython |
| `../hardware/HW-01/board/lsm6ds3.py` and `../hardware/HW-01/get_firmware.sh` | B: the IMU driver and the MicroPython firmware |
| `../hardware/HW-07/host/mqtt_check.py` | B: counts the messages and the lost messages |

`pi/forwarder.py` writes its queue into `forwarder.db` on the Raspberry Pi. Git
ignores this file.

## Steps

Write each result in `report.md` when you get it.

### Part A: broker (30 min)

1. **Start the broker (10 min).** On the laptop, copy the lab folder to the
   Raspberry Pi: `scp -r ../day12 ../hardware/HW-07 edge@pi-NN.local:edgeai/`.
   Then, on the Raspberry Pi (`ssh edge@pi-NN.local`):

   ```bash
   ls /etc/mosquitto/conf.d/
   sudo cp ~/edgeai/HW-07/mosquitto_lab.conf /etc/mosquitto/conf.d/lab.conf
   sudo systemctl restart mosquitto
   systemctl is-active mosquitto
   ss -tln | grep 1883
   ```

   Copy the file only if `lab.conf` is not in the folder. You see `active`,
   and `ss` shows `0.0.0.0:1883`. Mosquitto 2 accepts only local clients
   with no `listener` line.

2. **Publish and subscribe (10 min).** Terminal 1 on the Raspberry Pi, and
   terminal 2 on the laptop (or a second SSH terminal):

   ```bash
   mosquitto_sub -h localhost -t 'edgeai/g07/#' -v               # terminal 1
   mosquitto_pub -h pi-07.local -t edgeai/g07/test/a -m hello    # terminal 2
   mosquitto_pub -h pi-07.local -t edgeai/g07/test/b/c -m deep
   mosquitto_pub -h pi-07.local -t edgeai/g08/test/a -m other
   ```

   Terminal 1 shows the first two messages, not the third. Stop terminal 1
   and subscribe with `'edgeai/+/test/a'`. Send the three messages again.
   Write which messages each filter receives.

3. **QoS, retained message, last will (10 min).** In terminal 1:

   ```bash
   mosquitto_sub -h localhost -t 'edgeai/g07/#' -v -q 2 -d
   ```

   In terminal 2, send one message with each QoS level:
   `mosquitto_pub -h pi-07.local -t edgeai/g07/test/q -m x -q 2 -d`, then
   `-q 1` and `-q 0`. The option `-d` prints each packet. Write the packets
   of each level. Then send a retained message and start a new subscriber:

   ```bash
   mosquitto_pub -h pi-07.local -t edgeai/g07/test/state -m on -r
   mosquitto_sub -h pi-07.local -t edgeai/g07/test/state -v -C 1
   mosquitto_pub -h pi-07.local -t edgeai/g07/test/state -n -r     # delete it
   ```

   Last will: on the laptop, start a client with a will in the background,
   and end its process with no DISCONNECT packet:

   ```bash
   mosquitto_sub -h pi-07.local -t edgeai/g07/none -k 5 \
       --will-topic edgeai/g07/laptop/status --will-payload offline &
   kill -9 %1
   ```

   Terminal 1 shows `edgeai/g07/laptop/status offline` at once. Write the
   time that you see.

### Part B: telemetry (45 min)

1. **IMU readings with MicroPython (20 min).** Write the MicroPython firmware
   to the XIAO: steps 1 to 3 of `../hardware/HW-01/README.md` (as in the
   Day 2 lab). Change the four values of
   `../hardware/HW-07/micropython/config.py`. Then:

   ```bash
   mpremote connect PORT fs cp ../hardware/HW-01/board/lsm6ds3.py :lsm6ds3.py
   mpremote connect PORT fs cp ../hardware/HW-07/micropython/config.py :config.py
   mpremote connect PORT run ../hardware/HW-07/micropython/mqtt_imu.py
   ```

   On the laptop, count the messages for 30 s:

   ```bash
   python3 ../hardware/HW-07/host/mqtt_check.py --broker pi-07.local \
       --group g07 --seconds 30
   ```

   The table gives the messages, the lost messages, and the rate (nominal 5
   each second). Write the three values. Then remove the USB cable for 10 s
   and connect it again: write the size of the gap in `seq`.

2. **Keyword events with the Arduino sketch (25 min).** Open
   `sketches/kws_mqtt/kws_mqtt.ino` in the Arduino IDE. Add the ZIP library of
   your Day 5 project (`Sketch > Include Library > Add .ZIP Library`), and
   change the `#include` line to its header. Write the Wi-Fi password, the
   address of your Raspberry Pi, and your group in `arduino_secrets.h`.
   Select the board `XIAO_ESP32S3`, `Tools > PSRAM > OPI PSRAM`, and
   `Tools > Erase All Flash Before Sketch Upload > Enabled` (the MicroPython
   firmware must go). Upload, then set the erase option to `Disabled` again.

   The Serial Monitor (115200 baud) shows `MQTT: connecting to ...
   connected`. Say "yes" and "no". Each event prints a line
   `MQTT sent: {"seq":1,...}`. In terminal 1 of Part A, you see the events
   on `edgeai/g07/xiao/result` and one `stats` message each 10 s. Send a
   command by hand: `mosquitto_pub -h pi-07.local -t edgeai/g07/xiao/cmd -m
   led=1 -q 1`. The LED goes on. Write the number of events for 10 spoken
   words of each keyword.

### Part C: local decision (40 min)

1. **Task C1 (15 min).** Open `pi/decide.py` on the laptop. Complete the
   function `next_state`. The docstring gives the six rules of the state
   machine (states OFF, ON, FAULT). Copy the file to the Raspberry Pi:
   `scp pi/decide.py edge@pi-07.local:edgeai/day12/pi/`.

2. **Run the decision (15 min).** On the Raspberry Pi:

   ```bash
   cd ~/edgeai/day12/pi
   ~/yolo/bin/python decide.py --group g07
   ```

   The program prints `Task C1: complete`, then one line for each event
   and each change of state, for example:

   ```
   event   yes      score 0.91  seq 3
   state   OFF   -> ON     yes 0.91  command led=1  (0.20 ms)
   ```

   The time in brackets is the local time from the event to the command on
   the Raspberry Pi. Say "yes": the LED goes on. Say "no": the LED goes off.
   Say "yes" and wait 60 s: the LED goes off. Write the local times and the
   delay that you see from the word to the LED.

3. **A failed part (10 min).** Remove the USB cable of the XIAO. Write the
   seconds until `pi/decide.py` prints `-> FAULT  status offline` (the
   keep-alive of the sketch is 15 s). Connect the cable again: the state goes
   to OFF, and the program sends the command again.

### Part D: offline operation (35 min)

The instructor laptop runs the cloud broker at `X.10` (here `192.168.8.10`).

1. **Task D1 (5 min).** Open `cloud_check.py` on the laptop. Complete the
   function `count_sequence`.

2. **Start the two programs (10 min).** Keep `pi/decide.py` running. In a
   second SSH terminal on the Raspberry Pi:

   ```bash
   cd ~/edgeai/day12/pi
   ~/yolo/bin/python forwarder.py --group g07 --cloud 192.168.8.10 --reset
   ```

   It prints `Cloud broker: connected` and one line each 5 s, for example
   `queue     0  stored     12  forwarded     12  link up`. On the laptop:

   ```bash
   python3 cloud_check.py --broker 192.168.8.10 --group g07 --seconds 600
   ```

   It prints `Task D1: complete` and one line for each message of the group
   on the cloud broker.

3. **Cut the link (10 min).** In a third SSH terminal on the Raspberry Pi:

   ```bash
   bash ~/edgeai/day12/pi/link.sh down 192.168.8.10
   ```

   Now the Raspberry Pi cannot reach the cloud broker. All other traffic
   continues. During 3 minutes, say "yes" and "no": the LED must follow
   each word. After some seconds the forwarder prints `link lost`, and the
   queue grows. Write the queue length each minute.

4. **Restore the link (10 min).** Run `bash ~/edgeai/day12/pi/link.sh up
   192.168.8.10`. Write the seconds until the forwarder prints `connected`,
   and until the queue is 0 again. `cloud_check.py` marks the old messages
   with `late ... s`. Stop `cloud_check.py` with `Ctrl-C`: it prints a table
   for each topic and `RESULT: PASS - no lost message`. Copy the table into
   the report.

5. **Optional: the bridge of Mosquitto.** The Mosquitto bridge is a second
   way to the cloud with no program. Part 3 of the lecture gives the
   settings and the limit of its queue.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] `pi/decide.py` prints `Task C1: complete`, and `cloud_check.py` prints
      `Task D1: complete`.
- [ ] Live demonstration with the link connected: a spoken "yes" turns the
      LED on, "no" turns it off, and the decision appears on the cloud
      broker.
- [ ] Live demonstration with the link cut: the LED follows the keywords,
      and the queue of the forwarder grows.
- [ ] After the link returns, `cloud_check.py` prints `RESULT: PASS - no
      lost message`.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured
numbers, and name the trade-off.

Question of this lab: a cold store has five temperature sensors, a door
contact, and a fan. The cloud is behind a mobile modem, which loses the link
for up to 2 hours each day. Which decisions stay on the device? What does
each device send, how often, with which QoS, and which messages are
retained? How large must the queue of the forwarder be, and what happens
when it is full?

## Expected values

- Part B: `../hardware/HW-07/micropython/mqtt_imu.py` sends 5 messages each second (HW-07). The keyword
  sketch sends one message for each event: at most one each second, because
  of the suppression time of 1000 ms.
- Part C: the local time from the event to the command was below 1 ms on the
  work computer of the course. Your delay from the word to the LED also
  includes the window of the model (Day 5: 250 ms stride, the mean of 3
  windows) and the Wi-Fi.
- Part C: the broker sends the last will about 1.5 times the keep-alive
  after the last packet: about 22 s for the 15 s of the sketch. Mosquitto
  2.0.11 needed up to 3.6 s more in the lecture experiment. With the USB
  cable out, the board has no power, so the TCP connection does not close.
- Part D: `pi/decide.py` publishes one summary each 10 s, and the sketch one
  `stats` message each 10 s: about 12 messages each minute go into the
  queue. In a test on the work computer with a cut of 25 s, the forwarder
  sent its queue of 30 messages at once after the link came back, and the
  cloud got all messages: 0 lost, 0 double. A silent cut (the effect of
  `pi/link.sh`) needed 18.6 s until `link lost`, with the keep-alive of 10 s
  of the forwarder. Measure these values on the hardware of the lab.

## If a part does not work

| Problem | Fallback |
|---|---|
| A task is not complete in time | Use the file of the folder `solutions/`, and write this in the report |
| The Day 5 library is not on the laptop | Upload `../hardware/HW-07/sketches/mqtt_imu/` (its result is the axis with the largest acceleration), or send events by hand: `mosquitto_pub -h pi-07.local -t edgeai/g07/xiao/result -m '{"seq":1,"ms":0,"label":"yes","score":0.95}'`. Count `seq` up by hand. |
| MicroPython does not start | Skip step B1, and write this in the report. Part B2 needs the Arduino firmware. |
| The instructor broker does not answer | Use the Raspberry Pi of a second group as the cloud: `--cloud pi-MM.local`, and `cloud_check.py --broker pi-MM.local` |
| `pi/link.sh` reports an error | Ask the instructor to stop the cloud broker for 3 minutes. The forwarder sees a closed connection in place of a silent link. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| `Connection refused` from the laptop | The broker listens only on `127.0.0.1` | Copy `lab.conf` (step A1) and restart Mosquitto |
| The XIAO prints `failed, rc=-2` | A wrong broker address in `arduino_secrets.h`, or the broker does not run | Use the IP address of the Raspberry Pi (`hostname -I`), not `pi-NN.local` |
| `ImportError: no module named 'umqtt'` | The firmware has no `umqtt.simple` | `mpremote connect PORT mip install umqtt.simple` (needs the internet) |
| Two programs connect and disconnect again and again | Two clients use the same client ID | Each client needs its own ID. Stop the second copy of the program. |
| `pi/decide.py` changes nothing | Task C1 is not complete, or the score is below the threshold of 0.8 | Check the first line of the program. Speak nearer to the microphone. |
| `cloud_check.py` reports lost messages after a restart of `pi/decide.py` | The sequence numbers start again at 1 | Start `cloud_check.py` again after a restart of a program |
| The queue does not get smaller after the link is back | The forwarder waits for the next attempt (1 s to 5 s) | Wait 10 s. Check `bash link.sh show 192.168.8.10`: no `blackhole` line. |
| The LED does the opposite | The LED of the XIAO is on with LOW | The sketch already uses LOW for "on". Check that the sketch of Part B runs, not an old sketch. |

## Credits

This lab adapts material from these sources:

- Chapter 3.5 of "XIAO: Big Power, Small Board" by Lei Feng and Marcelo
  Rovai (github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook, GPL-3.0):
  telemetry and commands with MQTT, through the sketch of
  `Labs/hardware/HW-07/`.
- The sketch `xiaoml-kit_kws_oled.ino` of "XIAO ESP32S3 Sense" by Marcelo
  Rovai (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0), based on the
  example "esp32_microphone" of Edge Impulse: the microphone code, through
  the Day 5 sketch `kws_stream`. The changes are in `TEST_NOTES.md`.
- Eclipse Mosquitto (mosquitto.org, EPL-2.0 or EDL-1.0): the broker and its
  command-line clients.
- Eclipse Paho Python client (eclipse.dev/paho, EPL-2.0 or BSD-3-Clause):
  the MQTT client of the Python programs.

The programs `pi/decide.py`, `pi/forwarder.py`, `cloud_check.py`, and `pi/link.sh`,
the steps, and the report are new work of this course.
