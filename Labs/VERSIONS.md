# Software versions and board names

The Day 1 pilot fixes the versions on the lab computers. The whole course then
uses the same versions. Each lab task adds the rows of its lab.

The rows below come from the compile check on the work computer of the course
(2026-10-01). No board was connected. The pilot confirms each version on a lab
computer.

## Software on the lab computer

| Tool | Version | Used on day | Where to get it |
|---|---|---|---|
| `arduino-cli` | 1.5.1 | optional, every day with a sketch | `github.com/arduino/arduino-cli` |

## Python packages

`Labs/requirements.txt` lists the packages. Write the fixed version of each
package here after the pilot.

| Package | Version | Used on day |
|---|---|---|

## Arduino board cores and libraries

| Core or library | Version | Board name (FQBN) | Used on day |
|---|---|---|---|
| esp32 by Espressif Systems | 3.3.12 | `esp32:esp32:XIAO_ESP32S3` | Days 1 to 5, 11, 12 |
| Arduino Mbed OS Nano Boards | 4.6.0 | `arduino:mbed_nano:nano33ble` | Nano 33 backup modules |
| Seeed Arduino LSM6DS3 | 2.0.7 | — | Days 1 to 5 |
| U8g2 by oliver | 2.36.19 | — | Days 1 to 5 |
| Harvard_TinyMLx | 1.2.4-Alpha | — | Nano 33 backup modules |

The index of the esp32 core:
`https://espressif.github.io/arduino-esp32/package_esp32_index.json`

## Firmware and images

| Item | Version | Device | Used on day |
|---|---|---|---|

## Compile check without a board

`arduino-cli` compiles a sketch with no board. A sketch that compiles is still
**not tested on hardware**.

```bash
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3 <sketch folder>
arduino-cli compile --fqbn arduino:mbed_nano:nano33ble --library <library folder> <sketch folder>
```

Result of the first check (2026-10-01):

| Sketch | Board | Flash | RAM |
|---|---|---|---|
| `imu_test` of the XIAOML Kit code | XIAO ESP32S3 | 302 941 bytes (9% of 3 342 336) | 23 352 bytes (7% of 327 680) |
| `test_IMU` of the TinyMLx library | Nano 33 BLE | 95 552 bytes (9% of 983 040) | 45 944 bytes (17% of 262 144) |
