# Day 2 lab: MicroPython, sensor input, and a motion dataset

Hardware status: not tested on hardware (prepared on 2026-10-02)

**Goal.** Your group has a labelled motion dataset that Day 3 uses, with a
constant sampling rate and a correct split between training and test data.

**Deliverable.** The folder `data/` with your recordings and the file
`split.json`, and the file `report.md` with the data card and the Decision
Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | MicroPython start: firmware, REPL, GPIO, timer, I2C scan | 40 min |
| B | Sensor input: the IMU at a fixed rate, serial port and Wi-Fi | 50 min |
| C | Dataset: logger, four motion classes, split by session | 40 min |
| D | Edge Impulse: upload and inspect the same data | 20 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| XIAOML Kit | 1 | XIAO ESP32S3 Sense with the expansion board (IMU and display) |
| USB-C cable | 1 | A data cable. A cable for charging only does not work. |
| Wi-Fi antenna of the kit | 1 | Connect it before the Wi-Fi step of Part B |
| Laptop | 1 | Windows, macOS, or Linux, in the lab Wi-Fi |

MicroPython replaces the Arduino firmware of the board. The last step of
this lab puts the Arduino firmware back. Day 3 needs it.

## Software

| Tool | Version | Note |
|---|---|---|
| MicroPython firmware `SEEED_XIAO_ESP32S3` | v1.29.0 | `Labs/hardware/HW-01/get_firmware.sh` downloads the file |
| `esptool`, `mpremote` | see `Labs/VERSIONS.md` | Step 5 of `Labs/SETUP.md` |
| Python | 3.10 or later | The programs and the notebook ran with Python 3.10.12 |
| `numpy`, `matplotlib`, `pyserial`, `jupyterlab` | see `Labs/VERSIONS.md` | `Labs/requirements.txt` |
| Edge Impulse account and Edge Impulse CLI | see `Labs/VERSIONS.md` | Step 6 of `Labs/SETUP.md`. Part D works also with the browser only. |
| Arduino IDE 2 with the esp32 core | 3.3.12 | For the last step, and for the fallback of Part B |

Run all commands of this lab from the folder `Labs/day02/`. `PORT` is the
serial port of the board, for example `/dev/ttyACM0` (Linux),
`/dev/cu.usbmodem101` (macOS), or `COM4` (Windows). The commands use the
programs of the virtual environment of Day 1. On Linux and macOS, start it
one time in each terminal:

```bash
source ../../.venv/bin/activate
```

On Windows, the command is `..\..\.venv\Scripts\activate`.

## Files

| File | Content |
|---|---|
| `board/lsm6ds3.py` | The MicroPython driver of the IMU. You copy it to the board. |
| `board/blink_timer.py` | Part A. The LED with a hardware timer, and the button with an interrupt. |
| `board/i2c_scan.py` | Part A. Lists the I2C devices of the kit. |
| `board/imu_stream.py` | Part B. Sends IMU samples to the serial port. **Task B1** is in this file. |
| `board/imu_wifi.py`, `board/config.py` | Part B. Sends the same samples over Wi-Fi. |
| `host/check_rate.py` | Part B. Checks that the sampling rate is constant. |
| `host/logger.py` | Part C. Stores recordings in CSV files. **Tasks C1 and C2** are in this file. |
| `dataset.ipynb` | Part C. The student notebook. It has five tasks. |
| `host/to_edge_impulse.py` | Part D. Converts the recordings to the format of Edge Impulse. |
| `report.md` | The report to hand in. Fill it during the lab. |
| `host/sim_board.py`, `host/motion_sim.py` | A simulated board, for a test of the laptop programs with no board |
| `host/make_fallback_dataset.py` | Makes the fallback dataset. Its signals are simulated. |
| `sketches/imu_data_collection/` | Fallback for Part B: an Arduino sketch that sends the same lines |
| `solutions/` | The complete version of each student file, and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

## Steps

Write each result in `report.md` when you get it.

### Part A: MicroPython start (40 min)

1. **Tools.** Do step 5 of `Labs/SETUP.md`, if the lab computer does not
   have `esptool` and `mpremote`.
2. **Firmware file.** Download the firmware and check it:

   ```bash
   bash ../hardware/HW-01/get_firmware.sh
   ```

   You see: `downloads/SEEED_XIAO_ESP32S3-20260824-v1.29.0.bin: OK`, and the
   path of the file.

3. **Bootloader mode.** Disconnect the USB cable. Press and hold the `B`
   (boot) button of the XIAO. Connect the USB cable. Then release the
   button. The boot button is on the XIAO, not on the expansion board. It is
   very small.
4. **Write the firmware.**

   ```bash
   python3 -m esptool --chip esp32s3 --port PORT erase_flash
   python3 -m esptool --chip esp32s3 --port PORT write_flash 0 \
     ../hardware/HW-01/downloads/SEEED_XIAO_ESP32S3-20260824-v1.29.0.bin
   ```

   Then press the `RST` button of the expansion board. The port name can
   change after the reset.

5. **The REPL.** Open the prompt of MicroPython:

   ```bash
   mpremote connect PORT repl
   ```

   You see the prompt `>>>`. Enter these lines one after the other, and
   write the three results in the report:

   ```python
   import sys, machine, gc
   sys.implementation          # the MicroPython version
   machine.freq()              # the clock frequency of the processor in Hz
   gc.mem_free()               # the free memory of the interpreter in bytes
   ```

6. **GPIO.** In the REPL, switch the LED of the XIAO. The LED is on GPIO21,
   and it is on when the pin is low:

   ```python
   from machine import Pin
   led = Pin(21, Pin.OUT)
   led.value(0)                # LED on
   led.value(1)                # LED off
   ```

   Press `Ctrl-]` to close the REPL.

7. **Timer and interrupt.** Run the script from the laptop. `mpremote` sends
   the file to the RAM of the board and starts it:

   ```bash
   mpremote connect PORT run board/blink_timer.py
   ```

   You see: the LED changes two times each second. The script prints one
   line each second with the number of timer events (`ticks`). Press the
   boot button some times: the number `presses` increases. Press `Ctrl-C`
   to stop. Write in the report how many ticks the timer gives in 10 s.

8. **I2C scan.**

   ```bash
   mpremote connect PORT run board/i2c_scan.py
   ```

   You see two devices: `0x3C` (display) and `0x6A` (IMU). Write the two
   addresses in the report.

### Part B: sensor input (50 min)

1. **The driver (5 min).** Copy the driver of the IMU to the file system of
   the board. Then read the sensor in the REPL:

   ```bash
   mpremote connect PORT fs cp board/lsm6ds3.py :lsm6ds3.py
   mpremote connect PORT repl
   ```

   ```python
   from machine import I2C, Pin
   from lsm6ds3 import LSM6DS3
   imu = LSM6DS3(I2C(0, sda=Pin(5), scl=Pin(6), freq=400000))
   hex(imu.chip_id)            # the identity register: 0x6a
   imu.read()                  # (ax, ay, az, gx, gy, gz)
   ```

   You see six values. With the kit flat on the table, one acceleration
   axis is near 1.0 g and the other two are near 0. Write the six values in
   the report.

2. **Prediction (3 min).** Open `board/imu_stream.py`. The loop reads the
   sensor, prints one line, and then waits 20 ms. Write your prediction in
   the report before you measure: is the real rate equal to 50 Hz, lower, or
   higher? By how much?

3. **Measure the rate of the first version (10 min).** A script with the
   name `main.py` starts at each power-on. Copy the script as `main.py`,
   start the board again, and measure for 20 s:

   ```bash
   mpremote connect PORT fs cp board/imu_stream.py :main.py
   mpremote connect PORT reset
   python3 host/check_rate.py --port PORT --seconds 20 --save rate_wait.csv
   ```

   You see the mean rate, the statistics of the period, and `RESULT: PASS`
   or `RESULT: FAIL`. Write the mean rate and the result in the report.

4. **Task B1: a deadline for each sample (15 min).** Change
   `board/imu_stream.py`. The comment with the mark `TODO (student)` gives
   the five steps. Then copy the file, start the board again, and measure:

   ```bash
   mpremote connect PORT fs cp board/imu_stream.py :main.py
   mpremote connect PORT reset
   python3 host/check_rate.py --port PORT --seconds 20 --save rate_deadline.csv
   ```

   You see `RESULT: PASS - the sampling rate is constant`. Write the mean
   rate, the minimum period, and the maximum period in the report.

   If `mpremote` cannot connect because `main.py` runs, open
   `mpremote connect PORT repl`, press `Ctrl-C`, and close the REPL with
   `Ctrl-]`.

5. **Wi-Fi (17 min).** Connect the antenna to the XIAO.
   - Find the IP address of your laptop in the lab Wi-Fi: `ip addr` (Linux),
     `ipconfig getifaddr en0` (macOS), or `ipconfig` (Windows).
   - Write the name of the lab Wi-Fi, its password, and the IP address of
     your laptop in `board/config.py`.
   - Copy the settings to the board and start the Wi-Fi script:

     ```bash
     mpremote connect PORT fs cp board/config.py :config.py
     mpremote connect PORT run board/imu_wifi.py
     ```

     You see: `Board address:` with the address of the board, then
     `Sending to` with the address of your laptop.

   - In a second terminal, measure the rate of the samples that arrive over
     Wi-Fi:

     ```bash
     python3 host/check_rate.py --udp 5005 --seconds 20
     ```

   Write the mean rate and the number of lost lines in the report. Compare
   with the serial port: which connection loses samples, and why?

   Press `Ctrl-C` in the first terminal to stop the Wi-Fi script.

### Part C: dataset (40 min)

1. **Tasks C1 and C2: the logger (8 min).** Open `host/logger.py`. Complete
   the two functions with the mark `TODO (student)`: `file_name` and
   `count_lost`. Test them with no board:

   ```bash
   python3 host/logger.py --self-test
   ```

   You see: `Task C1 (file_name):  complete` and
   `Task C2 (count_lost): complete`.

2. **The protocol (4 min).** Write the collection protocol in the report
   before the first recording: one sentence for each class, and the person
   of each session. Use these rules of the lecture:

   - Classes: `idle`, `terrestrial`, `lift`, `maritime`.
   - One recording: 10 s of one motion with no pause.
   - Quantity: 4 recordings for each class in each session.
   - Sessions: `s1`, `s2`, `s3`. Change the person, the speed, or the size
     of the motion between the sessions.
   - Position of the kit: in the hand, with the display up. For `idle`, the
     kit lies on the table.

3. **Record (13 min).** The board must run the deadline version of
   `imu_stream.py` as `main.py` (step 4 of Part B). For each session and
   each class, start the motion and then start the logger:

   ```bash
   python3 host/logger.py --port PORT --label idle --session s1 --person A --count 4 --plot
   python3 host/logger.py --port PORT --label terrestrial --session s1 --person A --count 4 --plot
   python3 host/logger.py --port PORT --label lift --session s1 --person A --count 4 --plot
   python3 host/logger.py --port PORT --label maritime --session s1 --person A --count 4 --plot
   ```

   Repeat the four commands for the sessions `s2` and `s3`. The logger
   waits 3 s before each recording, records 10 s, and writes one file, for
   example `data/lift.s1.01.csv`. For each file it prints the number of
   samples, the rate, the lost samples, and the clipped samples.

   Look at the plots in `data/plots/` after each class. If a plot does not
   agree with its label, delete the file and its plot, and record again.

   The motions:
   - `idle`: the kit lies on the table.
   - `terrestrial`: move the kit left and right in a horizontal line.
   - `lift`: move the kit up and down.
   - `maritime`: move the kit slowly on all axes, as a boat on waves.

4. **The notebook (15 min).** Start Jupyter and do the five tasks in order:

   ```bash
   jupyter lab dataset.ipynb
   ```

   - Task 1: the mean sampling rate of a recording.
   - Task 2: the split by session.
   - Task 3: the number of windows.
   - Task 4: your prediction for the leakage experiment. Write it before
     you run the experiment.
   - Task 5: the data card in `report.md`.

   The notebook writes `data/split.json`. The complete notebook runs in
   less than one minute on a laptop CPU.

   If the folder `data/` has no recordings, the notebook uses a fallback
   dataset with simulated signals. Use it only if your group has no
   recordings.

### Part D: Edge Impulse (20 min)

1. **Convert (2 min).** Edge Impulse needs the time in milliseconds and the
   acceleration in m/s². The program reads `data/split.json` and writes
   one folder for each set:

   ```bash
   python3 host/to_edge_impulse.py --data data
   ```

   You see the number of training files and of test files, and the two
   upload commands.

2. **Project (3 min).** Log in to Edge Impulse Studio (`studio.edgeimpulse.com`)
   and make a new project with the name `motion-gNN`. `NN` is your group
   number.

3. **Upload (7 min).** Use the two commands that step 1 printed. The first
   command asks for your account and for the project:

   ```bash
   edge-impulse-uploader --category training ei_upload/training/*.csv
   edge-impulse-uploader --category testing ei_upload/testing/*.csv
   ```

   With no CLI: in the Studio, open `Data acquisition` and select
   `Add data`, then `Upload data`. Select the files of `ei_upload/training/`,
   the category `Training`, and the label option that reads the label from
   the file name. Repeat for `ei_upload/testing/` with the category
   `Testing`.

   Do not use the automatic split of the Studio. It splits the files and
   does not know your sessions.

4. **Inspect (5 min).** In `Data acquisition`:
   - Check that the four labels are correct.
   - Open one recording of each class and compare the plot with the plot of
     the logger.
   - Write in the report: the duration of the training data, the duration
     of the test data, and the ratio between training and test data that
     the Studio shows.

5. **Return to the Arduino firmware (3 min).** Day 3 needs the Arduino
   firmware.
   - Open the Arduino IDE. Select the board `XIAO_ESP32S3` and the port.
   - Set `Tools` > `Erase All Flash Before Sketch Upload` to `Enabled`.
   - Upload the sketch `Labs/day01/sketches/blink/blink.ino`.
   - If the upload fails, start bootloader mode (step 3 of Part A) and
     upload again.
   - Set `Erase All Flash Before Sketch Upload` to `Disabled` again.

   You see: the LED of the XIAO is on for one second and off for one
   second.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] `host/check_rate.py` prints `RESULT: PASS` for the deadline version of
      `imu_stream.py`. The report has the rate of the two versions.
- [ ] The report has the prediction of Part B and the prediction of task 4.
      The predictions were written before the measurement.
- [ ] `python3 host/logger.py --self-test` prints `complete` for the two
      tasks.
- [ ] The folder `data/` has recordings of four classes and of a minimum of
      two sessions. The notebook reports no recording with a problem.
- [ ] The notebook prints `Task 1: complete`, `Task 2: complete`, and
      `Task 3: complete`. No session is in the training set and also in the
      test set.
- [ ] The data card in the report is complete: classes, duration, sampling
      rate, split, known limits.
- [ ] The Edge Impulse project shows the four classes, with the test session
      in the test data.
- [ ] The board runs the Arduino Blink sketch again.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: your group has 10 more minutes to record data. Do you
add more recordings to the three sessions that you have, or do you record a
new session with a different person? Use the two results of your leakage
experiment.

## If a part does not work

| Problem | Fallback |
|---|---|
| MicroPython does not start on your kit | Upload the Arduino sketch `sketches/imu_data_collection/imu_data_collection.ino` with the Arduino IDE. It sends the same lines. Continue with step 3 of Part B and with Part C. |
| The board does not work at all | Start `python3 host/sim_board.py --label lift --session s1` in one terminal. Use `--udp 5005` in place of `--port PORT` with `host/check_rate.py` and with `host/logger.py`. The signals are simulated. |
| The lab Wi-Fi does not work | Do not do step 5 of Part B. Write the reason in the report. |
| Your group has no dataset at the end | The notebook makes the fallback dataset. The command `python3 host/make_fallback_dataset.py` makes it also. Write in the data card that the signals are simulated. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| `esptool` cannot connect | The board is not in bootloader mode | Do step 3 of Part A again. Hold the button before you connect the cable. |
| The port name is different after the reset | The firmware makes a new USB device | Look for the new port: `mpremote devs` |
| `mpremote` prints `could not enter raw repl` | `main.py` runs and uses the port | Open `mpremote connect PORT repl`, press `Ctrl-C`, then `Ctrl-]` |
| `ImportError: no module named 'lsm6ds3'` | The driver is not on the board | `mpremote connect PORT fs cp board/lsm6ds3.py :lsm6ds3.py` |
| `OSError: no LSM6DS3 at address 0x6A` | The expansion board is not connected correctly | Press the XIAO on the expansion board until all pins are in |
| `check_rate.py` prints `Not enough samples: 0` | No script sends data, or a different program has the port | Check that `main.py` is on the board. Close the REPL and the Serial Monitor. |
| `check_rate.py` prints `FAIL` with a low mean rate | The loop waits a fixed time after each sample | Complete task B1 |
| `check_rate.py --udp` gets no samples | Wrong laptop address in `config.py`, or the firewall of the laptop blocks the UDP port 5005 | Check the address. Permit the port in the firewall. Check that the laptop and the board are in the same Wi-Fi. |
| The board does not connect to the Wi-Fi | No antenna, a wrong password, or a network with 5 GHz only | Connect the antenna. Check `config.py`. The XIAO has 2.4 GHz Wi-Fi only. |
| The logger writes `recording.csv` | Task C1 is not complete | Complete the function `file_name` |
| The logger prints `WARNING: samples are missing` | The laptop did not read all lines | Record again. Close other programs that use the port. |
| The notebook prints `No module named 'numpy'` | Jupyter does not use the virtual environment | Start Jupyter from the terminal with the active environment |
| `edge-impulse-uploader` is not found | The Edge Impulse CLI is not installed | Do step 6 of `Labs/SETUP.md`, or upload in the browser |
| The Arduino upload fails after the lab | MicroPython has the port | Start bootloader mode and upload again |

## Credits

This lab adapts material from these sources:

- The chapters "Setup" and "Motion Classification and Anomaly Detection" of
  the XIAOML Kit in "Machine Learning Systems" by Vijay Janapa Reddi and
  contributors, written by Marcelo Rovai (mlsysbook.ai, CC BY-NC-SA 4.0):
  the four motion classes, the rate of 50 Hz, the recordings of 10 s, the
  window of 2 s with a stride of 0.2 s, the data collection sketch, and the
  upload to Edge Impulse Studio.
- "Machine Learning Systems", Volume I, chapter 4 "Data Engineering": the
  two types of quality check and the dataset versions.
- The library "Seeed Arduino LSM6DS3" by Seeed Studio
  (github.com/Seeed-Studio/Seeed_Arduino_LSM6DS3, MIT): the register
  addresses and the scale factors of the driver `board/lsm6ds3.py`.
- The repository XIAO-ESP32S3-Sense by Marcelo Rovai
  (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0): the I2C address of
  the IMU.
- The MicroPython documentation (docs.micropython.org) and the Edge Impulse
  documentation (docs.edgeimpulse.com): the commands of the tools and the
  CSV format of the upload.

The MicroPython scripts, the logger, the notebook, and the simulated
signals are new code of this course.
