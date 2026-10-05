# Test notes: Day 5 lab

## 1. Checklist for the instructor

Run the lab on the real hardware. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: XIAOML Kit, esp32 core version:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, steps 1 to 3 in the Studio | The menu names, the time for the upload and for the training, the accuracy, the estimates of the Studio | |
| 2 | Build the Arduino library of the keyword project and compile `solutions/sketches/kws_stream` with the core 3.3.12 | Does the library build? The time of the first build. `Sketch uses`. | |
| 3 | If step 2 fails: repeat with the core 2.0.17 | The result | |
| 4 | Read the Serial Monitor | `stride_ms`, `dsp_ms`, `classification_ms`. Is the work for one window shorter than 250 ms? | |
| 5 | Say `yes` 10 times with the student version, then with the solution | The number of events for each version | |
| 6 | The three tests of Part A, step 6 | False accepts in 30 s, missed words of 20, delay. The settings that give no false accept. | |
| 7 | Listen to the sound of the ring buffer, or plot it | Does the signal have jumps or gaps? | |
| 8 | Part B, steps 1 to 3 in the Studio with `image_dataset/` | The accuracy, the estimates of the Studio, the time for the training | |
| 9 | Build the library of the image project and compile `sketches/image_classifier` | Does it build with the core 3.3.12? `Sketch uses`. | |
| 10 | Point the camera at the nine photos of `test_images/` on a screen | The class for each photo. Is the test with a screen good enough? | |
| 11 | Part C | The times and the free heap of the two sketches | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

1. Write the measured numbers in `solutions/report_example.md` and in the
   lab deck.
2. Put the two library ZIP files of your test in a shared folder for the
   students, as the fallback of the README.
3. If the work for one window is longer than 250 ms, change the default
   value of `STRIDE_MS` in the two sketch folders.
4. Replace the image dataset with photos of objects that the classroom has,
   taken with the camera of the kit. The backup module MC-8 gives a method.
5. Correct the menu names of the Studio in the `README.md`.
