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
- The class needs a recap of a machine learning or deep learning topic. The group "Recap and theory modules" has one module for each topic.
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

### Hardware for the classroom

- One dedicated Wi-Fi router. Days 11 to 13 need direct traffic between devices.
- Spare boards: about 10 to 15 percent of each type.
- One microSD card reader.

### Software

| Area | Tools |
|---|---|
| Microcontroller development | Arduino IDE 2, "esp32" core by Espressif. |
| MicroPython | MicroPython firmware for the ESP32-S3, `mpremote` or Thonny |
| Training | Python 3.10 or later, PyTorch, Keras with the LiteRT converter, Ultralytics |
| Conversion and runtimes | ONNX, ONNX Runtime, LiteRT (TensorFlow Lite), TensorFlow Lite Micro, NCNN, ExecuTorch (optional), Netron |
| Data collection | Edge Impulse Studio account and Edge Impulse CLI |
| Generative AI | Ollama and the Ollama Python library. |
| Networking | Mosquitto, `paho-mqtt`, PubSubClient, MediaMTX, FFmpeg, OpenCV, `iperf3` |
| Monitoring | Grafana with Prometheus. Fallback: a Python dashboard. |
| Optional simulation labs | `marimo` and `mlsysim` (interactive labs from the book) |

Training labs use small models. They run on a laptop CPU or on the free tier of Google Colab.

---

## 4. Course overview

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

**Recap modules**

- TH-3: ML workflow and life cycle (50 min, theory only). Use it before Part 3 of the lecture, or in place of Part 3 when the class needs the life cycle in depth.






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

**Recap modules**

- TH-3: ML workflow and life cycle (50 min, theory only). Use it before Part 1 of the lecture, or in place of Part 1 when the class needs the life cycle in depth.



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

---

## 6. Backup modules

Each backup module is independent of the other backup modules, unless its description names another module. The column "Fits day" gives the core days that use the topic.

Type: **T** is a theory deck. **L** is a lab with a short lab deck. **T+L** is both.

Each module has the same parts, so that you can present it alone:

- One slide deck that compiles alone. The deck has a title frame, the learning outcomes, the content, and the credits frame.
- One lab folder with the files and a README. The README gives the goal, the hardware, the duration, the steps, and the check criterion.
- No reference to a slide number or a file of another day.

**Recap and theory modules**

| ID | Module | Type | Time | Fits day |
|---|---|---|---|---|
| TH-3 | ML workflow and life cycle | T | 50 min | 1, 14 |

- **TH-3.** The stages of an ML project from the problem definition to monitoring, and the feedback between the stages. *Exercise:* a team finds a limit during monitoring that was never written in the problem definition. Give the cost multiplier of the illustrative model of the chapter, and name the stages to revisit. Sources: *Machine Learning Systems*, Volume I, chapter 3, and the slide deck of the same chapter. Deck: `Lectures/modules/Module_TH-3.pdf`.

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


## 8. Sources and references

This course adapts material from the sources below.

### Main textbook

**Machine Learning Systems: Principles and Practices of Engineering Artificially Intelligent Systems.**
Vijay Janapa Reddi and contributors, Harvard University.
Website: mlsysbook.ai. Repository: https://github.com/harvard-edge/cs249r_book. Licence: CC BY-NC-SA 4.0.
Used for: theory decks, kit labs, simulation labs, assessment method.

**TinyTorch.** Vijay Janapa Reddi and the TinyTorch contributors, Harvard University.
TinyTorch is the companion of the textbook. It is in the folder `tinytorch` of the textbook repository. Licence: MIT.

### Companion books

**Edge AI Engineering: Raspberry Pi.** Marcelo Rovai (UNIFEI, TinyML4D).
Book: https://mjrovai.github.io/EdgeML_Made_Ease_ebook/. Book repository: https://github.com/Mjrovai/EdgeML_Made_Ease_ebook. Code: https://github.com/Mjrovai/EdgeML-with-Raspberry-Pi. Code licence: GPL-3.0.
Used for: Raspberry Pi labs (Days 6 to 10 and Day 13), lab check criteria.

**TinyML Made Easy: XIAO ESP32S3.** Marcelo Rovai (UNIFEI, TinyML4D).
Book: https://mjrovai.github.io/TinyML_Made_Easy_XIAO_ESP32S3_ebook/. Code: https://github.com/Mjrovai/XIAO-ESP32S3-Sense. Code licence: Apache-2.0.
Used for: XIAOML Kit labs (Days 1 to 5), camera streaming (Day 11).

**XIAO: Big Power, Small Board, Mastering Arduino and TinyML.** Lei Feng (Seeed Studio) and Marcelo Rovai.
Book: https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/. Repository: https://github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook. Licence: GPL-3.0.
Used for: Arduino basics, Wi-Fi and HTTP (Day 11), MQTT (Day 12).

### TinyML courseware for the Arduino Nano 33 BLE Sense

**HarvardX Professional Certificate in Tiny Machine Learning (TinyMLx).** Vijay Janapa Reddi, Laurence Moroney, Pete Warden, Lara Suzuki, and the TinyMLx team (Harvard University and Google).
Courseware: https://github.com/tinyMLx/courseware. Arduino library: https://github.com/tinyMLx/arduino-library. Licence: CC BY-NC-SA 4.0.

**TensorFlow Lite Micro Arduino examples.** The TensorFlow Authors.
Repository: https://github.com/tensorflow/tflite-micro-arduino-examples. Licence: Apache-2.0.

### Other references

- MIT 6.5940 "TinyML and Efficient Deep Learning Computing" (efficientml.ai): more depth for Days 4 and 6.
- Tool documentation: MicroPython, Edge Impulse, Ollama, Mosquitto, MediaMTX, Grafana, Prometheus.

---

## 9. Layout of the material in this repository

| Material | Location |
|---|---|
| Theory deck of a day | `LaTeX/DayNN_Theory.tex` with sections in `LaTeX/sections/dayNN/` |
| Lab deck of a day | `LaTeX/DayNN_Lab.tex` with sections in `LaTeX/sections/dayNN_lab/` |
| Lab files of a day | `Labs/dayNN/` |
| Backup module deck | `LaTeX/Module_<ID>.tex` with sections in `LaTeX/sections/modules/<ID>/` and the PDF in `Lectures/modules/Module_<ID>.pdf` |
| Backup module lab files | `Labs/modules/<ID>/` |
| Credits frame | `LaTeX/sections/credits.tex` |
