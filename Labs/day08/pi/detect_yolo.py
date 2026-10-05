#!/usr/bin/env python3
"""Day 8 lab, Parts A and C: a YOLO model on one image.

Runs on: the Raspberry Pi 5, in the environment ~/yolo, from the folder
         ~/edgeai/day08/. It also runs on the laptop.
Use:     python pi/detect_yolo.py images/bus.jpg
         python pi/detect_yolo.py images/bus.jpg --imgsz 320 --conf 0.5 --iou 0.9
         python pi/detect_yolo.py images/desk.jpg --model models/cupbottle_320_ncnn_model --imgsz 320
Output:  the times of the three steps, the list of detections, and the
         file yolo_result.jpg with the boxes.

The default model is yolo11n.pt, with the 80 classes of COCO. The package
downloads this file at the first run (5.4 MB) into the folder models/.
A model can be a PyTorch file (.pt), an NCNN folder, or a LiteRT file
(.tflite). An exported file has a fixed image size: give the same size
with --imgsz.

Credits: the steps follow the notebook
YOLO_Model_Prediction_with_Ultralytics.ipynb of "EdgeML with Raspberry Pi"
by Marcelo Rovai (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0) and
the kit lab "Object Detection" of "Machine Learning Systems" (mlsysbook.ai,
CC BY-NC-SA 4.0). The package ultralytics and its models have the licence
AGPL-3.0. The command line and the time measurement are new code of this
course.
"""
import argparse
import os
import statistics
import sys
import time

os.environ.setdefault("YOLO_VERBOSE", "False")      # no status lines of the package

try:
    from ultralytics import YOLO
except ImportError:
    sys.exit("ERROR: the package ultralytics is not available. "
             "Start the environment: source ~/yolo/bin/activate")

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.basename(LAB) == "solutions":
    LAB = os.path.dirname(LAB)


def main():
    parser = argparse.ArgumentParser(description="Run a YOLO model on one image.")
    parser.add_argument("image", help="the image file")
    parser.add_argument("--model", default=os.path.join(LAB, "models", "yolo11n.pt"),
                        help="model file or folder (default models/yolo11n.pt)")
    parser.add_argument("--imgsz", type=int, default=640, help="image size (default 640)")
    parser.add_argument("--conf", type=float, default=0.25, help="score threshold (default 0.25)")
    parser.add_argument("--iou", type=float, default=0.7,
                        help="IoU threshold of the suppression (default 0.7)")
    parser.add_argument("--runs", type=int, default=5, help="runs for the median (default 5)")
    parser.add_argument("--output", default="yolo_result.jpg", help="image file with the boxes")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        sys.exit("ERROR: the image %s does not exist." % args.image)
    os.makedirs(os.path.dirname(os.path.abspath(args.model)), exist_ok=True)

    start = time.perf_counter()
    model = YOLO(args.model, task="detect")
    load_ms = (time.perf_counter() - start) * 1000

    def run():
        start = time.perf_counter()
        result = model.predict(args.image, imgsz=args.imgsz, conf=args.conf, iou=args.iou,
                               save=False, verbose=False)[0]
        return result, (time.perf_counter() - start) * 1000

    result, first_ms = run()
    steps = {"preprocess": [], "inference": [], "postprocess": []}
    totals = []
    for _ in range(args.runs):
        result, total_ms = run()
        totals.append(total_ms)
        for key in steps:
            steps[key].append(result.speed[key])

    print("Model:  %s, %d classes" % (os.path.basename(os.path.normpath(args.model)), len(result.names)))
    print("Image:  %s, %d x %d pixels" % (args.image, result.orig_shape[1], result.orig_shape[0]))
    print("Thresholds: score %.2f, IoU %.2f. Image size: %d." % (args.conf, args.iou, args.imgsz))
    print("Load: %.0f ms. First run: %.0f ms." % (load_ms, first_ms))
    print("Median of the next %d runs, in ms:" % args.runs)
    print("  pre-processing %.1f   inference %.1f   post-processing %.1f   complete call %.1f"
          % (statistics.median(steps["preprocess"]), statistics.median(steps["inference"]),
             statistics.median(steps["postprocess"]), statistics.median(totals)))
    print("Detections: %d" % len(result.boxes))
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        print("  %-14s %.2f   box %4.0f %4.0f %4.0f %4.0f"
              % (result.names[int(box.cls)], float(box.conf), x1, y1, x2, y2))
    result.save(filename=args.output)
    print("Saved: %s" % args.output)


if __name__ == "__main__":
    main()
