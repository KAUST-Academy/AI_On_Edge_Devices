# Test notes: Day 8 lab

This file has three parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor. Part 3 gives the work
after the test.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `pi/detect_ssd.py`, `solutions/pi/detect_ssd.py` | changed | The function `detect_objects` of the notebook `SSD_MobileNetV1.ipynb` of EdgeML-with-Raspberry-Pi | New: the command line, the thread setting, the time measurement, the function `to_pixel_boxes` with its check, and the drawing with Pillow. The student version has no body in the function `to_pixel_boxes` (Task A1). Tested on the work computer. Not tested on a Raspberry Pi. |
| `pi/detect_yolo.py` | changed | The notebook `YOLO_Model_Prediction_with_Ultralytics.ipynb` of EdgeML-with-Raspberry-Pi | The calls of the notebook as one script. New: the command line and the median time of each step. Tested on the work computer with the PyTorch file, the two NCNN folders, and the four LiteRT files. Not tested on a Raspberry Pi. |
| `pi/live_detect.py` | changed | The script `object_detection_app.py` of EdgeML-with-Raspberry-Pi | The web server, the worker thread, and the stream of JPEG images of the source. New: a YOLO model in place of the SSD model, the camera gives arrays, the time of each step, a page with no file from the internet, and image files as a source. Tested on the work computer with image files, and with a replacement for the package `picamera2`. Not tested with a camera. |
| `pi/detector.py` | new | The camera settings of `object_detection_app.py` | The camera class is new and not tested: the format `RGB888`, the size 640 x 480, and `capture_array()`. The function `set_litert_threads` changes a value of the package `ultralytics` 8.4.171. |
| `pi/bench_detect.py`, `solutions/pi/bench_detect.py` | new | The method of Part 3 of the lecture | The student version has no body in the function `frame_rate` (Task D1). Tested on the work computer with image files and with the camera replacement. Not tested on a Raspberry Pi. |
| `get_dataset.py` | new | no source | Tested on the work computer: complete downloads into new folders, a second run that downloads nothing, and a simulated network error. |
| `dataset/cup_bottle.csv` | new | The annotations of COCO 2017 | A selection of 589 labels in 400 images. A person looked at each image, see below. |
| `train_detector.py` | changed | The training cell of the notebook `yolo11_box_vs_wheel.ipynb` of EdgeML-with-Raspberry-Pi | The dataset, the image size 320, the option `freeze=10`, the processor of a laptop, and a copy of the best weights into `models/`. It ran three times on the work computer. |
| `custom_detector.ipynb`, `solutions/custom_detector.ipynb` | new | The training, validation, and export steps of the two notebooks above | The two versions ran on the work computer from the first cell to the last cell. They need no board. |
| `models/ssd-mobilenet-v1-tflite-default-v1.tflite`, `models/coco_labels.txt` | copied with no change | The folder `OBJ_DETEC/models` of EdgeML-with-Raspberry-Pi | none |
| `Labs/hardware/HW-04/setup_pi.sh`, `check_pi.sh` | changed for this lab | See `Labs/hardware/HW-04/README.md` | The environment `~/yolo` gets `ultralytics==8.4.171`, `ncnn`, and `ai-edge-litert`. `check_pi.sh` tests the import of `ncnn`, `ai_edge_litert`, and `flask`. Not tested on a Raspberry Pi. |

Points that only a Raspberry Pi can confirm:

- The packages of `~/yolo`: a wheel of `ultralytics` 8.4.171, `ncnn`, and
  `ai-edge-litert` for the Python version of the operating system. The
  scripts ran on the work computer with `ultralytics` 8.4.171, `torch`
  2.14.1, `ncnn` 1.0.20260526, `ai-edge-litert` 2.2.0, `opencv-python`
  5.0.0.93, and `flask` 3.1.3.
- The camera class of `pi/detector.py`. The package `picamera2` names its
  format `RGB888` for bytes in the order blue, green, red, which OpenCV
  and the package `ultralytics` use. If a red object is blue in the live
  image, change the format to `BGR888` in the class `CameraSource`.
- The two NCNN folders and the four LiteRT files on an Arm processor. An
  x86 computer made them. The export to LiteRT does not run on the board.
- The function `set_litert_threads`. The package uses the number of cores
  minus 1 for a LiteRT file, at most 8: 3 threads on the board. NCNN uses
  its own default. The scripts set 4 threads for LiteRT. If a later version
  of the package has no value `NUM_THREADS` in `ultralytics.nn.backends.litert`,
  the scripts print a note and use the default.
- The web page of `pi/live_detect.py` in the browser of a laptop, with the
  port 5000 in the lab network.
- All times and all frame rates. The lab gives no expected value for the
  board. The companion book gives two published times for a custom YOLO11n
  model at 320 pixels on a Raspberry Pi 5: about 400 ms in PyTorch and
  about 80 ms in NCNN.
- The live check with a real bottle and a real cup. Nobody pointed a camera
  at an object. On two office photos of the source, the custom model found
  a cup on a desk with a score of 0.41 and a small bottle with 0.28.
- The download of `yolo11n.pt` on the board in the lab network.
- The time for each part.

Test of the dataset (work computer, 2026-10-02). The script
`get_dataset.py` downloaded the 400 images in 73 to 85 s with 8
parallel downloads, in three runs. The folder has 59 MB. In three
other runs, one or two images failed with a name resolution error of the
network, and one of these runs needed some minutes because the server was
slow. The script now tries each such image again in three more rounds. A
test with a simulated network error passed.

The selection of the images (the tool `day08_lab_dataset.py` of the private
course repository). The rules: 1 to 4 labels of the two classes, no label
with the mark "crowd", each label with a width and a height of 10 percent
of the image or more (8 percent for the test images), no caption with a
word for alcohol, tobacco, or little clothing, no label of the class
`wine glass`, and no person in the images of `train` and `valid`. A person
then looked at each of the selected images as a small picture, and at
each doubtful image in a larger size. This look removed 32 images: bottles
and glasses of beer, wine, cider, and liquor, one religious figure, and one
image of persons in close contact. A look at small pictures can miss a
detail. If you find an image that is not good for the classroom, add its
number to the list `EXCLUDE` of that tool and make the file again.

Test of `requirements.txt` (work computer, 2026-10-02, Linux on x86, Python
3.10.12). In a new environment with `pip` 26.2.1, the install needed 144 s,
and `pip check` found no broken requirement. The environment has 2.7 GB.
The two notebooks ran in this environment.

Test of the notebook (work computer, 2026-10-02, 4 cores of an Intel Xeon
E5-2680 v3, `torch` 2.13.0, `ultralytics` 8.4.171, `litert-torch` 0.9.4):

| Check | Student version | Solution |
|---|---|---|
| Runs from the first cell to the last cell | yes, 13 minutes | yes, 13 minutes |
| Task 1 | not complete | complete |
| Task 2 | not complete | complete |
| Task 3 | not complete | complete |
| Training time | 8.8 minutes | 8.7 minutes |
| Stored output | none | yes. The three figures with photos are not stored. |

Results of the solution. The student version trains the same model: its
validation mAP50 is 0.656.

| Item | Value |
|---|---|
| Candidates of `bus.jpg` above 0.25, and detections for the IoU thresholds 0.7 and 0.9 | 47, 5, 8 (the values of the lecture) |
| Best epoch, mAP50 and mAP50-95 on the 60 validation images | 25, 0.656, 0.491 |
| Your model on the 100 test images at 320 pixels: precision, recall, mAP50, mAP50-95 | 0.678, 0.468, 0.545, 0.380 |
| Pre-trained model at 320 pixels, both classes, score threshold 0.25: TP, FP, FN | 85, 27, 63 (precision 0.76, recall 0.57) |
| Pre-trained model at 640 pixels: TP, FP, FN | 105, 35, 43 (precision 0.75, recall 0.71) |
| Your model at 320 pixels: TP, FP, FN | 77, 66, 71 (precision 0.54, recall 0.52) |

The exported files and their accuracy on the 100 test images:

| File | Bytes | Export time in s | mAP50 | mAP50-95 |
|---|---|---|---|---|
| `cupbottle_320_ncnn_model` | 10 378 421 | 4 | not measured | not measured |
| `cupbottle_320.tflite` | 10 553 005 | 16 | 0.545 | 0.380 |
| `cupbottle_320_int8.tflite` | 3 023 254 | 32 | 0.520 | 0.339 |
| `cupbottle_640_ncnn_model` | 10 454 023 | 5 | not measured | not measured |
| `cupbottle_640.tflite` | 10 628 605 | 16 | 0.578 | 0.400 |
| `cupbottle_640_int8.tflite` | 3 041 798 | 53 | 0.543 | 0.320 |

The loss of `int8` against `float32` is 0.041 of mAP50-95 at 320 pixels
and 0.079 at 640 pixels. The pre-trained model has a higher recall than
the custom model. The notebook and the README say that this is a normal
result for 240 training images.

Other training runs on the work computer (2026-10-02, the first selection of
the images, 4 cores): with no fixed backbone and 30 epochs, the mAP50 on
the test images was 0.55 at 320 pixels after 16 minutes. With the fixed
backbone and 25 epochs, it was 0.60 after 9 minutes. A training at 640
pixels with no fixed backbone needed 18 minutes on 8 cores and gave 0.60 at
640 pixels.

Test of the scripts for the board (work computer, 2026-10-02, cores 8 to
11, the environment of the second list above). These are not values of the
board.

`solutions/pi/detect_ssd.py images/bus.jpg`: input 1 x 300 x 300 x 3 in
`uint8`, 10 rows in the output, 4 detections with a score of 0.5 or
more: person 0.83, bus 0.74, person 0.64, person 0.61. Median inference: 11.2 ms. The student version prints
`Task A1: not complete` and three rows of the raw output.

`pi/detect_yolo.py images/bus.jpg` with `yolo11n.pt`:

| Arguments | Detections | Scores | Inference, median in ms |
|---|---|---|---|
| none (640 pixels) | 5 | bus 0.94, person 0.89, person 0.88, person 0.86, person 0.62 | 81.8 |
| `--imgsz 320` | 5 | person 0.82, bus 0.81, person 0.80, person 0.57, person 0.28 | 55.7 |
| `--iou 0.9` | 6 | bus 0.94, person 0.89, person 0.88, person 0.86, person 0.62, person 0.39 | 77.7 |

The script gives the image to the package as a file. The package then uses
a rectangle of 640 x 480 pixels for the PyTorch file, so the scores differ
from the scores of the lecture, which used a square.

`pi/detect_yolo.py` with a test image of the dataset (`000000206027.jpg`,
4 labels: 2 bottles and 2 cups) and each exported file:

| File | Detections | Inference, median in ms |
|---|---|---|
| `cupbottle_320_ncnn_model` | bottle 0.98, cup 0.81, cup 0.48, bottle 0.37 | 55.9 |
| `cupbottle_320.tflite` | bottle 0.98, cup 0.81, cup 0.48, bottle 0.37 | 12.9 |
| `cupbottle_320_int8.tflite` | cup 0.58, bottle 0.58, cup 0.48, bottle 0.37 | 12.9 |
| `cupbottle_640_ncnn_model` | bottle 0.72, cup 0.59, cup 0.53, cup 0.32, cup 0.30 | 120.9 |
| `cupbottle_640.tflite` | bottle 0.72, cup 0.59, cup 0.53, cup 0.32, cup 0.30 | 43.0 |
| `cupbottle_640_int8.tflite` | bottle 0.71, cup 0.35, cup 0.28 | 58.7 |

`solutions/pi/bench_detect.py --source images/` (two image files in place
of the camera, 30 frames, median times in ms, second run):

| File | Runtime | Precision | Image size | Capture | Pre-processing | Inference | Post-processing | Frames in each second |
|---|---|---|---|---|---|---|---|---|
| `cupbottle_320_ncnn_model` | NCNN | `float32` | 320 | 5.8 | 1.0 | 54.8 | 1.2 | 15.9 |
| `cupbottle_320.tflite` | LiteRT | `float32` | 320 | 5.1 | 1.3 | 14.3 | 0.8 | 46.5 |
| `cupbottle_320_int8.tflite` | LiteRT | `int8` | 320 | 5.6 | 1.3 | 15.4 | 0.8 | 43.3 |
| `cupbottle_640_ncnn_model` | NCNN | `float32` | 640 | 5.2 | 2.1 | 118.9 | 1.1 | 7.8 |
| `cupbottle_640.tflite` | LiteRT | `float32` | 640 | 5.1 | 2.1 | 35.8 | 0.9 | 22.8 |
| `cupbottle_640_int8.tflite` | LiteRT | `int8` | 640 | 5.3 | 3.0 | 60.1 | 1.0 | 14.4 |

The largest difference of the frame rate between the two runs was 11
percent. On this x86 processor, LiteRT `float32` is the fastest file, and
`int8` is slower than `float32`, as in the lecture. The student version
prints `Task D1: not complete` and stops.

`pi/live_detect.py`: with image files and the option `--no-web`, 60 frames
with `cupbottle_320_ncnn_model` at 15.0 frames in each second. With
the camera replacement and the web server, `cupbottle_320_int8.tflite` ran
at 18.8 frames in each second. The page, the address `/stats`, and
the stream `/video` answered, and a frame of the stream showed the boxes.
The replacement waits 20 ms for each frame.

## 2. Checklist for the instructor

Run the lab on the real hardware. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: Raspberry Pi 5 (8 GB), release of Raspberry Pi OS:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | On the master card: `bash ~/HW-04/setup_pi.sh yolo`, then `bash ~/HW-04/check_pi.sh` | Do `ultralytics` 8.4.171, `ncnn`, `ai-edge-litert`, and `flask` install? The lines with `FAIL`. | |
| 2 | Part A, steps 1 and 2 | Does the copy command work? Does `rpicam-jpeg` save the photo of the desk? | |
| 3 | Part A, step 3 with `solutions/pi/detect_ssd.py` | The detections for `bus.jpg`. The load time, the first inference, the median. | |
| 4 | Part A, step 4 | Does the board download `yolo11n.pt`? The times of the three steps at 640 and at 320. The detections for the photo of the desk. | |
| 5 | On a lab laptop: install `requirements.txt` in a new environment | The time and the size of the install. Errors. | |
| 6 | Run `solutions/custom_detector.ipynb` on the lab laptop | The time of the download and of the training. The line `Tasks complete: 1, 2, 3`. The mAP on the test images. | |
| 7 | Copy the six exported files, and run `pi/detect_yolo.py` with each file on the photo of the desk | Does each file load? The detections. | |
| 8 | Part C, step 4: `pi/live_detect.py` with the NCNN folder and with the `int8` file | Does the page open on the laptop? Are the colours correct? The frame rate. Does the model find a real bottle and a real cup? At which distance? | |
| 9 | The same with `--model models/yolo11n.pt --imgsz 320` | Does the pre-trained model find the two objects? | |
| 10 | Part D: `solutions/pi/bench_detect.py`, two times | The complete table. The difference between the two runs. The two temperatures. | |
| 11 | `htop` during step 10 | The number of busy cores for NCNN and for LiteRT | |
| 12 | Look at the images of the dataset on the laptop: the folder `data/cup_bottle/` | An image that is not good for the classroom | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 30 min | |
| B | 50 min | |
| C | 40 min | |
| D | 30 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured frame-rate table of the board in
   `solutions/report_example.md` and in the lab deck.
2. Keep these files of your run of the solution notebook in a shared folder
   for the students: `models/cupbottle.pt`, the two NCNN folders, and the
   four LiteRT files. Keep also a copy of the folder `data/` and of the
   file `models/yolo11n.pt`. They are the fallbacks of the README. The
   private course repository has the weights of the run of 2026-10-02
   (`day08_cupbottle.pt`).
3. If the custom model does not find the real objects, train with more
   epochs (`python train_detector.py --epochs 50`), or let each group add
   20 photos of its own objects to the training images.
4. If a package of `~/yolo` needs a different version, correct
   `Labs/hardware/HW-04/setup_pi.sh` and `requirements.txt`: the laptop and
   the board must have the same version of `ultralytics`.
5. If the colours of the live image are wrong, change the camera format in
   `pi/detector.py`.
6. Write the package versions of the board and of the lab laptop in
   `Labs/VERSIONS.md`.
7. Answer question Q-7 of the plan: keep the dataset cup and bottle, or use
   the dataset "box and wheel" of the kit lab.
