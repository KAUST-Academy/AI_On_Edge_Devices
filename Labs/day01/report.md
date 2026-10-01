# Day 1 lab report

Group:

Names:

Date:

## Part A: toolchain

Versions:

| Tool | Version |
|---|---|
| Arduino IDE | |
| esp32 core | |
| Python | |
| `torch` | |
| `torchvision` | |

The last two lines of the build output for `blink` (PSRAM disabled):

```
Sketch uses ... bytes (...%) of program storage space. Maximum is ... bytes.
Global variables use ... bytes (...%) of dynamic memory, leaving ... bytes for local variables. Maximum is ... bytes.
```

## Part B: sensor tests

| Test | Result (pass or fail) | What you saw |
|---|---|---|
| IMU | | Z value with the kit flat on the table: |
| Display | | |
| Microphone | | |
| Camera | | Bytes of one frame: . Capture time in ms: . |
| Wi-Fi | | Number of networks: . RSSI of the strongest network: . |

Prediction before the camera test:

- Bytes of one frame of 320 x 240 pixels with one byte for each pixel:
- Does one frame fit in the RAM of a microcontroller with 256 KB?

## Part C: model budgets

### The memory of the board (`memory_report`)

| Value | PSRAM disabled | OPI PSRAM |
|---|---|---|
| Heap size (bytes) | | |
| Free heap (bytes) | | |
| Largest block that malloc can give (bytes) | | |
| PSRAM size (bytes) | not active | |
| Free PSRAM (bytes) | not active | |

### Predictions (task 2 of the notebook)

Write the predictions before you run section 4 of the notebook.

| Question | Your prediction | Result |
|---|---|---|
| Most parameters | | |
| Most operations (MACs) | | |
| Largest peak activation memory | | |
| Ratio of parameters, ResNet-18 to MobileNetV2 | | |

One sentence for each prediction that was wrong:

### The table "model and device"

Write "fits", or "does not fit" with the reason (flash, RAM, or flash and
RAM).

| Model | Type | Model size | Peak in RAM | Microcontroller, 256 KB | XIAO, no PSRAM | XIAO, with PSRAM | Raspberry Pi 5 |
|---|---|---|---|---|---|---|---|
| MobileNetV2 | `float32` | | | | | | |
| MobileNetV2 | `int8` | | | | | | |
| ResNet-18 | `float32` | | | | | | |
| ResNet-18 | `int8` | | | | | | |
| Small depthwise CNN | `float32` | | | | | | |
| Small depthwise CNN | `int8` | | | | | | |

The RAM budgets that you used for the XIAO (measured values, or the values
of the notebook):

### Answers to the four questions

1. Which model fits the microcontroller with 256 KB of RAM, and in which data
   type?

2. MobileNetV2 in `int8` on the XIAO with PSRAM: why does the model not fit?
   Which number must change?

3. Which model has the larger peak activation memory, ResNet-18 or
   MobileNetV2? Why?

4. Which device can run all six rows? What is the price in power?

## Decision Log

Question: you must classify images of 96 x 96 pixels on the XIAOML Kit. Which
of the three models do you select, in which data type, and with PSRAM or with
no PSRAM? Which budget decides?

About 100 words:
