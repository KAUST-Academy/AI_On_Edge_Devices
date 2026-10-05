# Test notes: Day 4 lab

## 1. Checklist for the instructor

Run the lab on the real hardware with a real Day 2 dataset. Record the
result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: XIAOML Kit, esp32 core version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run `solutions/quantization.ipynb` with a real dataset | The run time. The tables of sections 7, 9, 11, and 12. Does each experiment show an effect with real data? | |
| 2 | Copy the four files of the notebook into `solutions/sketches/motion_quant/` and upload with `MODEL_INT8 0` and PSRAM disabled | The build line `Sketch uses`. All lines of the Serial Monitor before the loop. | |
| 3 | Upload with `MODEL_INT8 1` | The same lines, and the line with the clipped input values | |
| 4 | Compare the two runs | Arena used, median and largest `invoke_us`, correct windows, same class as on the laptop | |
| 5 | Make each of the four motions for 10 s with the `int8` model | The class that the display shows. The value of `late_samples`. | |
| 6 | Upload the student version with `MODEL_INT8 1` and no change | Does it print `Task D1: not complete. Task D2: not complete.`? | |
| 7 | Read the build time | The time of a build after a change of `MODEL_INT8`. Part D has 30 minutes for two builds. | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

1. Write the measured numbers in `solutions/report_example.md` and in the
   lab deck.
2. Replace the four files `model_float.h`, `model_int8.h`,
   `model_settings.h`, and `test_set.h` of the two sketch folders with the
   files of a model from a real dataset.
3. If an experiment of Part C shows no effect with the real dataset, change
   the numbers of bits in the generator script.
4. Write the result of the latency comparison in the README: which model is
   faster on the board.
