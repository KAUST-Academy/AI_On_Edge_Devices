#!/usr/bin/env python3
"""Day 8 lab, Part D: the frame rate of each exported model.

Runs on: the Raspberry Pi 5 with the camera, in the environment ~/yolo, from
         the folder ~/edgeai/day08/.
Use:     python pi/bench_detect.py
         python pi/bench_detect.py --frames 50
         python pi/bench_detect.py --source images/desk.jpg
Output:  one line for each model file of the folder models/, and the file
         results.csv.

For each model, the script takes frames from the camera and runs the
complete pipeline of the lecture: capture, pre-processing, inference, and
post-processing. It gives the median time of each step and the frame rate.
It does not draw the boxes and it sends no image.

Credits: the method follows Part 3 of the Day 8 lecture and the
measurement rules of chapter 12 "Benchmarking" of "Machine Learning
Systems" by Vijay Janapa Reddi and contributors (mlsysbook.ai,
CC BY-NC-SA 4.0). The package ultralytics has the licence AGPL-3.0. The
script is new code of this course.
"""
import argparse
import csv
import os
import statistics
import sys
import time

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.basename(LAB) == "solutions":
    LAB = os.path.dirname(LAB)
sys.path.insert(0, os.path.join(LAB, "pi"))

from detector import describe, detect, load_model, open_source, set_litert_threads, temperature

# The files that the notebook of Parts B and C makes.
MODELS = [
    "cupbottle_320_ncnn_model",
    "cupbottle_320.tflite",
    "cupbottle_320_int8.tflite",
    "cupbottle_640_ncnn_model",
    "cupbottle_640.tflite",
    "cupbottle_640_int8.tflite",
]
STEPS = ["capture", "preprocess", "inference", "postprocess"]


def frame_rate(steps_ms):
    """Return the number of frames in each second.

    steps_ms: a list with the time in ms of each step of one frame: capture,
    pre-processing, inference, and post-processing. The program does the
    steps one after the other, so one frame needs the sum of the times.
    """
    # TODO (student), Task D1: return the frame rate as a float.
    # One second has 1000 ms.
    return None


def check_task_d1():
    """Test frame_rate with the example of the lecture: 15, 300, and 10 ms."""
    value = frame_rate([5.0, 10.0, 300.0, 10.0])
    return isinstance(value, float) and abs(value - 1000.0 / 325.0) < 1e-9


def measure(path, source, frames, warmup, conf):
    """Return the median time of each step in ms for one model."""
    runtime, precision, imgsz = describe(path)
    imgsz = imgsz or 640        # a name with no size, for example yolo11n.pt
    start = time.perf_counter()
    model = load_model(path)
    for _ in range(warmup):
        detect(model, source.read(), imgsz, conf)
    load_s = time.perf_counter() - start
    rows = {step: [] for step in STEPS}
    objects = 0
    for _ in range(frames):
        start = time.perf_counter()
        frame = source.read()
        rows["capture"].append((time.perf_counter() - start) * 1000)
        result = detect(model, frame, imgsz, conf)
        for step in STEPS[1:]:
            rows[step].append(result.speed[step])
        objects = len(result.boxes)
    medians = [statistics.median(rows[step]) for step in STEPS]
    return runtime, precision, imgsz, load_s, medians, objects


def main():
    parser = argparse.ArgumentParser(description="Measure the frame rate of each model.")
    parser.add_argument("--models", nargs="*", default=None,
                        help="model files or folders (default: the six files of the lab)")
    parser.add_argument("--source", default="camera",
                        help='"camera", an image file, or a folder with images (default camera)')
    parser.add_argument("--width", type=int, default=640, help="width of a frame (default 640)")
    parser.add_argument("--height", type=int, default=480, help="height of a frame (default 480)")
    parser.add_argument("--frames", type=int, default=30, help="measured frames (default 30)")
    parser.add_argument("--warmup", type=int, default=3, help="frames with no measurement (default 3)")
    parser.add_argument("--threads", type=int, default=4, help="threads for a LiteRT file (default 4)")
    parser.add_argument("--conf", type=float, default=0.25, help="score threshold (default 0.25)")
    parser.add_argument("--output", default="results.csv", help="CSV file with the results")
    args = parser.parse_args()

    if not check_task_d1():
        print("Task D1: not complete")
        print("Complete the function frame_rate in pi/bench_detect.py, then run the script again.")
        return
    print("Task D1: complete")

    paths = args.models or [os.path.join(LAB, "models", name) for name in MODELS]
    if not set_litert_threads(args.threads):
        print("NOTE: cannot set the threads for LiteRT. The package uses its default.")
    source = open_source(args.source, args.width, args.height)
    degrees = temperature()
    print("Source: %s, frames of %d x %d pixels. Measured frames: %d. Threads for LiteRT: %d."
          % (source.name, args.width, args.height, args.frames, args.threads))
    if degrees is not None:
        print("Temperature at the start: %.1f C" % degrees)
    print()
    print("%-28s %-7s %-8s %4s | %7s %7s %9s %7s | %8s | %s"
          % ("model", "runtime", "type", "size", "capture", "pre", "inference", "post",
             "frames/s", "objects"))
    results = []
    try:
        for path in paths:
            name = os.path.basename(os.path.normpath(path))
            if not os.path.exists(path):
                print("%-28s not found" % name)
                continue
            runtime, precision, imgsz, load_s, medians, objects = measure(
                path, source, args.frames, args.warmup, args.conf)
            fps = frame_rate(medians)
            print("%-28s %-7s %-8s %4d | %7.1f %7.1f %9.1f %7.1f | %8.2f | %d"
                  % (name, runtime, precision, imgsz, medians[0], medians[1], medians[2],
                     medians[3], fps, objects), flush=True)
            results.append([name, runtime, precision, imgsz] + ["%.2f" % v for v in medians]
                           + ["%.2f" % fps, objects, "%.1f" % load_s])
    finally:
        source.close()
    degrees = temperature()
    if degrees is not None:
        print("\nTemperature at the end: %.1f C" % degrees)
    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "runtime", "precision", "imgsz", "capture_ms", "preprocess_ms",
                         "inference_ms", "postprocess_ms", "frames_per_second",
                         "objects_last_frame", "load_s"])
        writer.writerows(results)
    print("Saved: %s (%d models). Times in ms: the median of %d frames."
          % (args.output, len(results), args.frames))


if __name__ == "__main__":
    main()
