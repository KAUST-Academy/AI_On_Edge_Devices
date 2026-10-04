# Test notes: Day 2 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `board/lsm6ds3.py` | copied with no change | `Labs/hardware/HW-01/board/lsm6ds3.py` | none. `HW-01` says that the driver is new and not tested. |
| `board/i2c_scan.py` | copied with no change | `Labs/hardware/HW-01/board/i2c_scan.py` | none |
| `board/blink_timer.py` | new | no source | not tested |
| `board/imu_stream.py` | changed | `Labs/hardware/HW-01/board/imu_stream.py` | Student version. The deadline is replaced by a fixed wait of 20 ms and a comment for task B1. |
| `solutions/board/imu_stream.py` | copied with no change | `Labs/hardware/HW-01/board/imu_stream.py` | none |
| `board/imu_wifi.py` | new | The Wi-Fi connection follows `Labs/hardware/HW-07/micropython/mqtt_imu.py` | not tested |
| `board/config.py` | new | no source | not tested |
| `host/check_rate.py` | changed | `Labs/hardware/HW-01/host/check_rate.py` | New: the option `--udp`. Tested on the work computer with the simulated board. |
| `host/logger.py`, `solutions/host/logger.py` | new | no source | Tested on the work computer with the simulated board (UDP) and with a simulated serial port |
| `host/motion_sim.py`, `host/sim_board.py`, `host/make_fallback_dataset.py` | new | The four classes and their axes come from the kit chapter. The signal model has no source. | Tested on the work computer. They need no board. |
| `host/to_edge_impulse.py` | new | The CSV format comes from the Edge Impulse documentation | Tested on the work computer. Nobody uploaded the files. |
| `dataset.ipynb`, `solutions/dataset.ipynb` | new | no source | Tested on the work computer with the fallback dataset. They need no board. |
| `sketches/imu_data_collection/imu_data_collection.ino` | changed | Data collection code of the chapter "Motion Classification and Anomaly Detection" of the XIAOML Kit in "Machine Learning Systems" | Six axes in g and dps with a sample number and a time stamp, a comma between the values, a deadline in microseconds, no wait in `setup()`. The header comment of the sketch lists each change. |

Points that only a board can confirm:

- The steps of Part A (firmware, REPL, timer, button, I2C scan). They come
  from `Labs/hardware/HW-01/`, which is also not tested.
- `blink_timer.py` uses `Timer(0)` with `freq=2` and an interrupt on GPIO0.
  Nobody checked that the boot button gives one interrupt for each press. A
  button with no filter can give more than one.
- The first version of `imu_stream.py` waits 20 ms after each sample. The
  lab expects that `check_rate.py` prints `FAIL` for this version, because
  the rate is more than 1 percent below 50 Hz. Nobody measured the real
  rate. If the first version passes, the prediction step of Part B needs a
  different text.
- `imu_wifi.py` sends one UDP packet for each 5 samples. Nobody measured
  the rate and the lost packets in the lab Wi-Fi.
- The README says that `mpremote` can copy a file when `main.py` runs.
  Nobody checked this. The fix in the table of the common problems is to
  press `Ctrl-C` in the REPL first.
- The upload to Edge Impulse Studio (Part D). The file format follows the
  documentation. Nobody checked that the Studio accepts the files with no
  step in the CSV Wizard, and that the menu names of the README are the
  names of the Studio today.
- The return to the Arduino firmware (last step of Part D).

Compile check (no board, `arduino-cli` 1.5.1, esp32 core 3.3.12, library
Seeed Arduino LSM6DS3 2.0.7, 2026-10-02):

| Sketch | Board name (FQBN) | Result | Flash (bytes) | Static RAM (bytes) |
|---|---|---|---|---|
| `imu_data_collection` | `esp32:esp32:XIAO_ESP32S3:PSRAM=disabled` | compiles, no compiler warning in the sketch | 301 381 | 23 344 |
| `imu_data_collection` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles, no compiler warning in the sketch | 306 599 | 23 812 |

"Static RAM" is the line `Global variables use ... bytes` of the build. The
library gives one compiler warning (`LSM6DS3.cpp`, line 135).

Syntax check: all MicroPython files and all laptop programs pass
`python3 -m py_compile`. This check finds a syntax error only. It does not
run the MicroPython files.

Tests on the work computer (2026-10-02, Python 3.10.12, `numpy` 2.2.6,
`matplotlib` 3.10.9, `pyserial` 3.5), with `host/sim_board.py` in place of
the board:

| Test | Result |
|---|---|
| `solutions/host/logger.py --udp`, 2 recordings of 5 s, with `--plot` | 2 files with 250 samples, 50.00 Hz, 0 lost samples, 2 plots |
| `solutions/host/logger.py --udp`, with one lost packet in 20 | The logger reports 15 lost samples and prints the warning. `check_rate.py --file` prints `FAIL` with 15 lost lines. |
| `solutions/host/logger.py --port` with a simulated serial port | 1 file with 300 samples. `check_rate.py --file` prints `PASS`. |
| `solutions/host/logger.py` when the data stops | The logger stops after 5 s with a message |
| `host/logger.py` (student version) | It records and writes `recording.csv`. `--self-test` prints `not complete` for the two tasks. |
| `solutions/host/logger.py --self-test` | `complete` for the two tasks |
| `host/check_rate.py --udp` | `PASS` with no lost packet. `FAIL` with lost packets. |
| `host/make_fallback_dataset.py` | 48 files, 1.4 MB. Two runs give the same files. |
| `host/to_edge_impulse.py` with the fallback dataset | 32 training files and 16 test files |

Notebook check (work computer, 2026-10-02):

| Notebook | Result | Run time |
|---|---|---|
| `dataset.ipynb` (student version) | Runs from the first cell to the last cell with no error. It prints `not complete` for tasks 1, 2, and 3, and it does not write `split.json`. | about 4 s |
| `solutions/dataset.ipynb` | Runs from the first cell to the last cell with no error. It prints `complete` for tasks 1, 2, and 3. | about 4 s |
| `solutions/dataset.ipynb` with a dataset of one class and one session | Runs with no error. It says that a split by session is not possible. | about 4 s |

Results of the solution notebook with the fallback dataset. The signals are
simulated, so these numbers say nothing about the real kit:

- 48 recordings, 500 rows in each recording, no recording with a problem.
- Procedure A (random split of the windows): 100.0 percent.
- Procedure B (split by session): 100.0, 75.6, and 100.0 percent for the
  test sessions `s1`, `s2`, and `s3`. The mean is 91.9 percent.
- 1312 training windows and 656 test windows with the test session `s3`.

The notebooks come from one generator script of the course repository
(`tools/notebooks/build_day02_dataset.py`). Change the script, not the two
notebooks.

## 2. Checklist for the instructor

Run the lab on the real hardware. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: XIAOML Kit, MicroPython version:
- `esptool` version and `mpremote` version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, steps 2 to 4 | The time to erase and to write. The port name before and after. | |
| 2 | Part A, step 5 | The version text, the clock frequency, and the free memory | |
| 3 | Part A, step 7 (`blink_timer.py`) | Ticks in 10 s. Does one press of the button give one count? | |
| 4 | Part A, step 8 | The addresses of the scan | |
| 5 | Part B, step 1 | The six values with the kit flat. Which axis shows 1.0 g? | |
| 6 | Part B, step 3: the first version of `imu_stream.py` | Mean rate, minimum and maximum period, PASS or FAIL | |
| 7 | Part B, step 4: the solution `solutions/board/imu_stream.py` as `main.py` | Mean rate, period std, minimum and maximum period, lost lines, PASS or FAIL | |
| 8 | Copy a file with `mpremote` when `main.py` runs | Does the copy work with no `Ctrl-C`? | |
| 9 | Part B, step 5 (Wi-Fi) | Mean rate, lost lines in 20 s. Does the firewall of the laptop block the port? | |
| 10 | Part C, step 3 with `solutions/host/logger.py`: one class, 4 recordings, `--plot` | Samples, rate, and lost samples of each file. Do the plots agree with the motion? | |
| 11 | Record the complete dataset: 4 classes, 3 sessions, 4 recordings | The time for all 48 recordings | |
| 12 | Run `solutions/dataset.ipynb` with the real dataset | Recordings with a problem. The accuracy of procedure A and of procedure B. | |
| 13 | Part D, steps 1 to 4 | Does the Studio accept the files? Is the CSV Wizard necessary? The menu names. | |
| 14 | Part D, step 5 | Does the Arduino upload work with no bootloader mode? | |
| 15 | Upload `sketches/imu_data_collection` and run `host/check_rate.py --port` | Mean rate, PASS or FAIL | |
| 16 | Keep the real dataset of step 11 | Put it in the place of the simulated fallback dataset (see "After the test") | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 40 min | |
| B | 50 min | |
| C | 40 min | |
| D | 20 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured rates in `solutions/report_example.md` and in the lab
   deck.
2. If the first version of `imu_stream.py` passes the rate check, change
   step 2 and step 3 of Part B.
3. Replace the simulated fallback dataset with the real dataset of step 11:
   add the files to the folder `Labs/day02/fallback_data/`, and change the
   setup cell of the generator script so that it does not simulate. Then
   run the solution notebook again and correct the numbers of
   `solutions/report_example.md`.
4. Correct the menu names of Part D in the `README.md`.
5. Change the line `Hardware status:` of the `README.md` to
   `tested on hardware (YYYY-MM-DD)`.
6. Write the versions of `esptool` and `mpremote` in `Labs/VERSIONS.md`.
