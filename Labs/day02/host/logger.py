#!/usr/bin/env python3
"""Record labelled IMU recordings from the board into CSV files.

Student version of the Day 2 lab. Complete the two functions with the mark
"TODO (student)": file_name (task C1) and count_lost (task C2).

Runs on: the laptop, Python 3.10 or later.
Needs:   the package pyserial for --port. The package matplotlib for --plot.
Input:   the CSV lines of board/imu_stream.py (serial port) or of
         board/imu_wifi.py (UDP): n,t_us,ax,ay,az,gx,gy,gz

Record four recordings of 10 s from the serial port:
    python3 host/logger.py --port /dev/ttyACM0 --label lift --session s1 \
        --person A --count 4

Record from Wi-Fi:
    python3 host/logger.py --udp 5005 --label lift --session s1 --person A

Test your two functions with no board:
    python3 host/logger.py --self-test

Each recording goes to one file: <out>/<label>.<session>.<number>.csv
The file starts with comment lines (#) that hold the settings. Then it has
the header line and one line for each sample. The sample number n and the
time t_us start at 0 in each file.

Credits: the recording length of 10 s and the rate of 50 Hz follow the
motion classification chapter of "Machine Learning Systems" (mlsysbook.ai,
CC BY-NC-SA 4.0). The code is new.
"""

import argparse
import datetime
import os
import re
import socket
import sys
import time

RATE_HZ = 50
ACCEL_RANGE_G = 16
GYRO_RANGE_DPS = 2000
HEADER = "n,t_us,ax,ay,az,gx,gy,gz"
NAME_RULE = re.compile(r"^[a-z0-9_-]+$")
SILENCE_S = 5.0          # stop when no line arrives for this time


# ---------------------------------------------------------------- student tasks
def file_name(label, session, number):
    """Task C1. Return the file name of one recording.

    Example: file_name("lift", "s2", 7) returns "lift.s2.07.csv".
    The number has two digits.
    """
    # TODO (student): replace the line below. Use the label, the session,
    # and the number, with a full stop between them.
    return "recording.csv"


def count_lost(numbers):
    """Task C2. Return how many samples are missing in a recording.

    numbers is the list of the sample numbers n of the board, in the order
    of arrival. The board adds 1 for each sample.
    Example: count_lost([4, 5, 6, 9, 10]) returns 2, because 7 and 8 are
    missing.
    """
    # TODO (student): replace the line below. Compare each number with the
    # number before it.
    return 0


# ------------------------------------------------------------------ line sources
def serial_lines(port, baud=115200):
    """Yield the text lines of the serial port. Yield None after 1 s of silence."""
    import serial  # pyserial

    with serial.Serial(port, baud, timeout=1) as link:
        link.reset_input_buffer()
        while True:
            raw = link.readline()
            yield raw.decode("ascii", errors="replace").strip() if raw else None


def udp_lines(port):
    """Yield the text lines of the UDP packets. Yield None after 1 s of silence."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    sock.settimeout(1.0)
    try:
        while True:
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                yield None
                continue
            for line in packet.decode("ascii", errors="replace").splitlines():
                yield line.strip()
    finally:
        sock.close()


def parse_sample(line):
    """Return [n, t_us, ax, ay, az, gx, gy, gz], or None for a different line."""
    if not line or line.startswith("#"):
        return None
    fields = line.split(",")
    if len(fields) != 8:
        return None
    try:
        return [int(fields[0]), int(fields[1])] + [float(f) for f in fields[2:]]
    except ValueError:
        return None           # the header line, or a broken line


# --------------------------------------------------------------------- recording
def samples_for(lines, seconds):
    """Read and drop the samples that arrive in the given time. Return their number."""
    end = time.monotonic() + seconds
    silent_since = time.monotonic()
    count = 0
    for line in lines:
        now = time.monotonic()
        if parse_sample(line) is not None:
            count += 1
            silent_since = now
        elif now - silent_since > SILENCE_S:
            raise SystemExit("No data from the board for %d s. Is the board "
                             "script active?" % SILENCE_S)
        if now >= end:
            break
    return count


def record(lines, count):
    """Return the next `count` samples of the board."""
    rows = []
    silent_since = time.monotonic()
    for line in lines:
        sample = parse_sample(line)
        now = time.monotonic()
        if sample is None:
            if now - silent_since > SILENCE_S:
                raise SystemExit("No data from the board for %d s. Is the "
                                 "board script active?" % SILENCE_S)
            continue
        silent_since = now
        if rows and sample[0] <= rows[-1][0]:
            raise SystemExit("The sample number went back. The board started "
                             "again. Record this recording again.")
        rows.append(sample)
        if len(rows) == count:
            break
    return rows


def statistics_of(rows):
    """Return a dictionary with the checks of one recording."""
    numbers = [row[0] for row in rows]
    span_us = rows[-1][1] - rows[0][1]
    steps = numbers[-1] - numbers[0]
    limit = 0.99 * ACCEL_RANGE_G
    clipped = sum(1 for row in rows if max(abs(v) for v in row[2:5]) >= limit)
    return {
        "samples": len(rows),
        "lost": count_lost(numbers),
        "rate_hz": 1e6 * steps / span_us if span_us > 0 else 0.0,
        "clipped": clipped,
    }


def write_file(path, rows, meta, stats):
    """Write one recording. n and t_us start at 0."""
    n0, t0 = rows[0][0], rows[0][1]
    with open(path, "w", encoding="ascii") as handle:
        for key, value in meta.items():
            handle.write("# %s: %s\n" % (key, value))
        handle.write("# lost_samples: %d\n" % stats["lost"])
        handle.write(HEADER + "\n")
        for row in rows:
            handle.write("%d,%d,%.4f,%.4f,%.4f,%.2f,%.2f,%.2f\n"
                         % (row[0] - n0, row[1] - t0, *row[2:]))


def save_plot(path, rows, title):
    """Save a plot of the three acceleration axes. Return False with no matplotlib."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    t = [(row[1] - rows[0][1]) / 1e6 for row in rows]
    figure, axis = plt.subplots(figsize=(8, 3))
    for k, name in enumerate(("ax", "ay", "az")):
        axis.plot(t, [row[2 + k] for row in rows], label=name)
    axis.set_xlabel("time (s)")
    axis.set_ylabel("acceleration (g)")
    axis.set_title(title)
    axis.legend(loc="upper right", ncol=3)
    figure.tight_layout()
    figure.savefig(path, dpi=80)
    plt.close(figure)
    return True


def next_number(folder, label, session):
    """Return the first number that has no file."""
    if file_name(label, session, 1) == file_name(label, session, 2):
        return 1              # task C1 is not complete: all names are equal
    number = 1
    while os.path.exists(os.path.join(folder, file_name(label, session, number))):
        number += 1
    return number


# --------------------------------------------------------------------- self test
def self_test():
    """Check the two student functions. Return 0 when the two are correct."""
    names_ok = (file_name("lift", "s2", 7) == "lift.s2.07.csv"
                and file_name("idle", "s1", 12) == "idle.s1.12.csv")
    lost_ok = (count_lost([4, 5, 6, 9, 10]) == 2
               and count_lost([0, 1, 2, 3]) == 0
               and count_lost([10, 20]) == 9)
    print("Task C1 (file_name):  %s" % ("complete" if names_ok else "not complete"))
    print("Task C2 (count_lost): %s" % ("complete" if lost_ok else "not complete"))
    return 0 if names_ok and lost_ok else 1


# -------------------------------------------------------------------------- main
def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--port", help="serial port, for example /dev/ttyACM0")
    parser.add_argument("--udp", type=int, metavar="PORT",
                        help="UDP port of board/imu_wifi.py, for example 5005")
    parser.add_argument("--label", help="class of the recording, for example lift")
    parser.add_argument("--session", help="session name, for example s1")
    parser.add_argument("--person", default="not stated",
                        help="the person who makes the motion")
    parser.add_argument("--seconds", type=float, default=10.0,
                        help="length of one recording (default: 10)")
    parser.add_argument("--count", type=int, default=1,
                        help="number of recordings in a row (default: 1)")
    parser.add_argument("--wait", type=float, default=3.0,
                        help="time before each recording (default: 3 s)")
    parser.add_argument("--out", default="data", help="output folder (default: data)")
    parser.add_argument("--plot", action="store_true",
                        help="save a plot of each recording in <out>/plots/")
    parser.add_argument("--self-test", action="store_true",
                        help="check tasks C1 and C2 with no board")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if (args.port is None) == (args.udp is None):
        parser.error("give --port or --udp")
    if not args.label or not args.session:
        parser.error("give --label and --session")
    for text in (args.label, args.session):
        if not NAME_RULE.match(text):
            parser.error("'%s': use only the characters a-z, 0-9, - and _" % text)

    os.makedirs(args.out, exist_ok=True)
    lines = serial_lines(args.port) if args.port else udp_lines(args.udp)
    wanted = int(round(args.seconds * RATE_HZ))
    source = "serial" if args.port else "udp"

    for index in range(args.count):
        print("Recording %d of %d, class '%s'. Start the motion now."
              % (index + 1, args.count, args.label))
        seen = samples_for(lines, args.wait)
        if seen == 0:
            raise SystemExit("No samples in %.0f s. Is the board script "
                             "active?" % args.wait)
        print("  recording %.0f s ..." % args.seconds)
        rows = record(lines, wanted)
        if len(rows) < wanted:
            raise SystemExit("The data stopped after %d samples." % len(rows))

        stats = statistics_of(rows)
        number = next_number(args.out, args.label, args.session)
        name = file_name(args.label, args.session, number)
        meta = {
            "device": "XIAOML Kit, LSM6DS3TR-C",
            "rate_hz": RATE_HZ,
            "accel_range_g": ACCEL_RANGE_G,
            "gyro_range_dps": GYRO_RANGE_DPS,
            "label": args.label,
            "session": args.session,
            "person": args.person,
            "source": source,
            "recorded": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        write_file(os.path.join(args.out, name), rows, meta, stats)
        print("  saved %s: %d samples, %.2f Hz, %d lost, %d clipped"
              % (os.path.join(args.out, name), stats["samples"],
                 stats["rate_hz"], stats["lost"], stats["clipped"]))
        if stats["lost"] > 0:
            print("  WARNING: samples are missing. Record this recording again.")
        if abs(stats["rate_hz"] - RATE_HZ) > 0.01 * RATE_HZ and stats["lost"] == 0:
            print("  WARNING: the rate is not %d Hz. Check the board script."
                  % RATE_HZ)
        if stats["clipped"] > 0:
            print("  WARNING: the acceleration is at the limit of the range.")
        if args.plot:
            folder = os.path.join(args.out, "plots")
            os.makedirs(folder, exist_ok=True)
            picture = os.path.join(folder, name[:-4] + ".png")
            if save_plot(picture, rows, name):
                print("  plot: %s" % picture)
            else:
                print("  no plot: the package matplotlib is not installed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
