# Test notes: Day 8 lab

## 1. Checklist for the instructor

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

Problems found:

| Problem | Fix | File to correct |
|---|---|---|

## 2. After the test

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
