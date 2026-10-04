#!/usr/bin/env python3
"""Day 8 lab, Part A: an SSD model on one image.

Runs on: the Raspberry Pi 5, in the environment ~/yolo, from the folder
         ~/edgeai/day08/. It also runs on a laptop with the packages
         ai-edge-litert, numpy, and pillow.
Use:     python pi/detect_ssd.py images/bus.jpg
         python pi/detect_ssd.py images/desk.jpg --score 0.3
Output:  the input and the outputs of the model, the times, the list of
         detections, and the file ssd_result.jpg with the boxes.

Hardware status: not tested on hardware (prepared on 2026-10-02).

Credits: the steps follow the notebook SSD_MobileNetV1.ipynb of
"EdgeML with Raspberry Pi" by Marcelo Rovai
(github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0) and the kit lab
"Object Detection" of "Machine Learning Systems" (mlsysbook.ai,
CC BY-NC-SA 4.0). The model file is SSD MobileNet V1 of the TensorFlow
authors (Apache-2.0). The command line, the time measurement, and the
function to_pixel_boxes are new code of this course.
"""
import argparse
import os
import statistics
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

try:
    from ai_edge_litert.interpreter import Interpreter
except ImportError:
    sys.exit("ERROR: the package ai-edge-litert is not available. "
             "Start the environment: source ~/yolo/bin/activate")

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.basename(LAB) == "solutions":
    LAB = os.path.dirname(LAB)
MODEL = os.path.join(LAB, "models", "ssd-mobilenet-v1-tflite-default-v1.tflite")
LABELS = os.path.join(LAB, "models", "coco_labels.txt")


def to_pixel_boxes(boxes, classes, scores, count, width, height, threshold):
    """Return the detections of an SSD model as a list for the image.

    boxes:   array (N, 4). Each row is ymin, xmin, ymax, xmax, from 0 to 1.
    classes: array (N,) with the class number of each box.
    scores:  array (N,) with the score of each box, from 0 to 1.
    count:   the number of valid rows.
    width, height: the size of the original image in pixels.
    threshold: keep a box only if its score is the threshold or more.

    Return a list. Each element is the tuple
    (class number as int, score as float, x1, y1, x2, y2), where x1, y1 is
    the top left corner in pixels and x2, y2 is the bottom right corner.
    """
    # TODO (student), Task A1: three steps for each of the first count rows.
    # 1. Skip the row if its score is below the threshold.
    # 2. Read ymin, xmin, ymax, xmax. Multiply the two x values by the width
    #    and the two y values by the height.
    # 3. Add the tuple (int(class), float(score), x1, y1, x2, y2) to the list.
    return None


def check_task_a1():
    """Test to_pixel_boxes with two boxes of a known result."""
    boxes = np.array([[0.25, 0.10, 0.75, 0.50], [0.0, 0.0, 1.0, 1.0]], dtype=np.float32)
    result = to_pixel_boxes(boxes, np.array([16.0, 0.0]), np.array([0.9, 0.2]), 2, 200, 100, 0.5)
    if not isinstance(result, list) or len(result) != 1 or len(result[0]) != 6:
        return False
    return (result[0][0] == 16 and abs(result[0][1] - 0.9) < 1e-6
            and np.allclose(result[0][2:], [20.0, 25.0, 100.0, 75.0], atol=1e-3))


def load_labels(path):
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle]


def main():
    parser = argparse.ArgumentParser(description="Run the SSD model on one image.")
    parser.add_argument("image", help="the image file")
    parser.add_argument("--score", type=float, default=0.5, help="score threshold (default 0.5)")
    parser.add_argument("--threads", type=int, default=4, help="number of threads (default 4)")
    parser.add_argument("--runs", type=int, default=20, help="runs for the median (default 20)")
    parser.add_argument("--output", default="ssd_result.jpg", help="image file with the boxes")
    args = parser.parse_args()

    labels = load_labels(LABELS)
    start = time.perf_counter()
    interpreter = Interpreter(model_path=MODEL, num_threads=args.threads)
    interpreter.allocate_tensors()
    load_ms = (time.perf_counter() - start) * 1000
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()

    print("Model:  %s (%d bytes)" % (os.path.basename(MODEL), os.path.getsize(MODEL)))
    print("Input:  shape %s, type %s" % (
        [int(v) for v in input_details["shape"]], input_details["dtype"].__name__))
    for k, detail in enumerate(output_details):
        print("Output %d: shape %s, type %s" % (
            k, [int(v) for v in detail["shape"]], detail["dtype"].__name__))

    # Pre-processing (kit lab): resize the complete image to the input size
    # of the model. The model takes the integers 0 to 255.
    original = Image.open(args.image).convert("RGB")
    side_h, side_w = int(input_details["shape"][1]), int(input_details["shape"][2])
    start = time.perf_counter()
    resized = original.resize((side_w, side_h))
    data = np.expand_dims(np.array(resized, dtype=np.uint8), axis=0)
    pre_ms = (time.perf_counter() - start) * 1000

    times = []
    for _ in range(args.runs + 1):
        start = time.perf_counter()
        interpreter.set_tensor(input_details["index"], data)
        interpreter.invoke()
        times.append((time.perf_counter() - start) * 1000)

    # The suppression is the last operator of the file. The four outputs are
    # the final list: boxes, classes, scores, and the number of detections.
    boxes = interpreter.get_tensor(output_details[0]["index"])[0]
    classes = interpreter.get_tensor(output_details[1]["index"])[0]
    scores = interpreter.get_tensor(output_details[2]["index"])[0]
    count = int(interpreter.get_tensor(output_details[3]["index"])[0])

    print("Image:  %s, %d x %d pixels" % (args.image, original.width, original.height))
    print("Load: %.1f ms. Pre-processing: %.1f ms. Threads: %d." % (load_ms, pre_ms, args.threads))
    print("First inference: %.1f ms. Median of the next %d runs: %.1f ms."
          % (times[0], args.runs, statistics.median(times[1:])))
    print("Rows in the output: %d. Rows with a score of %.2f or more: %d."
          % (count, args.score, int(np.sum(scores[:count] >= args.score))))

    if not check_task_a1():
        print("Task A1: not complete")
        print("Raw output, first 3 rows (ymin, xmin, ymax, xmax from 0 to 1, class, score):")
        for i in range(min(3, count)):
            print("  %s  class %d  score %.2f" % (np.round(boxes[i], 3), int(classes[i]), scores[i]))
        return
    print("Task A1: complete")

    detections = to_pixel_boxes(boxes, classes, scores, count,
                                original.width, original.height, args.score)
    draw = ImageDraw.Draw(original)
    line = max(2, original.width // 300)
    print("Detections: %d" % len(detections))
    for class_id, score, x1, y1, x2, y2 in detections:
        name = labels[class_id] if class_id < len(labels) else "class %d" % class_id
        print("  %-14s %.2f   box %4.0f %4.0f %4.0f %4.0f" % (name, score, x1, y1, x2, y2))
        draw.rectangle([x1, y1, x2, y2], outline="red", width=line)
        draw.text((x1 + 4, max(0, y1 - 12)), "%s %.2f" % (name, score), fill="red")
    original.save(args.output)
    print("Saved: %s" % args.output)


if __name__ == "__main__":
    main()
