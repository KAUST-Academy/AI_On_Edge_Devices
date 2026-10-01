# HW-01 — MicroPython on the XIAOML Kit

Hardware status: not tested on hardware (prepared on 2026-10-01)

Needed by: the Day 2 lab (MicroPython start, sensor input, dataset).

## Decision

| Topic | Decision |
|---|---|
| Firmware | MicroPython v1.29.0 for the board `SEEED_XIAO_ESP32S3`, file `SEEED_XIAO_ESP32S3-20260824-v1.29.0.bin` |
| Tools | `esptool` writes the firmware. `mpremote` opens the REPL, copies files, and runs scripts. |
| IMU driver | The small driver `board/lsm6ds3.py` of this folder |
| Sensor configuration | 16 g, 2000 degrees per second, 416 Hz output data rate |
| Sampling | 50 Hz, with one deadline for each sample (`board/imu_stream.py`) |
| Return to Arduino | Upload an Arduino sketch. Use bootloader mode if the upload fails. |

## Reason

- MicroPython has a firmware for this board. The page
  `micropython.org/download/SEEED_XIAO_ESP32S3/` says that the firmware works
  on the XIAO ESP32S3. No generic firmware is necessary.
- The sources give Arduino code only for the IMU. No source has a MicroPython
  driver. A driver of about 130 lines is small enough for the students to read on
  Day 2. It shows the registers that the theory block explains.
- The driver uses the default values of the Arduino library "Seeed Arduino
  LSM6DS3". The Day 3 sketch uses that library. The training data of Day 2 and
  the inference of Day 3 then use the same sensor configuration.
- The kit lab collects motion data at 50 Hz. The Day 2 lab uses the same rate,
  so the Day 2 dataset fits the Day 3 lab.
- A deadline for each sample keeps the rate constant. A fixed `sleep` after
  each sample does not: the read time and the print time add to each period.

## Sources

| Item | Source |
|---|---|
| Firmware and write commands | `micropython.org/download/SEEED_XIAO_ESP32S3/` (read on 2026-10-01) |
| Register addresses, bit values, scale factors | Library "Seeed Arduino LSM6DS3" 2.0.7, files `LSM6DS3.h` and `LSM6DS3.cpp` (MIT) |
| I2C address 0x6A, display address 0x3C | XIAOML Kit setup chapter of "Machine Learning Systems", and `XIAOML_Kit_code/imu_test/imu_test.ino` of "XIAO ESP32S3 Sense" |
| I2C pins: SDA = GPIO5, SCL = GPIO6 | `variants/XIAO_ESP32S3/pins_arduino.h` of the Arduino core "esp32" 3.3.12 |
| Sampling rate 50 Hz and the deadline method | Motion classification chapter of "Machine Learning Systems" (data collection sketch) |
| Bootloader mode | `wiki.seeedstudio.com/xiao_esp32s3_getting_started` (section "BootLoader Mode") |

## Files

| File | Content |
|---|---|
| `get_firmware.sh` | Downloads the firmware into `downloads/` and checks its SHA-256 |
| `board/lsm6ds3.py` | The IMU driver. Copy it to the board. |
| `board/i2c_scan.py` | Lists the I2C devices of the kit |
| `board/imu_stream.py` | Sends IMU samples at 50 Hz as CSV lines |
| `host/check_rate.py` | Laptop script. Checks that the sampling rate is constant. |

## Steps

Run the commands from this folder. `PORT` is the serial port of the board,
for example `/dev/ttyACM0` (Linux), `/dev/cu.usbmodem101` (macOS), or `COM4`
(Windows). The tools come from step 5 of `Labs/SETUP.md`.

### 1. Get the firmware

```bash
bash get_firmware.sh
```

You see: `downloads/SEEED_XIAO_ESP32S3-20260824-v1.29.0.bin: OK`.

### 2. Start bootloader mode

1. Disconnect the USB cable.
2. Press and hold the `B` (boot) button of the XIAO.
3. Connect the USB cable. Then release the button.

The boot button is on the XIAO, not on the expansion board. It is very small.

### 3. Write the firmware

```bash
python3 -m esptool --chip esp32s3 --port PORT erase_flash
python3 -m esptool --chip esp32s3 --port PORT write_flash 0 \
  downloads/SEEED_XIAO_ESP32S3-20260824-v1.29.0.bin
```

Then press the `RST` button of the expansion board. The port name can change
after the reset.

### 4. Open the REPL

```bash
mpremote connect PORT repl
```

You see the prompt `>>>`. Enter `import sys; sys.implementation`. The answer
gives the MicroPython version. Press `Ctrl-]` to close the REPL.

### 5. Scan the I2C bus

```bash
mpremote connect PORT run board/i2c_scan.py
```

You see two devices: `0x3C` (display) and `0x6A` (IMU).

### 6. Read the IMU

```bash
mpremote connect PORT fs cp board/lsm6ds3.py :lsm6ds3.py
mpremote connect PORT run board/imu_stream.py
```

You see one CSV line for each sample. With the kit flat on the table, one
acceleration axis is near 1.0 g and the other two are near 0. Press `Ctrl-C`
to stop.

In the REPL, the driver works like this:

```python
from machine import I2C, Pin
from lsm6ds3 import LSM6DS3
imu = LSM6DS3(I2C(0, sda=Pin(5), scl=Pin(6), freq=400000))
imu.read()        # (ax, ay, az, gx, gy, gz) in g and in degrees per second
```

### 7. Check the sampling rate

To start the stream at each power-on, copy the script as `main.py`:

```bash
mpremote connect PORT fs cp board/imu_stream.py :main.py
mpremote connect PORT reset
python3 host/check_rate.py --port PORT --seconds 20 --save run1.csv
```

The script needs the package `pyserial`. It prints the mean rate, the period
statistics, and `RESULT: PASS` or `RESULT: FAIL`.

Remove `main.py` when the test is complete:

```bash
mpremote connect PORT fs rm :main.py
```

If `mpremote` cannot connect because `main.py` runs, press `Ctrl-C` in
`mpremote connect PORT repl` first.

### 8. Return to the Arduino firmware

Day 3 needs the Arduino firmware again.

1. Open the Arduino IDE. Select the board `XIAO_ESP32S3` and the port.
2. Set `Tools` > `Erase All Flash Before Sketch Upload` to `Enabled`.
3. Upload a sketch, for example Blink.
4. If the upload fails, start bootloader mode (step 2) and upload again.
5. Set `Erase All Flash Before Sketch Upload` to `Disabled` again.

## Limits of the driver

- The driver sets the output data rate and the range only. It does not use
  the FIFO, the interrupts, or the filters of the sensor.
- `read()` makes a new tuple for each sample. At 50 Hz this is not a problem.
- The script `imu_stream.py` reads the sensor each 20 ms. The sensor makes a
  new sample each 2.4 ms (416 Hz). The read takes the newest sample.

## Difference from the source

The sketch `imu_test.ino` and the kit chapter say "±2g" and "±250 dps". The
library does not use these values. Its default values are 16 g and 2000
degrees per second (`LSM6DS3.cpp`, lines 368 and 376). The printed values are
correct in g, because the library scales with its real range. Only the
resolution is different: 0.488 mg for each count, not 0.061 mg.

## Code status

| File | State | Source | Change |
|---|---|---|---|
| `board/lsm6ds3.py` | new | Register values from `LSM6DS3.h` and `LSM6DS3.cpp` | not tested |
| `board/i2c_scan.py` | new | — | not tested |
| `board/imu_stream.py` | new | Method of the kit data collection sketch | not tested |
| `host/check_rate.py` | new | — | tested on the work computer with four synthetic files (constant rate, slow rate, lost lines, large jitter) |
| `get_firmware.sh` | new | — | tested on the work computer: the download and the checksum pass |

The driver was tested on the work computer with a simulated I2C bus. The
test confirms the register writes (`0x12 = 0x44`, `0x10 = 0x64`, `0x11 = 0x6C`)
and the scale factors. It does not replace a test on the board.

The driver sets the bit BDU (block data update) in `CTRL3_C`. The Arduino
library does not set this bit. This is one difference to test.

## Test steps for the instructor

- Date of the test:
- MicroPython version (from the REPL):
- `esptool` version and `mpremote` version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run step 1 | The checksum line prints `OK` | |
| 2 | Run steps 2 and 3 | Time to erase and to write. The port name before and after. | |
| 3 | Run step 4 | The version text of the REPL | |
| 4 | Run step 5 | The addresses that the scan finds | |
| 5 | Run step 6 with the kit flat on the table | The six values. Which axis shows 1.0 g? | |
| 6 | Turn the kit by hand around each axis | The gyroscope sign and the size of the values | |
| 7 | Upload `imu_test.ino` (Arduino) and compare with step 5 | The difference of each axis at rest | |
| 8 | Run step 7 for 20 s | Mean rate, period std, min, max, lost lines, PASS or FAIL | |
| 9 | Change `RATE_HZ` to 100 and to 200. Run step 7 with `--rate`. | The highest rate that passes | |
| 10 | Run step 8 | Does the upload work with no bootloader mode? Time for the return. | |
| 11 | Repeat steps 2 to 4 on a second kit | Total time for one student group | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## After the test

1. Change the line `Hardware status:` to `tested on hardware (YYYY-MM-DD)`.
2. Write the firmware version in `Labs/VERSIONS.md`.
3. Correct the Day 2 lab files with the measured rate and the measured times.

## Credits

The register values come from the library "Seeed Arduino LSM6DS3" by Seeed
Studio (github.com/Seeed-Studio/Seeed_Arduino_LSM6DS3, MIT). The sampling
method and the board data come from "Machine Learning Systems" by Vijay Janapa
Reddi and contributors (mlsysbook.ai, CC BY-NC-SA 4.0) and from "XIAO ESP32S3
Sense" by Marcelo Rovai (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0).
