# Test notes: Day 7 lab

This file has two parts. Part 1 lists the code that nobody tested on
hardware. Part 2 is the checklist for the instructor.

## 1. Code status

| File | State | Source | Change |
|---|---|---|---|
| `pi/classify_image.py`, `solutions/pi/classify_image.py` | changed | The function `image_classification()` of the kit lab "Image Classification" for the Raspberry Pi | New: the command line, the input for a `float32` file and for an `int8` file, the input order channel, height, width, the thread setting, and the latency output. The student version has no body in the function `dequantize_and_softmax` (Task B1). Tested on the work computer. Not tested on a Raspberry Pi. |
| `pi/classify_camera.py` | changed | The script `IMG_CLASS/python_scripts/capture_image.py` of EdgeML-with-Raspberry-Pi | New: the camera stays open for more than one photo, and each photo goes to the classifier. The logic was tested on the work computer with a replacement for the package `picamera2`. Not tested with a camera. |
| `pi/bench.py`, `solutions/pi/bench.py` | new | The method of Parts 2 and 3 of the lecture | The student version has no body in the function `median_latency_ms` (Task D1). Tested on the work computer. Not tested on a Raspberry Pi. |
| `export_inspect.ipynb`, `solutions/export_inspect.ipynb` | new | The graph optimizations of chapters 11 and 13 of "Machine Learning Systems" | The two versions ran on the work computer from the first cell to the last cell. They need no board. |
| `models/mobilenet_v2_1.0_224_quant.tflite`, `models/labels.txt` | copied with no change | The folder `IMG_CLASS/models` of EdgeML-with-Raspberry-Pi | none |
| `models/mnv2_int8.tflite` | new | MobileNetV2 of torchvision with the weights `IMAGENET1K_V1` | Converted with `litert-torch` 0.9.4, then quantized with `ai-edge-quantizer` 0.9.0 (`static_wi8_ai8`) and 100 training images of Imagenette |
| `models/mnv2_int8.onnx` | new | The same model | Exported with `torch.onnx.export`, then quantized with `quantize_static` of ONNX Runtime 1.23.2 (format QDQ, one range for each channel, range from a percentile) and the same 100 images |
| `models/imagenet_classes.txt` | new | The class names of the weights of torchvision | One name in each line |

Points that only a Raspberry Pi can confirm:

- All steps of Part A: the host name in the lab network, the script
  `~/HW-04/check_pi.sh`, and the two camera commands.
- The package versions of `~/tflite_env`. The scripts ran with
  `ai-edge-litert` 2.2.0, `onnxruntime` 1.23.2, `numpy` 2.2.6, and `pillow`
  12.3.0 on the work computer. A different version of `ai-edge-litert` can
  have a different default for the delegate.
- The import of `picamera2` in the environment, and the time of
  `capture_file()`.
- The two `int8` files on an Arm processor. The file `mnv2_int8.onnx` has
  `QuantizeLinear` and `DequantizeLinear` nodes. Nobody checked how ONNX
  Runtime runs them on Arm.
- All latencies. The lab gives no expected value for the board. The guide
  "Image Classification with EXECUTORCH" of EdgeML-with-Raspberry-Pi reports
  10.84 ms for MobileNetV2 in `float32` and 3.69 ms in `int8` on a
  Raspberry Pi 5, with ExecuTorch and XNNPACK.
- The download of the cat photo from Wikimedia Commons in the lab network.
- The time for each part.

Test of `requirements.txt` (work computer, 2026-10-02, Linux on x86, Python
3.10.12). In a new environment with `pip` 26.2.1, the install needed 141 s,
and `pip check` found no broken requirement. The environment has 2.3 GB. The
two notebooks ran in this environment. With the `pip` 22.0.2 of a new
environment, the install did not end in 8 minutes: so the README upgrades
`pip` first. Without the two version limits of `requirements.txt`, the
notebook packages install a version of `typing_extensions` that
`litert-torch` 0.9.4 does not accept.

Points that only a lab laptop can confirm:

- The install of `requirements.txt` on macOS and on Windows. The test was on
  Linux (x86) with Python 3.10.
- The notebook on Google Colab. Nobody ran it there.
- The time of the notebook on a laptop. On the work computer, the student
  version needs about 30 s and the solution about 50 s.

Test of the classification (work computer, 2026-10-02). The photo
`Cat03.jpg` of the kit lab, 4 threads:

| File | Input | First class | Probability | Second class |
|---|---|---|---|---|
| `mobilenet_v2_1.0_224_quant.tflite` | 1 x 224 x 224 x 3, `uint8` | tiger cat | 39 percent | Egyptian cat, 26 percent |
| `mnv2.tflite` (from the notebook) | 1 x 3 x 224 x 224, `float32` | Egyptian cat | 46 percent | tiger cat, 36 percent |
| `mnv2_int8.tflite` | 1 x 3 x 224 x 224, `int8` | Egyptian cat | 53 percent | tiger cat, 29 percent |

The kit lab reports `tiger cat` with 37 percent and `Egyptian cat` with 27
percent for the first file. The student version prints
`Task B1: not complete` and the raw values 173, 169, and 165 for the first
three classes.

Test of the accuracy of the two `int8` files (work computer, 2026-10-02):
500 validation images of Imagenette, 50 for each of the 10 classes. The
`float32` model: 77.4 percent. `mnv2_int8.tflite`: 75.2 percent.
`mnv2_int8.onnx`: 74.4 percent.

Test of `solutions/pi/bench.py` (work computer, 2026-10-02): an x86
processor with AVX2, cores 0 to 3, median of 50 runs in ms. These are not
values of the board.

| Runtime | File | 1 thread | 2 threads | 4 threads |
|---|---|---|---|---|
| LiteRT | `mnv2.tflite` | 11.41 | 6.40 | 3.47 |
| LiteRT | `mnv2_int8.tflite` | 15.32 | 8.42 | 4.35 |
| LiteRT | `mobilenet_v2_1.0_224_quant.tflite` | 19.30 | 10.47 | 5.64 |
| ONNX Runtime | `mnv2_static.onnx` | 11.33 | 6.67 | 3.59 |
| ONNX Runtime | `mnv2_dynamic.onnx` | 11.63 | 6.68 | 3.70 |
| ONNX Runtime | `mnv2_int8.onnx` | 12.37 | 6.74 | 3.97 |

The student version of `pi/bench.py` prints `Task D1: not complete` and
stops. The option `--levels` ran with the file `mnv2_unfused.onnx`. NCNN ran
in a second environment with the package `ncnn` 1.0.20260526 and the files
of the tool `pnnx`: 16.9, 9.7, and 6.1 ms. The lab does not make these files.

Test of the notebook (work computer, 2026-10-02, `torch` 2.13.0,
`torchvision` 0.28.0, `onnx` 1.23.1, `onnxscript` 0.7.2, `onnxruntime`
1.23.2, `litert-torch` 0.9.4):

| Check | Student version | Solution |
|---|---|---|
| Runs from the first cell to the last cell | yes | yes |
| Task 1 | not complete | complete |
| Task 2 | not complete | complete |
| Task 3 | not complete | complete |
| Stored output | none | yes |

## 2. Checklist for the instructor

Run the lab on the real hardware. Record the result here.

- Date of the test: YYYY-MM-DD
- Tool versions: see `Labs/VERSIONS.md`
- Board: Raspberry Pi 5 (8 GB), release of Raspberry Pi OS:

| Step | What to do | What to record | Result |
|---|---|---|---|
| 1 | Part A, steps 1 and 2 | Does `pi-NN.local` work? The lines of `check_pi.sh` with `FAIL`. | |
| 2 | Part A, step 3 | The camera name. Does `rpicam-jpeg` save a photo? | |
| 3 | In `~/tflite_env`: `pip list` | The versions of `ai-edge-litert`, `onnxruntime`, `numpy`, `pillow` | |
| 4 | Part B, steps 1 and 2 with `solutions/pi/classify_image.py` | The five classes, the load time, the first inference, the median | |
| 5 | Part B, step 4 | Does `picamera2` import? The capture time. The classes for three objects of the classroom. | |
| 6 | On a lab laptop: install `requirements.txt` in a new environment | The time and the size of the install. Errors. | |
| 7 | Run `solutions/export_inspect.ipynb` on the lab laptop | The run time. The line `Tasks complete: 1, 2, 3`. | |
| 8 | Open the five files of section 5 in Netron | Are the answers of `solutions/report_example.md` correct? | |
| 9 | Copy the model files, and run `solutions/pi/bench.py` two times | The complete table. The difference between the two runs. The temperature. | |
| 10 | `python pi/bench.py --levels` with `mnv2_unfused.onnx` | The latency of each level. Does the last level give a gain on Arm? | |
| 11 | `htop` during step 9 | The number of busy cores for 1, 2, and 4 threads | |

Time for each part:

| Part | Planned | Measured |
|---|---|---|
| A | 35 min | |
| B | 35 min | |
| C | 45 min | |
| D | 35 min | |

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 3. After the test

1. Write the measured table of the board in `solutions/report_example.md`
   and in the lab deck.
2. Keep the four files `mnv2.tflite`, `mnv2_static.onnx`,
   `mnv2_dynamic.onnx`, and `mnv2_unfused.onnx` of your run of the solution
   notebook in a shared
   folder for the students, or on the master card in
   `~/edgeai/day07/models/`. They are the fallback of the README.
3. If `picamera2` does not import in `~/tflite_env`, correct
   `Labs/hardware/HW-04/setup_pi.sh`.
4. If an `int8` file does not run on the board, write the error here, and
   remove the file from the list of `pi/bench.py`.
5. Write the package versions of the board and of the lab laptop in
   `Labs/VERSIONS.md`.
