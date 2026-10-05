# Day 5 lab: audio and vision on the microcontroller


**Goal.** Your group has one audio model and one vision model on the XIAOML
Kit: a keyword spotter that makes one event for each spoken keyword, and an
image classifier that shows the class on the display.

**Deliverable.** Two live demonstrations, and the file `report.md` with the
measurement table and the Decision Log.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Keyword spotting: data, training in Edge Impulse Studio, the `int8` model on the kit, smoothing and threshold | 80 min |
| B | Image classification: transfer learning on a prepared dataset, the `int8` model on the kit, the class on the display | 55 min |
| C | Measure: latency and RAM of the two models | 15 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| XIAOML Kit | 1 | XIAO ESP32S3 Sense with the expansion board: microphone, camera, and display |
| USB-C cable | 1 | A data cable |
| Laptop | 1 | With a microphone, for your own recordings |

## Software

| Tool | Version | Note |
|---|---|---|
| Arduino IDE 2 with the esp32 core | 3.3.12 | Steps 1 to 3 of `Labs/SETUP.md` |
| U8g2 (library) | 2.36.19 | Installed on Day 1 |
| Edge Impulse account | no version | One account for each student. Create it before the lab. |
| Python | 3.10 or later | Only for the script `host/get_keywords.py`. It needs no package. |

The two models of this lab come from Edge Impulse Studio. The Studio makes
one Arduino library for each model. No Python package is necessary.

Run all commands of this lab from the folder `Labs/day05/`.

## Files

| File | Content |
|---|---|
| `host/get_keywords.py` | Part A. Downloads the keyword dataset and writes 300 clips of each class into the folder `keywords/`. |
| `sketches/kws_stream/kws_stream.ino` | Part A. The sketch for the keyword model, with a sliding window. |
| `sketches/kws_stream/postprocess.h` | Part A. The post-processing. **Tasks A1 and A2** are in this file. |
| `host/postprocess_test.cpp` | A test of `postprocess.h` on the laptop with the example of the lecture. It is an option, for a laptop with a C++ compiler. |
| `image_dataset/` | Part B. The prepared dataset: 81 photos in the classes `background`, `periquito` (a toy parrot), and `robot`. |
| `test_images/` | Part B. Nine photos that are not in the dataset, three for each class. |
| `sketches/image_classifier/image_classifier.ino` | Part B. The sketch for the image model. It has no task. |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/` | The complete file `postprocess.h` with its sketch, and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

## Steps

Write each result in `report.md` when you get it.

### Part A: keyword spotting (80 min)

1. **Data (20 min).** Get the keyword dataset:

   ```bash
   python3 host/get_keywords.py
   ```

   The script downloads 139 MB one time. If the instructor gives you the
   file `keywords2.zip`, put it into the folder `downloads/` first. You
   then see four folders in `keywords/`: `yes`, `no`, `unknown`, and
   `noise`, with 300 clips of 1 s for each class.

   In Edge Impulse Studio, create a project. In `Data acquisition`, select
   `Upload data`. Upload each folder with the option
   `Automatically split between training and testing`. The Studio reads
   the label from the file name.

   Then record your own voice. In `Data acquisition`, connect the laptop
   or a phone as a device. Record 10 s with the label `yes`: say the word
   about 8 times. Do the same for `no`. Use `Split sample` in the menu of
   each recording to get clips of 1 s.

2. **Impulse and features (10 min).** In `Create impulse`, set a window
   size of 1000 ms and a window increase of 500 ms. Add the processing
   block `Audio (MFCC)` and the learning block `Classification`. Save the
   impulse. In `MFCC`, keep the default parameters, and generate the
   features.

   Write in the report: the number of frames and of coefficients, and the
   estimates of the Studio for the processing time and the peak RAM of the
   feature block.

3. **Train (10 min).** In `Classifier`, keep the default model: two
   convolution layers along the time axis with 8 and 16 filters. Set 100
   training cycles and a learning rate of 0.005. Start the training. Then
   run `Model testing`.

   Write in the report: the accuracy, the confusion matrix, and the
   estimates of the Studio for the inferencing time, the peak RAM, and the
   flash use.

4. **Deploy (15 min).** In `Deployment`, select `Arduino library` and the
   model type `Quantized (int8)`. Build. Add the ZIP file in the Arduino
   IDE: `Sketch` > `Include Library` > `Add .ZIP Library`.

   Open `sketches/kws_stream/kws_stream.ino`. Change the first `#include`
   line to the header of your library. Select the board `XIAO_ESP32S3` and
   the port. Set `Tools` > `PSRAM` > `OPI PSRAM`. Click Upload. The first
   build of the library needs some minutes.

   You see in the Serial Monitor at 115200 baud the settings, the line
   `Task A1: not complete, no mean. Task A2: not complete, no suppression.`,
   and then one line for each window:

   ```
   stride_ms,dsp_ms,classification_ms,no,noise,unknown,yes,event
   ```

   Say the word `yes` 10 times, with a pause of 2 s. Count the events in
   the Serial Monitor. Write the number in the report: it is the result
   with no post-processing.

5. **Tasks A1 and A2: the post-processing (10 min).** Open the tab
   `postprocess.h` in the Arduino IDE. Complete the two places with the
   mark `TODO (student)`:

   - Task A1: the function `pp_mean` returns the mean of the last `n`
     results for one class.
   - Task A2: the function `pp_event` gives no event during the
     suppression time.

   Set the two flags `kTaskA1Complete` and `kTaskA2Complete` to `true`.
   Upload. Say the word `yes` 10 times again, and count the events.

6. **Tune (15 min).** Do the three tests of the lecture. Write each result
   in the table of the report:

   - False accepts: one student reads a text with no keyword for 30 s.
     Count the events.
   - False rejects: say `yes` 20 times with pauses. Count the missed
     words.
   - Delay: estimate the time from the word to the event on the display.

   Change one setting of the sketch, and repeat the three tests:
   `SMOOTH_WINDOWS`, `THRESHOLD`, `SUPPRESSION_MS`, or `STRIDE_MS`. Do at
   least three rounds. The column `stride_ms` of the Serial Monitor shows
   the real time between two windows. If it is larger than `STRIDE_MS`,
   the work for one window is longer than your stride.

### Part B: image classification (55 min)

1. **Data (10 min).** Create a second project in the Studio. In
   `Data acquisition`, upload the three folders of `image_dataset/`, one
   after the other, with the option
   `Automatically split between training and testing`. Enter the label of
   each folder: `background`, `periquito`, or `robot`. To the question
   about an object detection project, answer no.

2. **Impulse (5 min).** In `Create impulse`, set an image size of 96 x 96.
   Add the processing block `Image` and the learning block
   `Transfer Learning (Images)`. Save. In `Image`, select the colour depth
   `RGB`, and generate the features.

3. **Train (15 min).** In `Transfer learning`, select the model
   `MobileNetV2 96x96 0.35` with 16 neurons in the last layer and a
   dropout of 0.1. Set 20 training cycles and a learning rate of 0.0005,
   with data augmentation. Start the training. Then run `Model testing`.

   Write in the report: the accuracy, and the estimates of the Studio for
   the inferencing time, the peak RAM, and the flash use.

4. **Deploy (15 min).** In `Deployment`, select `Arduino library` and
   `Quantized (int8)`. Build. Add the ZIP file in the Arduino IDE. Open
   `sketches/image_classifier/image_classifier.ino`. Change the first
   `#include` line to the header of your library. Keep the setting
   `OPI PSRAM`. Upload.

   You see in the Serial Monitor the classes of the model, and then for
   each frame:

   ```
   Predictions (DSP: ... ms., Classification: ... ms., Anomaly: ... ms.):
   Timing (Capture: ... ms., Loop: ... ms.), free internal heap: ... bytes
   Predictions:
     background: ...
     periquito: ...
     robot: ...
   Best: ... (... %), display: ...
   ```

5. **Test (10 min).** Open the nine photos of `test_images/` on the laptop
   screen, one after the other. Point the camera of the kit at the screen,
   so that the photo fills the image. Write the class of the display for
   each photo in the report. If the instructor gives you the two toys, test
   them also.

   The display shows `...` until three frames in sequence give the same
   class. Set `VOTE_FRAMES` to 1, upload, and compare.

### Part C: measure (15 min)

1. **Latency (8 min).** For each of the two sketches, copy 10 lines of the
   Serial Monitor. Write in the report the median of the feature time
   (`dsp_ms`, or `DSP`), of the inference time (`classification_ms`, or
   `Classification`), and of the complete loop (`stride_ms`, or `Loop`).
   For the image model, write the capture time also.

2. **RAM and flash (4 min).** Write the line `Sketch uses ... bytes` of
   each build, the free internal heap that each sketch prints, and the
   estimate of the Studio for the peak RAM of each model.

3. **Compare (3 min).** Compare your measured times with the estimates of
   the Studio. Write the Decision Log.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] The Serial Monitor of the keyword sketch shows
      `Task A1: complete. Task A2: complete.`
- [ ] The keyword sketch gives no event in 30 seconds of normal speech
      with no keyword.
- [ ] The keyword sketch gives one event for each spoken `yes`, in a test
      with 5 words.
- [ ] The image sketch shows the correct class for three test objects or
      test photos, one of each class.
- [ ] The report has the tuning table with at least three rounds.
- [ ] The report has the measurement table with the latency and the RAM of
      the two models.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: the two models go into one product, the
voice-controlled camera of the lecture. The keyword model is stage 1, and
the image model is stage 2. Which settings do you select for the
post-processing of stage 1? Use your tuning table. Can one XIAO ESP32S3 run
the two stages? Use your numbers for the RAM and for the time.

## If a part does not work

| Problem | Fallback |
|---|---|
| The download of the keyword dataset fails | The instructor gives the file `keywords2.zip` on a USB drive. Put it into `downloads/` and run the script again. |
| You cannot record your own voice in the Studio | Train with the 300 clips of each class only, and write this in the report. |
| The Studio is not available, or the training is not complete in time | Use the library ZIP file that the instructor gives, and write this in the report. |
| The build of the Edge Impulse library fails with the core 3.3.12 | Install the core 2.0.17 in the Boards Manager and build again. The two sketches work with the two cores. Write the core version in the report. |
| Tasks A1 and A2 are not complete in time | Use the file `solutions/sketches/kws_stream/postprocess.h`, and write this in the report. |
| The image model gives a wrong class for the photos on the screen | Decrease the brightness of the screen, and remove reflections. Test with the real objects if the instructor has them. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| The build prints `XIAO-ESP32S3-KWS_inferencing.h: No such file or directory` | The `#include` line has the name of a different project | Change the line to the header of your library: `Sketch` > `Include Library` shows the name |
| The build prints `Invalid model for current sensor` | The sketch has the library of the other model | Use the audio library for `kws_stream` and the image library for `image_classifier` |
| The Serial Monitor prints `ERROR: not enough memory for the audio buffers` | The PSRAM is not active | Set `Tools` > `PSRAM` > `OPI PSRAM` |
| The image sketch prints `Camera init failed` | The PSRAM is not active, or the camera cable is loose | Set `OPI PSRAM`. Push the camera connector into its socket. |
| All probabilities of the keyword model stay near `noise` | The microphone signal is too quiet, or the board is too far from the mouth | Speak at 20 to 30 cm from the kit |
| One spoken word gives two or three events | Task A2 is not complete, or the suppression time is too short | Complete task A2. Increase `SUPPRESSION_MS`. |
| A spoken word gives no event | The mean of `SMOOTH_WINDOWS` windows stays below the threshold | Use fewer windows, a lower threshold, or a smaller stride |
| `stride_ms` is much larger than `STRIDE_MS` | The features and the inference need more time than the stride | Write the real value in the report. Increase `STRIDE_MS` to this value. |
| The display of the image sketch shows `...` all the time | The frames do not agree | Hold the kit still. Set `VOTE_FRAMES` to 1 to see each frame. |

## Credits

This lab adapts material from these sources:

- The chapters "Keyword Spotting (KWS)" and "Image Classification" of the
  XIAOML Kit in "Machine Learning Systems" by Vijay Janapa Reddi and
  contributors, written by Marcelo Rovai (mlsysbook.ai, CC BY-NC-SA 4.0):
  the four keyword classes, the settings of the two impulses, the models,
  the training settings, and the steps in Edge Impulse Studio.
- The repository XIAO-ESP32S3-Sense by Marcelo Rovai
  (github.com/Mjrovai/XIAO-ESP32S3-Sense, Apache-2.0): the two sketches
  `xiaoml-kit_kws_oled` and `XIAOML-Kit-Img_Class_OLED_Gen`. The sketch
  `image_classifier` is a copy with small changes. The sketch `kws_stream`
  adapts the first sketch. The two sketches adapt examples of Edge Impulse
  (MIT licence). The licence notice is in each sketch.
- The repository EdgeML-with-Raspberry-Pi by Marcelo Rovai
  (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0): the 90 photos of
  the folders `image_dataset/` and `test_images/`.
- The keyword dataset of Edge Impulse, with words of the dataset "Speech
  Commands" by Pete Warden (CC BY 4.0). The script downloads it. It is not
  in this repository.

The sliding window of the keyword sketch, the post-processing, the vote of
the image sketch, and the measurements are new code of this course.
