# Test notes: Day 2 lab

## 1. Checklist for the instructor

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

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

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
5. Write the versions of `esptool` and `mpremote` in `Labs/VERSIONS.md`.
