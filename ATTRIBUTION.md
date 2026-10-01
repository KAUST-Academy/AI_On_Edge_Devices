# Attribution and reuse log

The course "AI on Edge Devices" adapts material from open textbooks, open
books, and open code. This file records every reused item with its source and
its licence.

This repository has the licence GPL-3.0 (see `LICENSE`). A reused item keeps
the licence of its own source. Section 1 gives the licence of each source.

## 1. Sources and licences

| Source | Authors | Repository or site | Licence |
|---|---|---|---|
| Machine Learning Systems (book, slides, kit labs, simulation labs) | Vijay Janapa Reddi and contributors, Harvard University | `mlsysbook.ai`, `github.com/harvard-edge/cs249r_book` | CC BY-NC-SA 4.0 |
| Edge AI Engineering: Raspberry Pi (book text and figures) | Marcelo Rovai | `mjrovai.github.io/EdgeML_Made_Ease_ebook` | Not stated |
| EdgeML with Raspberry Pi (code) | Marcelo Rovai | `github.com/Mjrovai/EdgeML-with-Raspberry-Pi` | GPL-3.0 |
| TinyML Made Easy: XIAO ESP32S3 (book text and figures) | Marcelo Rovai | `mjrovai.github.io/TinyML_Made_Easy_XIAO_ESP32S3_ebook` | Not stated |
| XIAO ESP32S3 Sense (code) | Marcelo Rovai | `github.com/Mjrovai/XIAO-ESP32S3-Sense` | Apache-2.0 |
| XIAO: Big Power, Small Board (book and code) | Lei Feng (Seeed Studio) and Marcelo Rovai | `github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook` | GPL-3.0 |
| HarvardX TinyML courseware | Vijay Janapa Reddi, Laurence Moroney, Pete Warden, Lara Suzuki, and the TinyMLx team | `github.com/tinyMLx/courseware` | CC BY-NC-SA 4.0 |
| TinyMLx Arduino library | The TinyMLx team | `github.com/tinyMLx/arduino-library` | CC BY-NC-SA 4.0 |
| TensorFlow Lite Micro Arduino examples | The TensorFlow Authors | `github.com/tensorflow/tflite-micro-arduino-examples` | Apache-2.0 |
| Chirale_TensorFlowLite (Arduino library and its example) | Chirale and the TensorFlow Authors | `github.com/spaziochirale/Chirale_TensorFlowLite` | Apache-2.0 |
| Seeed Arduino LSM6DS3 (Arduino library) | Seeed Studio | `github.com/Seeed-Studio/Seeed_Arduino_LSM6DS3` | MIT |

Conditions:

- **CC BY-NC-SA 4.0.** Name the author. Non-commercial use only. Material that
  you adapt keeps this licence.
- **Apache-2.0.** Keep the licence notice and the copyright line in the file.
- **GPL-3.0.** The licence of this repository. Name the author.
- **MIT.** Name the author. Keep the copyright line with a copy of the code.
- **Not stated.** The text and the figures of the two books above carry no
  licence. The course uses them with attribution.

The licence of each repository above was read from its `LICENSE` file on
2026-10-01.

## 2. Rules

1. Add one row to Section 3 for each figure, code file, data file, or text
   block that comes from a source.
2. Name the source on the same frame of the deck, or in the same cell of the
   notebook, or in the first comment of the sketch.
3. Write the path inside the source repository, not a path on your computer.
4. Write what you changed. "none" means a copy with no change.
5. Copy the file into this repository. No file here points to a path outside
   this repository.
6. For an Apache-2.0 file, keep the licence header of the file.

## 3. Reused items

Each deck, lab, and module adds its rows here.

| File in this repository | Type | Source | Path in the source | Licence | Change |
|---|---|---|---|---|---|
| `Labs/SETUP.md` | text | Machine Learning Systems | `kits/contents/seeed/xiao_esp32s3/setup/setup.qmd` | CC BY-NC-SA 4.0 | sections 1, 2, and 3 follow the steps of the chapter, rewritten in short sentences |
| `Labs/hardware/HW-01/board/lsm6ds3.py` | code | Seeed Arduino LSM6DS3 | `LSM6DS3.h`, `LSM6DS3.cpp` | MIT | new MicroPython driver. Only the register addresses, the bit values, and the scale factors come from the library. |
| `Labs/hardware/HW-01/board/imu_stream.py` | code | Machine Learning Systems | `kits/contents/seeed/xiao_esp32s3/motion_classification/motion_classification.qmd` | CC BY-NC-SA 4.0 | new MicroPython script. The 50 Hz rate and the deadline method follow the data collection sketch of the chapter. |
| `Labs/hardware/HW-02/sketches/tflm_hello/tflm_hello.ino` | code | Chirale_TensorFlowLite | `examples/hello_world/hello_world.ino` | Apache-2.0 | own input values, one operator in place of all operators, prints the arena use and the latency, serial speed 115200 |
| `Labs/hardware/HW-02/sketches/tflm_hello/model.h` | data | Chirale_TensorFlowLite | `examples/hello_world/model.h` | Apache-2.0 | the same model bytes, written again by `tflite_to_header.py` |
| `Labs/hardware/HW-02/models/hello_world.tflite` | data | Chirale_TensorFlowLite | `examples/hello_world/model.h` | Apache-2.0 | the model bytes of the C array as a file |
| `Labs/hardware/HW-03/sketches/arena_report/arena_report.ino` | code | Chirale_TensorFlowLite | `examples/hello_world/hello_world.ino` | Apache-2.0 | arena on the heap or in the PSRAM, memory report, latency loop, no serial input |
| `Labs/hardware/HW-03/sketches/arena_report/model.h` | data | Chirale_TensorFlowLite | `examples/hello_world/model.h` | Apache-2.0 | copy of `HW-02/sketches/tflm_hello/model.h` |
| `Labs/hardware/HW-03/README.md` | text | Machine Learning Systems | `kits/contents/seeed/xiao_esp32s3/setup/setup.qmd` | CC BY-NC-SA 4.0 | the PSRAM setting and the memory sizes of the board |
| `Labs/hardware/HW-04/setup_pi.sh`, `check_pi.sh`, `README.md` | code, text | Machine Learning Systems | `kits/contents/raspi/setup/setup.qmd`, `kits/contents/raspi/llm/llm.qmd` | CC BY-NC-SA 4.0 | the install, camera, shutdown, and temperature commands of the chapters, in two scripts |
| `Labs/hardware/HW-04/setup_pi.sh` | code | Edge AI Engineering: Raspberry Pi | `raspi/setup/setup.html`, `raspi/image_classification/image_classification_fund.html`, `raspi/object_detection/cv_yolo.html`, `raspi/llm/slm_intro.html` | Not stated | the environment names and the package lists of the chapters |
| `Labs/hardware/HW-05/README.md`, `prompts.txt` | text | Machine Learning Systems | `kits/contents/raspi/llm/llm.qmd` | CC BY-NC-SA 4.0 | the published speed numbers and three prompts, with the source name |
| `Labs/hardware/HW-05/README.md` | text | EdgeML with Raspberry Pi | `A_Guide_to_Local_Inference/README.md` | GPL-3.0 | the model table of section 5.1, the RAM rule, and the token speed limit, with the source name |
| `Labs/hardware/HW-07/sketches/mqtt_imu/mqtt_imu.ino` | code | XIAO: Big Power, Small Board | `chapter_3-5.qmd` (Task 2 and Task 3) | GPL-3.0 | board ESP32S3, local broker, IMU in place of the DHT20 sensor, JSON payload, topic tree, last will, LED command, connection with no blocking loop |
| `Labs/hardware/HW-07/sketches/mqtt_imu/mqtt_imu.ino` | code | XIAO ESP32S3 Sense | `XIAOML_Kit_code/imu_test/imu_test.ino` | Apache-2.0 | the IMU object and the six read calls |
| `Labs/hardware/HW-07/micropython/mqtt_imu.py` | code | XIAO: Big Power, Small Board | `chapter_3-5.qmd` | GPL-3.0 | new MicroPython script that follows the telemetry and command design of the chapter |
| `Labs/hardware/HW-08/python_dashboard/dashboard.py` | code | EdgeML with Raspberry Pi | `SLMs_for_IoT_CONTROL/data_logger.py` | GPL-3.0 | new program. Only the idea of a CSV log with a header row comes from the source. |
| `Labs/hardware/HW-10/README.md` | text | HarvardX TinyML courseware | `edX/readings/4-2-3.pdf`, `4-2-5.pdf`, `4-2-13.pdf` | CC BY-NC-SA 4.0 | the install steps and the sensor test steps, rewritten in short sentences and changed for the Rev2 board |
| `Labs/hardware/HW-10/README.md` | text | TinyMLx Arduino library | `examples/`, `library.properties` | CC BY-NC-SA 4.0 | the list of the examples with their sensors and arena sizes |
| `LaTeX/images/day01/edge-device-deployment.pdf` | figure | Machine Learning Systems | `books/vol1/02_ml_systems/images/svg/_edge_ml_iot.svg` | CC BY-NC-SA 4.0 | SVG file converted to PDF, new file name |
| `LaTeX/images/day01/xiaoml-kit.png` | figure | Machine Learning Systems | `kits/contents/seeed/xiao_esp32s3/setup/images/png/kit_assembled.png` | CC BY-NC-SA 4.0 | none (new file name) |
| `LaTeX/images/day01/raspberry-pi-5.jpg` | figure | Machine Learning Systems | `kits/contents/raspi/setup/images/jpeg/r5-hardware.jpg` | CC BY-NC-SA 4.0 | none (new file name) |
| `LaTeX/sections/day01/block1.tex` | text | Machine Learning Systems | `slides/vol1/02_ml_systems/02_ml_systems.tex`, `books/vol1/02_ml_systems/02_ml_systems.qmd`, `kits/contents/platforms.qmd`, `kits/contents/raspi/setup/setup.qmd` | CC BY-NC-SA 4.0 | the latency, power, memory, and privacy numbers, the four paradigms, the four filters, and the board data, rewritten in short sentences. The product names of the cloud device and of the edge device are removed. The diagram of the three physical limits and the filter diagram are drawn again. |
| `LaTeX/sections/day01/block1.tex` | text | XIAO: Big Power, Small Board | `chapter_4-1.qmd` | GPL-3.0 | the terms, the cloud path and the edge path, and the five factors, rewritten in short sentences. The two diagrams are drawn again. |
| `LaTeX/sections/day01/block2.tex` | text | Machine Learning Systems | `slides/vol1/05_nn_computation/05_nn_computation.tex`, `slides/vol1/06_nn_architectures/06_nn_architectures.tex`, `slides/vol1/02_ml_systems/02_ml_systems.tex` | CC BY-NC-SA 4.0 | the example layers (784 to 128, 1024 to 1024), the comparison of ResNet-50 and MobileNetV2, the keyword spotting model, and the statement that the operation count does not give the speed, rewritten in short sentences. The example network, its numbers, and all diagrams are new. |

<!-- Example rows. Keep them in this comment.
| `LaTeX/images/day01/paradigms.pdf` | figure | Machine Learning Systems | `slides/vol1/02_ml_systems/images/paradigms.svg` | CC BY-NC-SA 4.0 | SVG file converted to PDF |
| `Labs/day03/sketches/imu_test/imu_test.ino` | code | XIAO ESP32S3 Sense | `XIAOML_Kit_code/imu_test/imu_test.ino` | Apache-2.0 | sampling rate changed to 50 Hz |
-->
