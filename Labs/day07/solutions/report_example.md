# Day 7 lab report: example

This is an example of a complete report. Part C has the output of the
solution notebook on the work computer of the course, an x86 computer
(2026-10-02). Parts A, B, and D need a Raspberry Pi. The text "measure in
the lab" marks each such value.

Group: example

Names: the course team

Date: 2026-10-02

Host name of the Raspberry Pi: measure in the lab

## Part A: setup

| Item | Your result |
|---|---|
| Model (line `Model` of `check_pi.sh`) | measure in the lab |
| Release of the operating system | measure in the lab |
| Python version | measure in the lab |
| RAM in MB | measure in the lab |
| Temperature at the start | measure in the lab |
| Number of lines with `FAIL` | measure in the lab |
| Name of the camera in `rpicam-hello --list-cameras` | measure in the lab |
| Size of the test photo in bytes | measure in the lab |

## Part B: first inference

The model of the kit lab with the cat photo:

| Item | Your result |
|---|---|
| Shape and type of the input | 1 x 224 x 224 x 3, `uint8` |
| Number and type of the outputs | 1001 values, `uint8` |
| Load time in ms | measure in the lab |
| First inference in ms | measure in the lab |
| Median of the next runs in ms, 4 threads | measure in the lab |
| Median of the next runs in ms, 1 thread | measure in the lab |

The five classes after Task B1. These are the values of the work computer.
The values of the board can differ by some percent.

| Class | Probability in percent |
|---|---|
| tiger cat | 39 |
| Egyptian cat | 26 |
| tabby | 17 |
| lynx | 8 |
| carton | 2 |

The camera:

| Object in front of the camera | First class | Probability in percent | Median latency in ms |
|---|---|---|---|
| measure in the lab | | | |

Your answers:

1. The scale and the zero point of the output. The real value is
   `(integer - zero_point) * scale`.
2. measure in the lab. Possible reasons: the object is not one of the 1000 classes, the
   object is small in the image, or the light is low.

## Part C: export and inspect

Versions on the laptop:

| Tool | Version |
|---|---|
| Python | 3.10.12 |
| `torch` | 2.13.0+cpu |
| `onnx` | 1.23.1 |
| `onnxruntime` | 1.23.2 |
| `litert-torch` | 0.9.4 |

The graphs:

| Graph | Number | The four most frequent types |
|---|---|---|
| Layers of the PyTorch model (section 1) | 141 | BatchNorm2d 52, Conv2d 52, ReLU6 35, Dropout 1 |
| Nodes of `mnv2_static.onnx` (section 2) | 100 | Conv 52, Clip 35, Add 10, Gemm 1 |
| Operators of `mnv2.tflite` (section 4) | 70 | CONV_2D 35, DEPTHWISE_CONV_2D 17, ADD 10, PAD 5 |

Which layer type of the PyTorch model has no node in the ONNX file? The
batch normalization: the exporter folded each one into its convolution. The
dropout also has no node. The 35 activations are the 35 `Clip` nodes.

Static and dynamic shapes (section 3):

| Question | Your prediction | Result |
|---|---|---|
| Is the dynamic file slower for one image? | A little slower | No: 10.9 ms and 11.6 ms. The difference is noise. |
| What does the static file do with 2 images? | An error | An error: "Got invalid dimensions for input: image for the following indices index: 0 Got: 2 Expected: 1" |
| Is a batch of 4 faster for each image than 4 runs with one image? | Yes | No: 11.7 ms for each image. The first run with the new shape needs 60.7 ms, the next runs need 46.8 ms. |

The first run with a new shape is 30 percent slower than the next
runs, because the runtime plans the memory again.

The optimization levels of ONNX Runtime on the laptop (section 5).
Prediction: the basic level removes the batch normalizations, and it gives
the largest gain.

| Level | Nodes | Load time in s | Latency in ms | Node types |
|---|---|---|---|---|
| disabled | 152 | 0.048 | 26.8 | Conv 52, BatchNormalization 52, Clip 35, Add 10 |
| basic | 100 | 0.095 | 25.4 | Conv 52, Clip 35, Add 10, GlobalAveragePool 1 |
| extended | 65 | 0.079 | 24.2 | FusedConv 35, Conv 17, Add 10, GlobalAveragePool 1 |
| all | 56 | 0.084 | 11.6 | Conv 52, GlobalAveragePool 1, ReorderOutput 1, Flatten 1 |

The files in Netron:

1. `Conv`, `BatchNormalization`, and `Clip`.
2. The node `BatchNormalization` is gone. The `Conv` node has a third input:
   the bias `B`. The folding made it.
3. `FusedConv`. The attribute `activation` has the value `Clip`, and the
   attribute `activation_params` has the limits 0 and 6.
4. The property `fused_activation_function` with the value `RELU6`. Before
   the operator are a `Transpose` and a `Pad`. The `Transpose` changes the
   input from the order channel, height, width of PyTorch to the order
   height, width, channel of LiteRT. The `Pad` adds the border that the
   convolution of PyTorch has as a setting.
5. The level `all`, with a factor of 2.1 against the level before
   it. The prediction was wrong: the two fusion steps give a small gain, and
   the memory layout gives the large gain. This layout is for an x86
   processor.

Task 3:

| Item | Your result |
|---|---|
| Largest difference between the two outputs | 9.5e-07, with a largest output of 3.10 |
| Values of all batch normalizations of the model | 68224 |
| Bias values after the folding | 17056 |

The same result in each runtime (section 7):

| Runtime | Class | Difference |
|---|---|---|
| PyTorch | 644 (matchstick) | 0.0e+00 |
| ONNX Runtime, `float32` | 644 (matchstick) | 1.1e-06 |
| LiteRT, `float32` | 644 (matchstick) | 1.2e-06 |
| LiteRT, `int8` | 644 (matchstick) | 1.2e-01 |

## Part D: measure

| Question | Your prediction | Result |
|---|---|---|
| `float32`: which runtime is faster, LiteRT or ONNX Runtime? | Almost equal, as on the x86 processor of the lecture | measure in the lab |
| The gain from 1 thread to 4 threads: 4, more than 3, or less than 3? | About 3: a part of the work is not parallel | measure in the lab |
| LiteRT: is `int8` faster than `float32`? By which factor? | Yes, by a factor of 2 to 3: the guide for ExecuTorch reports 2.9 | measure in the lab |
| ONNX Runtime: is the dynamic file slower than the static file? | No, for one image | measure in the lab |

The latency table. Median latency in ms of the second run of `pi/bench.py`:

| Runtime | File | Precision | 1 thread | 2 threads | 4 threads |
|---|---|---|---|---|---|
| LiteRT | `mnv2.tflite` | `float32` | measure in the lab | | |
| LiteRT | `mnv2_int8.tflite` | `int8` | measure in the lab | | |
| LiteRT | `mobilenet_v2_1.0_224_quant.tflite` | `uint8` | measure in the lab | | |
| ONNX Runtime | `mnv2_static.onnx` | `float32` | measure in the lab | | |
| ONNX Runtime | `mnv2_dynamic.onnx` | `float32` | measure in the lab | | |
| ONNX Runtime | `mnv2_int8.onnx` | `int8` | measure in the lab | | |

`TEST_NOTES.md` has this table for the x86 work computer. Those values are
not values of the board.

| Item | Your result |
|---|---|
| Temperature at the start and at the end | measure in the lab |
| Largest difference between the two runs of the script, in percent | measure in the lab |
| Busy cores in `htop` for 1, 2, and 4 threads | measure in the lab |

The ratios:

| Ratio | LiteRT | ONNX Runtime |
|---|---|---|
| Gain from 1 thread to 4 threads, `float32` | measure in the lab | measure in the lab |
| Gain from `float32` to `int8`, 4 threads | measure in the lab | measure in the lab |
| Latency of the other runtime, divided by the latency of this runtime, `float32`, 4 threads | measure in the lab | measure in the lab |

Your answers:

1. measure in the lab
2. measure in the lab. A reason for a gain on the board: one NEON register holds 16
   values of `int8` and only 4 values of `float32`, and the `int8` kernels
   of XNNPACK are made for Arm.
3. measure in the lab. The method: 125 ms divided by the best `float32` latency.

## Decision Log

Question: a product with a Raspberry Pi 5 and a camera must classify 10
images in each second. The same program also reads the camera and sends each
result over the network. Which runtime, which precision, and how many threads
do you select for the model?

This is an example of the form. Replace each number with your number.

Decision: we select LiteRT with the `float32` file and 2 threads.

Numbers that support the decision: the budget is 100 ms for each image. Our
`float32` file needs ... ms with 2 threads and ... ms with 4 threads. The
`int8` file needs ... ms. The budget is not the limit for one of these
settings, so the fastest setting is not necessary.

Trade-off: 2 threads leave 2 cores for the camera and for the network, and
the board stays cooler. We keep `float32`, because the `int8` file loses
about 2 points of accuracy (77.4 percent against 75.2 percent on 500 test
images), and we do not need its speed. If the model becomes larger, or the
rate becomes higher, `int8` with 4 threads is the next step.
