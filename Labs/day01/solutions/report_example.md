# Day 1 lab report: example for the instructor


This file gives the parts of the report that need no board. The numbers come
from `solutions/model_budgets.ipynb`. The parts that need a board have the
text "measure in the lab".

## Part A: toolchain

The two lines of the build output for `blink` with PSRAM disabled (result of
the compiler on the work computer, esp32 core 3.3.12):

```
Sketch uses 271701 bytes (8%) of program storage space. Maximum is 3342336 bytes.
Global variables use 21824 bytes (6%) of dynamic memory, leaving 305856 bytes for local variables. Maximum is 327680 bytes.
```

## Part B: sensor tests

| Test | Result | What you see |
|---|---|---|
| IMU | measure in the lab | Z value near 1.0 g with the kit flat (statement of the kit setup chapter) |
| Display | measure in the lab | `Hello` and `World!` in a frame |
| Microphone | measure in the lab | The line of the Serial Plotter follows the voice |
| Camera | measure in the lab | Bytes of one frame: 76 800. Capture time: measure in the lab. |
| Wi-Fi | measure in the lab | The list of the networks |

Prediction before the camera test:

- One frame of 320 x 240 pixels with one byte for each pixel has
  320 x 240 = 76 800 bytes. This is 75 KB.
- The frame fits in 256 KB of RAM, but it uses 29 % of it. A colour frame
  with two bytes for each pixel has 153 600 bytes (150 KB) and uses 59 %.
  Then the model has less than half of the RAM.

## Part C: model budgets

### The memory of the board

Measure in the lab.

### Predictions (task 2 of the notebook)

| Question | Result |
|---|---|
| Most parameters | ResNet-18: 11 689 512 |
| Most operations (MACs) | ResNet-18: 1 814 073 344 |
| Largest peak activation memory | MobileNetV2: 1 505 280 values |
| Ratio of parameters, ResNet-18 to MobileNetV2 | 3.3 |

Many students predict that ResNet-18 has the largest peak, because it has the
most parameters. The peak of MobileNetV2 is larger: its second block expands
the tensor to 96 channels at 112 x 112.

The three budgets of the models:

| Model | Parameters | MACs | Peak (values) | Peak at layer |
|---|---|---|---|---|
| MobileNetV2 | 3 504 872 | 300 774 272 | 1 505 280 | `features_2_conv_1_0` |
| ResNet-18 | 11 689 512 | 1 814 073 344 | 1 003 520 | `maxpool` |
| Small depthwise CNN | 14 186 | 5 116 160 | 110 592 | `block1_3` |

### The table "model and device"

The RAM budgets of the XIAO in this table are the values of the notebook:
298.7 KB with no PSRAM (result of the compiler) and 8.0 MB with PSRAM (size of
the chip). The measured values can be smaller. A result can then change.

| Model | Type | Model size | Peak in RAM | Microcontroller, 256 KB | XIAO, no PSRAM | XIAO, with PSRAM | Raspberry Pi 5 |
|---|---|---|---|---|---|---|---|
| MobileNetV2 | `float32` | 13.4 MB | 5.7 MB | does not fit (flash and RAM) | does not fit (flash and RAM) | does not fit (flash) | fits |
| MobileNetV2 | `int8` | 3.3 MB | 1.4 MB | does not fit (flash and RAM) | does not fit (flash and RAM) | does not fit (flash) | fits |
| ResNet-18 | `float32` | 44.6 MB | 3.8 MB | does not fit (flash and RAM) | does not fit (flash and RAM) | does not fit (flash) | fits |
| ResNet-18 | `int8` | 11.1 MB | 980.0 KB | does not fit (flash and RAM) | does not fit (flash and RAM) | does not fit (flash) | fits |
| Small depthwise CNN | `float32` | 55.4 KB | 432.0 KB | does not fit (RAM) | does not fit (RAM) | fits | fits |
| Small depthwise CNN | `int8` | 13.9 KB | 108.0 KB | fits | fits | fits | fits |

### Answers to the four questions

1. Only the small depthwise CNN in `int8`. Its peak is 108.0 KB and the device
   has 211.1 KB for tensors. In `float32` the peak is 432.0 KB, so the RAM is
   too small. The model size (13.9 KB or 55.4 KB) is not the problem.
2. The flash decides, not the RAM. The model has 3 504 872 bytes. The default
   partition of the board gives 3 342 336 bytes to one sketch, and the program
   needs about 300 KB of it. The number of parameters must decrease, for
   example with a narrower MobileNetV2. A different partition scheme of the
   8 MB flash chip is a second option.
3. MobileNetV2: 1 505 280 values. ResNet-18: 1 003 520 values. The second
   block of MobileNetV2 expands the tensor to 96 channels at 112 x 112
   (1 204 224 values). ResNet-18 has its peak at the first pooling layer, and
   its later tensors are small. The parameters do not show the peak.
4. The Raspberry Pi 5 runs all six rows. The row "Edge" of the paradigm table
   gives 15 to 40 W. The row "TinyML" gives 100 mW. The factor is 150 to 400.
   The students measure the power of the two boards on Day 9.

## Decision Log (example)

We select the small depthwise CNN in `int8` on the XIAO with no PSRAM. Its
model size is 13.9 KB and its peak activation memory is 108.0 KB. The budget
of the board is 3.2 MB of flash and 298.7 KB of RAM, so the RAM budget
decides, and the model uses about one third of it. In `float32` the peak is
432.0 KB, which does not fit with no PSRAM. MobileNetV2 in `int8` needs 3.3 MB
of flash and 1.4 MB of RAM. It does not fit the flash, and it needs the PSRAM.
The trade-off: the small model has less capacity, so its accuracy is lower,
but it leaves the PSRAM free for the camera image. We measure the accuracy
and the latency on Day 5.

## What to check in a student report

- The predictions are in the report, and the student explains each wrong
  prediction.
- Each "does not fit" has a reason.
- The Decision Log gives numbers from the table, not only words.
- The Decision Log names a trade-off. Example: memory against accuracy.
