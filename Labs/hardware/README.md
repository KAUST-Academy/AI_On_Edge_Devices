# Hardware preparation

Each folder holds one hardware decision of the course: the decision, the
reason, the source, the code or the commands, and the test steps for the
instructor.

**No board was connected when this material was prepared (2026-10-01).** Each
folder has the line `Hardware status:` near the top of its `README.md`. The
instructor runs the test steps on the real hardware and then changes this
line.

## Index

| Folder | Decision | Board | Needed by |
|---|---|---|---|
| [`HW-01`](HW-01/README.md) | MicroPython v1.29.0 for `SEEED_XIAO_ESP32S3`, own IMU driver, 50 Hz with a deadline for each sample | XIAOML Kit | Day 2 |
| [`HW-02`](HW-02/README.md) | TensorFlow Lite Micro with the library Chirale_TensorFlowLite 2.0.0. Edge Impulse library for the kit labs. | XIAOML Kit | Days 3 and 5 |
| [`HW-03`](HW-03/README.md) | Build option `PSRAM=disabled` or `PSRAM=opi`. Arena size from `arena_used_bytes()`. | XIAOML Kit | Days 1, 3, and 4 |
| [`HW-04`](HW-04/README.md) | Raspberry Pi OS (64-bit), three Python environments, one master card that is copied | Raspberry Pi 5 | Days 7 and 8 |
| [`HW-05`](HW-05/README.md) | Ollama with `llama3.2:1b` and `llama3.2:3b` | Raspberry Pi 5 | Day 10 |
| [`HW-06`](HW-06/README.md) | MediaMTX v1.21.1 with the camera source, OpenCV reader, clock method for the latency | Raspberry Pi 5 | Day 11 |
| [`HW-07`](HW-07/README.md) | Mosquitto on each Raspberry Pi, PubSubClient (Arduino), `umqtt.simple` (MicroPython) | XIAOML Kit, Raspberry Pi 5 | Day 12 |
| [`HW-08`](HW-08/README.md) | Two options: Python dashboard (used now), Grafana with Prometheus (prepared). The instructor selects after the test. | Raspberry Pi 5 | Day 13 |
| [`HW-09`](HW-09/README.md) | Dedicated router, client isolation off, reserved addresses, names `pi-NN` | all | Days 11 to 13 |
| [`HW-10`](HW-10/README.md) | Core Arduino Mbed OS Nano Boards 4.6.0, library Harvard_TinyMLx 1.2.4-Alpha, switch `NANO33_BLE_REV2` | Nano 33 BLE Sense Rev2 | Modules NB-1 to NB-7 |

## Names that all folders use

| Item | Value |
|---|---|
| Wi-Fi name of the lab | `edgeai-lab` |
| User of each Raspberry Pi | `edge` |
| Host name of the Raspberry Pi of group `NN` | `pi-NN` (address `pi-NN.local`) |
| Group identifier | `gNN`, for example `g07` |
| MQTT topic tree | `edgeai/gNN/<device>/<channel>` |
| RTSP address | `rtsp://pi-NN.local:8554/cam` |
| Python environments on the Raspberry Pi | `~/tflite_env`, `~/yolo`, `~/ollama` |

## Order of work for the master card of the Raspberry Pi

1. `HW-09`: set the router.
2. `HW-04`: write the card, run `setup_pi.sh`.
3. `HW-05`: download the language models.
4. `HW-06`: install MediaMTX.
5. `HW-07`: set the Mosquitto broker.
6. `HW-08`: install Prometheus and Grafana, if the lab uses option A.
7. `HW-04`: run `check_pi.sh`, then copy the card.

## What "tested" means in these folders

| Text in a folder | Meaning |
|---|---|
| "compiles" | `arduino-cli` built the sketch for the board. No board ran it. |
| "tested on the work computer" | The script ran on a Linux computer with no board, with simulated input where necessary |
| "not tested" | The code did not run on the board |
| "tested on hardware (date)" | The instructor ran the test steps on the real board |

A number in a folder is from the compiler, from a source (with the source
name), or from a run on the work computer (with this label). All other
numbers are empty cells for the instructor.
