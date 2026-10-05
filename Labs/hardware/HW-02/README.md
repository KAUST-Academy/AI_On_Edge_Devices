# HW-02: TensorFlow Lite Micro on the ESP32-S3


Needed by: the Day 3 lab (convert and deploy) and the Day 5 lab.

## Decision

The course uses two paths to run a model on the XIAO ESP32S3.

| Path | Library | Used for |
|---|---|---|
| A. Own model | **Chirale_TensorFlowLite 2.0.0** (Arduino Library Manager) | Day 3 Part B and C, Day 4 Part D: the students convert a model and write the inference code |
| B. Edge Impulse | The Arduino library that Edge Impulse Studio makes for each project | Day 3 Part D, Day 5: keyword spotting and image classification |

This folder prepares path A. The kit labs of the sources give path B.

## Reason

- The library is in the Arduino Library Manager. A student installs it with
  one click. It needs no ESP-IDF and no command line.
- It supports the architecture `esp32`. The minimal sketch of this folder
  compiles for `esp32:esp32:XIAO_ESP32S3` with the core 3.3.12.
- It contains the source code of TensorFlow Lite Micro. The students can read
  the interpreter, the operator resolver, and the kernels. Day 3 teaches these
  parts.
- It uses the standard API of TensorFlow Lite Micro (`MicroInterpreter`,
  `MicroMutableOpResolver`, `arena_used_bytes()`). The same code works on the
  Nano 33 BLE, so the modules NB-2 and NB-8 can compare the two boards.
- Its licence is Apache-2.0.

Options that were compared on 2026-10-01:

| Library | Result |
|---|---|
| Chirale_TensorFlowLite 2.0.0 | **Selected.** Source code, architecture `esp32`, compiles with the core 3.3.12. |
| ArduTFLite 1.0.2 | A wrapper of the Chirale library with a simpler API. It hides the interpreter and the arena, which Day 3 must show. Not selected. |
| tflm_esp32 2.0.0 | A compiled binary (`libtflm_esp32.a`, 30 MB) from 2024. The students cannot read the kernels. Not selected. |
| Arduino_TensorFlowLite (`tflite-micro-arduino-examples`) | Its README says that it is for Arm Cortex-M boards. Not for the ESP32-S3. The Nano 33 modules use it. |
| esp-tflite-micro by Espressif | A component for ESP-IDF, not an Arduino library. It has the ESP-NN kernels. Not selected, because the course uses the Arduino IDE. |

**Limit of the decision.** The Chirale library has optimized kernels for Arm
(`cmsis_nn`) but none for the ESP32-S3. On the XIAO it runs the reference
kernels. Path A can then be slower than a build with the ESP-NN kernels of
Espressif. The instructor measures path A and path B in the test below. The
Part 2 of the Day 3 theory can use the result as an example for optimized kernels.

## Sources

| Item | Source |
|---|---|
| Minimal sketch | Example `hello_world` of Chirale_TensorFlowLite 2.0.0 (`github.com/spaziochirale/Chirale_TensorFlowLite`, Apache-2.0) |
| Sine model | The same example. The model comes from the TensorFlow Lite Micro "hello world" example of the TensorFlow Authors (Apache-2.0). |
| Path B | Motion classification chapter and keyword spotting chapter of "Machine Learning Systems", and `XIAOML_Kit_code/` of "XIAO ESP32S3 Sense" |
| Core version warning for path B | XIAOML Kit setup chapter of "Machine Learning Systems" |

## Files

| File | Content |
|---|---|
| `sketches/tflm_hello/tflm_hello.ino` | Minimal sketch: load the model, run it, print the arena use and the latency |
| `sketches/tflm_hello/model.h` | The sine model as a C array |
| `models/hello_world.tflite` | The same model as a file. Open it in Netron. |
| `models/NOTICE.txt` | The licence notice of the model |
| `tflite_to_header.py` | Converts a `.tflite` file to `model.h` |

## Steps

### 1. Install the library

1. Open the Library Manager of the Arduino IDE.
2. Enter `Chirale_TensorFlowLite`. Install version 2.0.0.

With `arduino-cli`:

```bash
arduino-cli lib install "Chirale_TensorFLowLite@2.0.0"
```

The name in the library index has a capital `L` in `FLow`.

### 2. Run the minimal sketch

1. Open `sketches/tflm_hello/tflm_hello.ino`.
2. Select the board `XIAO_ESP32S3` and the port. Upload.
3. Open the Serial Monitor at 115200 baud.

You see the model size (2488 bytes), the arena size (2000 bytes), the arena
use, and then one line for each inference:

```
x,y_model,y_true,error,latency_us
0.000,0.000,0.000,0.000,<latency>
0.314,...
```

The same model on the work computer (LiteRT 2.2.0) gives a maximum error of
0.118 and a mean error of 0.039 for the 20 input values. The board must give
the same values of `y_model`, because the model uses integer arithmetic.

### 3. Use your own model

```bash
python3 tflite_to_header.py my_model.tflite sketches/my_sketch/model.h
```

Then change three places in the sketch:

1. The operators. Add one `Add...()` call for each operator type of the model
   and set the number in `MicroMutableOpResolver<N>`. Netron shows the
   operators.
2. `kTensorArenaSize`. Start with a large value. Read "Arena used" in the
   Serial Monitor. `Labs/hardware/HW-03/` gives the method.
3. The input code and the output code. Use `input->type` to see if the model
   needs `int8` or `float` values.

## Facts from the compile check

These numbers come from the compiler on the work computer. They are not
measured on a board. Board: `esp32:esp32:XIAO_ESP32S3`, core 3.3.12,
PSRAM disabled.

| Sketch | Flash (bytes) | Static RAM (bytes) |
|---|---|---|
| Empty sketch with `Serial.begin` | 271 457 | 21 824 |
| `tflm_hello` with one operator (`MicroMutableOpResolver<1>`) | 336 157 | 25 616 |
| `tflm_hello` with all operators (`AllOpsResolver`) | 557 537 | 31 296 |

- TensorFlow Lite Micro with one operator adds 64 700 bytes of flash.
- All operators add 221 380 bytes more. The operator resolver is the reason
  that a sketch registers only the operators of its model.
- The maximum sketch size of the default partition scheme is 3 342 336 bytes.

## Path B: the Edge Impulse library

- Edge Impulse Studio makes one Arduino library for each project
  (`Deployment` > `Arduino library`). The library contains the model, the
  signal processing code, and its own copy of TensorFlow Lite Micro.
- The sketches of `XIAOML_Kit_code/` include this library, for example
  `#include <XIAOML_Kit_Motion_Class_-_AD_inferencing.h>`. The name depends
  on the project name.
- Only the Studio can make this library. A session cannot compile these
  sketches with no project. Each lab writes this in its `TEST_NOTES.md`.
- The kit setup chapter warns: an esp32 core of version 3.x can fail with the
  deployment code of Edge Impulse. Then use the core 2.0.17. The instructor
  tests this in step 6 below.
- Path A and path B install different libraries. They do not conflict,
  because each sketch includes only one of them.

## Code status

| File | State | Source | Change |
|---|---|---|---|
| `sketches/tflm_hello/tflm_hello.ino` | changed | `examples/hello_world/hello_world.ino` of Chirale_TensorFlowLite 2.0.0 | The sketch makes its own input values. One operator in place of `AllOpsResolver`. Prints the arena use and the latency. Serial speed 115200. Waits 3 s for the Serial Monitor, not without limit. |
| `sketches/tflm_hello/model.h` | changed | `examples/hello_world/model.h` of the same library | The same 2488 bytes. `tflite_to_header.py` made the file again, with an include guard. |
| `models/hello_world.tflite` | copied with no change | The bytes of `model.h` above | none |
| `tflite_to_header.py` | new | no source | tested on the work computer |

Compile check (no board):

| Sketch | Board name (FQBN) | Result | Date |
|---|---|---|---|
| `tflm_hello` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles: 336 157 bytes flash, 25 616 bytes RAM | 2026-10-01 |
| `tflm_hello` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles: 341 391 bytes flash, 26 100 bytes RAM | 2026-10-01 |

## Test steps for the instructor

- Date of the test:
- Core version, library version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run steps 1 and 2 | "Arena used" in bytes. "Free internal heap" in bytes. | |
| 2 | Read 20 lines of the output | The largest error. Compare with 0.118. | |
| 3 | Read the column `latency_us` | Minimum, typical value, maximum | |
| 4 | Set `kTensorArenaSize` to the "Arena used" value plus 16. Then decrease it in steps of 16. | The smallest value for which `AllocateTensors()` passes | |
| 5 | Replace the resolver with `AllOpsResolver` | Flash size in the IDE. Does the latency change? | |
| 6 | Deploy one Edge Impulse project (path B) with the core 3.3.12 | Does the sketch compile and run? If not: the error text, and the result with the core 2.0.17. | |
| 7 | Run the Day 3 motion model with path A and with path B. Look in the Edge Impulse library for the folder `edge-impulse-sdk/porting/espressif/ESP-NN`. | Latency of both paths. Is ESP-NN in the library? | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the core version that works with path B in `Labs/VERSIONS.md`.
3. If path A is too slow for Day 5, use path B for both Day 5 models.

## Credits

The sketch and the model adapt the example `hello_world` of the library
Chirale_TensorFlowLite by Chirale and the TensorFlow Authors
(github.com/spaziochirale/Chirale_TensorFlowLite, Apache-2.0).
