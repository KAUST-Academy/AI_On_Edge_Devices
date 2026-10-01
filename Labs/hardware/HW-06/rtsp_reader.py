#!/usr/bin/env python3
"""Read an RTSP stream with OpenCV and report the frame rate.

Runs on: the laptop or the Raspberry Pi.
Needs:   opencv-python (or opencv-python-headless) and numpy.

Use:
    python3 rtsp_reader.py rtsp://pi-07.local:8554/cam
    python3 rtsp_reader.py rtsp://pi-07.local:8554/cam --show
    python3 rtsp_reader.py rtsp://pi-07.local:8554/cam --seconds 20 --save frame.jpg

The class LatestFrameReader reads the stream in a thread and keeps only the
newest frame. The main loop then never works on an old frame. Without this,
a slow model fills the buffer of OpenCV and the delay grows.

Put your model in the function process().

Hardware status: tested on a Linux laptop with a synthetic stream.
Not tested with the Raspberry Pi camera (prepared on 2026-10-01).
"""

import argparse
import os
import sys
import threading
import time

# The transport must be set before OpenCV opens the stream.
# "tcp" loses no packet. "udp" has less delay but can lose packets on Wi-Fi.
TRANSPORT = os.environ.get("RTSP_TRANSPORT", "tcp")
os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS",
                      "rtsp_transport;%s|fflags;nobuffer|flags;low_delay" % TRANSPORT)

import cv2  # noqa: E402  (after the environment variable)


class LatestFrameReader:
    """Read a video stream in a thread. Keep only the newest frame."""

    def __init__(self, url):
        self.url = url
        self.capture = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        if not self.capture.isOpened():
            raise OSError("cannot open the stream %s" % url)
        self.lock = threading.Lock()
        self.frame = None
        self.frame_time = 0.0     # time.monotonic() when the frame arrived
        self.received = 0         # number of frames from the stream
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self):
        while self.running:
            ok, frame = self.capture.read()
            if not ok:
                self.running = False
                break
            with self.lock:
                self.frame = frame
                self.frame_time = time.monotonic()
                self.received += 1

    def read(self):
        """Return (frame, arrival time, frame number). The frame can be None."""
        with self.lock:
            return self.frame, self.frame_time, self.received

    def close(self):
        self.running = False
        self.thread.join(timeout=2)
        self.capture.release()


def process(frame):
    """Do the work on one frame. Replace this function with your model.

    Example for the Day 8 detector:
        results = model(frame, verbose=False)
        return results[0].plot()
    """
    return frame


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url", help="for example rtsp://pi-07.local:8554/cam")
    parser.add_argument("--seconds", type=float, default=0,
                        help="stop after this time (default: run until Ctrl-C)")
    parser.add_argument("--show", action="store_true",
                        help="show the frames in a window (press q to stop)")
    parser.add_argument("--save", help="write the last frame to this file")
    args = parser.parse_args()

    reader = LatestFrameReader(args.url)
    print("Stream open: %s (transport %s)" % (args.url, TRANSPORT))

    start = time.monotonic()
    last_report = start
    last_number = 0
    processed = 0
    processed_at_report = 0
    received_at_report = 0
    frame = None

    try:
        while reader.running:
            now = time.monotonic()
            if args.seconds and now - start >= args.seconds:
                break

            frame, _, number = reader.read()
            if frame is None or number == last_number:
                time.sleep(0.001)          # no new frame yet
                continue
            last_number = number

            output = process(frame)
            processed += 1

            if args.show:
                cv2.imshow("rtsp_reader", output)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            if now - last_report >= 2.0:
                span = now - last_report
                print("%dx%d  stream %.1f frames/s  processed %.1f frames/s  "
                      "skipped %d" % (
                          frame.shape[1], frame.shape[0],
                          (number - received_at_report) / span,
                          (processed - processed_at_report) / span,
                          (number - received_at_report)
                          - (processed - processed_at_report)), flush=True)
                last_report = now
                received_at_report = number
                processed_at_report = processed
    except KeyboardInterrupt:
        pass
    finally:
        reader.close()
        if args.show:
            cv2.destroyAllWindows()

    total = time.monotonic() - start
    print("Total: %d frames received, %d processed, %.1f s" % (
        reader.received, processed, total))
    if args.save and frame is not None:
        cv2.imwrite(args.save, frame)
        print("Last frame saved: %s" % args.save)
    return 0 if reader.received > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
