# Test notes: Day 3 lab

## 1. Checklist for the instructor

Run the lab on the real hardware with a real Day 2 dataset. Record the
result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: XIAOML Kit, esp32 core version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Run `solutions/motion_classifier.ipynb` with a real dataset | Test accuracy of the two inputs for each session. The run time. | |
| 2 | Copy the three files of the notebook into `solutions/sketches/motion_classifier/` and upload with PSRAM disabled | The time of the first build. The lines of the self-test. | |
| 3 | Read the memory lines | Sketch size, arena used, free internal heap | |
| 4 | Make each of the four motions for 10 s | The class that the display shows. The probability. | |
| 5 | Read 20 output lines | Median and maximum of `features_us` and `invoke_us`. The value of `late_samples`. | |
| 6 | Set `kTensorArenaSize` to 1024 | The message of the Serial Monitor | |
| 7 | OPI PSRAM with `ARENA_IN_PSRAM 1` | The same numbers as in steps 3 and 5 | |
| 8 | Upload the student version with no change | Does it print `Tasks B1 and B2 are not complete.`? | |
| 9 | Part D, steps 1 and 2 | The menu names, the test accuracy, the three estimates of the Studio, the time for the training | |
| 10 | Part D, step 3 with the core 3.3.12 | Does the library build? The time of the build. The two times of the output line. The sketch size. | |
| 11 | If step 10 fails: repeat with the core 2.0.17 | The result | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

1. Write the measured numbers in `solutions/report_example.md` and in the
   lab deck.
2. Replace the three files `model.h`, `model_settings.h`, and `test_window.h`
   of the two sketch folders with the files of a model from a real dataset.
3. If `late_samples` increases, change the display update in the two
   sketches.
4. Correct the menu names of Part D in the `README.md`.
