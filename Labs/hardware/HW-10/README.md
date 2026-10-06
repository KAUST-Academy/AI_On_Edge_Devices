# HW-10: Arduino Nano 33 BLE Sense Rev2

Needed by: the backup modules NB-1 to NB-7.

## The examples and their sensors

Sizes from the compile check: core 4.6.0, Harvard_TinyMLx 1.2.4-Alpha,
Arduino_BMI270_BMM150 1.2.4, ArduinoBLE 2.1.0, `NANO33_BLE_REV2` defined
where it applies. The sizes are not measured on a board.

| Example | Module | Sensors and outputs | Extra hardware | Tensor arena | Flash (bytes) | Static RAM (bytes) |
|---|---|---|---|---|---|---|
| `test_IMU` | NB-1 | IMU: accelerometer, gyroscope, magnetometer | none | no model | 116 768 (11%) | 46 600 (17%) |
| `test_microphone` | NB-1 | PDM microphone. Start with the shield button or with the serial command `click`. | shield optional | no model | 94 840 (9%) | 46 696 (17%) |
| `test_camera` | NB-1 | OV7675 camera, 176 × 144, RGB565 | camera module, shield or wires | no model | 96 896 (9%) | 97 664 (37%) |
| `hello_world` | NB-2 | none. Output: LED brightness. | none | 2 000 | 253 560 (25%) | 53 136 (20%) |
| `magic_wand` | NB-4 | IMU. Output: Bluetooth Low Energy. | none | 30 × 1024 | 443 936 (45%) | 159 240 (60%) |
| `micro_speech` | NB-5 | PDM microphone. Output: RGB LED. | none | 10 × 1024 | 180 544 (18%) | 76 800 (29%) |
| `person_detection` | NB-6 | OV7675 camera. Output: RGB LED. | camera module, shield or wires | 136 × 1024 | 453 512 (46%) | 186 616 (71%) |
| `multi_tenant` | NB-7 | PDM microphone and OV7675 camera | camera module, shield or wires | 136 × 1024 | 496 720 (50%) | 206 992 (78%) |

Facts for the modules:

- The tensor arena is a global array. It is in the "Static RAM" number.
  `person_detection` uses 71 percent of the RAM before the program starts.
  This is the example for "the model uses almost all the RAM of the board".
- `multi_tenant` runs two models with one arena of 136 KB. Its static RAM is
  only 20 376 bytes more than `person_detection`.
- `hello_world` and `micro_speech` need no shield and no camera.
- Module NB-3 (motion classification) uses no example of this library. It
  uses Edge Impulse (chapter 4.2 of "XIAO: Big Power, Small Board").
- The camera module is part of the Arduino Tiny Machine Learning Kit. With
  no shield, the reading 4-2-3 of the courseware gives the 20 wire
  connections.

## Steps

### 1. Install the core and the libraries

Arduino IDE:

1. Boards Manager: install **Arduino Mbed OS Nano Boards**.
2. Library Manager: install **Harvard_TinyMLx**, **Arduino_BMI270_BMM150**,
   and **ArduinoBLE**.

`arduino-cli`:

```bash
arduino-cli core install arduino:mbed_nano
arduino-cli lib install "Harvard_TinyMLx" "Arduino_BMI270_BMM150" "ArduinoBLE"
```

### 2. Select the board

1. Connect the board with a micro-USB **data** cable. The green LED is on.
2. `Tools` > `Board` > `Arduino Mbed OS Nano Boards` > `Arduino Nano 33 BLE`.
3. `Tools` > `Port`: the port that shows `Arduino Nano 33 BLE`.

If the upload fails, press the reset button of the board two times quickly.
The orange LED then fades in and out, and the board waits for an upload. The
port name can change in this mode.

### 3. Open an example

`File` > `Examples` > `Harvard_TinyMLx` > the example.

For `test_IMU` and `magic_wand` on the Rev2 board, change the line

```cpp
// #define NANO33_BLE_REV2
```

to

```cpp
#define NANO33_BLE_REV2
```

The IDE asks for a new location, because an example is read-only. Save the
sketch in your sketchbook.

### 4. Test the sensors (module NB-1)

Open the Serial Monitor at 9600 baud. Set the line ending to
`Both NL & CR`. The courseware reading 4-2-13 gives the details.

| Example | Commands | What you see |
|---|---|---|
| `test_IMU` | `a`, `g`, or `m` | Three values: acceleration in g, rotation in degrees per second, or magnetic field in microtesla. The Serial Plotter shows three lines. |
| `test_microphone` | Shield button, or `click` | A stream of numbers. The Serial Plotter shows the wave. |
| `test_camera` | `single`, then `capture`. Or `live`. | Bytes of one image in hexadecimal. The reading explains how to see the image. |

Only one program can use the serial port. Close the Serial Monitor and the
Serial Plotter before an upload.

### 5. Compile with no board

```bash
arduino-cli compile --fqbn arduino:mbed_nano:nano33ble <sketch folder>
```

Use the option `--clean` after you change the version of a library. Without
it, the tool can use old compiled files of the library, and the build fails
with "undefined reference".

## Test steps for the instructor

- Date of the test:
- Board revision that the label of the board shows:
- Core version and library versions:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run steps 1 and 2 | Does the port show the board? Time of the installation. | |
| 2 | Upload Blink (`File` > `Examples` > `01.Basics`) | Does the orange LED blink? | |
| 3 | Upload `test_IMU` **without** the define on the Rev2 board | The text that the board prints (the expected text is "Failed to initialize IMU") | |
| 4 | Upload `test_IMU` with the define | The values of `a` with the board flat. Which axis shows 1 g? | |
| 5 | Upload `test_microphone` | Does `click` start the stream with no shield? | |
| 6 | Upload `test_camera` with the camera module | Does `single` and `capture` give image bytes? | |
| 7 | Upload `hello_world` | Does the LED change its brightness? | |
| 8 | Upload `micro_speech` | Which LED colour shows "yes", "no", and an unknown word? Does it react to your voice? | |
| 9 | Upload `magic_wand` with the define | Does the board appear as a Bluetooth device? | |
| 10 | Upload `person_detection` and `multi_tenant` | Does each sketch start? The LED colour for "person" and for "no person". | |
| 11 | Time steps 1 to 5 | Minutes. The plan for NB-1 is 60 minutes. | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Write the versions that work in `Labs/VERSIONS.md`.
2. If an example fails with the core 4.6.0, test the older core that the
   courseware names, and write the result here.
