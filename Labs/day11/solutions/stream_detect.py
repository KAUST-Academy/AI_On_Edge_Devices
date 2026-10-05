#!/usr/bin/env python3
"""Day 11 lab, Parts C and D: run the Day 8 detector on a network stream.

Runs on: the laptop (a central node), or the Raspberry Pi.
Needs:   opencv-python and numpy. With --model also the package ultralytics
         (the environment of the Day 8 lab) and the folder day08/pi of the
         Day 8 lab.

Use:
    python stream_detect.py rtsp://pi-NN.local:8554/cam --seconds 20
    python stream_detect.py rtsp://pi-NN.local:8554/cam --model yolo11n.pt --imgsz 320
    python stream_detect.py http://192.168.8.163/ --model yolo11n.pt --imgsz 320
    python stream_detect.py URL --model yolo11n.pt --clock --label hd_2M
    python stream_detect.py URL --model yolo11n.pt --in-order --seconds 20

The reader opens the stream with one decoder thread: each decoder thread of
FFmpeg holds one frame (Part 3 of the lecture). A thread reads all frames and
keeps only the newest frame (Task C1), so a slow model always gets a new
frame. The option --in-order reads each frame in order instead: then the
delay grows when the model is slower than the stream, and each line ends with
"behind ... s", the time that the reader is behind the live stream.

Each 2 seconds the script prints one line:
    640x480  stream 30.0 frames/s  processed 9.8 frames/s  skipped 40  model 96.1 ms  objects 2.0
At the end it prints one line that starts with RESULT, and it adds one row to
results.csv.

--clock shows a window: on the left a clock with milliseconds, on the right
the stream with the boxes. Point the camera at the clock. Press s to save the
window (10 times), q to stop. The difference of the two clocks in an image is
the end-to-end latency. --no-window --count N saves N images with no window
(a test with no screen).
"""
import argparse
import csv
import os
import statistics
import sys
import threading
import time

# The transport must be set before OpenCV opens the stream. "tcp" loses no
# packet. "udp" can have less delay, but it loses packets on a bad link.
TRANSPORT = os.environ.get("RTSP_TRANSPORT", "tcp")
os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS",
                      "rtsp_transport;%s|fflags;nobuffer|flags;low_delay" % TRANSPORT)

import cv2  # noqa: E402  (after the environment variable)
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
# The lab folder day11/. The complete script is in day11/solutions/.
LAB = os.path.dirname(HERE) if os.path.basename(HERE) == "solutions" else HERE
CLOCK_WIDTH = 640
HEIGHT = 480


def open_capture(url, threads):
    """Open a stream with the FFmpeg backend and a fixed number of decoder threads."""
    capture = cv2.VideoCapture(url, cv2.CAP_FFMPEG, [cv2.CAP_PROP_N_THREADS, threads])
    if not capture.isOpened():
        sys.exit("ERROR: cannot open the stream %s" % url)
    return capture


class NewestFrameReader:
    """Read a stream in a thread. Keep only the newest frame."""

    def __init__(self, capture, start=True):
        self.capture = capture
        self.lock = threading.Lock()
        self.frame = None         # the newest frame
        self.received = 0         # frames that arrived from the stream
        self.taken = 0            # the number of the frame that take() returned last
        self.running = True
        if start:
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def _loop(self):
        while self.running:
            ok, frame = self.capture.read()
            if not ok:
                self.running = False
                break
            self._store(frame)

    def _store(self, frame):
        """Keep the new frame in place of the old frame, and count it."""
        with self.lock:
            self.frame = frame
            self.received += 1

    def take(self):
        """Return (frame, number) of the newest frame, or (None, 0) if no
        new frame arrived since the last call."""
        with self.lock:
            if self.frame is None or self.received == self.taken:
                return None, 0
            self.taken = self.received
            return self.frame, self.received

    def close(self):
        self.running = False
        if hasattr(self, "thread"):
            self.thread.join(timeout=2)
        self.capture.release()


class InOrderReader:
    """Read each frame in order, with no thread (for the comparison)."""

    def __init__(self, capture):
        self.capture = capture
        self.received = 0
        self.running = True
        # The frame rate of the stream, for the delay of this reader.
        self.fps = capture.get(cv2.CAP_PROP_FPS)

    def take(self):
        ok, frame = self.capture.read()
        if not ok:
            self.running = False
            return None, 0
        self.received += 1
        return frame, self.received

    def close(self):
        self.capture.release()


class FakeCapture:
    """A capture with no stream, for the check of Task C1."""

    def read(self):
        return False, None

    def release(self):
        pass


def check_task_c1():
    reader = NewestFrameReader(FakeCapture(), start=False)
    for number in range(1, 6):
        reader._store(np.full((2, 2, 3), number, dtype=np.uint8))
    frame, number = reader.take()
    if frame is None or number != 5 or int(frame[0, 0, 0]) != 5:
        return False
    again, _ = reader.take()
    if again is not None:
        return False
    reader._store(np.full((2, 2, 3), 6, dtype=np.uint8))
    frame, number = reader.take()
    return frame is not None and number == 6 and reader.received == 6


def clock_text(now):
    local = time.localtime(now)
    return "%02d:%02d:%02d.%03d" % (local.tm_hour, local.tm_min, local.tm_sec,
                                    int((now % 1) * 1000))


def clock_window(frame, now):
    """Return one image: the clock on the left, the stream on the right."""
    text = clock_text(now)
    panel = np.zeros((HEIGHT, CLOCK_WIDTH, 3), dtype=np.uint8)
    cv2.putText(panel, "clock now", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                (160, 160, 160), 2, cv2.LINE_AA)
    cv2.putText(panel, text, (20, 270), cv2.FONT_HERSHEY_SIMPLEX, 2.6,
                (255, 255, 255), 6, cv2.LINE_AA)
    if frame is None:
        right = np.zeros((HEIGHT, CLOCK_WIDTH, 3), dtype=np.uint8)
    else:
        scale = HEIGHT / frame.shape[0]
        right = cv2.resize(frame, (int(frame.shape[1] * scale), HEIGHT))
    return np.hstack([panel, right]), text


def load_detector(args):
    """Import the Day 8 detector and load the model. Return a function."""
    sys.path.insert(0, os.path.abspath(args.day08))
    try:
        import detector  # the file day08/pi/detector.py of the Day 8 lab
    except ImportError:
        sys.exit("ERROR: no file detector.py in %s. Give the folder with --day08."
                 % args.day08)
    detector.set_litert_threads(args.model_threads)
    model = detector.load_model(args.model)
    imgsz = args.imgsz or detector.describe(args.model)[2] or 640

    def run(frame):
        result = detector.detect(model, frame, imgsz, conf=args.conf)
        ms = sum(result.speed.values())
        return result.plot(), ms, len(result.boxes)

    # Warm-up (the method of Day 9): the first runs of a model are slow. Run
    # it 3 times on an empty frame before the stream opens.
    empty = np.zeros((480, 640, 3), dtype=np.uint8)
    for _ in range(3):
        run(empty)
    return run, imgsz


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url", help="rtsp://pi-NN.local:8554/cam or http://<address>/")
    parser.add_argument("--seconds", type=float, default=20.0,
                        help="stop after this time (default 20; 0 = until Ctrl-C)")
    parser.add_argument("--model", help="a model file of the Day 8 lab, for example yolo11n.pt")
    parser.add_argument("--imgsz", type=int, default=0,
                        help="image size of the model (default: from the name, or 640)")
    parser.add_argument("--conf", type=float, default=0.25, help="score threshold")
    parser.add_argument("--model-threads", type=int, default=4,
                        help="threads of a LiteRT model (default 4)")
    parser.add_argument("--day08", default=os.path.join(LAB, "..", "day08", "pi"),
                        help="the folder with detector.py (default ../day08/pi)")
    parser.add_argument("--threads", type=int, default=1,
                        help="decoder threads (default 1)")
    parser.add_argument("--in-order", action="store_true",
                        help="read each frame in order (no thread)")
    parser.add_argument("--show", action="store_true", help="show the stream in a window")
    parser.add_argument("--clock", action="store_true",
                        help="show the clock and the stream; s = save, q = stop")
    parser.add_argument("--no-window", action="store_true",
                        help="with --clock: save images with no window (a test)")
    parser.add_argument("--count", type=int, default=10,
                        help="images to save with --no-window (default 10)")
    parser.add_argument("--label", default="run", help="a name for this setting")
    parser.add_argument("--csv", default="results.csv", help="the file for the RESULT row")
    args = parser.parse_args()

    if not check_task_c1():
        print("Task C1: not complete")
        return 1
    print("Task C1: complete")

    detect, imgsz = (None, None)
    if args.model:
        detect, imgsz = load_detector(args)

    capture = open_capture(args.url, args.threads)
    reader = InOrderReader(capture) if args.in_order else NewestFrameReader(capture)
    kind = "in order" if args.in_order else "newest"
    print("Stream open: %s (transport %s, decoder threads %d, reader %s)"
          % (args.url, TRANSPORT, args.threads, kind), flush=True)

    start = time.monotonic()
    last_report = start
    processed = 0
    at_report = (0, 0)
    model_ms, objects = [], []
    shape = None
    saved = 0
    next_save = start + 2.0
    try:
        while reader.running:
            now = time.monotonic()
            if args.seconds and now - start >= args.seconds and not args.clock:
                break
            frame, number = reader.take()
            if frame is None:
                time.sleep(0.001)
                continue
            shape = frame.shape
            output = frame
            if detect:
                output, ms, count = detect(frame)
                model_ms.append(ms)
                objects.append(count)
            processed += 1

            if args.clock:
                window, text = clock_window(output, time.time())
                save = False
                if args.no_window:
                    save = time.monotonic() >= next_save
                    if save:
                        next_save = time.monotonic() + 1.0
                else:
                    cv2.imshow("stream_detect: s = save, q = stop", window)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        break
                    save = key == ord("s")
                if save:
                    saved += 1
                    name = "latency_%s_%02d.png" % (args.label, saved)
                    cv2.imwrite(name, window)
                    print("Saved %s (clock now: %s)" % (name, text), flush=True)
                    if args.no_window and saved >= args.count:
                        break
            elif args.show:
                cv2.imshow("stream_detect: q = stop", output)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            if now - last_report >= 2.0:
                span = now - last_report
                got = reader.received - at_report[0]
                done = processed - at_report[1]
                line = "%dx%d  stream %.1f frames/s  processed %.1f frames/s  skipped %d" % (
                    shape[1], shape[0], got / span, done / span, got - done)
                if model_ms:
                    line += "  model %.1f ms  objects %.1f" % (
                        statistics.median(model_ms[-done:] or model_ms),
                        statistics.mean(objects[-done:] or objects))
                if args.in_order and 1 <= reader.fps <= 120:
                    # The stream sent fps x time frames. The frames that this
                    # reader did not read yet wait in buffers.
                    behind = (now - start) - reader.received / reader.fps
                    line += "  behind %.1f s" % behind
                print(line, flush=True)
                last_report = now
                at_report = (reader.received, processed)
    except KeyboardInterrupt:
        pass
    finally:
        reader.close()
        if args.show or (args.clock and not args.no_window):
            cv2.destroyAllWindows()

    total = time.monotonic() - start
    if shape is None:
        print("ERROR: no frame arrived from %s" % args.url)
        return 1
    row = {
        "label": args.label, "url": args.url, "reader": kind.replace(" ", "_"),
        "decoder_threads": args.threads, "transport": TRANSPORT,
        "size": "%dx%d" % (shape[1], shape[0]),
        "model": os.path.basename(args.model) if args.model else "none",
        "imgsz": imgsz or "", "seconds": round(total, 1),
        "stream_fps": round(reader.received / total, 1),
        "processed_fps": round(processed / total, 1),
        "skipped": reader.received - processed,
        "model_ms": round(statistics.median(model_ms), 1) if model_ms else "",
    }
    print("RESULT " + " ".join("%s=%s" % item for item in row.items()))
    new = not os.path.exists(args.csv)
    with open(args.csv, "a", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        if new:
            writer.writeheader()
        writer.writerow(row)
    if args.clock:
        print("Images saved: %d. Read the two clock values of each image." % saved)
    return 0


if __name__ == "__main__":
    sys.exit(main())
