# Hardware list

This file lists the hardware of the course "AI on Edge Devices": the set of
one group, and the items of the classroom.

A
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
