#!/usr/bin/env python3
"""Day 11 lab, Part D: measure the frame rate and the bit rate of an MJPEG stream.

Runs on: the laptop. Needs: Python 3 only (no package).

Use:
    python mjpeg_rate.py http://192.168.8.163/ --seconds 10
    python mjpeg_rate.py http://192.168.8.163/ --seconds 10 --save xiao.jpg

The XIAO sends one HTTP answer of the type multipart/x-mixed-replace. Each
part of the answer is one JPEG image with the header Content-Length. The
script reads the parts for some seconds and calculates (Task D1) the frame
rate, the mean size of a JPEG image, and the bit rate. It prints one line
that starts with RESULT.

Hardware status: not tested on hardware (prepared on 2026-10-03). Tested on
the work computer of the course with an MJPEG stream of FFmpeg and with a
test server in the format of the XIAO sketch.

Credits: the stream format is the format of the sketch Streeming_Video.ino of
"XIAO ESP32S3 Sense" by Marcelo Rovai (github.com/Mjrovai/XIAO-ESP32S3-Sense,
Apache-2.0). The script is new code of this course.
"""
import argparse
import sys
import time
import urllib.request


def stream_stats(sizes, seconds):
    """Return (frames each second, mean JPEG size in KB, bit rate in Mbit/s).

    sizes is the list of the JPEG sizes in bytes, seconds the duration of the
    measurement. 1 KB = 1024 bytes. 1 Mbit/s = 1 000 000 bits each second.
    """
    # TODO (student), Task D1: return three values as a tuple:
    # the frames each second, the mean JPEG size in KB, and the bit rate in
    # Mbit/s. Bit rate = all bytes x 8 / seconds.
    return None


def check_task_d1():
    result = stream_stats([20480, 30720, 25600, 25600], 0.4)
    if result is None or len(result) != 3:
        return False
    fps, mean_kb, mbit_s = result
    return abs(fps - 10.0) < 1e-6 and abs(mean_kb - 25.0) < 1e-6 \
        and abs(mbit_s - 2.048) < 1e-6


def read_headers(stream):
    """Read the header lines of one part. Return them as a dictionary."""
    headers = {}
    while True:
        line = stream.readline()
        if not line:
            raise EOFError("the stream ended")
        line = line.strip()
        if not line:
            if headers:
                return headers
            continue                      # empty line before the part
        if line.startswith(b"--"):
            continue                      # the boundary line
        if b":" in line:
            key, value = line.split(b":", 1)
            headers[key.strip().lower().decode()] = value.strip().decode()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url", help="for example http://192.168.8.163/")
    parser.add_argument("--seconds", type=float, default=10.0,
                        help="duration of the measurement (default 10)")
    parser.add_argument("--save", help="write the last JPEG image to this file")
    args = parser.parse_args()

    if not check_task_d1():
        print("Task D1: not complete")
        return 1
    print("Task D1: complete")

    try:
        stream = urllib.request.urlopen(args.url, timeout=10)
    except OSError as error:
        print("ERROR: cannot open %s: %s" % (args.url, error))
        return 1
    content_type = stream.headers.get("Content-Type", "")
    print("Content-Type: %s" % content_type)
    if "multipart" not in content_type:
        print("ERROR: this is not an MJPEG stream (multipart)")
        return 1

    sizes = []
    image = b""
    first = None
    try:
        while True:
            headers = read_headers(stream)
            length = int(headers.get("content-length", "0"))
            if length <= 0:
                print("ERROR: a part has no Content-Length")
                return 1
            image = stream.read(length)
            now = time.monotonic()
            if first is None:
                first = now                # the clock starts with the first image
                continue
            sizes.append(len(image))
            if now - first >= args.seconds:
                break
    except (EOFError, OSError) as error:
        print("The stream stopped: %s" % error)
    if len(sizes) < 2:
        print("ERROR: fewer than 2 images in %.1f s" % args.seconds)
        return 1

    seconds = time.monotonic() - first
    fps, mean_kb, mbit_s = stream_stats(sizes, seconds)
    print("RESULT url=%s seconds=%.1f frames=%d fps=%.1f mean_kb=%.1f "
          "min_kb=%.1f max_kb=%.1f mbit_s=%.2f" % (
              args.url, seconds, len(sizes), fps, mean_kb, min(sizes) / 1024,
              max(sizes) / 1024, mbit_s))
    if args.save:
        with open(args.save, "wb") as handle:
            handle.write(image)
        print("Last image saved: %s" % args.save)
    return 0


if __name__ == "__main__":
    sys.exit(main())
