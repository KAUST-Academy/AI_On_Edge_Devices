# Test notes: Day 9 lab

## 1. Checklist for the instructor

Run the lab on the real hardware. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Boards: XIAOML Kit, Raspberry Pi 5 (8 GB) with the active cooler

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Copy `solutions/sketches/kit_bench/bench_stats.h` into the sketch folder. Build with `OPI PSRAM` and upload. | The time of the first build. The two lines of the build. | |
| 2 | Open the Serial Monitor | The complete output. Is each line `Same result as LiteRT: yes`? | |
| 3 | The same output | The memory of each arena: internal RAM or PSRAM. The free internal heap. | |
| 4 | Send a character two times | The median of each model for three runs: the noise | |
| 5 | Build with PSRAM disabled | Which model prints `ERROR: no memory`? | |
| 6 | Set `CPU_MHZ` to 80 and upload | The medians. Does the Serial Monitor work after the change? | |
| 7 | With a USB power meter at the kit | The power with no load and during the run | |
| 8 | On the Raspberry Pi: `vcgencmd pmic_read_adc` | The complete output, as a text file. The script needs lines of the form `NAME_A current(n)=...A` and `NAME_V volt(n)=...V`. | |
| 9 | `python solutions/pi/bench.py --idle 30` | The temperature and the power. Compare the power with a power meter. | |
| 10 | `python solutions/pi/bench.py --suite tiny` and `--suite classification` in `~/tflite_env` | The two tables. Is each class check `same as the kit sketch`? | |
| 11 | `python solutions/pi/bench.py --suite detection` in `~/yolo` | The table. Does `ncnn` import? | |
| 12 | `python solutions/pi/bench.py --sustain 180 --model ../day08/models/cupbottle_320.tflite --threads 4` | The first and the last line. The highest temperature. The throttle state. | |
| 13 | Copy `results_pi.csv`, make `results_kit.csv`, and run `python3 solutions/pi/make_report.py` | The four tables. Are the energy values plausible? | |
| 14 | Compare the latency of the two `int8` models on the kit with the published results in `report.md` | The factor to each board | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

1. Write the measured values of the two boards in
   `solutions/report_example.md` and in the lab deck.
2. If a `float32` model needs more than 5 seconds for one inference on the
   kit, decrease `TIMED_RUNS` in the sketch and in the README.
3. If the output of `vcgencmd pmic_read_adc` has a different form, correct
   the function `parse_pmic` in `pi/bench.py` and in
   `solutions/pi/bench.py`.
4. If the power estimate of the board differs much from the power meter,
   write the two values here, and change the fallback of the README.
5. Write the measured power of the kit in `power.csv`, with the method
   `USB power meter`.
6. Write the package versions of the board in `Labs/VERSIONS.md`.
