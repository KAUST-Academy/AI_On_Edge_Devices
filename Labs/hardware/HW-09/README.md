# HW-09: Lab network

Hardware status: not tested on hardware (prepared on 2026-10-01)

Needed by: the labs of Day 11 (RTSP), Day 12 (MQTT), and Day 13
(monitoring). Days 7 to 10 use the same network for SSH.

## Decision

| Topic | Decision |
|---|---|
| Network | One dedicated Wi-Fi router for the lab. KAUST Academy provides it. Not the campus Wi-Fi. |
| Wi-Fi name | `edgeai-lab`. One name for all bands, or a separate 2.4 GHz name if the XIAO does not connect. |
| Security | WPA2-Personal with one password for the course |
| Band | 2.4 GHz must be active. The XIAO ESP32S3 has 2.4 GHz Wi-Fi only. |
| Client isolation | **Off.** The devices must reach each other. |
| Addresses | DHCP for all devices. One reserved address for each Raspberry Pi. |
| Names | `pi-NN` for the Raspberry Pi of group `NN`, `xiao-gNN` as the MQTT client name of the XIAO |
| Internet | The router has an uplink for downloads. Day 12 Part D removes the uplink cable. |
| "Cloud" broker | The instructor laptop, with a reserved address |
| Test | `net_check.py` from a laptop to each Raspberry Pi |

Address plan. `X` is the network of the router, for example `192.168.8`:

| Device | Address | How |
|---|---|---|
| Router | `X.1` | Default of the router |
| Instructor laptop ("cloud" broker) | `X.10` | Reserved in the router |
| Raspberry Pi of group `NN` | `X.(100+NN)`, for example `X.107` for group 07 | Reserved in the router by the MAC address |
| XIAO boards and student laptops | `X.150` to `X.250` | DHCP pool |

The files of `HW-07` use `192.168.8.101` as the example for group 01. Change
the network part to the network of the real router.

Topic prefix of each group: `edgeai/gNN/`.

## Reason

- The syllabus says that Days 11 to 13 need direct traffic between devices,
  and that a campus network can block this traffic. A dedicated router gives
  the instructor control of this setting.
- The kit chapter states "2.4 GHz Wi-Fi" for the XIAO ESP32S3. A router that
  sends only on 5 GHz does not work for the kit.
- A campus Wi-Fi with a login for each user does not work for a
  microcontroller sketch that has only a network name and a password.
- The Arduino sketch and the MicroPython script of `HW-07` use the IP address
  of the broker. A reserved address stays the same for the full course, so a
  group changes its code one time only.
- The name `pi-NN.local` works from a laptop with no address list. It needs
  no DNS server. The Raspberry Pi OS sends this name with `avahi`.
- One removable uplink cable gives a clear "internet off" state for Day 12.
  The lab network continues to work, and this is the point of the lab.

## Sources

| Item | Source |
|---|---|
| Need for a dedicated router, firewall check, uplink for Part D | Syllabus, Days 11 and 12 (preparation notes) |
| 2.4 GHz Wi-Fi of the XIAO ESP32S3 | XIAOML Kit setup chapter of "Machine Learning Systems" |
| `hostname -I`, `ssh user@hostname.local` | Raspberry Pi setup chapter of "Machine Learning Systems" |
| Layer model, `ping`, Wi-Fi basics | `chapter_3-4.qmd` of "XIAO: Big Power, Small Board" |

The syllabus marks this preparation as "New". The script and the address plan
are new.

## Files

| File | Content |
|---|---|
| `net_check.py` | Checks the name, ping, the ports of the course, MQTT, and the throughput. Finds the devices of a network. |

## Router settings

Set these values in the web page of the router. The names of the menus
depend on the router model.

| Setting | Value | Reason |
|---|---|---|
| Wi-Fi name (SSID) | `edgeai-lab` | The files of the course use this name |
| Security | WPA2-Personal (AES) | The Arduino sketch and MicroPython support it |
| 2.4 GHz band | On, channel 1, 6, or 11, width 20 MHz | The XIAO needs 2.4 GHz |
| 5 GHz band | On, if the router has it | More capacity for laptops and for the Raspberry Pi |
| Client isolation (also "AP isolation", "guest mode") | Off | Devices must reach each other |
| DHCP pool | `X.150` to `X.250` | The addresses below 150 are for reserved devices |
| DHCP reservation | One for each Raspberry Pi and one for the instructor laptop | Fixed broker addresses |
| DHCP lease time | 24 hours or more | The addresses stay the same during a day |
| Multicast | On. "IGMP snooping" off if `.local` names fail. | The `.local` names use multicast |
| Captive portal, parental control, band steering | Off | These features block or move devices |
| Uplink (WAN) | Cable to the campus network | Remove it for Day 12 Part D |

If a wired switch is available, connect each Raspberry Pi with an Ethernet
cable. The video streams of Day 11 then do not share the Wi-Fi with the
XIAO boards. Write in the lab deck which connection the measurements used.

## Steps

### 1. Prepare the router (before Day 7)

1. Set the values of the table above.
2. Connect the instructor laptop. Reserve its address `X.10`.
3. Start each Raspberry Pi one time (`HW-04`, step 7). In the device list of
   the router, reserve the address `X.(100+NN)` for `pi-NN`.
4. Start each Raspberry Pi again. Confirm the address with `hostname -I`.
5. Print the address list. Put one copy on each table.

### 2. Check one Raspberry Pi from a laptop

```bash
python3 net_check.py pi-07.local
```

```
From laptop to pi-07.local
PASS  Name: pi-07.local is 192.168.8.107
PASS  Ping: 5 of 5 answers, mean 3.2 ms
PASS  Port    22 open:   SSH
INFO  Port  1883 closed: MQTT broker (Mosquitto, Days 12 and 13)
...
RESULT: PASS
```

The numbers in this example are not measured values.

- `PASS` for the name, for ping, and for port 22 is the minimum for Day 7.
- `INFO ... closed` means that the service does not run now.
- `--need 22 1883 8554` makes a closed port a `FAIL`. Use it before a lab
  that needs these services.

### 3. Check MQTT and the throughput

On the Raspberry Pi:

```bash
iperf3 -s
```

On the laptop:

```bash
python3 net_check.py pi-07.local --mqtt --iperf
```

The MQTT check needs `paho-mqtt` on the laptop and the broker of `HW-07`.
The throughput check needs `iperf3` on both devices.

### 4. Find the devices of the network (Day 11 Part A)

```bash
python3 net_check.py --scan 192.168.8.0/24
```

Other commands for the same task:

```bash
avahi-browse -art | grep -i "pi-"     # Linux: names that devices announce
ip neigh                               # Linux: devices that this computer saw
arp -a                                 # macOS and Windows
ping pi-07.local
```

### 5. Check the firewall of the lab computers

A laptop needs no open port to read a stream or to connect to a broker. It
needs an open port only when another device connects to it:

| Port | Service | Device that must accept it |
|---|---|---|
| 22 | SSH | Raspberry Pi |
| 1883 | MQTT broker | Raspberry Pi, and the instructor laptop |
| 8554 | RTSP (TCP). UDP transport also uses 8000 and 8001. | Raspberry Pi |
| 5201 | `iperf3` server | Raspberry Pi |
| 8080 | Python dashboard | Raspberry Pi |
| 3000, 9090 | Grafana, Prometheus | Raspberry Pi |
| 8888 | Jupyter | Raspberry Pi |
| 5353 (UDP) | `.local` names | All devices |
| 80 | MJPEG stream of the XIAO (Day 11 Part D) | XIAO |

Raspberry Pi OS has no active firewall by default. Check the instructor
laptop: port 1883 must accept connections from the lab network.

### 6. Internet off (Day 12 Part D)

1. Remove the uplink cable of the router.
2. `ping -c 3 1.1.1.1` on a laptop gives no answer.
3. `python3 net_check.py pi-07.local --mqtt` still gives `RESULT: PASS`.

## If a name with `.local` does not work

| Device | Check |
|---|---|
| Raspberry Pi | `systemctl is-active avahi-daemon` prints `active` |
| Linux laptop | The package `avahi-daemon` and `libnss-mdns` are installed |
| macOS | Works with no installation |
| Windows | Works on Windows 10 and later in most programs. If not, use the IP address. |
| Router | Multicast is on, client isolation is off |

The IP address always works. Use the printed address list.

## Result of the test on the work computer

One computer cannot test a network between two devices. The test checked the
script only, with the computer as its own target.

- Name, ping, and port checks: correct for open and closed ports.
- `--need` with a closed port gives `RESULT: FAIL` and the exit code 1.
- A name that does not exist gives `FAIL` and the exit code 1.
- `--mqtt`: round trip through a test broker.
- `--iperf`: the script reads the result of `iperf3`.
- `--scan`: tested on the loopback network `127.0.0.0/29`.

## Code status

| File | State | Change |
|---|---|---|
| `net_check.py` | new | tested on one Linux computer against itself. Not tested on macOS, on Windows, or between two devices. |

## Test steps for the instructor

- Date of the test:
- Router model and firmware version:
- Network of the router (`X`):

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Set the router (table "Router settings") | Each setting that the router does not have, and the name that the router uses for client isolation | |
| 2 | Connect one XIAO with the Arduino example `WiFiScan`, then with `mqtt_imu.ino` of `HW-07` | Does the XIAO see `edgeai-lab`? Seconds to connect. | |
| 3 | Run step 2 from a Linux, a macOS, and a Windows laptop | Does `pi-NN.local` work on each system? | |
| 4 | Run step 3 with the Raspberry Pi on Wi-Fi | Ping time, MQTT round trip, throughput in Mbit/s | |
| 5 | Run step 3 with the Raspberry Pi on Ethernet, if a switch is available | The same three values | |
| 6 | Start all Raspberry Pi boards. Run step 4. | Number of devices found. Is each `pi-NN` at `X.(100+NN)`? | |
| 7 | Run step 6 | Does the local system work with no uplink? Is the clock of the Raspberry Pi correct after a start with no internet? | |
| 8 | Connect the full number of devices of the class and run one RTSP stream for each group | Does the router stay stable? Throughput of one group during the load. | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the network `X`, the router model, and the address list in the
   instructor guide.
3. Change the example address `192.168.8.101` in `HW-07` if the network of
   the router is different.
4. Write the measured throughput in the Day 11 lab deck as the expected
   value.

## Credits

The network commands follow chapter 3.4 of "XIAO: Big Power, Small Board" by
Lei Feng and Marcelo Rovai
(github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook, GPL-3.0) and the
Raspberry Pi setup chapter of "Machine Learning Systems" by Vijay Janapa
Reddi and contributors (mlsysbook.ai, CC BY-NC-SA 4.0). The script is new.
