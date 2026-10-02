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

## Software on the Raspberry Pi

`Labs/hardware/` prepares these tools. The versions below are the versions of
the test on the work computer (x86, 2026-10-01), or the version that a script
installs. The pilot records the versions on the Raspberry Pi.

| Tool | Version | Used on day | Where to get it | Folder |
|---|---|---|---|---|
| Raspberry Pi OS (64-bit) | record on the pilot | Days 7 to 15 | Raspberry Pi Imager | `HW-04` |
| Ollama | 0.32.6 on the work computer | Day 10 | `ollama.com/install.sh` | `HW-05` |
| MediaMTX | v1.21.1 | Day 11 | `github.com/bluenviron/mediamtx` | `HW-06` |
| Mosquitto | record on the pilot | Days 12 and 13 | `apt` | `HW-07` |
| Prometheus | 3.15.0 on the work computer. The `apt` version is older. | Day 13, option A | `apt` | `HW-08` |
| Grafana | 13.2.3 on the work computer | Day 13, option A | `apt.grafana.com` | `HW-08` |

## Python packages

`Labs/requirements.txt` lists the packages. Write the fixed version of each
package here after the pilot.

| Package | Version | Used on day |
|---|---|---|

The scripts of `Labs/hardware/` were tested on the work computer with these
versions (Python 3.10.12, 2026-10-01). They are not fixed versions.

| Package | Version in the test | Used by |
|---|---|---|
| `ai-edge-litert` | 2.2.0 | `HW-02` (check of the sine model) |
| `numpy` | 2.2.6 | `HW-02`, `HW-06` |
| `opencv-python-headless` | 5.0.0.93 | `HW-06` |
| `paho-mqtt` | 2.1.0 | `HW-07`, `HW-08`, `HW-09` |
| `psutil` | 7.2.2 | `HW-08` |
| `prometheus-client` | 0.26.0 | `HW-08` |
| `ollama` | 0.6.3 | `HW-05` |
| `pyserial` | 3.5 | `HW-01` (`check_rate.py --port`), `day02` (`logger.py --port`, tested with a simulated serial port) |
| `esptool`, `mpremote` | not tested | `day02`, `HW-01` (they need a board) |
| `torch` | 2.14.1 (CPU version) | `day01` (`model_budgets.ipynb`) |
| `torchvision` | 0.29.1 (CPU version) | `day01` |
| `matplotlib` | 3.10.9 | `day01`, `day02` (`dataset.ipynb`, `logger.py --plot`) |
| `nbconvert` | 7.17.1 | Run of the notebooks with no browser |
| `tensorflow-cpu` | 2.21.0 | `day03` (`motion_classifier.ipynb`: training and conversion), `day04` (`quantization.ipynb`: quantization and conversion to `int8`) |
| `keras` | 3.12.4 | `day03`, `day04` (installed with `tensorflow-cpu`) |
| `onnx`, `onnxruntime` | 1.23.1, 1.23.2 | Day 3 lecture (export from PyTorch) |

## Arduino board cores and libraries

| Core or library | Version | Board name (FQBN) | Used on day |
|---|---|---|---|
| esp32 by Espressif Systems | 3.3.12 | `esp32:esp32:XIAO_ESP32S3` | Days 1 to 5, 11, 12 |
| Arduino Mbed OS Nano Boards | 4.6.0 | `arduino:mbed_nano:nano33ble` | Nano 33 backup modules |
| Seeed Arduino LSM6DS3 | 2.0.7 | no board name | Days 1 to 5 |
| U8g2 by oliver | 2.36.19 | no board name | Days 1 to 5 |
| Harvard_TinyMLx | 1.2.4-Alpha | no board name | Nano 33 backup modules |
| Chirale_TensorFlowLite | 2.0.0 | no board name | Days 3 and 4 (`HW-02`, `HW-03`) |
| PubSubClient by Nick O'Leary | 2.8 | no board name | Day 12 (`HW-07`) |
| Arduino_BMI270_BMM150 | 1.2.4 | no board name | Nano 33 BLE Sense Rev2 (`HW-10`) |
| ArduinoBLE | 2.1.0 | no board name | Nano 33 module NB-4 (`HW-10`) |

Build options of the XIAO ESP32S3 (`HW-03`):

| Option | Board name (FQBN) |
|---|---|
| No PSRAM (default of the board) | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` |
| 8 MB PSRAM | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` |

The index of the esp32 core:
`https://espressif.github.io/arduino-esp32/package_esp32_index.json`

## Firmware and images

| Item | Version | Device | Used on day |
|---|---|---|---|
| MicroPython `SEEED_XIAO_ESP32S3` | v1.29.0 (2026-08-24) | XIAO ESP32S3 | Days 2 and 12 (`HW-01`) |

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

Sketches of `Labs/hardware/` (2026-10-01, XIAO ESP32S3, PSRAM disabled):

| Sketch | Folder | Flash | RAM |
|---|---|---|---|
| `tflm_hello` | `HW-02` | 336 157 bytes | 25 616 bytes |
| `memory_report` | `HW-03` | 274 217 bytes | 21 832 bytes |
| `arena_report` | `HW-03` | 332 077 bytes | 23 592 bytes |
| `mqtt_imu` | `HW-07` | 885 880 bytes | 47 744 bytes |

Sketches of `Labs/day01/` (2026-10-01, XIAO ESP32S3, PSRAM disabled):

| Sketch | Flash | RAM |
|---|---|---|
| `blink` | 271 701 bytes | 21 824 bytes |
| `imu_test` | 303 021 bytes | 23 352 bytes |
| `oled_test` | 304 165 bytes | 23 544 bytes |
| `mic_test` | 301 981 bytes | 21 944 bytes |
| `camera_test` (with OPI PSRAM) | 353 535 bytes | 33 472 bytes |

`Labs/day01/TEST_NOTES.md` gives the sizes for the two PSRAM options and for
the two examples of the core that the lab uses.

Sketches of `Labs/day03/` (2026-10-02, XIAO ESP32S3, PSRAM disabled):

| Sketch | Flash | RAM |
|---|---|---|
| `motion_classifier` (student version, tasks not complete) | 311 297 bytes | 26 616 bytes |
| `motion_classifier` (solution) | 364 005 bytes | 26 952 bytes |

Sketches of `Labs/day04/` (2026-10-02, XIAO ESP32S3, PSRAM disabled):

| Sketch | Flash | RAM |
|---|---|---|
| `motion_quant` (solution), `float32` model, `MODEL_INT8 0` | 382 785 bytes | 31 384 bytes |
| `motion_quant` (solution), `int8` model, `MODEL_INT8 1` | 379 701 bytes | 31 384 bytes |
| `motion_quant` (student version, tasks not complete), `MODEL_INT8 1` | 378 961 bytes | 31 384 bytes |

Sketch of `Labs/day02/` (2026-10-02, XIAO ESP32S3, PSRAM disabled):

| Sketch | Flash | RAM |
|---|---|---|
| `imu_data_collection` (fallback for Part B) | 301 381 bytes | 23 344 bytes |

`Labs/hardware/HW-10/README.md` gives the sizes of the eight examples for the
Nano 33 BLE Sense Rev2.

Use the option `--clean` after you change the version of a library. Without
it, `arduino-cli` can use old compiled files of the library.
