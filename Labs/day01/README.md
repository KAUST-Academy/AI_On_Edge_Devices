# Day 1 lab: toolchain, sensor tests, and model budgets

Hardware status: not tested on hardware (prepared on 2026-10-01)

**Goal.** Your group has a toolchain that works, and a first resource budget
for each device class.

**Deliverable.** The file `report.md` with the results of the five sensor
tests, the completed table "model and device", and the Decision Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Toolchain: Arduino IDE, esp32 core, Python environment, Blink | 50 min |
| B | Sensor tests: IMU, display, microphone, camera, Wi-Fi | 45 min |
| C | Model budgets: memory of the board, notebook, table, Decision Log | 55 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| XIAOML Kit | 1 | XIAO ESP32S3 Sense with the camera, and the expansion board with the IMU and the display |
| USB-C cable | 1 | A data cable. A cable for charging only does not work. |
| Wi-Fi antenna of the kit | 1 | Connect it before the Wi-Fi test |
| Laptop | 1 | Windows, macOS, or Linux |

Do not install the heat sink on the XIAO. The heat sink does not fit under the
expansion board.

## Software

| Tool | Version | Note |
|---|---|---|
| Arduino IDE 2 | see `Labs/VERSIONS.md` | Step 1 of `Labs/SETUP.md` |
| esp32 by Espressif Systems (board core) | 3.3.12 | The sketches were compiled with this version |
| Seeed Arduino LSM6DS3 (library) | 2.0.7 | For the IMU test |
| U8g2 by oliver (library) | 2.36.19 | For the display test |
| Python | 3.10 or later | The notebook ran with Python 3.10.12 |
| `torch`, `torchvision`, `numpy`, `matplotlib`, `jupyterlab` | see `Labs/VERSIONS.md` | For the notebook |

Install the Python packages from the root of this repository:

```bash
python3 -m venv .venv
.venv/bin/pip install -r Labs/requirements.txt
```

On Windows, the programs of the environment are in `.venv\Scripts\`, not in
`.venv/bin/`.

On Linux, the default package of PyTorch is larger than 2 GB. The notebook
needs only the CPU version. Install the CPU version first:

```bash
.venv/bin/pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r Labs/requirements.txt
```

## Files

| File | Content |
|---|---|
| `sketches/blink/` | Part A. Switches the built-in LED on and off. |
| `sketches/imu_test/` | Part B. Prints the accelerometer and the gyroscope values. |
| `sketches/oled_test/` | Part B. Shows "Hello World!" on the display. |
| `sketches/mic_test/` | Part B. Prints the microphone samples for the Serial Plotter. |
| `sketches/camera_test/` | Part B. Prints the size, the capture time, and the mean brightness of camera frames. |
| `sketches/memory_report/` | Part C. Prints the flash, the internal RAM, and the PSRAM of the board. |
| `model_budgets.ipynb` | Part C. The student notebook. It has five tasks. |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/model_budgets.ipynb` | The notebook with all tasks complete and with its output. |
| `solutions/report_example.md` | The parts of the report that need no board, complete. |
| `TEST_NOTES.md` | The code status and the test steps for the instructor. |

Two tests use examples of the esp32 core. The Arduino IDE has them:
`File` > `Examples` > `WiFi` > `WiFiScan` and
`File` > `Examples` > `ESP32` > `Camera` > `CameraWebServer`.

## Steps

Write each result in `report.md` when you get it.

### Part A: toolchain (50 min)

1. Do steps 1 to 4 of `Labs/SETUP.md`: the Arduino IDE, the esp32 core, the
   two libraries, the board settings, and the Python environment. On Linux,
   do also step 9 (permission for the USB port). If the lab computer has the
   tools, check each version and continue.
2. Connect the kit with the USB-C cable. In the Arduino IDE, click
   `Select Board`, enter `xiao`, and select `XIAO_ESP32S3` and the port of
   the board.
3. Set `Tools` > `PSRAM` > `Disabled`.
4. Open `sketches/blink/blink.ino`. Click Upload.

   You see: the built-in LED of the XIAO is on for one second and off for one
   second. The Serial Monitor at 115200 baud prints `LED on` and `LED off`.

5. Read the last lines of the build output in the Arduino IDE. They have this
   form (result of the compiler for `blink` with core 3.3.12; your numbers
   can be different):

   ```
   Sketch uses 271701 bytes (8%) of program storage space. Maximum is 3342336 bytes.
   Global variables use 21824 bytes (6%) of dynamic memory, leaving 305856 bytes for local variables. Maximum is 327680 bytes.
   ```

   Write your two lines in the report. The first line is the flash budget of
   a sketch. The second line is the RAM budget with no PSRAM.
6. Start Jupyter and open the notebook. Run only section 0 (Setup):

   ```bash
   .venv/bin/jupyter lab Labs/day01/model_budgets.ipynb
   ```

   You see: the versions of Python, `numpy`, `torch`, and `torchvision`, and
   no error.

### Part B: sensor tests (45 min)

Use about 8 minutes for each test. All tests use the Serial Monitor at
115200 baud, unless the step names a different tool.

1. **IMU.** Upload `sketches/imu_test/imu_test.ino`. Open the Serial Monitor.

   You see: the line `IMU initialized successfully`, then ten readings of the
   six values each second. Put the kit flat on the table: the Z value of the
   accelerometer is near 1.0 g, and X and Y are near 0. Turn the kit on its
   side: a different axis shows a value near 1.0 g or -1.0 g.

2. **Display.** Upload `sketches/oled_test/oled_test.ino`.

   You see: the text `Hello` and `World!` in a frame on the display of the
   expansion board.

3. **Microphone.** Upload `sketches/mic_test/mic_test.ino`. Close the Serial
   Monitor and open `Tools` > `Serial Plotter`.

   You see: small values in silence. Speak or clap: the line shows large
   positive and negative values. The sketch starts only when the Serial
   Plotter or the Serial Monitor is open.

4. **Camera.** Before the test, write your prediction in the report: how many
   bytes has one frame of 320 x 240 pixels with one byte for each pixel? Does
   one frame fit in the RAM of a microcontroller with 256 KB?

   Set `Tools` > `PSRAM` > `OPI PSRAM`. Upload
   `sketches/camera_test/camera_test.ino`.

   You see: the line `Camera initialized`, then one line each second with
   this form: `width,height,bytes,capture_ms,mean_brightness`. Cover the lens
   with your hand: the last value decreases. Point the camera at a lamp: the
   last value increases. Write the capture time in the report.

   Optional, to see the image: open the example `CameraWebServer` of the
   core. In the tab `board_config.h`, put `//` before the line
   `#define CAMERA_MODEL_ESP_EYE` and remove the `//` before the line
   `#define CAMERA_MODEL_XIAO_ESP32S3`. Enter the name and the password of
   the lab Wi-Fi in the main tab. Upload with `OPI PSRAM`. Open the address
   that the Serial Monitor prints in a browser and click `Start Stream`.

5. **Wi-Fi.** Connect the antenna to the XIAO, if it is not connected. Open
   the example `WiFiScan` of the core and upload it. The example needs no
   password.

   You see: `Scan start`, `Scan done`, and a list of the networks with their
   signal strength (RSSI). Write the number of networks and the RSSI of the
   strongest network in the report.

### Part C: model budgets (55 min)

1. **The memory of the board (10 min).** Set `Tools` > `PSRAM` > `Disabled`.
   Upload `sketches/memory_report/memory_report.ino`. Write these three
   values of the first report in `report.md`: `Heap size`, `Free heap`, and
   `Largest block that malloc can give`.
2. Set `Tools` > `PSRAM` > `OPI PSRAM`. Upload again. Write the same three
   values, and `PSRAM size` and `Free PSRAM`.
3. **The notebook (35 min).** Open `model_budgets.ipynb`. Do the five tasks
   in order. Each task has the mark `TODO (student)`.
   - Task 1: the cost of one convolution layer.
   - Task 2: your predictions for three models. Write them before you run
     section 4.
   - Task 3: the two RAM budgets of the XIAO that you measured in steps 1
     and 2.
   - Task 4: the function that decides if a model fits a device.
   - Task 5: the Decision Log.

   The complete notebook runs in less than one minute on a laptop CPU.
4. **The report (10 min).** Copy the table of section 5 of the notebook into
   `report.md`. Answer the four questions. Write the Decision Log.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] All five sensor tests pass: IMU, display, microphone, camera, Wi-Fi.
- [ ] The report has the two lines of the build output and the values of
      `memory_report` for the two PSRAM settings.
- [ ] The notebook prints `Task 1: complete`.
- [ ] The report has the predictions of task 2. The predictions were written
      before the measurement.
- [ ] The table has six rows and four devices. Each "does not fit" has a
      reason: flash, RAM, or flash and RAM.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: you must classify images of 96 x 96 pixels on the
XIAOML Kit. Which of the three models do you select, in which data type, and
with PSRAM or with no PSRAM? Which budget decides?

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The Arduino IDE shows no port | A cable for charging only, or no permission for the port on Linux | Use a data cable. On Linux, do step 9 of `Labs/SETUP.md`. |
| The upload fails with a connection error | The board is not in bootloader mode | Disconnect the USB cable. Hold the `B` (boot) button of the XIAO. Connect the cable, then release the button. Upload again. |
| The Serial Monitor shows nothing or wrong characters | Wrong speed | Set 115200 baud |
| `imu_test` prints `IMU initialization failed` | The expansion board is not connected correctly | Press the XIAO on the expansion board until all pins are in. |
| `mic_test` prints nothing | The sketch waits for a serial program | Open the Serial Plotter or the Serial Monitor |
| `camera_test` prints `PSRAM is not active` | The PSRAM setting is `Disabled` | Set `Tools` > `PSRAM` > `OPI PSRAM` and upload again |
| `camera_test` prints `camera init failed` | The camera cable is loose | Disconnect the USB cable. Press the camera connector on the Sense board. |
| `WiFiScan` finds no network | The antenna is not connected | Connect the antenna to the small connector on the XIAO |
| The notebook prints `No module named 'torch'` | Jupyter does not use the virtual environment | Start Jupyter with `.venv/bin/jupyter lab` |
| The install of `torch` downloads more than 2 GB | The default package on Linux | Use the install command for the CPU version in "Software" |

## Credits

This lab adapts material from these sources:

- The XIAOML Kit setup chapter of "Machine Learning Systems" by Vijay Janapa
  Reddi and contributors, written by Marcelo Rovai (mlsysbook.ai,
  CC BY-NC-SA 4.0): the order of the tests, the Blink code, and the expected
  results.
- The repository XIAO-ESP32S3-Sense by Marcelo Rovai
  (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0): the sketches
  `imu_test`, `oled_test`, and `mic_test`.
- "Machine Learning Systems", Volume I, chapters 2 and 6: the three budgets
  of a model and the fit check of the notebook.
- The examples `WiFiScan` and `CameraWebServer` of the Arduino core for the
  ESP32 by Espressif Systems (github.com/espressif/arduino-esp32). The lab
  uses them from the Arduino IDE and copies no file. The pin numbers of
  `camera_test` come from the camera example (LGPL-2.1).
