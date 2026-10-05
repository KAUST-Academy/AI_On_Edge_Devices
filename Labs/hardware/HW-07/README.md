# HW-07: MQTT from the XIAO ESP32S3 to a local broker


Needed by: the Day 12 lab (broker, telemetry, local decision, offline
operation). The Day 13 lab uses the same broker.

## Decision

| Topic | Decision |
|---|---|
| Broker | Mosquitto on the Raspberry Pi of each group, port 1883, no password on the closed lab network |
| Arduino library | PubSubClient 2.8 by Nick O'Leary |
| MicroPython library | `umqtt.simple` |
| Broker address in the board code | The IP address of the Raspberry Pi, not the name `pi-NN.local` |
| Payload | One JSON object with a sequence number `seq` |
| Topic tree | `edgeai/<group>/<device>/<channel>`, for example `edgeai/g07/xiao/imu` |
| Device state | A retained status topic with a last will message |

Topics of the XIAO:

| Topic | Direction | Payload |
|---|---|---|
| `edgeai/<group>/xiao/status` | board to broker | `online` or `offline`, retained |
| `edgeai/<group>/xiao/imu` | board to broker | `{"seq":12,"ms":34567,"ax":0.010,"ay":0.020,"az":0.990,"gx":0.10,"gy":0.20,"gz":0.30}` |
| `edgeai/<group>/xiao/result` | board to broker | `{"seq":12,"ms":34567,"label":"z","score":0.97}` (Arduino sketch only) |
| `edgeai/<group>/xiao/cmd` | broker to board | `led=1` or `led=0` |

## Reason

- The source chapter uses PubSubClient for telemetry and for commands. The
  course keeps this library, so the code of the chapter stays valid.
- The chapter uses a public broker on the internet. Day 12 teaches a system
  that works with no internet connection. The broker must then be in the lab
  network.
- One broker for each group gives each group a system that it controls. A
  group can stop its broker in Part D with no effect on other groups.
- The syllabus asks for a unique topic prefix for each group. The group
  number in the topic gives this prefix. A group can also read the messages
  of the instructor broker with the same tree.
- The Arduino core does not resolve a `.local` name in `WiFi` connections
  without more code. An IP address works in the Arduino sketch and in
  MicroPython. `HW-09` gives each Raspberry Pi a fixed address.
- The sequence number lets the laptop count the lost messages. The Day 12
  check is "no message is lost after the link returns".
- The last will message shows the state of the board with no polling. Day 12
  teaches this feature.

## Sources

| Item | Source |
|---|---|
| Telemetry sketch, command sketch, reconnection | `chapter_3-5.qmd` of "XIAO: Big Power, Small Board", Task 2 and Task 3 (GPL-3.0) |
| IMU code | `XIAOML_Kit_code/imu_test/imu_test.ino` of "XIAO ESP32S3 Sense" (Apache-2.0) |
| LED pin and its inverted logic | XIAOML Kit setup chapter of "Machine Learning Systems" |
| Broker settings | Mosquitto documentation (`mosquitto.org/man/mosquitto-conf-5.html`) |
| `umqtt.simple` | MicroPython library documentation (`github.com/micropython/micropython-lib`, folder `micropython/umqtt.simple`) |
| Python client | `paho-mqtt` documentation (version 2 API) |

## Files

| File | Runs on | Content |
|---|---|---|
| `mosquitto_lab.conf` | Raspberry Pi | Broker settings for the lab network |
| `sketches/mqtt_imu/mqtt_imu.ino` | XIAO (Arduino) | Sends IMU telemetry and a result. Receives the LED command. |
| `sketches/mqtt_imu/arduino_secrets.h` | XIAO (Arduino) | Wi-Fi name, password, broker address, group |
| `micropython/mqtt_imu.py` | XIAO (MicroPython) | Sends IMU telemetry. Receives the LED command. |
| `micropython/config.py` | XIAO (MicroPython) | Wi-Fi name, password, broker address, group |
| `host/mqtt_check.py` | laptop or Raspberry Pi | Prints the messages, counts lost messages, sends a command |

## Steps

### 1. Set up the broker (on the Raspberry Pi)

`setup_pi.sh` of `HW-04` installs Mosquitto. To install it by hand:

```bash
sudo apt install -y mosquitto mosquitto-clients
```

Permit connections from the lab network:

```bash
sudo cp mosquitto_lab.conf /etc/mosquitto/conf.d/lab.conf
sudo systemctl restart mosquitto
systemctl is-active mosquitto
```

You see `active`. Read the IP address of the Raspberry Pi:

```bash
hostname -I
```

### 2. Test the broker from the command line

Terminal 1 (subscribe to all topics of the group):

```bash
mosquitto_sub -h localhost -t 'edgeai/g07/#' -v
```

Terminal 2 (publish):

```bash
mosquitto_pub -h localhost -t edgeai/g07/test -m hello
```

Terminal 1 shows `edgeai/g07/test hello`. Then repeat terminal 2 on the
laptop with `-h pi-07.local`.

### 3. Arduino sketch

1. Install the library **PubSubClient** by Nick O'Leary in the Library
   Manager.
2. Open `sketches/mqtt_imu/mqtt_imu.ino`.
3. In the tab `arduino_secrets.h`, set the Wi-Fi name, the password, the IP
   address of the Raspberry Pi, and the group.
4. Upload. Open the Serial Monitor at 115200 baud.

You see `WiFi connected`, then `Attempting MQTT connection ... connected`,
then one JSON line each second.

### 4. MicroPython script

`HW-01` gives the firmware and the IMU driver. Change `micropython/config.py`.
Then copy the files and run the script:

```bash
mpremote connect PORT fs cp ../HW-01/board/lsm6ds3.py :lsm6ds3.py
mpremote connect PORT fs cp micropython/config.py :config.py
mpremote connect PORT run micropython/mqtt_imu.py
```

You see the IP address, then `Connected to the broker`.

If the board reports `ImportError: no module named 'umqtt'`, install the
module. The board must have a Wi-Fi connection with internet access:

```bash
mpremote connect PORT mip install umqtt.simple
```

### 5. Check the messages

```bash
python3 host/mqtt_check.py --broker pi-07.local --group g07 --seconds 30
```

The script prints each message and then a table:

```
topic                              messages     lost restarts   rate 1/s
edgeai/g07/xiao/imu                     150        0        0       5.00
RESULT: PASS - no gap in the sequence numbers
```

### 6. Send a command

```bash
python3 host/mqtt_check.py --broker pi-07.local --group g07 --send led=1
python3 host/mqtt_check.py --broker pi-07.local --group g07 --send led=0
```

The built-in LED of the XIAO goes on and off. The same command with the
Mosquitto tool:

```bash
mosquitto_pub -h pi-07.local -t edgeai/g07/xiao/cmd -m led=1
```

### 7. Test the last will

1. Subscribe: `mosquitto_sub -h pi-07.local -t 'edgeai/g07/xiao/status' -v`.
   You see `online`.
2. Remove the USB cable of the XIAO.
3. After 15 to 25 seconds, you see `offline`. The keep-alive time of the
   board is 15 seconds. The broker waits 1.5 times this time.

## Limits

- PubSubClient sends with quality of service 0 only. It can receive with
  quality of service 0 or 1. Its default message buffer is 256 bytes. The
  messages of the sketch are shorter than 160 bytes.
- The board code stores no message while the broker is away. A message that
  the board makes in that time is lost, and the `seq` field shows the gap.
  The store-and-forward part of Day 12 Part D runs on the Raspberry Pi,
  between the local broker and the instructor broker. The Day 12 lab task
  writes that part.
- `mosquitto_lab.conf` has no password. Use it only on the lab router.

## Result of the test on the work computer

No board was connected. The test used a broker on the work computer.

- `mqtt_imu.ino` compiles for the XIAO ESP32S3: 885 880 bytes of flash,
  47 744 bytes of static RAM (core 3.3.12, PubSubClient 2.8, Seeed Arduino
  LSM6DS3 2.0.7).
- `micropython/mqtt_imu.py` ran under Python on the work computer with
  stand-in modules for `machine`, `network`, and `umqtt.simple`. Result: 21
  messages in 4 seconds (5.00 each second), no gap, the command `led=1`
  arrived, and the broker sent `offline` after the script stopped. This test
  checks the logic of the script. It does not check the Wi-Fi, the sensor, or
  the real `umqtt.simple` module.
- `host/mqtt_check.py`: the sequence 1, 2, 5, 6, 0, 1 gives "2 lost,
  1 restart" and `RESULT: FAIL`. A wrong port gives a clear error. `--send`
  works.

## Code status

| File | State | Source | Change |
|---|---|---|---|
| `sketches/mqtt_imu/mqtt_imu.ino` | changed | Task 2 and Task 3 programs of `chapter_3-5.qmd` | Board ESP32S3. Local broker by IP address. IMU in place of the DHT20 sensor. JSON payload with `seq`. Topic tree `edgeai/<group>/xiao/`. Last will. LED command in place of the buzzer. One connection attempt each 5 seconds with no blocking loop. New function `publishResult()`. |
| `sketches/mqtt_imu/arduino_secrets.h` | new | no source | not tested |
| `micropython/mqtt_imu.py` | new | Design of the chapter | Logic tested with stand-in modules. Not tested on the board. |
| `micropython/config.py` | new | no source | not tested |
| `host/mqtt_check.py` | new | no source | tested on the work computer |
| `mosquitto_lab.conf` | new | Mosquitto documentation | not tested (the work computer has no Mosquitto broker) |

Compile check (no board):

| Sketch | Board name (FQBN) | Result | Date |
|---|---|---|---|
| `mqtt_imu` | `esp32:esp32:XIAO_ESP32S3` | compiles: 885 880 bytes flash, 47 744 bytes RAM | 2026-10-01 |

## Test steps for the instructor

- Date of the test:
- Mosquitto version (`mosquitto -h`), MicroPython version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run steps 1 and 2 | Does a laptop connect to the broker? The Mosquitto version. | |
| 2 | Run step 3 | Seconds from reset to the first message | |
| 3 | Run step 5 for 60 s with the Arduino sketch | Messages, lost, rate | |
| 4 | Run step 4 | Is `umqtt.simple` in the firmware? If not, does `mip install` work? | |
| 5 | Run step 5 for 60 s with the MicroPython script | Messages, lost, rate (nominal 5 each second) | |
| 6 | Run step 6 with both programs | Does the LED follow the command? Delay that you see. | |
| 7 | Run step 7 | Seconds until `offline` | |
| 8 | `sudo systemctl stop mosquitto` for 30 s, then start it | Does each program connect again? Seconds until the next message. Size of the `seq` gap. | |
| 9 | Switch the router off for 30 s, then on | The same values as step 8 | |
| 10 | Run two groups on one broker | Do the two topic trees stay separate? | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the Mosquitto version and the PubSubClient version in
   `Labs/VERSIONS.md`.
3. Put `mosquitto_lab.conf` on the master card (`HW-04`, step 4).
4. Write the measured reconnection time in the Day 12 lab deck.

## Credits

The Arduino sketch adapts chapter 3.5 of "XIAO: Big Power, Small Board" by
Lei Feng and Marcelo Rovai
(github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook, GPL-3.0). The IMU code
comes from "XIAO ESP32S3 Sense" by Marcelo Rovai
(github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0).
