# Day 8 lab: object detection on the Raspberry Pi


**Goal.** Your group has a live detection on the Raspberry Pi 5 with a
custom model for two classes, and a table with the frame rate and the
accuracy of the model for two image sizes and two precisions.

**Deliverable.** A live demonstration, and the frame-rate table and the
Decision Log in the file `report.md`.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Pre-trained models: an SSD model and a YOLO model on test images | 30 min |
| B | Custom model: train a YOLO model on a small dataset with two classes | 50 min |
| C | Export and deploy: NCNN and LiteRT `int8`, and the live detection with the camera | 40 min |
| D | Measure: the frame rate for two image sizes and two precisions, and the accuracy loss of `int8` | 30 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| Raspberry Pi 5 (8 GB) with the active cooler | 1 | With the microSD card of the course. The card has the label of your group: `pi-NN`. |
| Power supply for the Raspberry Pi 5 | 1 | 27 W, USB-C |
| Camera Module 3 with its cable | 1 | Connected to the camera port. Do not connect or remove the cable when the power is on. |
| Laptop | 1 | In the same network as the Raspberry Pi (the Wi-Fi `edgeai-lab`) |
| A bottle and a cup | 1 of each | The two classes of the custom model. Each object of the classroom is good: a water bottle, a paper cup, a mug. |

## Software

| Tool | Version | Note |
|---|---|---|
| Raspberry Pi OS (64-bit) with the environment `~/yolo` | the card of the course | `Labs/hardware/HW-04/` prepares the card. The environment has `ultralytics`, `torch`, `ncnn`, `ai-edge-litert`, `opencv-python`, and `flask`. The camera package `picamera2` comes from the operating system. |
| SSH client on the laptop | no version | The commands `ssh` and `scp` |
| Python on the laptop | 3.10 or later | For the notebook of Parts B and C, in a new environment |
| The packages of `requirements.txt` | see `Labs/VERSIONS.md` | `ultralytics` 8.4.171, `torch`, `litert-torch`, `ncnn`, `pnnx`, `onnx`, `notebook` |
| A browser on the laptop | no version | It shows the live image of Part C |

Make the environment for the notebook before the lab. It needs about 2.7 GB
on the disk. Run the commands in the folder `Labs/day08/`:

```bash
python3 -m venv ~/day08_env
~/day08_env/bin/pip install --upgrade pip
~/day08_env/bin/pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
```

The second command is necessary. An old version of `pip` needs a very long
time to find the package versions. Use this environment only for this lab.
The environment `~/day07_env` of the Day 7 lab does not have the package
`ultralytics`.

The export to LiteRT runs on Linux and on macOS. On Windows, use WSL or
Colab for the notebook.

Run all commands of this lab from the folder `Labs/day08/` on the laptop, and
from the folder `~/edgeai/day08/` on the Raspberry Pi. `NN` is the number of
your group.

## Files

| File | Content |
|---|---|
| `pi/detect_ssd.py` | Part A. Runs the SSD model on one image. **Task A1** is in this file. |
| `pi/detect_yolo.py` | Parts A and C. Runs a YOLO model on one image. It has no task. |
| `get_dataset.py` | Part B. Downloads the 400 images of the dataset into the folder `data/`. |
| `dataset/cup_bottle.csv` | The list of the images and their 589 labels |
| `train_detector.py` | Part B. Trains the model. The notebook starts this script. |
| `custom_detector.ipynb` | Parts B and C. The notebook for the laptop, with **Tasks 1, 2, and 3**. |
| `pi/live_detect.py` | Part C. The live detection with the camera and a web page. It has no task. |
| `pi/bench_detect.py` | Part D. Measures the frame rate of each model file. **Task D1** is in this file. |
| `pi/detector.py` | Shared code of the two scripts above: the camera, the model, the temperature |
| `models/ssd-mobilenet-v1-tflite-default-v1.tflite`, `models/coco_labels.txt` | The SSD model of the kit lab: SSD MobileNet V1 in `uint8` with 90 classes, 4 183 312 bytes |
| `requirements.txt` | The packages for the laptop |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/` | The complete notebook with its output, the two complete scripts, and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

The lab makes the folders `data/`, `runs/`, and `images/`, and it writes the
YOLO model files into the folder `models/`. Git ignores these files.

The package `ultralytics` and its models have the licence AGPL-3.0. This
repository holds no file of the package: the package downloads the weights
`yolo11n.pt` (5.4 MB) at the first run.

## The dataset

The kit lab uses photos of a box and a wheel. A classroom does not have
these two objects. This lab uses a bottle and a cup, which are two of the 80
classes of the dataset COCO.

| Split | Images | Labels `bottle` | Labels `cup` | Source |
|---|---|---|---|---|
| `train` | 240 | 172 | 185 | COCO `train2017` |
| `valid` | 60 | 41 | 43 | COCO `train2017` |
| `test` | 100 | 71 | 77 | COCO `val2017` |

Each image has 1 to 4 labels, and each label has a width and a height of
10 percent of the image or more (8 percent for the test images). The test
images come from a part of COCO that the pre-trained model did not see in
its training.

The pre-trained model already knows the two classes. The notebook measures
it as a baseline, and it compares your model with it.

## Steps

Write each result in `report.md` when you get it.

### Part A: pre-trained models (30 min)

1. **Start and copy (8 min).** Connect the power supply of the Raspberry Pi
   and wait for one minute. On the laptop, in the folder `Labs/`, make the
   lab folder on the board and copy two folders:

   ```bash
   ssh edge@pi-NN.local "mkdir -p ~/edgeai/day08/images"
   scp -r day08/pi day08/models edge@pi-NN.local:~/edgeai/day08/
   ```

   Then connect, go to the folder, and start the environment:

   ```bash
   ssh edge@pi-NN.local
   cd ~/edgeai/day08
   source ~/yolo/bin/activate
   ```

   Do the last two commands again in each new terminal. If the name
   `pi-NN.local` does not work, use the IP address that the instructor gives.

2. **Get two test images (4 min).** The first image is the photo `bus.jpg`
   of the package `ultralytics`, the image of the lecture. The second image
   is a photo of your desk. Put a bottle and a cup in front of the camera.

   ```bash
   python -c "from ultralytics.utils import ASSETS; import shutil; shutil.copy(ASSETS / 'bus.jpg', 'images/bus.jpg')"
   rpicam-jpeg --output images/desk.jpg --width 1280 --height 960
   ```

3. **The SSD model (9 min).** The model is SSD MobileNet V1 of the kit lab,
   with an input of 300 x 300 pixels:

   ```bash
   python pi/detect_ssd.py images/bus.jpg
   ```

   You see the input and the four outputs of the model, the times, the line
   `Task A1: not complete`, and three rows of the raw output.

   **Task A1.** Open `pi/detect_ssd.py` with `nano`, and complete the
   function `to_pixel_boxes` at the mark `TODO (student)`. The model gives
   each box as `ymin, xmin, ymax, xmax` from 0 to 1. The function changes it
   to pixels of the image, and it keeps the boxes above the score threshold.
   Run the script again. You see `Task A1: complete` and the detections.
   Then run it with your photo:

   ```bash
   python pi/detect_ssd.py images/desk.jpg --output ssd_desk.jpg
   ```

4. **The YOLO model (9 min).** The model is YOLO11n with the 80 classes of
   COCO. The first run downloads the weights (5.4 MB):

   ```bash
   python pi/detect_yolo.py images/bus.jpg
   python pi/detect_yolo.py images/bus.jpg --imgsz 320
   python pi/detect_yolo.py images/bus.jpg --iou 0.9
   python pi/detect_yolo.py images/desk.jpg --output yolo_desk.jpg
   ```

   You see the time of the three steps and the detections. Write the values
   in the report. Copy the result images to the laptop and look at them. Run
   this command on the laptop:

   ```bash
   scp "edge@pi-NN.local:~/edgeai/day08/*.jpg" .
   ```

   Tip: the download of the dataset and the training of Part B run in the
   background on the laptop. One student of the group can start sections 0
   to 2 of the notebook during this step.

### Part B: custom model (50 min)

Work on the laptop. Start the notebook:

```bash
~/day08_env/bin/jupyter notebook custom_detector.ipynb
```

Run the cells in order. The notebook has the detailed instructions.

| Section of the notebook | Content | Time |
|---|---|---|
| 0 and 1 | Setup, the download of the dataset, and a look at the labels | 8 min |
| 2 | Start the training in the background (about 9 minutes on 4 cores) | 2 min |
| 3 | **Task 1:** the IoU of two boxes | 7 min |
| 4 | **Task 2:** non-maximum suppression for the candidates of one image | 8 min |
| 5 | **Task 3:** count the true positives, the false positives, and the false negatives. The baseline of the pre-trained model. | 10 min |
| 6 | The result of the training: the curves | 8 min |
| 7 | Your model on the test images, and the comparison with the baseline | 7 min |

### Part C: export and deploy (40 min)

1. **Export (15 min).** Run sections 8 to 10 of the notebook. Section 8
   exports your model to NCNN and to LiteRT in `float32` and in `int8`, for
   the image sizes 320 and 640. Section 9 measures the accuracy of each
   file on the test images. Write the two tables in the report.

2. **Copy the files (3 min).** On the laptop, in the folder `Labs/day08/`:

   ```bash
   scp -r models/cupbottle_*_ncnn_model models/cupbottle_*.tflite edge@pi-NN.local:~/edgeai/day08/models/
   ```

3. **Check with one image (5 min).** On the Raspberry Pi, run your model on
   the photo of your desk. Give the image size of the file:

   ```bash
   python pi/detect_yolo.py images/desk.jpg --model models/cupbottle_320_ncnn_model --imgsz 320
   ```

   Compare with the result of the pre-trained model in Part A.

4. **Live detection (12 min).** Start the application:

   ```bash
   python pi/live_detect.py --model models/cupbottle_320_ncnn_model
   ```

   Open `http://pi-NN.local:5000` in the browser of the laptop. You see the
   live image with the boxes, the frame rate, and the time of each step.
   The terminal prints one line in each second. Put the bottle and the cup
   in front of the camera. Move them, change the distance, and change the
   background.

   Stop the application with Ctrl+C. Then start it with the `int8` file, and
   with a different score threshold:

   ```bash
   python pi/live_detect.py --model models/cupbottle_320_int8.tflite
   python pi/live_detect.py --model models/cupbottle_320_ncnn_model --conf 0.5
   ```

   Write in the report: which objects does the model find, which objects
   does it miss, and which wrong detections do you see?

5. **Demonstration (5 min).** Show the live image to the instructor: the
   model detects the bottle and the cup.

### Part D: measure (30 min)

Work on the Raspberry Pi. Stop the live application first.

1. **Predict (5 min).** Before you measure, write your prediction for each
   question of Part D in the report. Give a reason from the lecture.

2. **Task D1 (5 min).** Open `pi/bench_detect.py` with `nano`, and complete
   the function `frame_rate` at the mark `TODO (student)`: one frame needs
   the sum of the times of the four steps.

3. **Measure (10 min).** Point the camera at the bottle and the cup. Run:

   ```bash
   python pi/bench_detect.py
   ```

   The script prints one line for each of the six model files: the median
   time of each step for 30 frames of the camera, the frame rate, and the
   number of objects in the last frame. It also writes the file
   `results.csv`. Run the script a second time. The difference between the
   two runs is the noise of your measurement.

4. **Fill the table (5 min).** Write the frame-rate table in the report.
   Add the mAP of each file from section 9 of the notebook. Calculate the
   two ratios of the report: the gain from 640 to 320 pixels, and the gain
   from `float32` to `int8`.

5. **Compare and decide (5 min).** Compare the results with your
   predictions. Write the Decision Log.

If you have time: train a second model with images of 640 pixels
(`python train_detector.py --imgsz 640 --name cupbottle640` on the laptop,
about 4 times longer), and compare its mAP at 640 pixels with the mAP of
your first model at 640 pixels.

## Check criterion

The instructor checks this at the end of the lab:

- [ ] `python pi/detect_ssd.py images/bus.jpg` prints `Task A1: complete`
      and a list of detections.
- [ ] The notebook prints `Tasks complete: 1, 2, 3` in its last cell.
- [ ] The live image shows a box for the bottle and a box for the cup, with
      the custom model.
- [ ] `python pi/bench_detect.py` prints `Task D1: complete`.
- [ ] The frame-rate table of the report has four measured rows or more:
      two image sizes and two precisions.
- [ ] The report gives the accuracy loss of the `int8` file.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: a product with a Raspberry Pi 5 and a camera must
count the bottles and the cups on a table, with 10 frames in each second or
more. Which file do you select: which runtime, which image size, and which
precision? Use your frame-rate table and the mAP of each file.

## A second dataset: box and wheel

The kit lab trains its model with the dataset "box and wheel" (about 150
images, licence CC BY 4.0). The dataset is on Roboflow. A download needs a
free account and a key of your own.

1. Make an account on `roboflow.com`, and copy your key from the settings.
2. Install the package and download the dataset on the laptop:

   ```bash
   ~/day08_env/bin/pip install roboflow
   ```

   ```python
   from roboflow import Roboflow
   project = Roboflow(api_key="YOUR_KEY").workspace("marcelo-rovai-riila").project("box-versus-wheel-auto-dataset")
   dataset = project.version(8).download("yolov11")
   print(dataset.location)
   ```

3. Train with the file `data.yaml` of the folder that the last line prints:

   ```bash
   ~/day08_env/bin/python train_detector.py --data PATH/data.yaml --name boxwheel
   ```

The live check then uses the test photos of the dataset on the laptop
screen. Give the files to the scripts with the options `--model` and
`--models`.

## If a part does not work

| Problem | Fallback |
|---|---|
| The name `pi-NN.local` does not work | Use the IP address that the instructor gives |
| The Raspberry Pi has no internet connection for the weights `yolo11n.pt` | The notebook downloads the same file on the laptop. Copy it: `scp models/yolo11n.pt edge@pi-NN.local:~/edgeai/day08/models/` |
| The camera gives no photo | Use `images/bus.jpg` in Part A. In Parts C and D, give image files to the scripts: `--source images/`. Write this in the report, and tell the instructor. |
| The download of the dataset stops | Run `python get_dataset.py` again: it keeps the complete images. The instructor has a copy of the folder `data/`. |
| The environment for the notebook does not install, or the laptop has Windows with no WSL | Work with a second group on one laptop, or use Colab: upload the folder `Labs/day08/`, and install `requirements.txt` in the first cell |
| The training is not complete in time | The instructor gives the file `cupbottle.pt`. Put it into the folder `models/` and run the notebook from section 3: the notebook uses the file and does not train. |
| A task of the notebook is not complete in time | Use the cell of `solutions/custom_detector.ipynb`, and write this in the report |
| Task A1 or Task D1 is not complete in time | Use the file of the folder `solutions/pi/`, and write this in the report |
| The export to LiteRT stops with an error | Do Parts C and D with the two NCNN folders. The instructor gives the four LiteRT files. |
| The custom model does not find your objects | Use a lower score threshold (`--conf 0.15`), a plain background, and a distance of about 50 cm. Compare with the pre-trained model: `python pi/live_detect.py --model models/yolo11n.pt --imgsz 320`. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| `ERROR: the package ultralytics is not available` | The environment is not active | `source ~/yolo/bin/activate` |
| `ERROR: the package picamera2 is not available` | The script does not run on the Raspberry Pi, or the environment cannot see the system packages | Run it on the Raspberry Pi. Tell the instructor if it fails there. |
| The package prints `requirements: ... not found, attempting AutoUpdate` | A runtime package (`ncnn` or `ai-edge-litert`) is not in the environment | Let the package install it, or run `pip install ncnn ai-edge-litert` in the environment `~/yolo` |
| The browser shows no page at `http://pi-NN.local:5000` | The application is not active, or the laptop is in a different network | Read the terminal of the application. Use the IP address of the board. |
| The colours of the live image are wrong: a red object is blue | The camera gives a different order of the colours | Tell the instructor. `TEST_NOTES.md` gives the line to change in `pi/detector.py`. |
| The live image has many wrong boxes | The image size of the command is not the image size of the file | Use the size of the file name: `cupbottle_320...` runs with 320. The scripts `pi/live_detect.py` and `pi/bench_detect.py` read the size from the name. |
| `ERROR: the name of the model gives no image size` | The file name has no number such as `_320` | Give the option `--imgsz` |
| The export stops with a message about `typing_extensions` or `jupyter_client` | The packages are not the versions of `requirements.txt` | Make a new environment and install only `requirements.txt` |
| The notebook cell of section 6 prints `ERROR: the training stopped with an error` | The dataset is not complete, or the disk is full | Read the file `runs/train_log.txt`. Run `python get_dataset.py --check`. |
| `pi/bench_detect.py` prints `not found` for a file | The file is not in the folder `models/` on the Raspberry Pi | Copy it with the `scp` command of Part C |
| The frame rate changes much between two runs | A second program uses the cores, or the processor is hot | Stop the live application. The script prints the temperature. Wait for one minute and run again. |

## Credits

This lab adapts material from these sources:

- The chapter "Object Detection" of the Raspberry Pi kit labs in "Machine
  Learning Systems" by Vijay Janapa Reddi and contributors, written by
  Marcelo Rovai (mlsysbook.ai, CC BY-NC-SA 4.0): the steps of the inference
  with the SSD model and with YOLO, the training of a custom model, the
  export to NCNN, and the live application.
- The repository EdgeML-with-Raspberry-Pi by Marcelo Rovai
  (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0): the notebooks
  `SSD_MobileNetV1.ipynb`, `YOLO_Model_Prediction_with_Ultralytics.ipynb`,
  and `yolo11_box_vs_wheel.ipynb`, the script `object_detection_app.py`, and
  the model file `ssd-mobilenet-v1-tflite-default-v1.tflite` with its labels
  (a model of the TensorFlow authors, Apache-2.0).
- The dataset COCO 2017 (cocodataset.org; Lin et al., "Microsoft COCO:
  Common Objects in Context", 2014): the images and the labels of the
  dataset cup and bottle. The annotations have the licence CC BY 4.0. Each
  image keeps the licence of its author, so the images are not in this
  repository.
- Chapter 12 "Benchmarking" of "Machine Learning Systems"
  (CC BY-NC-SA 4.0): the measurement rules of Part D.
- The package `ultralytics` and the model YOLO11n (Ultralytics, AGPL-3.0).

The dataset selection, the three tasks of the notebook, the comparison with
the pre-trained model, the training script, the benchmark script, and the
accuracy table of the exported files are new work of this course.
