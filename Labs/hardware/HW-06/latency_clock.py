#!/usr/bin/env python3
"""Measure the end-to-end latency of a video stream with a clock on the screen.

Runs on: the laptop that shows the stream. Needs a screen.
Needs:   opencv-python (the version with windows) and numpy.

Method:
  1. This script shows a window with two parts. The left part is a clock
     with milliseconds. The right part is the video stream.
  2. Point the camera at the clock.
  3. The stream then shows the clock of the past. The difference between
     the two clocks is the end-to-end latency: camera, encoder, network,
     decoder, and display.
  4. Press "s". The script saves the window as an image. Read the two
     clock values from the image and subtract them.

Use:
    python3 latency_clock.py rtsp://pi-07.local:8554/cam
    Keys: s = save the window, q = stop

Take 10 images for each setting. Report the median and the range.

Limits of the method:
  - The laptop screen shows a new image each 16.7 ms (60 Hz). The camera
    makes a new frame each 33 ms (30 frames per second). One reading can
    have an error of about 50 ms. Use the median of 10 readings.
  - The clock digits can be unsharp in the stream when the exposure time
    is long. Use more light.

Test with no camera and no screen (the script saves 3 images and stops):
    python3 latency_clock.py rtsp://localhost:8554/test --no-window --count 3

"""

import argparse
import sys
import time

import numpy as np

from rtsp_reader import LatestFrameReader, cv2

CLOCK_WIDTH = 640
HEIGHT = 480


def clock_text(now):
    """Return the time of day as HH:MM:SS.mmm."""
    local = time.localtime(now)
    return "%02d:%02d:%02d.%03d" % (local.tm_hour, local.tm_min, local.tm_sec,
                                    int((now % 1) * 1000))


def clock_panel(text):
    """Return an image with the clock text in large white digits."""
    panel = np.zeros((HEIGHT, CLOCK_WIDTH, 3), dtype=np.uint8)
    cv2.putText(panel, "clock now", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                (160, 160, 160), 2, cv2.LINE_AA)
    cv2.putText(panel, text, (20, 270), cv2.FONT_HERSHEY_SIMPLEX, 2.6,
                (255, 255, 255), 6, cv2.LINE_AA)
    return panel


def stream_panel(frame):
    """Return the stream frame with the height of the window."""
    if frame is None:
        panel = np.zeros((HEIGHT, CLOCK_WIDTH, 3), dtype=np.uint8)
        cv2.putText(panel, "no frame yet", (20, 240), cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (0, 0, 255), 3, cv2.LINE_AA)
        return panel
    scale = HEIGHT / frame.shape[0]
    return cv2.resize(frame, (int(frame.shape[1] * scale), HEIGHT))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url", help="for example rtsp://pi-07.local:8554/cam")
    parser.add_argument("--prefix", default="latency",
                        help="start of the image file names (default: latency)")
    parser.add_argument("--no-window", action="store_true",
                        help="save images with no window (for a test)")
    parser.add_argument("--count", type=int, default=3,
                        help="number of images for --no-window (default: 3)")
    args = parser.parse_args()

    reader = LatestFrameReader(args.url)
    saved = 0
    next_save = time.monotonic() + 2.0
    try:
        while reader.running:
            frame, _, _ = reader.read()
            now = time.time()
            text = clock_text(now)
            window = np.hstack([clock_panel(text), stream_panel(frame)])

            save = False
            if args.no_window:
                if frame is not None and time.monotonic() >= next_save:
                    save = True
                    next_save = time.monotonic() + 1.0
                else:
                    time.sleep(0.005)
            else:
                cv2.imshow("latency_clock: s = save, q = stop", window)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                save = key == ord("s")

            if save:
                saved += 1
                name = "%s_%02d.png" % (args.prefix, saved)
                cv2.imwrite(name, window)
                print("Saved %s (clock now: %s)" % (name, text), flush=True)
                if args.no_window and saved >= args.count:
                    break
    except KeyboardInterrupt:
        pass
    finally:
        reader.close()
        if not args.no_window:
            cv2.destroyAllWindows()

    print("Images saved: %d. Read the two clock values of each image." % saved)
    return 0 if saved > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
