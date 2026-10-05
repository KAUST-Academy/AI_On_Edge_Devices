# Test notes: Day 7 lab

## 1. Checklist for the instructor

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

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

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
