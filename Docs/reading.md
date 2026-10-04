# Reading list

This file gives the books of the course "AI on Edge Devices" and the
reading for each day. The books are free to read online.

- The first item of each day is the main source of the lecture. Start
  there.
- "Papers and standards" are for more depth. They are not necessary for the
  lab.
- "Tools" are the manuals of the programs that the lab of the day uses.
- The last frames of each theory deck (`Lectures/DayNN_Theory.pdf`) give the
  same list, and the credits of the lecture.

## 1. The books

| Book | Authors | Where | Licence |
|---|---|---|---|
| *Machine Learning Systems*, Volume I and Volume II | Vijay Janapa Reddi and contributors, Harvard University | [mlsysbook.ai/vol1](https://mlsysbook.ai/vol1/), [mlsysbook.ai/vol2](https://mlsysbook.ai/vol2/) | CC BY-NC-SA 4.0 |
| *Machine Learning Systems*, hardware kits: the labs for the XIAOML Kit and the Raspberry Pi | Vijay Janapa Reddi and contributors | [mlsysbook.ai/kits](https://mlsysbook.ai/kits/) | CC BY-NC-SA 4.0 |
| TinyTorch, the companion of the textbook | Vijay Janapa Reddi and the TinyTorch contributors | [mlsysbook.ai/tinytorch](https://mlsysbook.ai/tinytorch/) | MIT |
| *Edge AI Engineering: Raspberry Pi* | Marcelo Rovai | [mjrovai.github.io/EdgeML_Made_Ease_ebook](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/) | Not stated |
| *TinyML Made Easy: XIAO ESP32S3* | Marcelo Rovai | [mjrovai.github.io/TinyML_Made_Easy_XIAO_ESP32S3_ebook](https://mjrovai.github.io/TinyML_Made_Easy_XIAO_ESP32S3_ebook/) | Not stated |
| *XIAO: Big Power, Small Board* | Lei Feng and Marcelo Rovai | [mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/) | GPL-3.0 |
| HarvardX TinyML courseware (slides and readings) | Vijay Janapa Reddi, Laurence Moroney, Pete Warden, Lara Suzuki, and the TinyMLx team | [github.com/tinyMLx/courseware](https://github.com/tinyMLx/courseware) | CC BY-NC-SA 4.0 |
| MIT 6.5940, "TinyML and Efficient Deep Learning Computing" (lecture course) | Song Han, MIT | [efficientml.ai](https://efficientml.ai) | See the site |

Notes:

- *Machine Learning Systems* is the main textbook.
- *Edge AI Engineering* is the main source of the Raspberry Pi labs.
- Some chapters of *XIAO: Big Power, Small Board* use the XIAO ESP32C3 or
  the XIAO nRF52840. The labs of this course have the code for the XIAO
  ESP32S3.


## 2. Reading for each day

### Day 1: Edge AI landscape and system constraints

Books:

- *Machine Learning Systems*, Volume I, chapter [Introduction](https://mlsysbook.ai/vol1/introduction/introduction.html)
- *Machine Learning Systems*, Volume I, chapter [ML Systems](https://mlsysbook.ai/vol1/ml_systems/ml_systems.html)
- *Machine Learning Systems*, hardware kits: [Hardware Platforms](https://mlsysbook.ai/kits/contents/platforms.html)
- *Machine Learning Systems*, hardware kits: [XIAOML Kit, Setup](https://mlsysbook.ai/kits/contents/seeed/xiao_esp32s3/setup/setup.html)
- *XIAO: Big Power, Small Board*, chapter 4.1: [Understanding TinyML and Edge Impulse Studio](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/chapter_4-1.html)

Papers and standards:

- [MobileNetV2: Inverted Residuals and Linear Bottlenecks](https://arxiv.org/abs/1801.04381), Sandler et al., 2018
- [MCUNet: Tiny Deep Learning on IoT Devices](https://arxiv.org/abs/2007.10319), Lin et al., 2020

Tools:

- [Arduino IDE 2](https://docs.arduino.cc/software/ide/)
- [Arduino core for the ESP32](https://docs.espressif.com/projects/arduino-esp32/)

### Day 2: Embedded systems, MicroPython, and sensor data collection

Books:

- *Machine Learning Systems*, Volume I, chapter [Data Engineering](https://mlsysbook.ai/vol1/data_engineering/data_engineering.html)
- *Machine Learning Systems*, hardware kits: [XIAOML Kit, Setup](https://mlsysbook.ai/kits/contents/seeed/xiao_esp32s3/setup/setup.html)
- *Machine Learning Systems*, hardware kits: [XIAOML Kit, Motion Classification and Anomaly Detection](https://mlsysbook.ai/kits/contents/seeed/xiao_esp32s3/motion_classification/motion_classification.html)
- *XIAO: Big Power, Small Board*, chapter 2.4: [Rhythmic Dance with a Triaxial Accelerometer](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/chapter_2-4.html)

Papers and standards:

- [ESP32-S3 Series Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf), Espressif Systems
- LSM6DS3TR-C: iNEMO inertial module, data sheet, STMicroelectronics (search for the part number on `st.com`)

Tools:

- [MicroPython documentation](https://docs.micropython.org/)
- [Edge Impulse documentation](https://docs.edgeimpulse.com/)

### Day 3: From trained model to microcontroller

Books:

- *Machine Learning Systems*, Volume I, chapter [ML Frameworks](https://mlsysbook.ai/vol1/frameworks/frameworks.html), section "Deployment Targets"
- *Machine Learning Systems*, hardware kits: [XIAOML Kit, Motion Classification and Anomaly Detection](https://mlsysbook.ai/kits/contents/seeed/xiao_esp32s3/motion_classification/motion_classification.html)
- *Machine Learning Systems*, hardware kits: [DSP Spectral Features](https://mlsysbook.ai/kits/contents/shared/dsp_spectral_features_block/dsp_spectral_features_block.html)
- *XIAO: Big Power, Small Board*, chapter 4.2: [Anomaly Detection & Motion Classification](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/chapter_4-2.html)

Papers and standards:

- [TensorFlow Lite Micro: Embedded Machine Learning on TinyML Systems](https://arxiv.org/abs/2010.08678), David et al., 2021

Tools:

- [LiteRT documentation](https://ai.google.dev/edge/litert)
- [Netron](https://netron.app), a viewer for model files
- [ONNX](https://onnx.ai)

### Day 4: Quantization

Books:

- *Machine Learning Systems*, Volume I, chapter [Model Compression](https://mlsysbook.ai/vol1/model_compression/model_compression.html), section "Quantization and Precision"

Papers and standards:

- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](https://arxiv.org/abs/1712.05877), Jacob et al., 2018
- [A White Paper on Neural Network Quantization](https://arxiv.org/abs/2106.08295), Nagel et al., 2021
- [Estimating or Propagating Gradients Through Stochastic Neurons for Conditional Computation](https://arxiv.org/abs/1308.3432), Bengio et al., 2013 (the straight-through estimator)

Tools:

- [LiteRT documentation](https://ai.google.dev/edge/litert), the pages on model optimization
- [Netron](https://netron.app), a viewer for model files. It shows the scale and the zero point of each tensor.

### Day 5: Audio and vision on microcontrollers

Books:

- *Machine Learning Systems*, Volume I, chapter [Network Architectures](https://mlsysbook.ai/vol1/nn_architectures/nn_architectures.html), section "CNNs: Spatial Pattern Processing"
- *Machine Learning Systems*, hardware kits: [XIAOML Kit, Keyword Spotting (KWS)](https://mlsysbook.ai/kits/contents/seeed/xiao_esp32s3/kws/kws.html)
- *Machine Learning Systems*, hardware kits: [KWS Feature Engineering](https://mlsysbook.ai/kits/contents/shared/kws_feature_eng/kws_feature_eng.html)
- *Machine Learning Systems*, hardware kits: [XIAOML Kit, Image Classification](https://mlsysbook.ai/kits/contents/seeed/xiao_esp32s3/image_classification/image_classification.html)
- *XIAO: Big Power, Small Board*, chapter 4.3: [Sound Classification (KWS)](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/chapter_4-3.html)
- *XIAO: Big Power, Small Board*, chapter 4.4: [Image Classification](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/chapter_4-4.html)

Papers and standards:

- [Hello Edge: Keyword Spotting on Microcontrollers](https://arxiv.org/abs/1711.07128), Zhang et al., 2017
- [Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition](https://arxiv.org/abs/1804.03209), Warden, 2018
- [Visual Wake Words Dataset](https://arxiv.org/abs/1906.05721), Chowdhery et al., 2019
- [MCUNet: Tiny Deep Learning on IoT Devices](https://arxiv.org/abs/2007.10319), Lin et al., 2020

Tools:

- [Edge Impulse documentation](https://docs.edgeimpulse.com/), with the pages on MFCC and on FOMO

### Day 6: Pruning, distillation, and efficient design

Books:

- *Machine Learning Systems*, Volume I, chapter [Model Compression](https://mlsysbook.ai/vol1/model_compression/model_compression.html), sections "Structural Optimization", "Architectural Efficiency", and "Technique Selection"

Papers and standards:

- [Learning both Weights and Connections for Efficient Neural Networks](https://arxiv.org/abs/1506.02626), Han et al., 2015
- [The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks](https://arxiv.org/abs/1803.03635), Frankle and Carbin, 2019
- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531), Hinton, Vinyals, and Dean, 2015
- [EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks](https://arxiv.org/abs/1905.11946), Tan and Le, 2019
- [MCUNet: Tiny Deep Learning on IoT Devices](https://arxiv.org/abs/2007.10319), Lin et al., 2020

Tools:

- [MIT 6.5940, "TinyML and Efficient Deep Learning Computing"](https://efficientml.ai), for more depth

### Day 7: Hardware acceleration and inference runtimes

Books:

- *Machine Learning Systems*, Volume I, chapter [Hardware Acceleration](https://mlsysbook.ai/vol1/hw_acceleration/hw_acceleration.html)
- *Machine Learning Systems*, Volume I, chapter [Model Serving](https://mlsysbook.ai/vol1/model_serving/model_serving.html)
- *Machine Learning Systems*, hardware kits: [Raspberry Pi, Setup](https://mlsysbook.ai/kits/contents/raspi/setup/setup.html)
- *Machine Learning Systems*, hardware kits: [Raspberry Pi, Image Classification](https://mlsysbook.ai/kits/contents/raspi/image_classification/image_classification.html)

Papers and standards:

- [Roofline: An Insightful Visual Performance Model for Multicore Architectures](https://doi.org/10.1145/1498765.1498785), Williams, Waterman, and Patterson, 2009
- [TVM: An Automated End-to-End Optimizing Compiler for Deep Learning](https://arxiv.org/abs/1802.04799), Chen et al., 2018

Tools:

- [ONNX Runtime](https://onnxruntime.ai/docs)
- [LiteRT documentation](https://ai.google.dev/edge/litert)
- [NCNN](https://github.com/Tencent/ncnn)
- [ExecuTorch](https://executorch.ai)

### Day 8: Object detection at the edge

Books:

- *Machine Learning Systems*, hardware kits: [Raspberry Pi, Object Detection](https://mlsysbook.ai/kits/contents/raspi/object_detection/object_detection.html)
- *Machine Learning Systems*, Volume I, chapter [Model Compression](https://mlsysbook.ai/vol1/model_compression/model_compression.html) (calibration)
- *Edge AI Engineering*: [Object Detection: Fundamentals](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/object_detection/object_detection_fundamentals.html)
- *Edge AI Engineering*: [Computer Vision Applications with YOLO](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/object_detection/cv_yolo.html)
- *Edge AI Engineering*: [Custom Object Detection Project](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/object_detection/custom_object_detection.html)

Papers and standards:

- [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640), Redmon, Divvala, Girshick, and Farhadi, 2016
- [SSD: Single Shot MultiBox Detector](https://arxiv.org/abs/1512.02325), Liu et al., 2016
- [EfficientDet: Scalable and Efficient Object Detection](https://arxiv.org/abs/1911.09070), Tan, Pang, and Le, 2020

Tools:

- [Ultralytics YOLO](https://docs.ultralytics.com)
- [Ultralytics guide for the Raspberry Pi](https://docs.ultralytics.com/guides/raspberry-pi)
- [COCO dataset](https://cocodataset.org)

### Day 9: Benchmarking and profiling

Books:

- *Machine Learning Systems*, Volume I, chapter [Benchmarking](https://mlsysbook.ai/vol1/benchmarking/benchmarking.html)
- *Edge AI Engineering*: [Multi-Token Prediction on the Raspberry Pi 5](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/mtp/mtp.html), section "How this was measured"

Papers and standards:

- [MLPerf Tiny Benchmark](https://arxiv.org/abs/2106.07597), Banbury et al., 2021
- [MLPerf Inference Benchmark](https://arxiv.org/abs/1911.02549), Reddi et al., 2020
- [MLPerf Power: Benchmarking the Energy Efficiency of Machine Learning Systems from Microwatts to Megawatts for Sustainable AI](https://arxiv.org/abs/2410.12032), Tschand et al., 2025

Tools:

- [MLPerf Tiny](https://mlcommons.org/benchmarks/inference-tiny/)
- [MLPerf Inference Edge](https://mlcommons.org/benchmarks/inference-edge/)

### Day 10: Generative AI at the edge

Books:

- *Machine Learning Systems*, hardware kits: [Raspberry Pi, Small Language Models](https://mlsysbook.ai/kits/contents/raspi/llm/llm.html)
- *Machine Learning Systems*, hardware kits: [Raspberry Pi, Vision-Language Models](https://mlsysbook.ai/kits/contents/raspi/vlm/vlm.html)
- *Edge AI Engineering*: [SLMs at the Edge](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/local_inference/local_inference.html)
- *Edge AI Engineering*: [SLM: Basic Optimization Techniques](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/llm/slm_opt_tech.html)
- *Edge AI Engineering*: [Vision-Language Models at the Edge](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/vlm/vlm.html)

Papers and standards:

- [LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971), Touvron et al., 2023
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401), Lewis et al., 2020
- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531), Hinton, Vinyals, and Dean, 2015

Tools:

- [Ollama](https://ollama.com)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM)

### Day 11: Networking fundamentals and RTSP streaming

Books:

- *Machine Learning Systems*, Volume I, chapter [ML Systems](https://mlsysbook.ai/vol1/ml_systems/ml_systems.html), section "Edge ML: Latency and Privacy"
- *XIAO: Big Power, Small Board*, chapter 3.4: [Implementing Wi-Fi Connection and Applications](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/chapter_3-4.html)

Papers and standards:

- [RFC 3550: RTP, A Transport Protocol for Real-Time Applications](https://www.rfc-editor.org/rfc/rfc3550), 2003
- [RFC 7826: Real-Time Streaming Protocol Version 2.0](https://www.rfc-editor.org/rfc/rfc7826), 2016
- [Overview of the H.264/AVC Video Coding Standard](https://doi.org/10.1109/TCSVT.2003.815165), Wiegand, Sullivan, Bjøntegaard, and Luthra, 2003

Tools:

- [MediaMTX](https://github.com/bluenviron/mediamtx)
- [FFmpeg](https://ffmpeg.org/documentation.html)
- [iperf3](https://github.com/esnet/iperf)

### Day 12: Local decision-making and MQTT

Books:

- *Machine Learning Systems*, Volume I, chapter [ML Systems](https://mlsysbook.ai/vol1/ml_systems/ml_systems.html), section "Hybrid Architectures"
- *XIAO: Big Power, Small Board*, chapter 3.5: [Telemetry and Commands using the MQTT protocol](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/chapter_3-5.html)

Papers and standards:

- [MQTT Version 3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html), OASIS, 2014
- [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html), OASIS, 2019

Tools:

- [Mosquitto](https://mosquitto.org/documentation/)
- [Eclipse Paho Python client](https://eclipse.dev/paho/)
- [MicroPython library `umqtt.simple`](https://github.com/micropython/micropython-lib)

### Day 13: Monitoring, logging, and visualization

Books:

- *Machine Learning Systems*, Volume I, chapter [ML Operations](https://mlsysbook.ai/vol1/ml_ops/ml_ops.html), section "Production Operations"
- *Machine Learning Systems*, Volume II, chapter [ML Operations at Scale](https://mlsysbook.ai/vol2/ops_scale/ops_scale.html), section "Monitoring at Scale"
- *Edge AI Engineering*: [Experimenting with SLMs for IoT Control](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/iot/slm_iot.html), section "Adding Data Logging"

Papers and standards:

- [A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks](https://arxiv.org/abs/1610.02136), Hendrycks and Gimpel, 2017
- [Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift](https://arxiv.org/abs/1810.11953), Rabanser, Günnemann, and Lipton, 2019

Tools:

- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/grafana/latest/)

### Day 14: Production edge AI design and capstone start

Books:

- *Machine Learning Systems*, Volume II, chapter [Edge Intelligence](https://mlsysbook.ai/vol2/edge_intelligence/edge_intelligence.html), sections "Design Constraints" and "Production Integration"
- *Machine Learning Systems*, Volume II, chapter [Security & Privacy](https://mlsysbook.ai/vol2/security_privacy/security_privacy.html)
- *XIAO: Big Power, Small Board*, chapter 2.1: [Introduction to Product Prototype Design](https://mjrovai.github.io/XIAO_Big_Power_Small_Board-ebook/chapter_2-1.html)

Papers and standards:

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629), McMahan et al., 2017
- [Stealing Machine Learning Models via Prediction APIs](https://arxiv.org/abs/1609.02943), Tramèr et al., 2016

Tools:

- [The Update Framework](https://theupdateframework.io/)
- [Mender](https://docs.mender.io/), over-the-air updates

### Day 15: Capstone build and demonstrations

Books:

- *Machine Learning Systems*, Volume I, chapter [Conclusion](https://mlsysbook.ai/vol1/conclusion/conclusion.html)
- *Machine Learning Systems*, Volume I, chapter [ML Systems](https://mlsysbook.ai/vol1/ml_systems/ml_systems.html)
- *Machine Learning Systems*, Volume I, chapter [Benchmarking](https://mlsysbook.ai/vol1/benchmarking/benchmarking.html)
- *Machine Learning Systems*, Volume II, chapter [Edge Intelligence](https://mlsysbook.ai/vol2/edge_intelligence/edge_intelligence.html)
- *Edge AI Engineering*: [the labs](https://mjrovai.github.io/EdgeML_Made_Ease_ebook/) that your capstone uses

Papers and standards:

- [MLPerf Tiny Benchmark](https://arxiv.org/abs/2106.07597), Banbury et al., 2021
- [MCUNet: Tiny Deep Learning on IoT Devices](https://arxiv.org/abs/2007.10319), Lin et al., 2020


