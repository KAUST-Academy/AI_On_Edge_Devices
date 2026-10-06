# HW-09: Lab network

Needed by: the labs of Day 11 (RTSP), Day 12 (MQTT), and Day 13
(monitoring). Days 7 to 10 use the same network for SSH.

## Files

| File | Content |
|---|---|
| `net_check.py` | Checks the name, ping, the ports of the course, MQTT, and the throughput. Finds the devices of a network. |

## Router settings

Set these values in the web page of the router. The names of the menus
depend on the router model.

| Setting | Value |
|---|---|
| Wi-Fi name (SSID) | `edgeai-lab` | 
| Security | WPA2-Personal (AES) | 
| 2.4 GHz band | On, channel 1, 6, or 11, width 20 MHz | 
| 5 GHz band | On, if the router has it | 
| Client isolation (also "AP isolation", "guest mode") | Off | 
| DHCP pool | `X.150` to `X.250` | 
| DHCP reservation | One for each Raspberry Pi and one for the instructor laptop | 
| DHCP lease time | 24 hours or more | 
| Multicast | On. "IGMP snooping" off if `.local` names fail. | 
| Captive portal, parental control, band steering | Off | 
| Uplink (WAN) | Cable to the campus network |

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

1. Write the network `X`, the router model, and the address list in the
   instructor guide.
2. Change the example address `192.168.8.101` in `HW-07` if the network of
   the router is different.
3. Write the measured throughput in the Day 11 lab deck as the expected
   value.
