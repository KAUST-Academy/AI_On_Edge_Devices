# HW-07: MQTT from the XIAO ESP32S3 to a local broker

Needed by: the Day 12 lab (broker, telemetry, local decision, offline
operation). The Day 13 lab uses the same broker.

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

1. Write the Mosquitto version and the PubSubClient version in
   `Labs/VERSIONS.md`.
2. Put `mosquitto_lab.conf` on the master card (`HW-04`, step 4).
3. Write the measured reconnection time in the Day 12 lab deck.
