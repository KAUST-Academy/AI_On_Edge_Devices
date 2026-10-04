# Test notes: Day 5 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `sketches/kws_stream/kws_stream.ino`, `solutions/sketches/kws_stream/kws_stream.ino` | changed | The sketch `xiaoml-kit_kws_oled` of XIAO-ESP32S3-Sense | The two files are equal. New: the microphone code for the core 3.x (library ESP_I2S), the ring buffer, the sliding window, the post-processing, the output lines, a shorter display code. The microphone lines of the source stay for a build with the core 2.0.17. Not tested on a board. |
| `sketches/kws_stream/postprocess.h` | new | The method of Part 3 of the lecture | Student version. Tasks A1 and A2 are not complete. Tested on the work computer. |
| `solutions/sketches/kws_stream/postprocess.h` | new | The same method | Tested on the work computer with the example of the lecture. |
| `sketches/image_classifier/image_classifier.ino` | changed | The sketch `XIAOML-Kit-Img_Class_OLED_Gen` of XIAO-ESP32S3-Sense | New: the header comment, the two pin names of the camera bus for the core 3.x, a wait of 3 s for the Serial Monitor in place of a wait with no end, the output of the capture time, the loop time, and the free memory, and the setting `VOTE_FRAMES`. Not tested on a board. |
| `host/get_keywords.py` | new | The dataset link of the kit lab | Tested on the work computer: the download and the four folders. |
| `host/postprocess_test.cpp` | new | The example values of the lecture | Tested on the work computer with the two versions of `postprocess.h`. |
| `image_dataset/`, `test_images/` | copied with no change of the photos | The folder `IMG_CLASS/dataset` of EdgeML-with-Raspberry-Pi | The last three photos of each class are in `test_images/`, with new file names. The other 81 photos are in `image_dataset/`. |

Points that only a board and Edge Impulse Studio can confirm:

- The build of an Edge Impulse library with the core 3.3.12. The kit lab
  names the core 2.0.17. Nobody built a real library for this lab.
- The microphone code with the library ESP_I2S in the capture task: the
  call `I2S.readBytes()` with 512 samples, and the gain of 8.
- The sliding window: the time of the features and of the inference for one
  window. If it is larger than 250 ms, the column `stride_ms` shows the real
  stride, and the default settings of the post-processing need a change.
- The capture task and the loop use the ring buffer with no lock. The ring
  buffer holds 2 s, and the loop copies the newest second. Nobody checked
  this for errors in the sound.
- The lines of the source for the core 2.0.17 in `kws_stream.ino`. Nobody
  compiled them: the work computer has the core 3.3.12 only.
- All steps in Edge Impulse Studio, the menu names of the README, and the
  time for the uploads and for the two trainings.
- The image dataset has 81 photos of two toys. Nobody trained a model with
  it in the Studio. The test with photos on a laptop screen is a
  replacement for a test with the real toys.
- The times of Part C. The lab gives no expected value.

Compile check (no board, `arduino-cli` 1.5.1, esp32 core 3.3.12, library
U8g2 2.36.19, 2026-10-02). The sketches need the Arduino library of an Edge
Impulse project. For the check, a small replacement library gave the names
that the sketches use, with no model. The replacement is not in this
repository. So the sizes are not the sizes of a real build.

| Sketch | Board name (FQBN) and option | Result |
|---|---|---|
| `sketches/kws_stream` (student version of `postprocess.h`) | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles with the replacement library |
| `solutions/sketches/kws_stream` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles with the replacement library |
| `sketches/image_classifier` | `esp32:esp32:XIAO_ESP32S3:PSRAM=opi` | compiles with the replacement library |

Test with no board (work computer, 2026-10-02). The program
`host/postprocess_test.cpp` gives the 15 example windows of the lecture to
the functions of `postprocess.h`, with a mean of 3 windows, a threshold of
0.6, a suppression time of 1000 ms, and a stride of 250 ms:

| Version of `postprocess.h` | Events | Windows with an event |
|---|---|---|
| Student version (each window alone, no suppression) | 4 | 3, 8, 9, and 10 |
| Solution | 1 | 9 |

These are the values of the lecture frames "One word, many results" and
"Smoothing". Build the test from the folder `Labs/day05/`:

```bash
g++ -std=c++17 -iquote solutions/sketches/kws_stream host/postprocess_test.cpp -o postprocess_test
./postprocess_test
```

Test of `host/get_keywords.py` (work computer, 2026-10-02): the file
`keywords2.zip` has 145 511 868 bytes and 1500, 1500, 1500, and 1536 clips
for the classes `yes`, `no`, `unknown`, and `noise`. The script wrote 300
clips of each class: 38 MB. Each clip has 16 000 samples at 16 kHz with 16
bits. The 300 clips of `yes` come from 299 speakers.

## 2. Checklist for the instructor

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

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 80 min | |
| B | 55 min | |
| C | 15 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured numbers in `solutions/report_example.md` and in the
   lab deck.
2. Put the two library ZIP files of your test in a shared folder for the
   students, as the fallback of the README.
3. If the work for one window is longer than 250 ms, change the default
   value of `STRIDE_MS` in the two sketch folders.
4. Replace the image dataset with photos of objects that the classroom has,
   taken with the camera of the kit. The backup module MC-8 gives a method.
5. Correct the menu names of the Studio in the `README.md`.
6. Change the line `Hardware status:` of the `README.md` to
   `tested on hardware (YYYY-MM-DD)`.
