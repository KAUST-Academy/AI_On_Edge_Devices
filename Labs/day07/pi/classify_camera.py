#!/usr/bin/env python3
"""Day 7 lab, Part B: take photos with the camera and classify them.

Run on: the Raspberry Pi 5 with the Camera Module 3, in the environment
        ~/tflite_env. The package picamera2 comes from the operating system.
Use:    python pi/classify_camera.py
        python pi/classify_camera.py --count 5 --interval 2
        python pi/classify_camera.py --model models/mnv2.tflite

The script saves each photo as capture_N.jpg in the current folder. Copy a
photo to the laptop to look at it:
    scp edge@pi-NN.local:~/edgeai/day07/capture_1.jpg .
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import classify_image


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--model", default=os.path.join(
        classify_image.MODELS, "mobilenet_v2_1.0_224_quant.tflite"))
    parser.add_argument("--count", type=int, default=1, help="number of photos")
    parser.add_argument("--interval", type=float, default=2.0,
                        help="seconds between two photos")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()

    try:
        from picamera2 import Picamera2
    except ImportError:
        print("ERROR: the package picamera2 is not available. Run this script "
              "on the Raspberry Pi, in the environment ~/tflite_env.")
        sys.exit(1)

    # Initialize and configure the camera (from capture_image.py).
    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    # Wait for the camera to warm up.
    time.sleep(2)

    try:
        for number in range(1, args.count + 1):
            path = "capture_%d.jpg" % number
            start = time.perf_counter()
            picam2.capture_file(path)
            capture_ms = 1000 * (time.perf_counter() - start)
            print("\nPhoto %d of %d saved as %s (capture: %.0f ms)"
                  % (number, args.count, path, capture_ms))
            result = classify_image.classify(path, args.model, args.threads, runs=5)
            labels = classify_image.labels_for(args.model, len(result["raw"]))
            classify_image.print_result(result, labels, top=3)
            if number < args.count:
                time.sleep(args.interval)
    finally:
        picam2.stop()


if __name__ == "__main__":
    main()
