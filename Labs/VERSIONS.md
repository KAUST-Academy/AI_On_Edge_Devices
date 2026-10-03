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
| `iperf3` | 3.9 on the work computer; any version 3 | Day 11 | the package manager of the system, or `iperf.fr` |
| FFmpeg (`ffplay`) or VLC | FFmpeg 4.4 on the work computer | Day 11 | the package manager of the system |

## Software on the Raspberry Pi

`Labs/hardware/` prepares these tools. The versions below are the versions of
the test on the work computer (x86, 2026-10-01), or the version that a script
installs. The pilot records the versions on the Raspberry Pi.

| Tool | Version | Used on day | Where to get it | Folder |
|---|---|---|---|---|
| Raspberry Pi OS (64-bit) | record on the pilot | Days 7 to 15 | Raspberry Pi Imager | `HW-04` |
| Ollama | 0.32.6 on the work computer | Day 10 | `ollama.com/install.sh` | `HW-05` |
| MediaMTX | v1.21.1 | Day 11 | `github.com/bluenviron/mediamtx` | `HW-06` |
| Mosquitto | record on the pilot; 2.0.11 on the work computer (Day 12 tests) | Days 12 and 13 | `apt` | `HW-07` |
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
| `paho-mqtt` | 2.1.0 | `HW-07`, `HW-08`, `HW-09`, Day 12 lab (`decide.py`, `forwarder.py`, `cloud_check.py`), Day 13 lab (`pi/monitor.py`, `pi/alert.py`, `dashboard/dashboard.py`) |
| `psutil` | 7.2.2 | `HW-08`, Day 13 lab (`pi/monitor.py`: CPU, RAM, memory of the process) |
| `prometheus-client` | 0.26.0 | `HW-08` |
| `ollama` | 0.6.3 | `HW-05` |
| `pyserial` | 3.5 | `HW-01` (`check_rate.py --port`), `day02` (`logger.py --port`, tested with a simulated serial port) |
| `esptool`, `mpremote` | not tested | `day02`, `HW-01` (they need a board) |
| `torch` | 2.14.1 (CPU version) | `day01` (`model_budgets.ipynb`) |
| `torchvision` | 0.29.1 (CPU version) | `day01` |
| `matplotlib` | 3.10.9 | `day01`, `day02` (`dataset.ipynb`, `logger.py --plot`) |
| `nbconvert` | 7.17.1 | Run of the notebooks with no browser |
| `tensorflow-cpu` | 2.21.0 | `day03` (`motion_classifier.ipynb`: training and conversion), `day04` (`quantization.ipynb`: quantization and conversion to `int8`), `day06` (`compression.ipynb`: pruning, distillation, and quantization) |
| `keras` | 3.12.4 | `day03`, `day04` (installed with `tensorflow-cpu`) |
| `onnx`, `onnxruntime` | 1.23.1, 1.23.2 | Day 3 lecture (export from PyTorch) |
| `torch`, `torchvision` in the environment of the Day 7 lab | 2.13.0, 0.28.0 (CPU versions) | `day07` (`export_inspect.ipynb`). The package `litert-torch` selects these versions, so this lab has its own environment and its own file `Labs/day07/requirements.txt`. |
| `litert-torch` | 0.9.4 | `day07` (export from PyTorch to LiteRT) |
| `onnxscript` | 0.7.2 | `day07` (`torch.onnx.export` with `dynamo=True`) |
| `onnx`, `onnxruntime` | 1.23.1, 1.23.2 | `day07` (`export_inspect.ipynb`, `pi/bench.py`, and the file `models/mnv2_int8.onnx`) |
| `ai-edge-litert` | 2.2.0 | `day07` (`pi/classify_image.py`, `pi/bench.py`) |
| `ai-edge-quantizer` | 0.9.0 | `day07` (the file `models/mnv2_int8.tflite`) |
| `pillow` | 12.3.0 | `day07` (`pi/classify_image.py`) |
| `ipykernel`, `jupyter-client` | 6.31.0, 8.6.3 | `day07`: the newest versions that `litert-torch` 0.9.4 accepts |
| `notebook`, `netron` | 7.6.3, 9.3.0 | `day07` (the notebook, and the viewer for model files) |
| `ncnn`, `pnnx` | 1.0.20260526, 20260526 | Day 7 lecture. The lab does not need them. |
| `ultralytics` | 8.4.171 (fixed in `Labs/day08/requirements.txt` and in `Labs/hardware/HW-04/setup_pi.sh`) | `day08` (training, export, and all scripts of `pi/`). The export arguments `format=litert` and `quantize=8` are the arguments of this version. |
| `torch`, `torchvision` in the environment of the Day 8 lab | 2.13.0, 0.28.0 (CPU versions) | `day08` (`train_detector.py`, `custom_detector.ipynb`). The package `litert-torch` selects these versions, so this lab has its own environment and its own file `Labs/day08/requirements.txt`. |
| `litert-torch`, `ai-edge-quantizer`, `ai-edge-litert` | 0.9.4, 0.9.0, 2.2.0 | `day08` (export of the detector to LiteRT in `float32` and in `int8`, and the validation of the files) |
| `ncnn`, `pnnx` | 1.0.20260526, 20260526 | `day08` (export of the detector to NCNN, and `pi/detect_yolo.py`, `pi/live_detect.py`, `pi/bench_detect.py` with an NCNN folder) |
| `onnx`, `onnxslim` | 1.23.1, 0.1.97 | `day08` (the export of the package uses them) |
| `opencv-python`, `pillow`, `numpy` | 5.0.0.93, 12.3.0, 2.2.6 | `day08` (installed with `ultralytics`) |
| `notebook`, `ipykernel`, `jupyter-client` | 7.6.3, 6.31.0, 8.6.3 | `day08`: the same limits as in the Day 7 lab |
| `flask` | 3.1.3 | `day08` (`pi/live_detect.py`: the web page of the live image) |
| `torch`, `torchvision` in the test of the scripts of `pi/` | 2.14.1, 0.29.1 (CPU versions) | `day08`: the scripts for the board ran on the work computer in a second environment, with the files that the notebook exported |
| `ai-edge-litert`, `onnxruntime`, `ncnn`, `numpy` | 2.2.0, 1.23.2, 1.0.20260526, 2.2.6 | `day09` (`pi/bench.py`: the three runtimes of the benchmark harness). `pi/make_report.py` needs no package. |
| `ollama` (Python library), `pydantic` | 0.6.3, 2.13.5 | `day10` (all scripts). The models `llama3.2:1b`, `llama3.2:3b`, `nomic-embed-text`, and `llava-phi3:3.8b` of the Ollama library, read on 2026-10-03. |
| `opencv-python`, `ultralytics` in the Day 8 environment | 5.0.0.93, 8.4.171 | `day11` (`stream_detect.py`: the reader with `cv2.CAP_PROP_N_THREADS` and the Day 8 detector). `mjpeg_rate.py` needs no package. |
| `ultralytics`, `ncnn`, `opencv-python`, `flask` in `~/yolo` | 8.4.171, 1.0.20260526, 5.0.0.93, 3.1.3 | `day13` (`pi/monitor_detect.py`: the Day 8 detector with an NCNN folder, the statistics of a frame, and the Day 8 web page with `--web`). `pi/reference.py` needs no package. |

## Arduino board cores and libraries

| Core or library | Version | Board name (FQBN) | Used on day |
|---|---|---|---|
| esp32 by Espressif Systems | 3.3.12 | `esp32:esp32:XIAO_ESP32S3` | Days 1 to 5, 11, 12 |
| Arduino Mbed OS Nano Boards | 4.6.0 | `arduino:mbed_nano:nano33ble` | Nano 33 backup modules |
| Seeed Arduino LSM6DS3 | 2.0.7 | no board name | Days 1 to 5 |
| U8g2 by oliver | 2.36.19 | no board name | Days 1 to 5, 12 |
| Harvard_TinyMLx | 1.2.4-Alpha | no board name | Nano 33 backup modules |
| Chirale_TensorFlowLite | 2.0.0 | no board name | Days 3, 4, and 9 (`HW-02`, `HW-03`) |
| PubSubClient by Nick O'Leary | 2.8 | no board name | Day 12 (`HW-07`, `Labs/day12/sketches/kws_mqtt`) |
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

Sketches of `Labs/day05/` (2026-10-02, XIAO ESP32S3, OPI PSRAM): `kws_stream`
and `image_classifier` need the Arduino library of an Edge Impulse project.
They compile with a replacement for that library, so this file gives no
size. The kit lab of the source names the core 2.0.17 for these libraries.
Nobody built a real library with the core 3.3.12.

Sketch of `Labs/day09/` (2026-10-02, XIAO ESP32S3, OPI PSRAM):

| Sketch | Flash | RAM |
|---|---|---|
| `kit_bench` (student version, Task B1 not complete) | 944 575 bytes | 24 692 bytes |
| `kit_bench` (solution) | 944 679 bytes | 24 692 bytes |
| `kit_bench` (solution), PSRAM disabled | 939 421 bytes | 24 208 bytes |

The four models of this sketch have 567 540 bytes of the program.

Sketch of `Labs/day02/` (2026-10-02, XIAO ESP32S3, PSRAM disabled):

| Sketch | Flash | RAM |
|---|---|---|
| `imu_data_collection` (fallback for Part B) | 301 381 bytes | 23 344 bytes |

`Labs/hardware/HW-10/README.md` gives the sizes of the eight examples for the
Nano 33 BLE Sense Rev2.

Use the option `--clean` after you change the version of a library. Without
it, `arduino-cli` can use old compiled files of the library.
