# Day 7 lab report

Group:

Names:

Date:

Host name of the Raspberry Pi:

## Part A: setup

| Item | Your result |
|---|---|
| Model (line `Model` of `check_pi.sh`) | |
| Release of the operating system | |
| Python version | |
| RAM in MB | |
| Temperature at the start | |
| Number of lines with `FAIL` | |
| Name of the camera in `rpicam-hello --list-cameras` | |
| Size of the test photo in bytes | |

## Part B: first inference

The model of the kit lab with the cat photo:

| Item | Your result |
|---|---|
| Shape and type of the input | |
| Number and type of the outputs | |
| Load time in ms | |
| First inference in ms | |
| Median of the next runs in ms, 4 threads | |
| Median of the next runs in ms, 1 thread | |

The five classes after Task B1:

| Class | Probability in percent |
|---|---|
| | |
| | |
| | |
| | |
| | |

The camera:

| Object in front of the camera | First class | Probability in percent | Median latency in ms |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

Your answers:

1. The output of this model has the type `uint8`. Which two numbers of the
   output details do you need to get a real value?
2. Which object did the model not name correctly? Give a possible reason.

## Part C: export and inspect

Versions on the laptop:

| Tool | Version |
|---|---|
| Python | |
| `torch` | |
| `onnx` | |
| `onnxruntime` | |
| `litert-torch` | |

The graphs:

| Graph | Number | The four most frequent types |
|---|---|---|
| Layers of the PyTorch model (section 1) | | |
| Nodes of `mnv2_static.onnx` (section 2) | | |
| Operators of `mnv2.tflite` (section 4) | | |

Which layer type of the PyTorch model has no node in the ONNX file?

Static and dynamic shapes (section 3). Write the prediction before you run
the cell.

| Question | Your prediction | Result |
|---|---|---|
| Is the dynamic file slower for one image? | | |
| What does the static file do with 2 images? | | |
| Is a batch of 4 faster for each image than 4 runs with one image? | | |

The optimization levels of ONNX Runtime on the laptop (section 5). Write the
prediction before you run the cell: which level removes the batch
normalizations, and which level gives the largest gain in time?

| Level | Nodes | Load time in s | Latency in ms | Node types |
|---|---|---|---|---|
| disabled | | | | |
| basic | | | | |
| extended | | | | |
| all | | | | |

The files in Netron:

1. In `mnv2_unfused.onnx`, which three nodes come after the input?
2. In `mnv2_level_basic.onnx`, which of these nodes is gone? Which new input
   does the first `Conv` node have?
3. In `mnv2_level_extended.onnx`, what is the name of the first node? Which
   attribute holds the activation?
4. In `mnv2.tflite`, which property of the first `Conv2D` operator holds the
   activation? Which operator comes before it, and why?
5. Which level gives the largest gain on your laptop?

Task 3:

| Item | Your result |
|---|---|
| Largest difference between the two outputs | |
| Values of all batch normalizations of the model | |
| Bias values after the folding | |

The same result in each runtime (section 7):

| Runtime | Class | Difference |
|---|---|---|
| PyTorch | | |
| ONNX Runtime, `float32` | | |
| LiteRT, `float32` | | |
| LiteRT, `int8` | | |

## Part D: measure

Write the prediction before you run `pi/bench.py`.

| Question | Your prediction | Result |
|---|---|---|
| `float32`: which runtime is faster, LiteRT or ONNX Runtime? | | |
| The gain from 1 thread to 4 threads: 4, more than 3, or less than 3? | | |
| LiteRT: is `int8` faster than `float32`? By which factor? | | |
| ONNX Runtime: is the dynamic file slower than the static file? | | |

The latency table. Median latency in ms of the second run of `pi/bench.py`:

| Runtime | File | Precision | 1 thread | 2 threads | 4 threads |
|---|---|---|---|---|---|
| LiteRT | `mnv2.tflite` | `float32` | | | |
| LiteRT | `mnv2_int8.tflite` | `int8` | | | |
| LiteRT | `mobilenet_v2_1.0_224_quant.tflite` | `uint8` | | | |
| ONNX Runtime | `mnv2_static.onnx` | `float32` | | | |
| ONNX Runtime | `mnv2_dynamic.onnx` | `float32` | | | |
| ONNX Runtime | `mnv2_int8.onnx` | `int8` | | | |

| Item | Your result |
|---|---|
| Temperature at the start and at the end | |
| Largest difference between the two runs of the script, in percent | |
| Busy cores in `htop` for 1, 2, and 4 threads | |

The ratios:

| Ratio | LiteRT | ONNX Runtime |
|---|---|---|
| Gain from 1 thread to 4 threads, `float32` | | |
| Gain from `float32` to `int8`, 4 threads | | |
| Latency of the other runtime, divided by the latency of this runtime, `float32`, 4 threads | | |

Your answers:

1. Compare the results with your predictions.
2. The lecture measured these files on an x86 processor: `int8` gave no gain
   in time there. What do you measure on the Raspberry Pi? Give a reason.
3. With one MAC in each clock cycle, the model needs 125 ms on this board
   (Part 1 of the lecture). How many times faster is your best `float32`
   result?

## Decision Log

Question: a product with a Raspberry Pi 5 and a camera must classify 10
images in each second. The same program also reads the camera and sends each
result over the network. Which runtime, which precision, and how many threads
do you select for the model?

Decision:

Numbers that support the decision:

Trade-off:
