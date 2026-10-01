# Setup of a lab computer

This guide prepares one lab computer for the course "AI on Edge Devices".
Do every step before Day 1. The Day 1 pilot fixes the version of each tool.
Write the fixed versions in `VERSIONS.md`.

The guide prepares the computer. It does not prepare a board. The folder
`Labs/hardware/` holds the steps for the boards.

## 0. What you install

| Step | Tool | Needed for |
|---|---|---|
| 1 | Arduino IDE 2 and the esp32 board core | Days 1 to 5, Days 11 and 12 |
| 2 | Arduino libraries of the XIAOML Kit | Days 1 to 5 |
| 3 | Board settings of the XIAO ESP32S3 | Days 1 to 5 |
| 4 | Python environment | every day |
| 5 | MicroPython tools | Day 2 |
| 6 | Edge Impulse CLI and account | Days 3 and 5 |
| 7 | Arduino core and library of the Nano 33 BLE Sense | backup modules only |
| 8 | `arduino-cli` | optional: compile with no board |
| 9 | Permission for the USB port (Linux) | every lab with a board |

## 1. Arduino IDE 2 and the esp32 board core

1. Download the stable Arduino IDE for your operating system from
   `www.arduino.cc/en/software`. Install it.
2. Open the Arduino IDE. Open the Boards Manager (the board icon on the left).
3. Enter `esp32`. Select **esp32 by Espressif Systems**. Click Install.

   Do not select "Arduino ESP32 Boards" by Arduino. That package supports the
   Arduino Nano ESP32, not the XIAO.

4. Write the installed version in `VERSIONS.md`.

> Version note from the kit setup chapter: a core of version 3.x can fail with
> the deployment code of Edge Impulse. If the code fails, install the last
> 2.0.x version instead, for example 2.0.17.

## 2. Arduino libraries of the XIAOML Kit

1. Open the Library Manager (the books icon on the left).
2. Install **Seeed Arduino LSM6DS3** by Seeed. The expansion board uses this
   IMU (I2C address 0x6A).
3. Install **U8g2** by oliver. The expansion board uses the 0.42" OLED display
   with the controller SSD1306 (I2C address 0x3C).
4. Write both versions in `VERSIONS.md`.

The lab of each day names the other libraries that it needs.

## 3. Board settings of the XIAO ESP32S3

1. Connect the kit to the computer with the USB-C cable.
2. Click `Select Board`. Enter `xiao` or `esp32s3`. Select `XIAO_ESP32S3` and
   the port of the board.
3. For the camera labs and the audio labs, set `Tools` > `PSRAM` to
   `OPI PSRAM`. The ESP32-S3 has only a few hundred kilobytes of internal RAM.
   The 8 MB of PSRAM hold the image buffers and the audio buffers.

   The memory labs of Days 1, 3, and 4 measure the model first **without**
   PSRAM. `Labs/hardware/HW-03/` gives that method.

4. Test the board. Open `File` > `Examples` > `01.Basics` > `Blink` and upload
   it. The built-in LED is on GPIO21. The LED works with inverted logic: `LOW`
   turns it on and `HIGH` turns it off.

## 4. Python environment

1. Install Python 3.10 or later.
2. Make a virtual environment and install the packages:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r Labs/requirements.txt
   ```

3. Start every notebook from this environment:

   ```bash
   .venv/bin/jupyter lab
   ```

4. Write the version of Python and of each package in `VERSIONS.md`.

The training labs use small models. They run on a laptop CPU. Google Colab is
the fallback when a laptop is too slow.

## 5. MicroPython tools

Day 2 runs MicroPython on the XIAO ESP32S3.

1. Install the two tools in the same virtual environment:

   ```bash
   .venv/bin/pip install esptool mpremote
   ```

   - `esptool` writes the firmware to the board.
   - `mpremote` opens the REPL, copies a file to the board, and runs a script.

2. Thonny is a graphical option for the students who prefer an editor. Install
   it from `thonny.org`.
3. `Labs/hardware/HW-01/` gives the firmware file, the write command, and the
   way back to the Arduino firmware.

## 6. Edge Impulse CLI and account

Days 3 and 5 collect data and train a model with Edge Impulse.

1. Install Node.js (the LTS version) from `nodejs.org`.
2. Install the CLI:

   ```bash
   npm install -g edge-impulse-cli
   ```

3. Create a free account on `edgeimpulse.com`.
4. Test the installation:

   ```bash
   edge-impulse-daemon --version
   ```

The official steps are on `docs.edgeimpulse.com/docs/edge-impulse-cli/cli-installation`.

## 7. Arduino core and library of the Nano 33 BLE Sense

Install this step only for the backup modules that use the Nano 33 BLE Sense
Rev2.

1. Open the Boards Manager. Install **Arduino Mbed OS Nano Boards**.
2. Open the Library Manager. Install **Harvard_TinyMLx**.
3. Write both versions in `VERSIONS.md`.

## 8. `arduino-cli` (optional)

`arduino-cli` compiles a sketch without a board. Use it to check that a sketch
builds.

1. Download the archive for your operating system from the releases page of
   `github.com/arduino/arduino-cli`. Unpack it into a folder of your user
   account. No administrator right is necessary.
2. Add the index of the esp32 core and install the cores:

   ```bash
   arduino-cli config init
   arduino-cli config add board_manager.additional_urls \
     https://espressif.github.io/arduino-esp32/package_esp32_index.json
   arduino-cli core update-index
   arduino-cli core install esp32:esp32
   arduino-cli core install arduino:mbed_nano
   ```

3. Compile a sketch:

   ```bash
   arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3 <sketch folder>
   ```

`VERSIONS.md` gives the board name (FQBN) of each board.

## 9. Permission for the USB port (Linux)

The Arduino IDE needs write access to the serial port. Add the user to the
group `dialout`:

```bash
sudo usermod -a -G dialout $USER
```

Log out and log in again. Then the port appears in the Arduino IDE.

## 10. Check the setup

The computer is ready when all these checks pass:

- [ ] The Arduino IDE shows the board `XIAO_ESP32S3` and its port.
- [ ] Blink runs on the board.
- [ ] `.venv/bin/python -c "import numpy, torch"` prints no error.
- [ ] `.venv/bin/jupyter lab` opens in the browser.
- [ ] `.venv/bin/mpremote --help` prints the help text.
- [ ] `edge-impulse-daemon --version` prints a version.
- [ ] `VERSIONS.md` has one row for each tool above.


