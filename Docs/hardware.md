# Hardware list

This file lists the hardware of the course "AI on Edge Devices": the set of
one group, the items of the classroom, and the parts of each backup module.

The list has no totals, because the number of students is not known. A
group has two students. Multiply the set of one group by the number of
groups, and add the spare boards of Section 3.

## 1. The set of one group

Each group of two students needs this set for the 15 core days.

| Item | Quantity | Days | Notes |
|---|---|---|---|
| XIAOML Kit | 1 | 1 to 5, 9, 11, 12, 14, 15 | The XIAO ESP32S3 Sense (camera, microphone, 8 MB PSRAM, 8 MB flash) and the expansion board (6-axis IMU, OLED display). The kit also has a microSD card, a Wi-Fi antenna, and heat sinks. |
| USB-C data cable | 1 | The days of the kit | A cable for charging only does not work |
| Raspberry Pi 5, 8 GB | 1 | 7 to 15 | The reason for this model is below the table |
| Raspberry Pi active cooler | 1 | 7 to 15 | The Raspberry Pi 5 reduces its clock speed when it is hot |
| 27 W USB-C power supply | 1 | 7 to 15 | For the Raspberry Pi 5 |
| microSD card, 64 GB, class A2 | 1 | 7 to 15 | The instructor writes the cards before Day 7 (`Labs/hardware/HW-04/`) |
| Raspberry Pi Camera Module 3 | 1 | 7, 8, 11, 13, 14, 15 | |
| Camera cable for the Raspberry Pi 5 | 1 | The days of the camera | The Raspberry Pi 5 has a smaller camera connector than older models |
| Laptop | 1 | All days | Windows, macOS, or Linux. With a microphone for Day 5. `Labs/SETUP.md` gives the software. |

- Do not install the heat sinks on the XIAO. They do not fit under the
  expansion board.
- Connect the Wi-Fi antenna of the kit before the first Wi-Fi test.
- Day 6 uses no board. Day 13 uses the Raspberry Pi; the kit is optional
  there.


## 2. Small items for the core labs

Each classroom has most of these items. One of each is necessary for each
group.

| Item | Days | Notes |
|---|---|---|
| A bottle and a cup | 8, 13 | The two classes of the custom detector. A water bottle, a paper cup, or a mug is good. |
| An object that the detector does not know | 13 | For example a phone, a box, or a book |
| A desk lamp | 13 | For the dim light event. Not necessary if the light of the room can change. |
| USB power meter | 9, 15 | Optional. Between the power supply and the board. Without the meter, the students estimate the energy from data sheet values. |
| Ethernet cable | 11 | Optional, with one wired switch for the classroom. The video streams then do not share the Wi-Fi with the XIAO boards. |

## 3. The classroom

| Item | Quantity | Days | Notes |
|---|---|---|---|
| Dedicated Wi-Fi router | 1 | 7 to 15 |The router must have the 2.4 GHz band, and the client isolation must be off. `Labs/hardware/HW-09/README.md` gives all settings. Days 11 to 13 need direct traffic between the devices. |
| Instructor laptop with a Mosquitto broker | 1 | 12, 15 | The "cloud" broker, with a reserved address in the router |
| Spare XIAOML Kits | about 10 to 15 percent of the kits | All days | One spare kit runs the keyword spotting demonstration of Day 1 |
| Spare Raspberry Pi 5 boards, with cooler, power supply, card, and camera | about 10 to 15 percent of the boards | 7 to 15 | |
| Spare microSD card with the master image | 1 or more | 7 to 15 | Also the fallback of Day 10, if a card has no language models |
| microSD card reader | 1 | Before Day 7 | To write and to copy the cards |
| USB drive, or a shared folder | 1 | 5 to 9 | For the fallback files. `Docs/instructor_guide.md` has the list. |
| Wired switch | 1 | 11 | Optional, see Section 2 |

Label each kit, each Raspberry Pi, each card, and each cable with the group
number.

## 4. Parts for the backup modules

The syllabus (`Docs/SYLLABUS.md`, Section 6) describes each backup module.
Most modules need only the set of one group. This section lists the parts
that a module needs in addition.

Buy one set of parts for each group if you use a module as a class lab. One
set is enough for a demonstration by the instructor.

### 4.1 Parts

| Part | Modules | Notes |
|---|---|---|
| Arduino Nano 33 BLE Sense Rev2 with a micro-USB data cable | NB-1 to NB-11 | The modules NB-2, NB-3, NB-4, NB-8, and NB-9 need the IMU only. They also run on the Nano 33 BLE with no sensors. |
| OV7675 camera module | NB-6, NB-7 (and the camera test of NB-1) | A part of the Arduino Tiny Machine Learning Kit. With no shield, the camera needs 20 jumper wires (`Labs/hardware/HW-10/README.md`). |
| USB power meter | MC-9, NB-11 | Also for the energy measurement of Day 9 |
| Small LiPo battery for the XIAO | MC-9 | The expansion board of the kit has a battery connector (BAT+, BAT-) |
| Grove Vision AI V2 module with a camera | MC-11 | |
| Sensor and LED set | PI-7, GA-8, SY-9 (optional there) | See the list below |
| Smartphone | PI-8 | The phone of a student is good |
| USB microphone and small speaker | GA-7 | |
| M.2 accelerator module (MemryX MX3) | PI-5 | Optional. The module is theory. The part is for a demonstration by the instructor only. |

The sensor and LED set has these parts:

| Part | Quantity |
|---|---|
| DHT22 temperature and humidity sensor | 1 |
| BMP280 pressure and temperature sensor | 1 |
| LED (red, yellow, green) | 3 |
| Push button | 1 |
| Resistor, 4.7 kilohm | 2 |
| Resistor, 220 or 330 ohm | 3 |
| Breadboard | 1 |
| Jumper wires | 1 set |

### 4.2 Each module

"Board" is the board of the set of one group that the module uses. A module
of type T is a theory deck and needs no board. Type L is a lab, and T+L is
both.

| ID | Module | Type | Board | Extra parts |
|---|---|---|---|---|
| MC-1 | Arduino basics for Python users | L | XIAOML Kit | none |
| MC-2 | Sensor data logger on the SD card | L | XIAOML Kit | none |
| MC-3 | Spectral features for motion data | T+L | XIAOML Kit | none |
| MC-4 | Anomaly detection on motion data | L | XIAOML Kit | none |
| MC-5 | Keyword spotting features and training in Python | T+L | XIAOML Kit | none |
| MC-6 | FOMO object detection on the XIAOML Kit | L | XIAOML Kit | none |
| MC-7 | No-code deployment with SenseCraft AI | L | XIAOML Kit | none |
| MC-8 | Custom image dataset with the camera web server | L | XIAOML Kit | none |
| MC-9 | Low power: sleep modes and battery life | T+L | XIAOML Kit | USB power meter, small LiPo battery for the XIAO |
| MC-10 | Arm Cortex-M and CMSIS-NN | T | none | none |
| MC-11 | Grove Vision AI V2: vision with a neural processing unit | T+L | XIAOML Kit | Grove Vision AI V2 module with a camera |
| PI-1 | Custom image classification project | L | Raspberry Pi 5 | none |
| PI-2 | ExecuTorch with XNNPACK | T+L | Raspberry Pi 5 | none |
| PI-3 | SSD, EfficientDet, and FOMO comparison | L | Raspberry Pi 5 | none |
| PI-4 | Object counting application | L | Raspberry Pi 5 | none |
| PI-5 | Hardware accelerators for the Raspberry Pi | T | none | M.2 accelerator module (MemryX MX3), for a demonstration by the instructor only |
| PI-6 | Thermal throttling experiment | L | Raspberry Pi 5 | none |
| PI-7 | Physical computing: GPIO, sensors, actuators | L | Raspberry Pi 5 | sensor and LED set |
| PI-8 | YOLO inference in a mobile browser | T+L | Raspberry Pi 5 | smartphone |
| PI-9 | Instance segmentation with YOLO | L | Raspberry Pi 5 | none |
| PI-10 | Train a CNN and convert it to LiteRT | L | Raspberry Pi 5 | none |
| GA-1 | Retrieval-augmented generation at the edge | T+L | Raspberry Pi 5 | none |
| GA-2 | Vision-language models with Florence-2 | T+L | Raspberry Pi 5 | none |
| GA-3 | Agents and function calling | L | Raspberry Pi 5 | none |
| GA-4 | llama.cpp from source and multimodal inference | L | Raspberry Pi 5 | none |
| GA-5 | LiteRT-LM | L | Raspberry Pi 5 | none |
| GA-6 | Multi-token prediction and model selection | T+L | Raspberry Pi 5 | none |
| GA-7 | Voice pipeline: speech, language model, speech | L | Raspberry Pi 5 | USB microphone, small speaker |
| GA-8 | Language model for IoT control | L | Raspberry Pi 5 | sensor and LED set |
| GA-9 | Knowledge distillation from MNIST to language models | T+L | laptop only | none |
| GA-10 | Text generation with a small RNN | T+L | laptop only | none |
| GA-11 | Fine-tune a vision-language model | L | Raspberry Pi 5 | none. The training needs a GPU of Colab. |
| GA-12 | Agentic retrieval-augmented generation | L | Raspberry Pi 5 | none |
| SY-1 | Wi-Fi and HTTP on the XIAO | T+L | XIAOML Kit | none |
| SY-2 | MQTT security: authentication and TLS | T+L | XIAOML Kit and Raspberry Pi 5 | none |
| SY-3 | Model serving and tail latency | T | none | none |
| SY-4 | On-device learning and federated learning | T | none | none |
| SY-5 | Security and privacy of edge AI | T | none | none |
| SY-6 | Responsible and sustainable edge AI | T | none | none |
| SY-7 | Over-the-air update of the XIAO | L | XIAOML Kit | none |
| SY-8 | Containers on the Raspberry Pi | T+L | Raspberry Pi 5, and the board of a second group | none |
| SY-9 | Jupyter widget dashboard | L | Raspberry Pi 5 | sensor and LED set (optional) |
| SY-10 | Robust AI: faults, drift, and attacks | T | none | none |
| SY-11 | Model inference as a local web service | T+L | Raspberry Pi 5 | none |
| SY-12 | Bluetooth Low Energy from the XIAO to the Raspberry Pi | T+L | XIAOML Kit and Raspberry Pi 5 | none |
| NB-1 | Board setup and sensor tests | L | Nano 33 BLE Sense Rev2 | none |
| NB-2 | TensorFlow Lite Micro "hello world" and the tensor arena | L | Nano 33 BLE Sense Rev2 | none |
| NB-3 | Motion classification on the Nano 33 | L | Nano 33 BLE Sense Rev2 | none |
| NB-4 | Magic wand: gesture recognition with the IMU | L | Nano 33 BLE Sense Rev2 | none |
| NB-5 | Keyword spotting on the Nano 33 | L | Nano 33 BLE Sense Rev2 | none |
| NB-6 | Person detection with a camera | L | Nano 33 BLE Sense Rev2 | OV7675 camera module |
| NB-7 | Two models on one microcontroller | T+L | Nano 33 BLE Sense Rev2 | OV7675 camera module |
| NB-8 | The 256 KB budget: float and int8 on a Cortex-M4 | L | Nano 33 BLE Sense Rev2 | none |
| NB-9 | Bluetooth Low Energy gateway to MQTT | T+L | Nano 33 BLE Sense Rev2 and Raspberry Pi 5 | none |
| NB-10 | MicroPython on the Nano 33 | L | Nano 33 BLE Sense Rev2 | none |
| NB-11 | Power of an always-on device | L | Nano 33 BLE Sense Rev2 | USB power meter |
| NB-12 | Embedded hardware and software for TinyML | T | none | none |

These modules need no hardware:

| Modules | Content | What they need |
|---|---|---|
| SIM-1 to SIM-10 | Simulation warm-ups | A laptop with the Python packages `marimo` and `mlsysim` |
| TH-2 to TH-37 | Recap and theory modules | Nothing. A module with a notebook needs a laptop. |

**One full day with the Nano 33:** the modules NB-12 and MC-10 for the
theory, then NB-1, NB-2, and NB-5 for the lab. This day needs one Nano 33
BLE Sense Rev2 with its cable for each group. Only the camera test of NB-1
needs the camera module.


