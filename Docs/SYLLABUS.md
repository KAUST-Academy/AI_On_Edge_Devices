# AI on Edge Devices: Course Syllabus

## 1. Course summary
### Description

This course teaches how to run deep learning models on devices with small memory, low power, and no reliable cloud connection.
Students optimize models, deploy them on a microcontroller and on a Linux single-board computer, connect the devices, and monitor them.
The course ends with a team project that combines all parts into one working system.



### Prerequisites

- Understanding of deep learning and model development
- Experience with Python
- Basic use of the Linux command line
- Earlier contact with computer vision is an advantage

### Course learning outcomes

At the end of the course, a student can:

1. Select a deployment paradigm (cloud, edge, mobile, TinyML) from latency, memory, power, and privacy constraints.
2. Collect and prepare sensor data from a microcontroller.
3. Convert a trained model and deploy it on a microcontroller with TensorFlow Lite Micro.
4. Apply quantization, pruning, and knowledge distillation, and measure the effect on accuracy, size, and latency.
5. Run and optimize vision models on a Raspberry Pi with different inference runtimes.
6. Benchmark latency, memory, and energy with a correct method.
7. Run a small language model on a Raspberry Pi and use it in an application.
8. Connect edge devices with RTSP and MQTT, and make decisions locally without the cloud.
9. Monitor a deployed system and design an edge AI system for production.

### Hardware platforms

| Board | Class | Used for |
|---|---|---|
| XIAOML Kit (Seeed XIAO ESP32S3 Sense with expansion board) | Microcontroller with Wi-Fi, 8 MB PSRAM, camera, microphone, IMU, display | MicroPython, motion, keyword spotting, vision, MQTT |
| Raspberry Pi 5 (8 GB) | Linux single-board computer | Inference runtimes, object detection, language models, RTSP, broker, monitoring |

---

## 2. Daily format

Each day has about 6 contact hours. The order of the activities can change when a topic needs the hardware earlier.

| Activity | Duration | Content |
|---|---|---|
| Theory Part 1 | 50 min | Main concept of the day |
| Break | 10 min | |
| Theory Part 2 | 50 min | Methods and tools |
| Break | 10 min | |
| Theory Part 3 | 50 min | Design trade-offs and lab briefing |
| Recap | 10 min | Questions and summary |
| Lab work | 150 min | Students work in groups. Each lab has two to four parts: Part A to Part D. |
| Lab check | 30 min | Demonstration to the instructor and Decision Log |

Each theory part has one short exercise of 5 to 10 minutes.

Each day has two slide decks: one theory deck and one lab deck.
Each lab has a notebook, a sketch folder, or both.

### How to use the backup modules

Section 6 lists the backup modules. A backup module is a short, independent unit: one slide deck, one lab, or both.
Each module has its own deck file and its own lab folder, so you can present it alone or add it to a day.
Each day section names the backup modules that fit that day.

Use a backup module when:

- A group completes the core lab early.
- A core lab fails because of hardware, network, or cloud service problems.
- The class needs more depth, or less depth, on a topic.
- The class needs a recap of a machine learning or deep learning topic. Section 6.7 has one module for each topic.
- You want to replace a lab part with a different application.

---

## 3. Hardware and software

### Hardware for one group (two students)

| Item | Quantity | Notes |
|---|---|---|
| XIAOML Kit | 1 | XIAO ESP32S3 Sense, expansion board (6-axis IMU, OLED display), microSD card. Needs a USB-C data cable. |
| Raspberry Pi 5, 8 GB | 1 | See the reason below |
| Raspberry Pi active cooler | 1 | The Raspberry Pi 5 reduces its clock speed when it is hot |
| 27 W USB-C power supply | 1 | |
| microSD card, 64 GB, class A2 | 1 | The instructor flashes the cards before Day 7 |
| Raspberry Pi Camera Module 3 | 1 | |
| Camera cable for the Raspberry Pi 5 | 1 | The Raspberry Pi 5 has a smaller camera connector than older models |

**Why the Raspberry Pi 5 with 8 GB:** it runs YOLO at a usable frame rate, it can encode an RTSP stream and run inference at the same time, and it can run a small language model.

### Hardware for backup modules

| Item | Used by |
|---|---|
| Arduino Nano 33 BLE Sense Rev2 with a micro-USB data cable | Modules NB-1 to NB-12 |
| OV7675 camera module (part of the Arduino Tiny Machine Learning Kit) | Modules NB-6 and NB-7 |
| USB power meter | Day 9 energy measurement, modules MC-9 and NB-11 |
| DHT22 sensor, BMP280 sensor, three LEDs, one push button, resistors, breadboard, jumper wires | Modules PI-7, GA-8, and SY-9 |
| USB microphone and small speaker | Module GA-7 |
| Small LiPo battery for the XIAO | Module MC-9 |
| Grove Vision AI V2 module with a camera | Module MC-11 |
| Smartphone | Module PI-8 |

Buy one set for each group if you plan to use a module as a class lab. One set is enough for an instructor demonstration.

### Hardware for the classroom

- One dedicated Wi-Fi router. Days 11 to 13 need direct traffic between devices.
- Spare boards: about 10 to 15 percent of each type.
- One microSD card reader.

### Software

| Area | Tools |
|---|---|
| Microcontroller development | Arduino IDE 2, "esp32" core by Espressif. For the Nano 33 modules: "Arduino Mbed OS Nano Boards" core and the Harvard_TinyMLx library. |
| MicroPython | MicroPython firmware for the ESP32-S3, `mpremote` or Thonny |
| Training | Python 3.10 or later, PyTorch, Keras with the LiteRT converter, Ultralytics |
| Conversion and runtimes | ONNX, ONNX Runtime, LiteRT (TensorFlow Lite), TensorFlow Lite Micro, NCNN, ExecuTorch (optional), Netron |
| Data collection | Edge Impulse Studio account and Edge Impulse CLI |
| Generative AI | Ollama and the Ollama Python library. llama.cpp and LiteRT-LM for backup modules. |
| Networking | Mosquitto, `paho-mqtt`, PubSubClient, MediaMTX, FFmpeg, OpenCV, `iperf3` |
| Monitoring | Grafana with Prometheus. Fallback: a Python dashboard. |
| Optional simulation labs | `marimo` and `mlsysim` (interactive labs from the book) |

Fix the exact software versions during the Day 1 pilot. Use the same versions for the full course.

Training labs use small models. They run on a laptop CPU or on the free tier of Google Colab.

---

## 4. Course overview

Material status: **Adapt** means that a source covers the topic. **New** means that you must write the material. **Mixed** means both.

### Week 1: Foundations and TinyML on the XIAOML Kit

| Day | Title | Board |
|---|---|---|
| 1 | Edge AI landscape and system constraints | XIAOML Kit |
| 2 | Embedded systems, MicroPython, and sensor data collection | XIAOML Kit |
| 3 | From trained model to microcontroller | XIAOML Kit |
| 4 | Quantization | XIAOML Kit |
| 5 | Audio and vision on microcontrollers | XIAOML Kit |

### Week 2: Optimization and Linux-class edge devices

| Day | Title | Board |
|---|---|---|
| 6 | Pruning, distillation, and efficient design | Laptop only |
| 7 | Hardware acceleration and inference runtimes | Raspberry Pi |
| 8 | Object detection at the edge | Raspberry Pi |
| 9 | Benchmarking and profiling | Both |
| 10 | Generative AI at the edge | Raspberry Pi |

### Week 3: Connected systems and production

| Day | Title | Board |
|---|---|---|
| 11 | Networking fundamentals and RTSP streaming | Both |
| 12 | Local decision-making and MQTT | Both |
| 13 | Monitoring, logging, and visualization | Raspberry Pi |
| 14 | Production edge AI design and capstone start | Both |
| 15 | Capstone build and demonstrations | Both |

---

## 5. Daily plan

## Week 1: Foundations and TinyML on the XIAOML Kit

### Day 1: Edge AI landscape and system constraints

**Learning outcomes**

- Explain the four deployment paradigms and the constraints that separate them.
- Estimate the parameters, the operations, and the peak activation memory of a model.
- Decide from flash and RAM numbers if a model fits a device.
- Set up the toolchain and test each sensor of the XIAOML Kit.

**Theory**

- *Part 1: Why inference moves to the edge.* Course overview. Latency, bandwidth, privacy, cost, and availability. Cloud, edge, mobile, and TinyML paradigms. Comparison of the two course boards with a typical Cortex-M4 microcontroller and with a cloud GPU.
  - *Exercise:* for three applications, select a paradigm and state the constraint that decides.
- *Part 2: Deep learning recap from a cost view.* Cost of each layer type. Parameters, operations, and activation memory are three different budgets. Efficient blocks: depthwise separable convolution and inverted residual.
  - *Exercise:* calculate the parameters and the output size of three layers by hand.
- *Part 3: The edge AI workflow.* Data, training, optimization, conversion, deployment, monitoring. Hybrid architectures. Course map. Live demonstration of keyword spotting on the XIAOML Kit.
  - *Exercise:* predict which of three models fits in 256 KB of RAM.

**Lab**

- *Goal:* a working toolchain and a first resource budget for each device class.
- *Board:* XIAOML Kit.
- *Part A (50 min): Toolchain.* Install the Arduino IDE, the esp32 core, and the Python environment. Run Blink.
- *Part B (45 min): Sensor tests.* Test the IMU, the microphone, the camera, the display, and Wi-Fi with the kit test sketches.
- *Part C (55 min): Model budgets.* In a notebook, profile three models (MobileNetV2, ResNet-18, a small depthwise CNN). Report parameters, operations, and peak activation memory. Fill a table for four budgets: a 256 KB microcontroller, the XIAO without PSRAM, the XIAO with PSRAM, and the Raspberry Pi 5.
- *Deliverable:* the completed table and a Decision Log.
- *Check:* all five sensor tests pass, and the table gives a reason for each "fits" or "does not fit".

**Preparation notes**

- Install the software on the lab computers before the course. Test the USB driver for the XIAO.
- Label each kit and each cable with the group number.
- Do not install the heat sink on the XIAO. The heat sink does not fit under the expansion board.
- Prepare the keyword spotting demonstration on one kit.

**Backup modules:** MC-1 (Arduino basics), MC-10 (Cortex-M and CMSIS-NN), SIM-1 (Iron Law simulation), NB-1 (Nano 33 setup).

**Recap modules:** TH-2 (PyTorch basics), TH-3 (ML workflow), TH-4 (cost of neural network computation), TH-7 (linear algebra and tensors), TH-9 (machine learning paradigm), TH-13 (neurons, layers, and the forward pass), TH-14 (activation functions), TH-20 (depth and skip connections), TH-23 (convolution), TH-24 (CNN architectures), TH-33 (computer architecture essentials).

---

### Day 2: Embedded systems, MicroPython, and sensor data collection

**Learning outcomes**

- Describe the memory, the clock, and the buses of a microcontroller.
- Select a sampling rate and a window length for a sensor signal.
- Write a MicroPython program that reads a sensor and sends the data.
- Build a labelled dataset with a correct split between training and test data.

**Theory**

- *Part 1: Microcontroller anatomy.* Flash, RAM, PSRAM, clock, GPIO, ADC, I2C, SPI, I2S, UART. Interrupts and timers. Power modes.
  - *Exercise:* read a data sheet extract and find the RAM, the flash, and the bus of each sensor.
- *Part 2: Sensors and sampling.* IMU, microphone, camera. Sampling rate, aliasing, windows, buffers. MicroPython and C++: when to use each.
  - *Exercise:* select the sampling rate and the window for three signals (gesture, speech, vibration).
- *Part 3: Sensor data engineering.* Collection protocol, labels, class balance. Data leakage between overlapping windows. Dataset versions and data quality.
  - *Exercise:* find the leakage error in a given dataset split.

**Lab**

- *Goal:* a labelled motion dataset that Day 3 uses.
- *Board:* XIAOML Kit.
- *Part A (40 min): MicroPython start.* Flash MicroPython. Use the REPL, GPIO, a timer, and an I2C scan.
- *Part B (50 min): Sensor input.* Read the IMU over I2C at a fixed sampling rate. Send the samples to the laptop over the serial port and over Wi-Fi.
- *Part C (40 min): Dataset.* Write a Python logger that stores samples in CSV files with labels. Record four motion classes. Split the data by recording session.
- *Part D (20 min): Edge Impulse.* Upload the same data to Edge Impulse Studio and inspect it.
- *Deliverable:* the dataset and a short data card (classes, duration, sampling rate, split).
- *Check:* the sampling rate is constant, and no recording session is in both the training set and the test set.

**Preparation notes**

- Write and test a MicroPython driver for the kit IMU (LSM6DS3TR-C) before the course. The sources give Arduino code only.
- MicroPython replaces the Arduino firmware. Show students how to upload an Arduino sketch again for Day 3.
- Keep the Arduino data collection sketch from the kit lab as the fallback for Part B.
- Prepare a fallback dataset for groups that do not finish.

**Backup modules:** MC-1 (Arduino basics), MC-2 (SD card data logger), NB-10 (MicroPython on the Nano 33), NB-12 (embedded hardware and software).

**Recap modules:** TH-6 (data selection), TH-10 (datasets and generalization), TH-26 (signals in time and frequency).

---

### Day 3: From trained model to microcontroller

**Learning outcomes**

- Explain the TensorFlow Lite Micro interpreter, the operator resolver, and the tensor arena.
- Convert a Keras model and a PyTorch model to the LiteRT format.
- Extract spectral features from a time series.
- Deploy a model on a microcontroller and measure arena size, flash use, and latency.

**Theory**

- *Part 1: Deployment formats and conversion.* Keras to LiteRT. PyTorch to ONNX to LiteRT. FlatBuffers. Operator support and conversion errors.
  - *Exercise:* open a LiteRT file in Netron and list its operators and tensor types.
- *Part 2: TensorFlow Lite Micro internals.* Interpreter, operator resolver, tensor arena, static memory plan, no dynamic allocation. Optimized kernels (ESP-NN, CMSIS-NN). The on-device loop: initialize, pre-process, infer, post-process.
  - *Exercise:* estimate the arena size of a small model from its largest activations.
- *Part 3: Features for time series.* Statistical features and spectral features. Why signal processing before the network reduces the model size.
  - *Exercise:* compare the input size of raw windows and of spectral features.

**Lab**

- *Goal:* a motion classifier that runs on the XIAOML Kit.
- *Board:* XIAOML Kit.
- *Part A (45 min): Train.* In a notebook, compute features from the Day 2 dataset and train a small classifier.
- *Part B (50 min): Convert and deploy.* Convert the model to LiteRT and generate a C array. Write the Arduino sketch with TensorFlow Lite Micro. Show the class on the display.
- *Part C (30 min): Measure.* Measure arena size, flash use, and latency. Repeat the measurement without PSRAM.
- *Part D (25 min): Compare.* Train the same task in Edge Impulse Studio and compare the two results.
- *Deliverable:* a live demonstration and a comparison table.
- *Check:* the board classifies four motions correctly, and the table has measured numbers for both paths.

**Preparation notes**

- Select and test one TensorFlow Lite Micro library for the ESP32-S3 on the pilot.
- Give students a sketch template with the sensor code. Students write the inference part.

**Backup modules:** MC-3 (spectral features), MC-4 (anomaly detection), MC-10 (Cortex-M and CMSIS-NN), NB-2 (TensorFlow Lite Micro hello world), NB-3 (motion classification on the Nano 33), NB-4 (magic wand).

**Recap modules:** TH-10 (datasets and generalization), TH-11 (evaluation metrics), TH-12 (unsupervised learning and anomaly detection), TH-15 (loss functions), TH-16 (backpropagation), TH-17 (optimizers and the learning rate), TH-18 (training loop), TH-26 (signals in time and frequency), TH-35 (ML frameworks).

---

### Day 4: Quantization

**Learning outcomes**

- Derive the scale and the zero point of an affine quantizer.
- Apply post-training quantization with a representative dataset.
- Apply quantization-aware training.
- Explain per-tensor and per-channel quantization.
- Measure the effect of int8 quantization on size, accuracy, and latency.

**Theory**

- *Part 1: Number formats and the affine mapping.* FP32, FP16, INT8. Memory and energy per operation. Scale, zero point, rounding error.
  - *Exercise:* quantize five numbers by hand and calculate the error.
- *Part 2: Post-training quantization.* Dynamic range and full integer quantization. Calibration methods. Per-channel scales. Batch normalization folding before quantization.
  - *Exercise:* predict the result of a calibration set that has one class only.
- *Part 3: Quantization-aware training and debugging.* Simulated quantization and the straight-through estimator. Mixed precision. How to find the layer that loses accuracy. Short overview of binary and ternary networks.
  - *Exercise:* read a per-layer error report and name the layer to keep in float.

**Lab**

- *Goal:* a measured comparison of float and int8 models.
- *Board:* XIAOML Kit.
- *Part A (30 min): By hand.* Quantize tensors in NumPy and measure the error.
- *Part B (50 min): Post-training quantization.* Quantize a small CNN. Change the calibration set and observe the accuracy.
- *Part C (40 min): Quantization-aware training.* Train the same CNN with simulated quantization.
- *Part D (30 min): On the board.* Deploy the float model and the int8 model from Day 3. Compare flash use, arena size, latency, and accuracy.
- *Deliverable:* the comparison table and a Decision Log.
- *Check:* the table has float and int8 rows for size, accuracy, and latency, and the Decision Log explains the accuracy change.

**Preparation notes**

- Prepare a trained float model so that students start from the same baseline.

**Backup modules:** SIM-2 (compression simulation), PI-2 (int8 calibration with ExecuTorch, after Day 7), NB-8 (float and int8 on a Cortex-M4).

**Recap modules:** TH-14 (activation functions), TH-16 (backpropagation), TH-21 (normalization layers), TH-32 (number formats).

---

### Day 5: Audio and vision on microcontrollers

**Learning outcomes**

- Compute a spectrogram and MFCC features from an audio signal.
- Describe the keyword spotting pipeline and the cascade design.
- Explain why peak activation memory limits vision models on a microcontroller.
- Deploy a keyword spotting model and an image classifier on the XIAOML Kit.
- Tune the post-processing to reduce false activations.

**Theory**

- *Part 1: Audio features and keyword spotting.* Frames, FFT, Mel scale, MFCC. Small convolutional models. Unknown and noise classes. False accept rate and false reject rate.
  - *Exercise:* match three spectrograms to three spoken words.
- *Part 2: Vision under microcontroller constraints.* Input resolution, width multiplier, visual wake words. Peak activation memory and PSRAM. Transfer learning. Capture, resize, and colour conversion on the device.
  - *Exercise:* calculate the peak activation memory of a MobileNet at two input resolutions.
- *Part 3: Streaming inference and detection.* Sliding windows, smoothing, thresholds. Cascade: an always-on microcontroller wakes a larger device. Why SSD and YOLO do not fit on a microcontroller. The centroid method of FOMO.
  - *Exercise:* design the cascade for a voice-controlled camera.

**Lab**

- *Goal:* one audio model and one vision model on the kit.
- *Board:* XIAOML Kit.
- *Part A (80 min): Keyword spotting.* Collect two keywords, a noise class, and an unknown class with Edge Impulse Studio. Train the model. Deploy the int8 model. Tune the smoothing and the threshold.
- *Part B (55 min): Image classification.* Train a MobileNet with transfer learning on a prepared dataset. Deploy the int8 model. Show the class on the display.
- *Part C (15 min): Measure.* Report latency and RAM for both models.
- *Deliverable:* two live demonstrations and the measurement table.
- *Check:* the keyword model gives no false activation in 30 seconds of normal speech, and the image model classifies three test objects.

**Preparation notes**

- This day has two applications. Give the image dataset to the students. They do not collect images in the core lab.
- The room is noisy when many groups record. Plan the recording in turns or in a second room.
- Each student needs an Edge Impulse account before the lab.
- If the class needs more time, move Part B to the start of Day 6. Day 6 uses no board.

**Backup modules:** MC-5 (KWS features in Python), MC-6 (FOMO object detection), MC-7 (SenseCraft AI), MC-8 (custom image dataset), MC-2 (audio recording to the SD card), NB-5 (keyword spotting on the Nano 33), NB-6 (person detection), NB-7 (two models on one microcontroller), MC-11 (Grove Vision AI V2).

**Recap modules:** TH-11 (evaluation metrics), TH-19 (regularization), TH-22 (transfer learning), TH-23 (convolution), TH-25 (computer vision tasks), TH-26 (signals in time and frequency).

---

## Week 2: Optimization and Linux-class edge devices

### Day 6: Pruning, distillation, and efficient design

**Learning outcomes**

- Apply unstructured and structured magnitude pruning.
- Explain why sparsity does not always reduce latency.
- Train a small student model with knowledge distillation.
- Select an optimization technique from a hardware constraint.

**Theory**

- *Part 1: Pruning.* Criteria, granularity, schedules, fine-tuning. Sparsity and real speedup on real hardware.
  - *Exercise:* predict the latency of a model with 80 percent unstructured sparsity on a CPU.
- *Part 2: Knowledge distillation and low-rank methods.* Soft targets and temperature. Feature distillation. Low-rank factorization.
  - *Exercise:* calculate soft targets at two temperatures.
- *Part 3: Efficient design and technique selection.* MobileNet, EfficientNet, and MCUNet. Hardware-aware neural architecture search. Order of techniques: prune, distill, quantize.
  - *Exercise:* select techniques for three cases (flash limit, RAM limit, latency limit).

**Lab**

- *Goal:* a trade-off curve for one task and a model selection for the two boards.
- *Boards:* none. The lab runs on a laptop or on Colab.
- *Quiz (20 min): Week 1 quiz.*
- *Part A (45 min): Pruning.* Prune a CNN at several sparsity levels and fine-tune it.
- *Part B (45 min): Distillation.* Distill a teacher model into a smaller student model.
- *Part C (40 min): Selection.* Quantize the best candidates with the Day 4 method. Plot accuracy against size and against latency. Select one model for the XIAO and one model for the Raspberry Pi.
- *Deliverable:* the plot and a Decision Log.
- *Check:* the plot has at least six models, and the selection states the constraint that decides.

**Preparation notes**

- This day uses no board. Use spare time to complete Week 1 hardware labs.
- Prepare a trained baseline model. Training from the start takes too long on a CPU.

**Backup modules:** GA-9 (distillation from MNIST to language models), SIM-2 (compression simulation).

**Recap modules:** TH-6 (data selection), TH-8 (probability and information theory), TH-15 (loss functions), TH-17 (optimizers and the learning rate), TH-19 (regularization), TH-20 (depth and skip connections), TH-24 (CNN architectures), TH-36 (cost of training).

---

### Day 7: Hardware acceleration and inference runtimes

**Learning outcomes**

- Explain how SIMD, accelerators, and memory bandwidth limit inference speed.
- Name the main graph optimizations and state what each one does.
- Export a PyTorch model to ONNX and to LiteRT.
- Compare inference runtimes on the Raspberry Pi.
- Explain the trade-off between static and dynamic input shapes.

**Theory**

- *Part 1: Acceleration fundamentals.* CPU SIMD, GPU, NPU. Compute-bound and memory-bound workloads. The Roofline model.
  - *Exercise:* place three workloads on a Roofline plot.
- *Part 2: The runtime stack.* Model format, graph optimizer, kernel library. ONNX Runtime, LiteRT, NCNN, ExecuTorch. Threads and execution providers.
  - *Exercise:* select a runtime for three deployment cases.
- *Part 3: Graph optimization.* Constant folding, removal of unused nodes, operator fusion, memory layout, static and dynamic shapes, precision selection.
  - *Exercise:* fuse a convolution, a batch normalization, and a ReLU on paper.

Part 3 teaches layer fusion, precision calibration, and dynamic shapes with tools that run on the Raspberry Pi.

**Lab**

- *Goal:* a runtime comparison on the Raspberry Pi.
- *Board:* Raspberry Pi 5.
- *Part A (35 min): Setup.* Start the Raspberry Pi, connect with SSH, and test the camera.
- *Part B (35 min): First inference.* Run MobileNetV2 with LiteRT on test images and on the camera.
- *Part C (45 min): Export and inspect.* Export one PyTorch model to ONNX with a static shape and with a dynamic shape. Export it to LiteRT. Open the graphs in Netron before and after optimization. Find the fused operators.
- *Part D (35 min): Measure.* Measure latency for each runtime, thread count, and precision.
- *Deliverable:* the latency table and a Decision Log.
- *Check:* the table has at least two runtimes, two thread counts, and two precisions.

**Preparation notes**

- Flash all microSD cards before the day. Set a unique host name for each Raspberry Pi.
- Test SSH on the lab router.

**Backup modules:** PI-1 (custom image classification), PI-2 (ExecuTorch), PI-5 (hardware accelerators), SIM-3 (kernel fusion simulation), SIM-4 (Roofline simulation), PI-10 (train and convert a CNN).

**Recap modules:** TH-7 (linear algebra and tensors), TH-21 (normalization layers), TH-33 (computer architecture essentials), TH-34 (performance laws), TH-35 (ML frameworks).

---

### Day 8: Object detection at the edge

**Learning outcomes**

- Describe the structure of a single-stage detector.
- Compute IoU, apply non-maximum suppression, and read an mAP result.
- Train a custom YOLO model and export it for the Raspberry Pi.
- Tune input resolution and precision for a target frame rate.

**Theory**

- *Part 1: Detection models.* SSD, EfficientDet, FOMO, and the YOLO family. Detection head outputs. Non-maximum suppression.
  - *Exercise:* apply non-maximum suppression to six boxes by hand.
- *Part 2: Metrics and data.* IoU, precision and recall, mAP. Labelling rules and label quality.
  - *Exercise:* calculate the IoU of two box pairs.
- *Part 3: Deployment.* Input resolution and model scale. Export formats. Int8 calibration for detectors. Latency of the full pipeline: capture, pre-process, infer, post-process.
  - *Exercise:* predict the frame rate change when the resolution goes from 640 to 320.

**Lab**

- *Goal:* live detection with a custom model on the Raspberry Pi.
- *Board:* Raspberry Pi 5 with the camera.
- *Part A (30 min): Pre-trained models.* Run an SSD model and a YOLO model on test images.
- *Part B (50 min): Custom model.* Train a YOLO model on a small custom dataset (Colab or laptop).
- *Part C (40 min): Export and deploy.* Export the model to NCNN and to LiteRT int8. Run live detection with the camera.
- *Part D (30 min): Measure.* Measure the frame rate for two resolutions and two precisions. Report the accuracy loss of the int8 model.
- *Deliverable:* a live demonstration and the frame-rate table.
- *Check:* the custom model detects both classes in the live image, and the table has four measured rows.

**Preparation notes**

- The repository has trained weights for the box and wheel dataset. Use them for groups that have no time to train.
- The template notebook downloads its dataset from Roboflow. Prepare a local copy if you use it.

**Backup modules:** PI-3 (SSD, EfficientDet, and FOMO comparison), PI-4 (object counting), PI-8 (YOLO in a mobile browser), MC-6 (FOMO on the XIAOML Kit), PI-9 (instance segmentation).

**Recap modules:** TH-11 (evaluation metrics), TH-18 (training loop), TH-22 (transfer learning), TH-25 (computer vision tasks).

---

### Day 9: Benchmarking and profiling

**Learning outcomes**

- Define latency percentiles, throughput, peak memory, and energy per inference.
- Design a fair benchmark with warm-up, repetitions, and fixed inputs.
- Measure one task on two boards and explain the differences.
- Explain thermal throttling and its effect on results.

**Theory**

- *Part 1: What to measure.* System, model, and data benchmarks. MLPerf Tiny and MLPerf Inference Edge.
  - *Exercise:* read one MLPerf Tiny result table and compare two devices.
- *Part 2: Measurement method.* Warm-up, variance, percentiles. Full pipeline time and model-only time. Common errors.
  - *Exercise:* find three errors in a given benchmark script.
- *Part 3: Power, energy, and temperature.* Power measurement methods. Energy per inference. Duty cycle and battery life estimate.
  - *Exercise:* estimate the battery life of an always-on keyword spotting device.

**Lab**

- *Goal:* one benchmark report across the two boards.
- *Boards:* XIAOML Kit, Raspberry Pi 5.
- *Part A (20 min): Protocol.* Write the benchmark protocol before you measure.
- *Part B (45 min): Microcontroller.* Measure keyword spotting and image classification on the kit, with float and int8 models.
- *Part C (50 min): Raspberry Pi.* Measure image classification and object detection for two runtimes and two thread counts. Record the CPU temperature during the run.
- *Part D (35 min): Report.* Report latency (median and 95th percentile), RAM, flash, accuracy, and estimated energy.
- *Deliverable:* the benchmark report.
- *Check:* each number has a method (repetitions, warm-up, input), and the report compares the same task on both boards.

**Preparation notes**

- A USB power meter gives real energy numbers. Without the meter, students estimate energy from data sheet values.

**Backup modules:** PI-6 (thermal throttling), MC-9 (low power), SY-3 (tail latency), SIM-5 (benchmark simulation), NB-8 (float and int8 on a Cortex-M4), NB-11 (power of an always-on device).

**Recap modules:** TH-33 (computer architecture essentials), TH-34 (performance laws), TH-37 (D·A·M taxonomy).

---

### Day 10: Generative AI at the edge

**Learning outcomes**

- Estimate the RAM that a small language model needs from its parameters, its precision, and its context length.
- Run small language models on the Raspberry Pi and measure tokens per second.
- Call a small language model from Python with structured output and function calling.
- Explain retrieval-augmented generation and vision-language models at the edge.
- State when a small language model is the wrong tool.

**Theory**

- *Part 1: Small language models from a systems view.* Parameters, precision, and disk size. Quantization levels and the GGUF format. RAM budget: weights, KV cache, and the rest of the system. Tokens per second and what is usable. Why distillation makes small models good.
  - *Exercise:* calculate the RAM of a 3-billion-parameter model at 4 bits with two context lengths.
- *Part 2: Tools and runtimes.* llama.cpp, Ollama, LiteRT-LM. Server and library use. Threads. Prompt rate and generation rate. Model selection for an 8 GB device.
  - *Exercise:* select a model and a quantization level for three applications.
- *Part 3: Applications and limits.* Structured output and function calling. Retrieval-augmented generation. Vision-language models. Language models that control devices. Wrong answers, latency, heat, and power.
  - *Exercise:* decide for four tasks if a classifier, a rule, or a language model is the correct tool.

**Lab**

- *Goal:* a measured comparison of small language models and one working application.
- *Board:* Raspberry Pi 5 (8 GB) with the active cooler.
- *Part A (45 min): Run and measure.* Install Ollama. Run two models of different size. Measure tokens per second, RAM, and CPU temperature with the Day 9 method.
- *Part B (45 min): Python integration.* Use the Ollama Python library. Get structured output with a data schema. Call a Python function from the model output.
- *Part C (60 min): Application.* Select one: a simple retrieval-augmented generation system, or image description with a multimodal model.
- *Deliverable:* the benchmark table, the application, and a Decision Log.
- *Check:* the table has two models with measured numbers, and the application gives valid structured output for five test prompts.

**Preparation notes**

- Download the models to each Raspberry Pi before the lab. The files are large.
- Select the models on the pilot. Model names change quickly. The guide has a section on model selection.
- Make sure that each Raspberry Pi has the active cooler.

**Backup modules:** GA-1 (retrieval-augmented generation), GA-2 (Florence-2), GA-3 (agents), GA-4 (llama.cpp), GA-5 (LiteRT-LM), GA-6 (multi-token prediction), GA-7 (voice pipeline), GA-8 (IoT control), GA-9 (distillation), GA-10 (text generation with an RNN), GA-11 (fine-tune a vision-language model), GA-12 (agentic RAG).

**Recap modules:** TH-5 (transformers from a cost view), TH-27 (recurrent networks), TH-28 (tokenization and embeddings), TH-29 (attention mechanism), TH-30 (transformer architecture), TH-31 (text generation).

---

## Week 3: Connected systems and production

### Day 11: Networking fundamentals and RTSP streaming

**Learning outcomes**

- Explain when to use TCP and when to use UDP.
- Describe an RTSP session and the role of RTP and H.264.
- Set up an RTSP server on the Raspberry Pi.
- Read a video stream in Python and run inference on it.
- Measure the end-to-end latency of a stream.

**Theory**

- *Part 1: Networking for edge devices.* The layer model. IP addresses, DHCP, ports, TCP and UDP. Wi-Fi and Ethernet. Bandwidth, latency, jitter. Tools: `ping`, `ip`, `ss`, `iperf3`.
  - *Exercise:* read the output of three network commands and find the fault.
- *Part 2: Video streaming.* Resolution, frame rate, bit rate. H.264 and MJPEG. Keyframes. RTP, RTSP, and RTCP. HTTP streaming as an alternative.
  - *Exercise:* calculate the bit rate of an MJPEG stream and of an H.264 stream.
- *Part 3: Stream architectures.* Inference on the camera node or on a central node. Buffers, dropped frames, and latency. Privacy of video data.
  - *Exercise:* select the inference location for three camera systems.

**Lab**

- *Goal:* inference on a live network video stream.
- *Boards:* Raspberry Pi 5, XIAOML Kit.
- *Quiz (20 min): Week 2 quiz.*
- *Part A (20 min): Network tools.* Find the devices on the lab network. Measure throughput with `iperf3`.
- *Part B (40 min): RTSP server.* Publish the Raspberry Pi camera as an RTSP stream with MediaMTX. Open the stream on a laptop.
- *Part C (45 min): Inference on the stream.* Read the stream with OpenCV in Python and run the Day 8 detector. Measure the end-to-end latency. Change the resolution and the bit rate.
- *Part D (25 min): Microcontroller camera.* Publish the XIAO camera as an MJPEG stream and compare.
- *Deliverable:* a live demonstration and the latency measurements.
- *Check:* the detector runs on the network stream, and the report gives the latency for two settings.

**Preparation notes**

- Use the dedicated router. A campus network can block traffic between devices.
- Download MediaMTX for the Raspberry Pi before the lab.
- Check the firewall of the lab computers.
- The companion book chapter targets the XIAO ESP32C3. Test the code on the ESP32S3.

**Backup modules:** SY-1 (Wi-Fi and HTTP on the XIAO), MC-8 (camera web server), SY-11 (model as a local web service).

---

### Day 12: Local decision-making and MQTT

**Learning outcomes**

- Design a cascade that makes decisions locally.
- Explain MQTT topics, quality of service levels, retained messages, and the last will message.
- Publish inference results from a microcontroller.
- Build a system that continues to work without an internet connection.

**Theory**

- *Part 1: Local decision-making.* Hybrid architecture patterns. Which decisions must stay local. Rules, state machines, hysteresis. Safe behaviour when a part fails.
  - *Exercise:* write the state machine for a door monitor with two sensors.
- *Part 2: MQTT.* Broker, publish and subscribe, topics and wildcards. Quality of service 0, 1, and 2. Retained messages, last will, keep-alive. Telemetry and commands. Payload formats.
  - *Exercise:* design the topic tree for ten devices in two rooms.
- *Part 3: Edge-to-cloud design.* Send results and not raw data. How often to send telemetry. Offline buffers and lost connections. Time synchronization. Device identity.
  - *Exercise:* calculate the data volume of raw video and of detection results for one day.

**Lab**

- *Goal:* a two-board system with local decisions and edge-to-cloud messages.
- *Boards:* XIAOML Kit, Raspberry Pi 5.
- *Part A (30 min): Broker.* Install the Mosquitto broker on the Raspberry Pi. Publish and subscribe from the command line.
- *Part B (45 min): Telemetry.* Publish IMU readings from the XIAO with MicroPython. Publish inference results (keyword or image class) from the Arduino sketch.
- *Part C (40 min): Local decision.* On the Raspberry Pi, subscribe and apply a local rule that starts an action. Send a command back to the XIAO.
- *Part D (35 min): Offline operation.* Disconnect the internet link and show that the system continues to work. Store messages when the cloud broker is not available. Send the messages when the link returns.
- *Deliverable:* a live demonstration with the link connected and disconnected.
- *Check:* the local action works without the internet, and no message is lost after the link returns.

**Preparation notes**

- The instructor laptop runs the "cloud" broker.
- Give each group a unique topic prefix.
- The companion book chapter targets the XIAO ESP32C3 and a public broker. Change the code for the ESP32S3 and the local broker.

**Backup modules:** SY-2 (MQTT security), PI-7 (physical computing), GA-8 (language model for IoT control), NB-9 (Bluetooth gateway for the Nano 33), SY-12 (Bluetooth from the XIAO).

---

### Day 13: Monitoring, logging, and visualization

**Learning outcomes**

- Select metrics for model health and for system health.
- Write structured logs on a device with small storage.
- Build a live dashboard for an edge device.
- Detect data drift without labels.

**Theory**

- *Part 1: Failures of deployed edge AI.* Silent accuracy loss, data drift, sensor faults, heat, memory leaks. System metrics and model metrics.
  - *Exercise:* for three failures, name the metric that shows the failure first.
- *Part 2: Logging.* Structured logs, log levels, log rotation, sampling. Time-series storage. Privacy of logged data.
  - *Exercise:* calculate the storage that one day of logs needs at three sampling rates.
- *Part 3: Visualization and alerts.* Dashboards and thresholds. Drift detection from confidence and input statistics. The loop back to data collection and training.
  - *Exercise:* set alert thresholds from a given metric history.

**Lab**

- *Goal:* a monitored inference application.
- *Board:* Raspberry Pi 5.
- *Part A (40 min): Instrument.* Add measurements to the Day 8 application: latency, frame rate, CPU temperature, RAM, confidence. Write structured logs with rotation.
- *Part B (45 min): Dashboard.* Publish the metrics with MQTT, store them, and build a live dashboard.
- *Part C (40 min): Drift.* Cause a drift event (change the light or show a new object). Detect the event from the confidence values.
- *Part D (25 min): Alert.* Add one alert rule and test it.
- *Deliverable:* the dashboard and a short incident report for the drift event.
- *Check:* the dashboard shows live system and model metrics, and the alert fires during the drift event.

**Preparation notes**

- Select the dashboard tool during the build of this day. Grafana with Prometheus is the default. A Python dashboard is the fallback.
- Install the monitoring software before the lab.

**Backup modules:** SY-9 (Jupyter widget dashboard), SY-3 (tail latency), SIM-6 (operations simulation), SIM-8 (fleet monitoring simulation), SY-10 (robust AI).

**Recap modules:** TH-8 (probability and information theory).

---

### Day 14: Production edge AI design and capstone start

**Learning outcomes**

- Plan model versions and over-the-air updates for a group of devices.
- Identify security and privacy threats of an edge AI system and select mitigations.
- Estimate the power budget and the cost of a deployment.
- Write a system design proposal.

**Theory**

- *Part 1: Life cycle in production.* Model versions, over-the-air updates, rollback. Different hardware in one fleet. Overview of on-device adaptation and federated learning.
  - *Exercise:* write the update plan for 100 devices with a bad network.
- *Part 2: Security, privacy, and reliability.* Attack surface, model theft, physical access. Keys and encrypted transport. Data minimization. Watchdogs and reduced operation after a failure.
  - *Exercise:* list the threats for the Day 12 system and select two mitigations.
- *Part 3: Design method.* From requirements to paradigm, hardware, model, and pipeline. Power and cost budgets. Design review exercise. Capstone briefing.
  - *Exercise:* review a given system design and find three weak points.

**Lab**

- *Goal:* an approved capstone proposal and a started build.
- *Boards:* XIAOML Kit, Raspberry Pi 5.
- *Part A (20 min): Teams.* Form teams of three or four students.
- *Part B (50 min): Proposal.* Write a one-page proposal: problem, boards, model, data, metrics.
- *Part C (40 min): Design review.* Present the proposal to the instructor.
- *Part D (40 min): Build.* Start the build.
- *Deliverable:* the approved proposal.
- *Check:* the proposal meets the five capstone requirements in Section 7.

**Preparation notes**

- Prepare three or four example projects for teams that have no idea.
- Vol II of the book is a preview. Check the content before you use it.

**Backup modules:** SY-4 (on-device and federated learning), SY-5 (security and privacy), SY-6 (responsible and sustainable AI), SY-7 (over-the-air update), SY-8 (containers), SY-10 (robust AI).

**Recap modules:** TH-3 (ML workflow), TH-36 (cost of training), TH-37 (D·A·M taxonomy).

---

### Day 15: Capstone build and demonstrations

**Learning outcomes**

- Integrate models, devices, messages, and monitoring into one system.
- Report system performance with measured numbers.
- Present and defend design decisions.

**Theory**

- *Part 1: Course summary.* Review of the main trade-offs from the three weeks. Questions.
- *Parts 2 and 3: Capstone build.* Teams work. The instructor visits each team.

**Lab**

- *Goal:* a working system and a short report.
- *Boards:* XIAOML Kit, Raspberry Pi 5.
- *Part A (80 min): Build.* Complete the build and the measurements.
- *Part B (70 min): Demonstrations.* Each team gives a 10-minute demonstration.
- *Part C (30 min): Close.* Submit the report. Give course feedback.
- *Deliverable:* the demonstration and the report.
- *Check:* the capstone rubric in Section 7.

**Preparation notes**

- Publish the demonstration schedule on Day 14.
- Keep spare boards ready.

**Backup modules:** any module from Section 6 can be a capstone component.

---

## 6. Backup modules

Each backup module is independent of the other backup modules, unless its description names another module. The column "After day" gives the core day that a module needs.

Type: **T** is a theory deck. **L** is a lab with a short lab deck. **T+L** is both.

Each module has the same parts, so that you can present it alone:

- One slide deck that compiles alone. The deck has a title frame, the learning outcomes, the content, and the credits frame.
- One lab folder with the files and a README. The README gives the goal, the hardware, the duration, the steps, and the check criterion.
- No reference to a slide number or a file of another day.

### 6.1 Microcontroller modules (XIAOML Kit)

| ID | Module | Type | Time | After day | Extra hardware |
|---|---|---|---|---|---|
| MC-1 | Arduino basics for Python users | L | 60 min | 1 | None |
| MC-2 | Sensor data logger on the SD card | L | 45 min | 2 | None |
| MC-3 | Spectral features for motion data | T+L | 90 min | 2 | None |
| MC-4 | Anomaly detection on motion data | L | 60 min | 3 | None |
| MC-5 | Keyword spotting features and training in Python | T+L | 90 min | 4 | None |
| MC-6 | FOMO object detection on the XIAOML Kit | L | 120 min | 5 | None |
| MC-7 | No-code deployment with SenseCraft AI | L | 45 min | 1 | None |
| MC-8 | Custom image dataset with the camera web server | L | 60 min | 1 | None |
| MC-9 | Low power: sleep modes and battery life | T+L | 90 min | 5 | USB power meter, LiPo battery |
| MC-10 | Arm Cortex-M and CMSIS-NN | T | 30 min | 1 | None |
| MC-11 | Grove Vision AI V2: vision with a neural processing unit | T+L | 120 min | 5 | Grove Vision AI V2 |

- **MC-1.** Program structure, digital output, button input, serial monitor, and the display. The source code uses a different expansion board. Change the pin numbers for the XIAOML Kit.
- **MC-2.** Record audio and store it on the microSD card without a computer.
- **MC-3.** Time-domain statistics, FFT, and spectral power as model inputs.
- **MC-4.** Detect motions that are not in the training set.
- **MC-5.** Compute MFCC features and train the keyword classifier in a notebook, without Edge Impulse training.
- **MC-6.** Collect and label images, train a FOMO model, and deploy it.
- **MC-7.** Deploy a trained model from the browser with no code. Use this module when the Arduino build fails.
- **MC-8.** Collect an image dataset with the XIAO camera.
- **MC-9.** Measure current in active mode and in deep sleep. Calculate battery life for a duty cycle.
- **MC-10.** The Cortex-M processor family, memory sizes, and the CMSIS-NN kernels. This module replaces the hands-on work with a Cortex-M board.
- **MC-11.** Deploy vision models on a microcontroller that has a neural processing unit, and compare the speed with the XIAO. The module gives a hardware example for Day 7.

### 6.2 Raspberry Pi modules

| ID | Module | Type | Time | After day | Extra hardware |
|---|---|---|---|---|---|
| PI-1 | Custom image classification project | L | 120 min | 7 | None |
| PI-2 | ExecuTorch with XNNPACK | T+L | 120 min | 7 | None |
| PI-3 | SSD, EfficientDet, and FOMO comparison | L | 90 min | 8 | None |
| PI-4 | Object counting application | L | 90 min | 8 | None |
| PI-5 | Hardware accelerators for the Raspberry Pi | T | 45 min | 7 | Accelerator module for a demonstration only |
| PI-6 | Thermal throttling experiment | L | 45 min | 9 | None |
| PI-7 | Physical computing: GPIO, sensors, actuators | L | 90 min | 7 | Sensor and LED parts |
| PI-8 | YOLO inference in a mobile browser | T+L | 90 min | 8 | Smartphone |
| PI-9 | Instance segmentation with YOLO | L | 120 min | 8 | None |
| PI-10 | Train a CNN and convert it to LiteRT | L | 90 min | 7 | None |

- **PI-1.** Collect images with the Raspberry Pi camera, train in Edge Impulse Studio, and deploy the model.
- **PI-2.** Export a PyTorch model to ExecuTorch, apply int8 quantization with a calibration set, and compare with LiteRT. This module fits students who use PyTorch.
- **PI-3.** Run three detector types on the same images and compare accuracy and speed.
- **PI-4.** Count objects in an image with a custom YOLO model and store the counts in a database.
- **PI-5.** How an M.2 accelerator compiles and runs a model. The lab part needs a MemryX MX3 module, so the module is theory with an optional instructor demonstration.
- **PI-6.** Run a long inference job with and without the active cooler. Plot temperature, clock speed, and latency.
- **PI-7.** Read a temperature sensor and a pressure sensor, control LEDs, and read a button with GPIO Zero.
- **PI-8.** Run a YOLO model in the browser of a smartphone as a web application. The module shows the mobile paradigm of Day 1.
- **PI-9.** Train a YOLO segmentation model for fire and smoke, and run it on the Raspberry Pi. The notebook is ready in the template.
- **PI-10.** Train a small CNN on CIFAR-10, convert it to LiteRT, and run it on the Raspberry Pi.

### 6.3 Generative AI modules (Raspberry Pi 5, 8 GB)

All modules in this group need Day 10, except GA-9 and GA-10. These two modules run on a laptop and need Day 6 only.

| ID | Module | Type | Time | Extra hardware |
|---|---|---|---|---|
| GA-1 | Retrieval-augmented generation at the edge | T+L | 120 min | None |
| GA-2 | Vision-language models with Florence-2 | T+L | 120 min | None |
| GA-3 | Agents and function calling | L | 120 min | None |
| GA-4 | llama.cpp from source and multimodal inference | L | 120 min | None |
| GA-5 | LiteRT-LM | L | 90 min | None |
| GA-6 | Multi-token prediction and model selection | T+L | 90 min | None |
| GA-7 | Voice pipeline: speech, language model, speech | L | 120 min | USB microphone, speaker |
| GA-8 | Language model for IoT control | L | 120 min | Sensor and LED parts (needs PI-7) |
| GA-9 | Knowledge distillation from MNIST to language models | T+L | 90 min | None |
| GA-10 | Text generation with a small RNN | T+L | 90 min | None |
| GA-11 | Fine-tune a vision-language model | L | 120 min | None (training needs a Colab GPU) |
| GA-12 | Agentic retrieval-augmented generation | L | 120 min | None (needs GA-1 and GA-3) |

- **GA-1.** Build a persistent vector database, query it, and optimize the query.
- **GA-2.** Caption images, detect objects, and read text with one model. Measure the latency of each task.
- **GA-3.** Show the limits of a small language model, then add tools: a calculator, a search, and response validation.
- **GA-4.** Build llama.cpp, start the server, and use it from Python with text and images.
- **GA-5.** Install LiteRT-LM, run a model, and compare it with Ollama.
- **GA-6.** Compare two models with and without multi-token prediction. Use the same measurement method for both models.
- **GA-7.** Record speech, transcribe it, send it to a language model, and speak the answer.
- **GA-8.** A language model reads sensor values and controls LEDs. The module connects Day 10 to Day 12 (local decisions) and Day 13 (logging).
- **GA-9.** Train a teacher and a student on MNIST, then connect the method to small language models. The notebook runs on a CPU.
- **GA-10.** Train a character-level RNN that writes text, then compare it with a transformer. The module is a short introduction to language models before Day 10.
- **GA-11.** Fine-tune Florence-2 on a small detection dataset and run the result on the Raspberry Pi.
- **GA-12.** Combine a vector database, tools, and response validation in one agent.

### 6.4 Systems modules

| ID | Module | Type | Time | After day | Extra hardware |
|---|---|---|---|---|---|
| SY-1 | Wi-Fi and HTTP on the XIAO | T+L | 90 min | 1 | None |
| SY-2 | MQTT security: authentication and TLS | T+L | 60 min | 12 | None |
| SY-3 | Model serving and tail latency | T | 50 min | 9 | None |
| SY-4 | On-device learning and federated learning | T | 50 min | 6 | None |
| SY-5 | Security and privacy of edge AI | T | 50 min | 12 | None |
| SY-6 | Responsible and sustainable edge AI | T | 50 min | 1 | None |
| SY-7 | Over-the-air update of the XIAO | L | 60 min | 11 | None |
| SY-8 | Containers on the Raspberry Pi | T+L | 90 min | 7 | None |
| SY-9 | Jupyter widget dashboard | L | 45 min | 7 | Sensor and LED parts (optional) |
| SY-10 | Robust AI: faults, drift, and attacks | T | 50 min | 9 | None |
| SY-11 | Model inference as a local web service | T+L | 90 min | 7 | None |
| SY-12 | Bluetooth Low Energy from the XIAO to the Raspberry Pi | T+L | 90 min | 7 | None |

- **SY-1.** Connect to Wi-Fi, use `ping`, and send HTTP GET and POST requests.
- **SY-2.** Add user names, passwords, and TLS to the Day 12 broker.
- **SY-3.** Queues, tail latency, and batch size.
- **SY-4.** Model adaptation on the device and federated learning.
- **SY-5.** Threat analysis, model attacks, hardware attacks, and defences.
- **SY-6.** Fairness, accountability, energy, and carbon cost.
- **SY-7.** Send a new firmware and a new model to the XIAO over Wi-Fi.
- **SY-8.** Package the Day 8 application in a container and start it on a second Raspberry Pi.
- **SY-9.** Show sensor values and control outputs from a notebook with widgets.
- **SY-10.** Hardware faults, distribution shift, and adversarial inputs, with detection and mitigation.
- **SY-11.** Put a model behind an HTTP interface on the Raspberry Pi and call it from a second device. The inference part is new.
- **SY-12.** Send inference results from the XIAO to the Raspberry Pi with Bluetooth Low Energy, and compare with Wi-Fi and MQTT.

### 6.5 Simulation warm-ups

These modules are interactive notebooks from the book. They need no hardware. Each one takes 20 to 30 minutes. Students predict a result first and then test the prediction. They need `marimo` and `mlsysim`.

| ID | Simulation | Fits day | Source |
|---|---|---|---|
| SIM-1 | The Iron Law | 1 | [lab_02_ml_systems.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol1/lab_02_ml_systems.py) |
| SIM-2 | The Compression Frontier | 4, 6 | [lab_10_model_compress.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol1/lab_10_model_compress.py) |
| SIM-3 | The Kernel Fusion Dividend | 7 | [lab_07_ml_frameworks.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol1/lab_07_ml_frameworks.py) |
| SIM-4 | The Roofline | 7 | [lab_11_hw_accel.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol1/lab_11_hw_accel.py) |
| SIM-5 | The Speedup Ceiling | 9 | [lab_12_perf_bench.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol1/lab_12_perf_bench.py) |
| SIM-6 | The Silent Degradation Problem | 13 | [lab_14_ml_ops.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol1/lab_14_ml_ops.py) |
| SIM-7 | The Tail Latency Trap | 9, 13 | [lab_13_model_serving.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol1/lab_13_model_serving.py) |
| SIM-8 | The Silent Fleet | 13, 14 | [lab_12_ops_scale.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol2/lab_12_ops_scale.py) |
| SIM-9 | The Edge Thermodynamics Lab | 9, 14 | [lab_11_edge_intelligence.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol2/lab_11_edge_intelligence.py) |
| SIM-10 | The Price of Privacy | 14 | [lab_13_security_privacy.py](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/labs/vol2/lab_13_security_privacy.py) |

### 6.6 Arduino Nano 33 BLE Sense modules

These modules add a second microcontroller class to the course: an Arm Cortex-M4 with 256 KB of RAM and 1 MB of flash.
Use them as a replacement for a XIAOML Kit lab, as an addition to a day, or together as one full day.

The modules use the Nano 33 BLE Sense Rev2. Modules NB-2, NB-3, NB-4, NB-8, and NB-9 need the IMU only, so they also run on the Nano 33 BLE without sensors.

| ID | Module | Type | Time | Fits day | Extra hardware |
|---|---|---|---|---|---|
| NB-1 | Board setup and sensor tests | L | 60 min | 1 | None |
| NB-2 | TensorFlow Lite Micro "hello world" and the tensor arena | L | 60 min | 3 | None |
| NB-3 | Motion classification on the Nano 33 | L | 120 min | 3 | None |
| NB-4 | Magic wand: gesture recognition with the IMU | L | 90 min | 3 | None |
| NB-5 | Keyword spotting on the Nano 33 | L | 120 min | 5 | None |
| NB-6 | Person detection with a camera | L | 90 min | 5 | OV7675 camera module |
| NB-7 | Two models on one microcontroller | T+L | 90 min | 5 | OV7675 camera module |
| NB-8 | The 256 KB budget: float and int8 on a Cortex-M4 | L | 60 min | 4, 9 | None |
| NB-9 | Bluetooth Low Energy gateway to MQTT | T+L | 90 min | 12 | None |
| NB-10 | MicroPython on the Nano 33 | L | 60 min | 2 | None |
| NB-11 | Power of an always-on device | L | 60 min | 9 | USB power meter |
| NB-12 | Embedded hardware and software for TinyML | T | 50 min | 2, 3 | None |

- **NB-1.** Install the board core and the library. Test the IMU, the microphone, and the camera.
- **NB-2.** Run a small model that predicts a sine value. Read the interpreter code, change the arena size, and find the smallest size that works.
- **NB-3.** Collect motion data with the IMU, train a classifier, and deploy it. This module can replace the Day 3 lab.
- **NB-4.** Recognize gestures that you draw in the air.
- **NB-5.** Deploy a trained keyword spotting model, then train and deploy your own keywords. This module can replace Day 5 Part A.
- **NB-6.** Detect a person in a 96 by 96 pixel image. The model uses almost all the RAM of the board.
- **NB-7.** Run keyword spotting and person detection in one program. The module shows how two models share one tensor arena.
- **NB-8.** Deploy the Day 3 and Day 4 models on the Nano 33. Compare flash, arena size, and latency with the XIAO. Find the largest model that fits. The module gives a third device for the Day 9 benchmark.
- **NB-9.** The Nano 33 has no Wi-Fi. Send inference results with Bluetooth Low Energy to the Raspberry Pi, and publish them to the Day 12 broker.
- **NB-10.** Read the IMU with MicroPython and log the data. Test this module on the board before use.
- **NB-11.** Measure the current of the board during keyword spotting and calculate the battery life.
- **NB-12.** Embedded systems, microcontroller hardware, input and output, embedded software, and the internals of TensorFlow Lite Micro.

**One full day with the Nano 33:** NB-12 and MC-10 for the theory, then NB-1, NB-2, and NB-5 for the lab.

### 6.7 Recap and theory modules

These modules need no hardware. Use them when the class needs a recap of a machine learning or deep learning topic, or more theory depth.

This section has 36 modules. Each module has one topic only, so that you can add one module to a day and not a full lecture.

- A module of type T is one deck of 25 or 50 minutes, with one exercise that the students do by hand.
- A module does not need another module of this section, unless its description names that module.
- The column "Fits day" gives the core days that use the topic. Each day section in Section 5 has a line "Recap modules".
- A recap module explains the topic. The core days explain the cost of the topic on an edge device.

**Mathematics**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-7 | Linear algebra and tensors | T | 50 min | 1, 7 |
| TH-8 | Probability and information theory | T | 50 min | 6, 13 |

- **TH-7.** Vectors, matrices, and tensors. Shapes and memory layout. The dot product as a measure of similarity. Matrix multiplication as the main operation of a network. Broadcasting. *Exercise:* calculate the output shape and the number of multiplications of three matrix products.
- **TH-8.** Distributions and the long tail. Entropy, cross-entropy, and KL divergence. Measures of the drift between two distributions. Logits and the numerical stability of the softmax. *Exercise:* calculate the entropy of two small distributions and the KL divergence between them.

**Machine learning foundations**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-9 | The machine learning paradigm | T | 50 min | 1 |
| TH-10 | Datasets and generalization | T | 50 min | 2, 3 |
| TH-11 | Evaluation metrics for classifiers | T | 50 min | 3, 5, 8 |
| TH-12 | Unsupervised learning and anomaly detection | T | 50 min | 3 |

- **TH-9.** Rules that a programmer writes and rules that a model learns from data. Features, labels, model, and loss. Regression and classification. Training and inference. *Exercise:* for three problems, decide if written rules or a learned model is the correct tool.
- **TH-10.** Training, validation, and test sets. Overfitting and underfitting. The generalization gap. How to read loss curves. Class balance. *Exercise:* read three pairs of loss curves and name the problem of each pair.
- **TH-11.** Accuracy and its limits. The confusion matrix, precision, recall, and F1. The decision threshold. False accepts and false rejects. Calibration of the confidence values. *Exercise:* calculate precision, recall, and F1 from a confusion matrix.
- **TH-12.** Learning with no labels. K-means clustering. The autoencoder and its reconstruction error. How to select the anomaly threshold. *Exercise:* run two K-means steps by hand on six points. Module MC-4 is the lab for this topic.

**Neural network foundations**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-13 | Neurons, layers, and the forward pass | T | 50 min | 1 |
| TH-14 | Activation functions | T | 25 min | 1, 4 |
| TH-15 | Loss functions | T | 25 min | 3, 6 |
| TH-16 | Backpropagation and automatic differentiation | T | 50 min | 3, 4 |

- **TH-13.** The weighted sum of a neuron, the bias, and the activation. Layers and connections. The multilayer perceptron. The forward pass as a sequence of matrix multiplications. The parameter count of a network. *Exercise:* calculate the output of a network with two layers by hand.
- **TH-14.** Why a network needs a nonlinear function. Sigmoid, tanh, ReLU, and softmax. Saturation and the range of the output. The cost of each function on small hardware. *Exercise:* calculate the output of four activation functions for five inputs.
- **TH-15.** Mean squared error and cross-entropy. Logits, softmax, and probabilities. The loss of one batch. Numerical stability. *Exercise:* calculate the cross-entropy loss of three predictions.
- **TH-16.** The chain rule. The computational graph. The forward pass and the backward pass. Reverse-mode automatic differentiation. Why training needs more memory than inference. Day 4 uses this topic for the straight-through estimator. *Exercise:* calculate the gradients of a graph with three nodes by hand.

**Training**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-17 | Optimizers and the learning rate | T | 50 min | 3, 6 |
| TH-18 | The training loop in practice | T | 50 min | 3, 8 |
| TH-19 | Regularization | T | 50 min | 5, 6 |
| TH-20 | Depth: initialization, vanishing gradients, and skip connections | T | 50 min | 1, 6 |
| TH-21 | Normalization layers | T | 25 min | 4, 7 |
| TH-22 | Transfer learning and fine-tuning | T | 50 min | 5, 8 |
| TH-2 | PyTorch basics | L | 90 min | 1 |

- **TH-17.** Gradient descent and mini-batch stochastic gradient descent. Momentum, Adam, and AdamW. The learning rate, its schedule, and the batch size. The memory that an optimizer needs. *Exercise:* calculate three update steps with momentum and with no momentum.
- **TH-18.** Epochs, batches, and the data loader. The steps of the loop for one batch. Loss curves and metrics during training. Hyperparameters. Checkpoints and early stopping. *Exercise:* find the two errors in a given training loop. Module TH-2 is the practice for this topic.
- **TH-19.** Dropout, weight decay, data augmentation, and early stopping. The problem that each method solves. *Exercise:* select a method for three training problems.
- **TH-20.** Why a deep network is hard to train. Weight initialization. Vanishing and exploding gradients. The residual connection and the flow of the gradient. *Exercise:* calculate how a gradient changes through 20 layers with a skip connection and with no skip connection.
- **TH-21.** Batch normalization and layer normalization. The statistics during training and the fixed values during inference. When to use each layer. Days 4 and 7 fold a batch normalization layer into the convolution before it. *Exercise:* calculate the output of a batch normalization layer for one channel.
- **TH-22.** A pre-trained model as a feature extractor. Frozen layers and a new classifier. Fine-tuning. The quantity of data that each method needs. Common errors. *Exercise:* select the layers to freeze for three cases.
- **TH-2.** Tensors, automatic differentiation, a model, and a training loop in PyTorch. The template has this notebook.

**Vision models and signals**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-23 | The convolution operation | T | 50 min | 1, 5 |
| TH-24 | CNN architectures from LeNet to MobileNet | T | 50 min | 1, 6 |
| TH-25 | Computer vision tasks | T | 25 min | 5, 8 |
| TH-26 | Signals in time and frequency | T | 50 min | 2, 3, 5 |

- **TH-23.** Kernel, stride, padding, and channels. The output size and the parameter count. Pooling. The receptive field. Why a convolution fits image data. *Exercise:* calculate the output of a 3 x 3 kernel on a 5 x 5 image by hand, for stride 1 and for stride 2.
- **TH-24.** LeNet, AlexNet, VGG, ResNet, MobileNet, and EfficientNet. The idea that each architecture added, and its cost in parameters and operations. *Exercise:* match six architectures to their main idea and order them by parameter count.
- **TH-25.** Image classification, object detection, instance segmentation, and pose estimation. The output of each task and its cost. *Exercise:* select the task for four applications.
- **TH-26.** Sampling and aliasing. The Fourier transform and the FFT. Windows. The spectrogram and the Mel scale. Modules MC-3 and MC-5 continue from the spectrogram to the features of a model. *Exercise:* read a spectrogram and find the sampling rate, the window length, and the highest frequency.

**Sequence and language models**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-27 | Recurrent networks | T | 25 min | 10 |
| TH-28 | Tokenization and embeddings | T | 50 min | 10 |
| TH-29 | The attention mechanism | T | 50 min | 10 |
| TH-30 | The transformer architecture | T | 50 min | 10 |
| TH-5 | Attention and transformers from a cost view | T | 50 min | 10 |
| TH-31 | Text generation: sampling, context, and the KV cache | T | 50 min | 10 |

- **TH-27.** Sequence data and the hidden state. The simple RNN and its memory problem. The gates of LSTM and GRU. Module GA-10 is the lab for this topic. *Exercise:* calculate two steps of a simple RNN by hand.
- **TH-28.** Characters, words, and subword tokens. Byte-pair encoding and the vocabulary. The embedding table. Positional encoding. *Exercise:* run three merge steps of byte-pair encoding by hand.
- **TH-29.** Query, key, and value. Scaled dot-product attention. Self-attention and multi-head attention. The causal mask. *Exercise:* calculate the attention weights of three tokens by hand.
- **TH-30.** The transformer block: attention, feed-forward layer, residual connection, and layer normalization. How a stack of blocks makes a GPT model. The parameter count. This module needs TH-29. *Exercise:* count the parameters of one transformer block.
- **TH-5.** The compute and the memory of attention when the sequence grows. The cost of training and the cost of decoding. Use TH-29 first if the students do not know attention.
- **TH-31.** Next-token prediction and the autoregressive loop. Temperature and sampling. The context window. The KV cache and its memory. *Exercise:* calculate the token probabilities of a small vocabulary at two temperatures.

**Computer systems foundations**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-32 | Number formats: floating point and integers | T | 25 min | 4 |
| TH-33 | Computer architecture essentials | T | 50 min | 1, 7, 9 |
| TH-34 | Performance laws: Amdahl, Gustafson, and Little | T | 50 min | 7, 9 |

- **TH-32.** The bits of a floating-point number: sign, exponent, and mantissa. FP32, FP16, and BF16. Integers and INT8. Range, precision, and rounding. *Exercise:* give the largest value and the smallest step of three formats.
- **TH-33.** Processor, cache, RAM, and storage. The memory hierarchy. The latency and energy numbers to know. Bandwidth and latency. *Exercise:* estimate the time to read a model of 10 MB from three levels of the memory hierarchy.
- **TH-34.** Amdahl's Law and Gustafson's Law: the limit of a speedup. Little's Law: queues and waiting time. Dimensional analysis as a check of a calculation. The Roofline model is not in this module: Day 7 and SIM-4 have it. *Exercise:* calculate the speedup of a pipeline when only the model becomes four times faster.

**Machine learning systems**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-3 | ML workflow and life cycle | T | 50 min | 1, 14 |
| TH-4 | Cost of neural network computation | T | 50 min | 1 |
| TH-35 | ML frameworks: graphs and execution | T | 50 min | 3, 7 |
| TH-36 | The cost of training | T | 50 min | 6, 14 |
| TH-6 | Data selection: less data for the same accuracy | T | 50 min | 2, 6 |
| TH-37 | The D·A·M taxonomy: find the bottleneck | T | 25 min | 9, 14 |

- **TH-3.** The stages of an ML project from the problem definition to monitoring, and the feedback between the stages.
- **TH-4.** Parameters, operations, and memory of a network, with a digit classifier as the example.
- **TH-35.** The computational graph. Eager execution, graph execution, and just-in-time compilation. Tensors and modules. Why a deployment format needs a static graph. *Exercise:* draw the computational graph of a function with five operations.
- **TH-36.** Why training costs more than inference: stored activations, gradients, and optimizer state. The memory of one training step. Mixed precision. The limits of training on an edge device. *Exercise:* estimate the training memory of a small CNN for two batch sizes.
- **TH-6.** Coresets, active learning, and data augmentation: methods that reach the same accuracy with less data.
- **TH-37.** Data, Algorithm, and Machine: the three places of a bottleneck. A method to find the bottleneck before you optimize. *Exercise:* name the bottleneck in three cases.

**Recap paths.** A path is a sequence of modules for one need. Present the modules in this order.

| Need | Modules | Time | Notes |
|---|---|---|---|
| Deep learning from the start | TH-9, TH-13, TH-14, TH-15, TH-16, TH-17, TH-18 | 300 min | Before Day 1, or as homework. TH-2 gives the practice. |
| Convolutional networks | TH-23, TH-24, TH-21, TH-22 | 175 min | Before Day 1 or Day 5. This path replaces the CNN recap deck that the template had. |
| Training of a model | TH-10, TH-17, TH-18, TH-19, TH-11 | 250 min | Before Day 3 or Day 6. |
| Language models | TH-28, TH-29, TH-30, TH-31, TH-5 | 250 min | Before Day 10. Add TH-27 if the class uses GA-10. |
| Mathematics | TH-7, TH-8 | 100 min | Before Day 1 and Day 6. |
| Computer systems | TH-33, TH-32, TH-34 | 125 min | Before Day 4, Day 7, and Day 9. |

The ID TH-1 was the CNN recap deck of the template. That deck was an example of the deck structure. It is not part of the course, and the ID is not used again.

### 6.8 Recommended replacements

| Problem | Replacement |
|---|---|
| Edge Impulse Studio is not available | MC-5 for keyword spotting. The notebook path of Day 3 for motion. |
| The Arduino build fails for many groups | MC-7 (SenseCraft AI) |
| The lab network fails on Days 11 to 13 | PI-7 and SY-9 (local sensors and a local dashboard), or GA-8 |
| Language model downloads fail on Day 10 | GA-9, GA-10, PI-2, or PI-3 |
| A group completes Week 1 labs early | MC-4, MC-6 |
| A group completes Week 2 labs early | PI-2, PI-4, GA-1, GA-3 |
| The class wants more generative AI | Replace Day 6 Part A with GA-9. Use GA-1, GA-2, and GA-8 as capstone components. |
| The class wants hands-on work with a Cortex-M board | NB-3 in place of the Day 3 lab, NB-5 in place of Day 5 Part A, NB-8 on Day 9 |
| Students need a recap of machine learning or deep learning | A recap path of Section 6.7. Example: the path "Deep learning from the start" and TH-2, before Day 1 or as homework. |

---

## 7. Assessment

This section is a proposal. Align the weights with the KAUST Academy rules.

| Component | Weight | Description |
|---|---|---|
| Daily labs | 40% | Demonstration to the instructor and a Decision Log (Days 1 to 13) |
| Quizzes | 20% | Two quizzes of 20 minutes (start of the Day 6 lab, start of the Day 11 lab) |
| Capstone | 40% | Proposal, demonstration, report (Days 14 and 15) |

**Decision Log.** A Decision Log is a short text of about 100 words. The student states one design decision, gives the measured numbers, and names the trade-off. The method comes from [assessment.qmd](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/instructors/assessment.qmd).

**Prediction before measurement.** Before each measurement, students write a numeric prediction. Then they measure and explain the difference. The method comes from [pedagogy.qmd](https://github.com/harvard-edge/cs249r_book/blob/330d4eaeadd5e0e2d9cd055aa78094d1ca660bd2/instructors/pedagogy.qmd).

**Lab deliverables.** The companion book lists deliverables and grading criteria for 30 Raspberry Pi labs: [Weekly Labs](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/weekly_labs.html). Use this page as a model for the lab check criteria.

**Capstone requirements.** The system must:

1. Use the XIAOML Kit and the Raspberry Pi.
2. Run at least one optimized model, with the size and accuracy before and after optimization.
3. Make one decision locally, and continue to work without the internet.
4. Send telemetry with MQTT to a dashboard.
5. Include a benchmark table with latency, memory, and energy.

**Capstone rubric (proposal).**

| Criterion | Weight |
|---|---|
| The system works in the demonstration | 30% |
| Integration of the two boards, messages, and monitoring | 25% |
| Measured results and analysis of trade-offs | 25% |
| Report and presentation | 20% |


## 10. Sources and references

This course adapts material from the sources below.

### Main textbook

**Machine Learning Systems: Principles and Practices of Engineering Artificially Intelligent Systems.**
Vijay Janapa Reddi and contributors, Harvard University.
Website: mlsysbook.ai. Repository: https://github.com/harvard-edge/cs249r_book. Licence: CC BY-NC-SA 4.0.
Used for: theory decks, kit labs, simulation labs, assessment method.

**TinyTorch.** Vijay Janapa Reddi and the TinyTorch contributors, Harvard University.
TinyTorch is the companion of the textbook. It is in the folder `tinytorch` of the textbook repository. Licence: MIT.
Used for: recap modules of Section 6.7 (tensors, activations, layers, losses, automatic differentiation, optimizers, the training loop, convolutions, tokenization, embeddings, attention, transformers, the KV cache).

### Companion books

**Edge AI Engineering: Raspberry Pi.** Marcelo Rovai (UNIFEI, TinyML4D).
Book: https://mjrovai.github.io/EdgeML_Made_Ease_ebook/. Book repository: https://github.com/Mjrovai/EdgeML_Made_Ease_ebook. Code: https://github.com/Mjrovai/EdgeML-with-Raspberry-Pi. Code licence: GPL-3.0.
Used for: Raspberry Pi labs (Days 6 to 10 and Day 13), generative AI modules, physical computing modules, lab check criteria.

**TinyML Made Easy: XIAO ESP32S3.** Marcelo Rovai (UNIFEI, TinyML4D).
Book: https://mjrovai.github.io/TinyML_Made_Easy_XIAO_ESP32S3_ebook/. Code: https://github.com/Mjrovai/XIAO-ESP32S3-Sense. Code licence: Apache-2.0.
Used for: XIAOML Kit labs (Days 1 to 5), camera streaming (Day 11).

**XIAO: Big Power, Small Board, Mastering Arduino and TinyML.** Lei Feng (Seeed Studio) and Marcelo Rovai.
Book: https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/. Repository: https://github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook. Licence: GPL-3.0.
Used for: Arduino basics, Wi-Fi and HTTP (Day 11), MQTT (Day 12).

### TinyML courseware for the Arduino Nano 33 BLE Sense

**HarvardX Professional Certificate in Tiny Machine Learning (TinyMLx).** Vijay Janapa Reddi, Laurence Moroney, Pete Warden, Lara Suzuki, and the TinyMLx team (Harvard University and Google).
Courseware: https://github.com/tinyMLx/courseware. Arduino library: https://github.com/tinyMLx/arduino-library. Licence: CC BY-NC-SA 4.0.
Used for: Nano 33 modules NB-1 to NB-12, and recap modules of Section 6.7.

**TensorFlow Lite Micro Arduino examples.** The TensorFlow Authors.
Repository: https://github.com/tensorflow/tflite-micro-arduino-examples. Licence: Apache-2.0.
Used for: module NB-2.

### Other references

- MIT 6.5940 "TinyML and Efficient Deep Learning Computing" (efficientml.ai): more depth for Days 4 and 6.
- Tool documentation: MicroPython, Edge Impulse, Ollama, Mosquitto, MediaMTX, Grafana, Prometheus.
---

## 12. Layout of the material in this repository

| Material | Location |
|---|---|
| Theory deck of a day | `LaTeX/DayNN_Theory.tex` with sections in `LaTeX/sections/dayNN/` |
| Lab deck of a day | `LaTeX/DayNN_Lab.tex` with sections in `LaTeX/sections/dayNN_lab/` |
| Lab files of a day | `Labs/dayNN/` |
| Backup module deck | `LaTeX/Module_<ID>.tex` with sections in `LaTeX/sections/modules/<ID>/` |
| Backup module lab files | `Labs/modules/<ID>/` with a `README.md` |
| Credits frame | `LaTeX/sections/credits.tex` |

Each backup module deck compiles alone. To add a module to a day, add its section files to the day deck with `\input` lines.
