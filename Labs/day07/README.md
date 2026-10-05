# Day 7 lab: inference runtimes on the Raspberry Pi


**Goal.** Your group has a runtime comparison on the Raspberry Pi 5: the
latency of one model for each runtime, thread count, and precision.

**Deliverable.** The latency table and the Decision Log in the file
`report.md`.

**Time.** 150 minutes of work, then 30 minutes for the check by the
instructor.

| Part | Content | Time |
|---|---|---|
| A | Setup: start the Raspberry Pi, connect with SSH, and test the camera | 35 min |
| B | First inference: MobileNetV2 with LiteRT on a test image and on the camera | 35 min |
| C | Export and inspect: one PyTorch model to ONNX and to LiteRT, and the graphs in Netron | 45 min |
| D | Measure: the latency for each runtime, thread count, and precision | 35 min |

## Hardware

| Item | Number for each group | Note |
|---|---|---|
| Raspberry Pi 5 (8 GB) with the active cooler | 1 | With the microSD card of the course. The card has the label of your group: `pi-NN`. |
| Power supply for the Raspberry Pi 5 | 1 | 27 W, USB-C |
| Camera Module 3 with its cable | 1 | Connected to the camera port. Do not connect or remove the cable when the power is on. |
| Laptop | 1 | In the same network as the Raspberry Pi (the Wi-Fi `edgeai-lab`) |

## Software

| Tool | Version | Note |
|---|---|---|
| Raspberry Pi OS (64-bit) with the environment `~/tflite_env` | the card of the course | `Labs/hardware/HW-04/` prepares the card. The environment has `ai-edge-litert`, `onnxruntime`, `numpy`, and `pillow`. The camera package `picamera2` comes from the operating system. |
| SSH client on the laptop | no version | The commands `ssh` and `scp` |
| Python on the laptop | 3.10 or later | For the notebook of Part C, in a new environment |
| The packages of `requirements.txt` | see `Labs/VERSIONS.md` | `torch`, `torchvision`, `onnx`, `onnxscript`, `onnxruntime`, `litert-torch`, `notebook`, `netron` |
| Netron | no version | The viewer for model files: `netron.app` in a browser, or the command `netron` of the package |

Make the environment for the notebook before the lab. It needs 2.3 GB on the
disk. Run the commands in the folder `Labs/day07/`:

```bash
python3 -m venv ~/day07_env
~/day07_env/bin/pip install --upgrade pip
~/day07_env/bin/pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
```

The second command is necessary. An old version of `pip` needs a very long
time to find the package versions. Use this environment only for this lab.
The package `litert-torch` needs its own version of `torch`.

Run all commands of this lab from the folder `Labs/day07/` on the laptop, and
from the folder `~/edgeai/day07/` on the Raspberry Pi. `NN` is the number of
your group.

## Files

| File | Content |
|---|---|
| `pi/classify_image.py` | Part B. Classifies one image with LiteRT. **Task B1** is in this file. |
| `pi/classify_camera.py` | Part B. Takes photos with the camera and classifies them. It has no task. |
| `export_inspect.ipynb` | Part C. The notebook for the laptop, with **Tasks 1, 2, and 3**. |
| `pi/bench.py` | Part D. Measures the latency of each model file. **Task D1** is in this file. |
| `models/mobilenet_v2_1.0_224_quant.tflite`, `models/labels.txt` | The model of the kit lab: MobileNetV2 in `uint8` with 1001 classes, 3 577 760 bytes |
| `models/mnv2_int8.tflite` | The model of Part C in `int8` for LiteRT, 4 107 968 bytes |
| `models/mnv2_int8.onnx` | The model of Part C in `int8` for ONNX Runtime, 4 025 896 bytes |
| `models/imagenet_classes.txt` | The 1000 class names for the model of Part C |
| `requirements.txt` | The packages for the notebook on the laptop |
| `report.md` | The report to hand in. Fill it during the lab. |
| `solutions/` | The complete notebook with its output, the two complete scripts, and an example report |
| `TEST_NOTES.md` | The code status and the test steps for the instructor |

The notebook writes its model files into the folder `models/`. Git ignores
these files.

The two `int8` files come from the model of Part C. The course made them with
a calibration on 100 training images of the dataset Imagenette, which has 10
classes of ImageNet. On 500 validation images of this dataset, the
`float32` model has an accuracy of 77.4 percent, the file `mnv2_int8.tflite`
has 75.2 percent, and the file `mnv2_int8.onnx` has 74.4 percent.

## Steps

Write each result in `report.md` when you get it.

### Part A: setup (35 min)

1. **Start and connect (10 min).** Check that the camera cable and the cable
   of the cooler are connected. Then connect the power supply. Wait for one
   minute. Connect from the laptop:

   ```bash
   ssh edge@pi-NN.local
   ```

   The instructor gives the password. If the name does not work, ask the
   instructor for the IP address of your board and use
   `ssh edge@IP_ADDRESS`.

2. **Check the system (10 min).** Run the check script of the course card:

   ```bash
   bash ~/HW-04/check_pi.sh
   ```

   Each line starts with `PASS`, `FAIL`, or `INFO`. Write in the report: the
   model, the release of the operating system, the Python version, the RAM,
   and the temperature. Tell the instructor if a line shows `FAIL`.

   Open a second terminal with a second SSH connection and start `htop`.
   Keep it open during the lab. It shows the load of each of the 4 cores.

3. **Test the camera (10 min).** List the camera, and take one photo:

   ```bash
   rpicam-hello --list-cameras
   rpicam-jpeg --output test.jpg --width 640 --height 480
   ```

   Copy the photo to the laptop and look at it. Run this command on the
   laptop:

   ```bash
   scp edge@pi-NN.local:~/test.jpg .
   ```

4. **Copy the lab folder (5 min).** On the laptop, in the folder `Labs/`:

   ```bash
   scp -r day07 edge@pi-NN.local:~/edgeai/
   ```

   On the Raspberry Pi, go to the folder and start the environment:

   ```bash
   cd ~/edgeai/day07
   source ~/tflite_env/bin/activate
   ```

   Do these two commands again in each new terminal.

### Part B: first inference (35 min)

1. **Get a test image (5 min).** The kit lab uses a photo of a cat from
   Wikimedia Commons (author: Fir0002, licence GFDL 1.2). The photo is not in
   this repository. Download it on the Raspberry Pi:

   ```bash
   mkdir -p images
   wget -P images https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg
   ```

2. **Run the model (10 min).** The model is MobileNetV2 in the `uint8` file
   of the kit lab:

   ```bash
   python pi/classify_image.py images/Cat03.jpg
   ```

   You see the shape and the type of the input, the number of outputs, the
   load time, the time of the first inference, and the median time of the
   next runs. Write these values in the report. You also see the line
   `Task B1: not complete`, and the five classes with the largest raw output
   values.

3. **Task B1 (10 min).** The raw outputs are integers. Open
   `pi/classify_image.py` with `nano` on the Raspberry Pi, and complete the
   function `dequantize_and_softmax` at the mark `TODO (student)`. Use the
   mapping of Day 4: the real value is `(integer - zero_point) * scale`.
   Run the script again. You see the line `Task B1: complete`, and a
   probability for each of the five classes. Write the five lines in the
   report.

   On the work computer of the course, the first class of the cat photo is
   `tiger cat` with 39 percent.

4. **Use the camera (10 min).** Point the camera at an object of the
   classroom: a keyboard, a mouse, a cup, a bottle, a backpack. Run:

   ```bash
   python pi/classify_camera.py --count 3 --interval 3
   ```

   The script saves each photo as `capture_N.jpg`, and prints three classes
   for each photo. Write in the report: the object, the first class, and the
   median latency. Copy one photo to the laptop with `scp` and look at it.

   Then run the cat photo with one thread, and compare with the default of
   four threads:

   ```bash
   python pi/classify_image.py images/Cat03.jpg --threads 1
   ```

### Part C: export and inspect (45 min)

Work on the laptop. Start the notebook:

```bash
~/day07_env/bin/jupyter notebook export_inspect.ipynb
```

Run the cells in order. The notebook has the detailed instructions.

| Section of the notebook | Content | Time |
|---|---|---|
| 0 and 1 | Setup, and the layers of the PyTorch model | 3 min |
| 2 | **Task 1:** export to ONNX with a static shape | 7 min |
| 3 | **Task 2:** export with a dynamic batch size, and a comparison of the two files | 8 min |
| 4 | Export to LiteRT, and the operators of the file | 5 min |
| 5 | The graph in ONNX Runtime for each optimization level, and the files in Netron | 12 min |
| 6 | **Task 3:** fold a batch normalization into a convolution by hand | 7 min |
| 7 and 8 | The same result in each runtime, and the files for the Raspberry Pi | 3 min |

In section 5, open the files in Netron and answer the five questions of the
report. To open a file: drag it into the page `netron.app`, or run
`~/day07_env/bin/netron models/mnv2_unfused.onnx`.

At the end, copy four model files to the Raspberry Pi. Run this command on
the laptop:

```bash
scp models/mnv2.tflite models/mnv2_static.onnx models/mnv2_dynamic.onnx models/mnv2_unfused.onnx edge@pi-NN.local:~/edgeai/day07/models/
```

### Part D: measure (35 min)

Work on the Raspberry Pi, in the folder `~/edgeai/day07/` with the
environment `~/tflite_env`.

1. **Predict (5 min).** Before you measure, write your prediction for each
   question of Part D in the report. Give a reason from the lecture.

2. **Task D1 (5 min).** Open `pi/bench.py` with `nano`, and complete the
   function `median_latency_ms` at the mark `TODO (student)`: some calls to
   warm up with no measurement, then one time for each call, then the median.

3. **Measure (10 min).** Close each other program on the Raspberry Pi, but
   keep `htop` open in its terminal. Run:

   ```bash
   python pi/bench.py
   ```

   The script prints one line for each model file and thread count: the
   runtime, the file, the precision, the number of threads, the load time,
   and the median latency of 50 runs. It also writes the file `results.csv`.
   Look at `htop` during the run: how many cores are busy for each thread
   count?

   Run the script a second time. Compare the two runs: the difference is the
   noise of your measurement.

4. **Fill the table (10 min).** Write the latency table in the report. Then
   calculate the three ratios of the report: the gain from 1 thread to 4
   threads, the gain from `float32` to `int8`, and the ratio between the two
   runtimes.

5. **Compare and decide (5 min).** Compare the results with your predictions
   and with the numbers of the lecture, which are from an x86 processor.
   Write the Decision Log.

If you have time: measure the optimization levels of ONNX Runtime on the
Raspberry Pi. The file `models/mnv2_unfused.onnx` of Part C is on the board.
Run `python pi/bench.py --levels`. The
lecture measured a factor of 2.2 for the last level on an x86 processor. Is
the factor the same on the Raspberry Pi?

## Check criterion

The instructor checks this at the end of the lab:

- [ ] `python pi/classify_image.py images/Cat03.jpg` prints
      `Task B1: complete` and a cat class as the first class.
- [ ] The notebook prints `Tasks complete: 1, 2, 3` in its last cell.
- [ ] `python pi/bench.py` prints `Task D1: complete`.
- [ ] The latency table of the report has two runtimes or more, two thread
      counts or more, and two precisions or more.
- [ ] The report has the five answers of the Netron questions.
- [ ] The report has a prediction and a result for each question of Part D.
- [ ] The Decision Log gives numbers and names one trade-off.

## Decision Log

Write about 100 words. State one design decision, give your measured numbers,
and name the trade-off.

Question of this lab: a product with a Raspberry Pi 5 and a camera must
classify 10 images in each second. The same program also reads the camera and
sends each result over the network. Which runtime, which precision, and how
many threads do you select for the model? Use your latency table. The
`int8` file loses about 2 points of accuracy against the `float32` file.

## If a part does not work

| Problem | Fallback |
|---|---|
| The name `pi-NN.local` does not work | Use the IP address that the instructor gives |
| The camera gives no photo | Do Part B with the cat photo only, and write this in the report. Tell the instructor. |
| The Raspberry Pi has no internet connection for the cat photo | Download the photo on the laptop and copy it with `scp`, or use a photo of the camera |
| Task B1 or Task D1 is not complete in time | Use the file of the folder `solutions/pi/`, and write this in the report |
| The environment for the notebook does not install | Work with a second group on one laptop, or use the solution notebook to read the results. The instructor gives the exported model files. |
| A task of the notebook is not complete in time | Use the cell of `solutions/export_inspect.ipynb`, and write this in the report |
| The exported files are not on the Raspberry Pi | `pi/bench.py` measures the files that it finds. The two `int8` files and the kit model are in the folder `models/`. The instructor gives the `float32` files. |

## Common problems

| Problem | Cause | Fix |
|---|---|---|
| `ssh: Could not resolve hostname pi-NN.local` | The laptop is in a different network, or it cannot find names of the type `.local` | Join the Wi-Fi `edgeai-lab`. Use the IP address of the board. |
| `ModuleNotFoundError: No module named 'ai_edge_litert'` | The environment is not active | `source ~/tflite_env/bin/activate` |
| `ERROR: the package picamera2 is not available` | The script does not run on the Raspberry Pi, or the environment cannot see the system packages | Run it on the Raspberry Pi. Tell the instructor if it fails there. |
| `rpicam-hello` prints `No cameras available` | The camera cable is loose or in the wrong direction | Shut down, remove the power, connect the cable again |
| `Cannot set tensor: Dimension mismatch` | The input has the wrong order of the dimensions | Use the function `preprocess` of `pi/classify_image.py`: it reads the order from the model |
| The export in the notebook stops with a message about `typing_extensions` or `jupyter_client` | The packages are not the versions of `requirements.txt` | Make a new environment and install only `requirements.txt` |
| ONNX Runtime prints `Got: 2 Expected: 1` | The static file got a batch of 2 images | This is the result of section 3 of the notebook. Use the dynamic file for a batch. |
| The latency changes much between two runs | A second program uses the cores, or the processor is hot | Close the other programs. Read the temperature with `vcgencmd measure_temp`. Wait for one minute and run again. |
| `pi/bench.py` prints `not found` for a file | The file is not in the folder `models/` on the Raspberry Pi | Copy it with the `scp` command of Part C |

## Credits

This lab adapts material from these sources:

- The chapters "Setup" and "Image Classification" of the Raspberry Pi kit
  labs in "Machine Learning Systems" by Vijay Janapa Reddi and contributors,
  written by Marcelo Rovai (mlsysbook.ai, CC BY-NC-SA 4.0): the SSH and
  camera commands, the test image, and the steps of the first inference
  with MobileNetV2.
- The repository EdgeML-with-Raspberry-Pi by Marcelo Rovai
  (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0): the model file
  `mobilenet_v2_1.0_224_quant.tflite` with its labels (a model of the
  TensorFlow authors, Apache-2.0), and the camera script for one photo.
- Chapters 11 "Hardware Acceleration" and 13 "Model Serving" of "Machine
  Learning Systems" (CC BY-NC-SA 4.0): the graph optimizations of Part C.
- The model MobileNetV2 of torchvision with its ImageNet weights
  (BSD-3-Clause). The two `int8` files of the folder `models/` are
  quantized copies of this model.

The export notebook, the benchmark script, the command line of the
classification script, and the two `int8` files are new work of this course.
