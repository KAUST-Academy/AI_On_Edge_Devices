# Day 9 lab report

Group:

Names:

Date:

Host name of the Raspberry Pi:

## Part A: the protocol

Write this part before the first measurement. Do not change it after you
see a result. If you must change the method, write the change and the
reason in the last row.

The seven parts of your benchmark:

| Part | XIAOML Kit | Raspberry Pi 5 |
|---|---|---|
| Task | Keyword spotting and image classification | The same two tasks, image classification with MobileNetV2, and object detection |
| Dataset: the input of each run | | |
| Model: the files | | |
| Metrics, with their units | | |
| Harness: the program that reads the clock | | |
| System description: board, clock, runtime, threads | | |
| Run rules: warm-up runs | | |
| Run rules: timed runs | | |
| Run rules: the statistic that you report | | |
| The timed window | | |
| What your benchmark does not include | | |
| Changes of the method, with the reason | | |

Your predictions. Give a number or a factor, and one reason from the
lecture.

| Question | Your prediction | Result |
|---|---|---|
| Kit: is the `int8` model faster than the `float32` model? By which factor? | | |
| Kit: is the first inference slower than the median? | | |
| Kit: by which factor does the latency change from 240 MHz to 80 MHz? | | |
| The same `int8` file on the two boards: how many times faster is the Raspberry Pi? | | |
| Raspberry Pi: the gain of MobileNetV2 from 1 thread to 4 threads | | |
| Raspberry Pi: which runtime is faster for the detector, NCNN or LiteRT? | | |
| The same `int8` keyword model: which board uses less energy for one inference? | | |
| Raspberry Pi: does the latency change in a run of 3 minutes? | | |

## Part B: the microcontroller

| Item | Your result |
|---|---|
| Version of the esp32 core | |
| Setting of `Tools` > `PSRAM` | |
| `WARMUP_RUNS` and `TIMED_RUNS` | |
| The line `Sketch uses ... bytes` of the build | |
| The line `Global variables use ... bytes` of the build | |
| Free internal heap and PSRAM (second line of the Serial Monitor) | |
| The line of Task B1 in the Serial Monitor | |

The four models at 240 MHz. Copy the values of the Serial Monitor.

| Model | Model bytes (flash) | Arena bytes (RAM) | Arena memory | First inference in ms | Median in ms | p95 in ms | Maximum in ms | Same result as LiteRT |
|---|---|---|---|---|---|---|---|---|
| Keyword spotting, `int8` | | | | | | | | |
| Keyword spotting, `float32` | | | | | | | | |
| Image classification, `int8` | | | | | | | | |
| Image classification, `float32` | | | | | | | | |

The second run of the same sketch (send a character in the Serial Monitor):

| Model | Median of run 1 in ms | Median of run 2 in ms | Difference in percent |
|---|---|---|---|
| Keyword spotting, `int8` | | | |
| Image classification, `int8` | | | |

The clock of the processor:

| Model | Median at 240 MHz in ms | Median at 80 MHz in ms | Factor |
|---|---|---|---|
| Keyword spotting, `int8` | | | |
| Image classification, `int8` | | | |

Published results of MLPerf Tiny v1.2 for the same two `int8` reference
models (closed division, the latency is 1000 divided by the published rate):

| Board | Processor | Software | Keyword spotting | Image classification |
|---|---|---|---|---|
| NUCLEO-L4R5ZI | Cortex-M4 at 120 MHz | X-CUBE-AI v9.0 | 43.2 ms | 165.1 ms |
| NUCLEO-U575ZI-Q | Cortex-M33 at 160 MHz | X-CUBE-AI v9.0 | 29.1 ms | 111.1 ms |
| NUCLEO-H7A3ZI-Q | Cortex-M7 at 280 MHz | X-CUBE-AI v9.0 | 11.3 ms | 40.8 ms |
| Your XIAO ESP32S3 | Xtensa LX7 at 240 MHz | TensorFlow Lite Micro (Chirale_TensorFlowLite 2.0.0) | | |

Your keyword model of Day 5 (from your Day 5 report, if you have it):

| Item | Day 5 value | Method of Day 5 |
|---|---|---|
| Feature time (`dsp_ms`) | | |
| Inference time (`classification_ms`) | | |

Your answers:

1. Which arena is in the PSRAM? Why?
2. Compare your latency with the three published boards. Your clock is
   faster than the clock of two of them. Give two possible reasons for the
   difference.
3. The Day 5 measurement used the median of 10 lines of the Serial Monitor.
   Which parts of your protocol did it not have?

## Part C: the Raspberry Pi

| Item | Your result |
|---|---|
| The line `Device` of `pi/bench.py` | |
| Versions of `ai_edge_litert`, `onnxruntime`, and `ncnn` | |
| `--warmup` and `--runs` | |
| Idle: temperature and estimated power (`--idle 30`) | |
| The line of Task C1 | |

The kit models on the Raspberry Pi (`--suite tiny`, 1 thread):

| Model | First inference in ms | Median in ms | p95 in ms | Class check |
|---|---|---|---|---|
| Keyword spotting, `int8` | | | | |
| Keyword spotting, `float32` | | | | |
| Image classification, `int8` | | | | |
| Image classification, `float32` | | | | |

Image classification with MobileNetV2 (`--suite classification`):

| Runtime | File | Threads | First inference in ms | Median in ms | p95 in ms | Peak RAM in MB | Highest temperature in C | Power in W |
|---|---|---|---|---|---|---|---|---|
| LiteRT | `mnv2.tflite` | 1 | | | | | | |
| LiteRT | `mnv2.tflite` | 4 | | | | | | |
| LiteRT | `mnv2_int8.tflite` | 1 | | | | | | |
| LiteRT | `mnv2_int8.tflite` | 4 | | | | | | |
| ONNX Runtime | `mnv2_static.onnx` | 1 | | | | | | |
| ONNX Runtime | `mnv2_static.onnx` | 4 | | | | | | |
| ONNX Runtime | `mnv2_int8.onnx` | 1 | | | | | | |
| ONNX Runtime | `mnv2_int8.onnx` | 4 | | | | | | |

Object detection with your model of Day 8 (`--suite detection`):

| Runtime | File | Threads | First inference in ms | Median in ms | p95 in ms | Peak RAM in MB | Highest temperature in C | Power in W |
|---|---|---|---|---|---|---|---|---|
| NCNN | `cupbottle_320_ncnn_model` | 1 | | | | | | |
| NCNN | `cupbottle_320_ncnn_model` | 4 | | | | | | |
| LiteRT | `cupbottle_320.tflite` | 1 | | | | | | |
| LiteRT | `cupbottle_320.tflite` | 4 | | | | | | |
| LiteRT | `cupbottle_320_int8.tflite` | 1 | | | | | | |
| LiteRT | `cupbottle_320_int8.tflite` | 4 | | | | | | |

The sustained run of 180 seconds (`--sustain 180`):

| Item | First window | Last window |
|---|---|---|
| Median latency in ms | | |
| p95 in ms | | |
| Temperature in C | | |
| Clock in MHz | | |
| Throttle state | | |
| Estimated power in W | | |

Your answers:

1. The Day 8 lab measured the frame rate of this detector with the camera
   (end to end). Write that value. Calculate 1000 divided by your median of
   today for the same file and the same threads. Explain the difference.
2. Which case has the largest ratio of p95 to the median? Give a possible
   reason.
3. Did the temperature change the latency in the sustained run? Give the
   two latencies and the two temperatures.

## Part D: the report

The power of each board:

| Board and state | Power in W | Method: power meter, estimate of the board, or data sheet |
|---|---|---|
| Kit, active | | |
| Kit, idle | | |
| Kit, sleep | | |
| Raspberry Pi, active | | |
| Raspberry Pi, idle | | |

The line of Tasks D1 and D2 of `pi/make_report.py`:

Copy the four tables of the file `report_tables.md` here:

The accuracy of each model. You did not measure it today: write the source.

| Model | Accuracy | Test set | Source of the value |
|---|---|---|---|
| Keyword spotting, `int8` | | | |
| Keyword spotting, `float32` | | | |
| Image classification, `int8` | | | |
| Image classification, `float32` | | | |
| MobileNetV2, `float32` | | | |
| MobileNetV2, `int8` (LiteRT) | | | |
| Your detector, `float32`: mAP50-95 | | | |
| Your detector, `int8`: mAP50-95 | | | |

Your answers:

1. For which model is the factor between the two boards the largest? Give a
   reason.
2. One inference of the `int8` keyword model: which board uses less energy?
   By which factor? Which board is faster?
3. The image classifier of MLPerf Tiny has a published accuracy from 200
   test images. Which difference of two models can you see with 200 images?
4. Which three numbers of this report have the weakest method? Say how you
   can measure each of them better.

## Decision Log

Question: a company wants a keyword detector that runs from a battery for
one month, and a camera that counts cups on a desk with 10 frames in each
second. You have the two boards of this course. Which board do you select
for each product? Which precision, which runtime, and how many threads?

Decision:

Numbers that support the decision, each with its method:

Trade-off:
