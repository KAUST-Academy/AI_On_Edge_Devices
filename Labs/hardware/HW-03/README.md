# HW-03: Memory budget on the XIAO ESP32S3


Needed by: the Day 1 lab (model budgets), the Day 3 lab (measure), and the
Day 4 lab (float and int8 on the board).

## Decision

| Topic | Decision |
|---|---|
| Build with no PSRAM | Arduino IDE: `Tools` > `PSRAM` > `Disabled`. `arduino-cli`: the board name `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled`. |
| Build with PSRAM | Arduino IDE: `Tools` > `PSRAM` > `OPI PSRAM`. `arduino-cli`: `esp32:esp32:XIAO_ESP32S3:PSRAM=opi`. |
| Free memory | The functions of `ESP` in the Arduino core: `getFreeHeap()`, `getMaxAllocHeap()`, `getFreePsram()` |
| Arena size | `interpreter->arena_used_bytes()` after `AllocateTensors()`, then a search for the smallest size that works |
| Flash use | The line `Sketch uses ... bytes` of the build, and `ESP.getSketchSize()` |

## Reason

- The PSRAM setting is a build option of the board. It needs no change of the
  hardware. One sketch then gives both budgets.
- `Disabled` is the default value of the board `XIAO_ESP32S3`. A student who
  forgets the setting measures the small budget, not the large one. The camera
  labs fail without PSRAM, so each lab names the setting that it needs.
- `arena_used_bytes()` is the number that TensorFlow Lite Micro itself
  reports. It is exact for one model and one library version.
- The functions of `ESP` need no library. The Day 1 lab uses them before the
  students know TensorFlow Lite Micro.

## Sources

| Item | Source |
|---|---|
| PSRAM setting, 8 MB PSRAM, 8 MB flash | XIAOML Kit setup chapter of "Machine Learning Systems" (section "Microphone Test") |
| Build options `PSRAM=disabled` and `PSRAM=opi` | `boards.txt` of the Arduino core "esp32" 3.3.12, board `XIAO_ESP32S3` |
| Memory functions | `cores/esp32/Esp.h` and `cores/esp32/esp32-hal-psram.h` of the same core |
| `arena_used_bytes()` | `tensorflow/lite/micro/micro_interpreter.h` of Chirale_TensorFlowLite 2.0.0 |
| 512 KB of internal SRAM | ESP32-S3 data sheet of Espressif |

## Files

| File | Content |
|---|---|
| `sketches/memory_report/memory_report.ino` | Prints the flash, the internal RAM, and the PSRAM. Needs no library. For Day 1. |
| `sketches/arena_report/arena_report.ino` | Loads a model, prints the arena use and the latency. The arena is in the internal RAM or in the PSRAM. For Days 3 and 4. |
| `sketches/arena_report/model.h` | The sine model of `HW-02`. Replace it with your model. |

## The three memories of the board

| Memory | Size | What it holds |
|---|---|---|
| Flash | 8 MB chip. The default partition gives 3 342 336 bytes to one sketch. | The program, the model weights (`model.h`), the constants |
| Internal RAM | 512 KB in the chip. The build tool reports a limit of 327 680 bytes for the data of a sketch. | The stack, the global variables, the heap, the tensor arena |
| PSRAM | 8 MB, external, active only with `OPI PSRAM` | Large buffers: images, audio, a large tensor arena |

The model weights stay in flash. Only the arena needs RAM. The arena holds
the activations, so its size depends on the peak activation memory of the
model, not on the number of parameters. Day 1 calculates this number. Day 3
measures it.

## Method 1: the memory budget (Day 1)

1. Open `sketches/memory_report/memory_report.ino`.
2. Set `Tools` > `PSRAM` > `Disabled`. Upload. Open the Serial Monitor at
   115200 baud.
3. Write down: free heap, largest block, sketch size.
4. Set `Tools` > `PSRAM` > `OPI PSRAM`. Upload again.
5. Write down the same values, and the free PSRAM.

The value "Largest block that malloc can give" is the budget for one tensor
arena in the internal RAM. It is smaller than the free heap, because the heap
has more than one region.

With `arduino-cli`:

```bash
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3:PSRAM=disabled sketches/memory_report
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3:PSRAM=opi sketches/memory_report
```

Add `--upload --port PORT` to upload.

## Method 2: the arena size of a model (Days 3 and 4)

1. Open `sketches/arena_report/arena_report.ino`. Put your `model.h` in the
   sketch folder (`Labs/hardware/HW-02/tflite_to_header.py` makes it).
2. Register the operators of your model in the sketch.
3. Set `kTensorArenaSize` to a large value, for example `64 * 1024`.
4. Upload with `PSRAM` > `Disabled`. Read "Arena used".
5. Set `kTensorArenaSize` to "Arena used", rounded up to the next multiple
   of 16. Upload. If `AllocateTensors()` fails, add 16 and try again.
6. Write down: model size (flash), smallest arena size, mean latency.
7. If the arena does not fit in the internal RAM: set `ARENA_IN_PSRAM` to 1,
   select `OPI PSRAM`, and upload. Write down the latency again.

Results to expect:

- The message `not enough memory for the arena` means that the arena is
  larger than the largest free block.
- The message `AllocateTensors() failed` means that the arena is smaller
  than the model needs.
- Predict the latency with the arena in the PSRAM before you measure it. The
  PSRAM is an external chip.

## Facts from the compile check

These numbers come from the compiler on the work computer (core 3.3.12). They
are not measured on a board.

| Sketch | PSRAM option | Flash (bytes) | Static RAM (bytes) |
|---|---|---|---|
| `memory_report` | Disabled | 274 217 | 21 832 |
| `memory_report` | OPI PSRAM | 279 435 | 22 308 |
| `arena_report` | Disabled | 332 077 | 23 592 |
| `arena_report` | OPI PSRAM | 337 311 | 24 076 |

- The PSRAM driver adds about 5 200 bytes of flash and about 480 bytes of
  static RAM.
- "Static RAM" is the line `Global variables use ... bytes` of the build. The
  arena of `arena_report` is not in this number, because the sketch reserves
  it at run time.

The free heap, the largest block, the arena use, and the latency are **not**
in this file. Nobody measured them. The instructor measures them in the test
below.

## Code status

| File | State | Source | Change |
|---|---|---|---|
| `sketches/memory_report/memory_report.ino` | new | Functions of `Esp.h` | not tested |
| `sketches/arena_report/arena_report.ino` | changed | `examples/hello_world/hello_world.ino` of Chirale_TensorFlowLite 2.0.0 | New: the arena on the heap with `heap_caps_aligned_alloc`, the switch `ARENA_IN_PSRAM`, the memory lines, the latency loop. Removed: the serial input. |
| `sketches/arena_report/model.h` | copied with no change | `Labs/hardware/HW-02/sketches/tflm_hello/model.h` | none |

Compile check (no board):

| Sketch | Board name (FQBN) | Result | Date |
|---|---|---|---|
| `memory_report` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 2026-10-01 |
| `memory_report` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 2026-10-01 |
| `arena_report` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles | 2026-10-01 |
| `arena_report` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 2026-10-01 |
| `arena_report` with `ARENA_IN_PSRAM 1` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles | 2026-10-01 |

## Test steps for the instructor

- Date of the test:
- Core version, library version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Method 1, PSRAM disabled | Heap size, free heap, largest block, sketch size, flash chip size | |
| 2 | Method 1, OPI PSRAM | The same values, and PSRAM size and free PSRAM | |
| 3 | Read the report "with 100 KB reserved" in both builds | From which memory does `malloc` take the 100 KB when PSRAM is active? | |
| 4 | Method 2 with the sine model, PSRAM disabled | Arena used, smallest arena that works, mean latency | |
| 5 | Method 2, `ARENA_IN_PSRAM 1`, OPI PSRAM | Mean latency. The ratio to step 4. | |
| 6 | In `arena_report`, set `kTensorArenaSize` to `400 * 1024`, PSRAM disabled | The error message that the board prints | |
| 7 | Fill the Day 1 table | "XIAO without PSRAM": the largest block of step 1. "XIAO with PSRAM": the free PSRAM of step 2. | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the measured budgets in the Day 1 lab `README.md` and in the Day 1
   lab deck.
3. Write the answer of step 3 in this file. The Day 5 lab needs it.

## Credits

The PSRAM setting comes from the XIAOML Kit setup chapter of "Machine Learning
Systems" by Vijay Janapa Reddi and contributors (mlsysbook.ai,
CC BY-NC-SA 4.0). The interpreter code adapts the example `hello_world` of
Chirale_TensorFlowLite (github.com/spaziochirale/Chirale_TensorFlowLite,
Apache-2.0).
