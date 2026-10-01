#!/usr/bin/env python3
"""Convert the recordings of the Day 2 lab to the CSV format of Edge Impulse.

Runs on: the laptop, Python 3.10 or later. It needs no package.

    python3 host/to_edge_impulse.py --data data

The program reads the file split.json that the notebook dataset.ipynb writes
into the data folder. It writes two folders:

    ei_upload/training/   the recordings of the training sessions
    ei_upload/testing/    the recordings of the test sessions

Each output file has the header "timestamp,accX,accY,accZ". The time is in
milliseconds and the acceleration is in m/s^2. Edge Impulse reads the label
from the file name: the text before the first full stop.

With no split.json, name the test sessions yourself:

    python3 host/to_edge_impulse.py --data data --test-sessions s3

Credits: the file format follows the Edge Impulse documentation
(docs.edgeimpulse.com, data acquisition format CSV). The use of the three
accelerometer axes in m/s^2 follows the motion classification chapter of
"Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0). The code is new.
"""

import argparse
import json
import os
import sys

G_TO_MS2 = 9.81          # the kit lab uses this value
RATE_HZ = 50
PERIOD_MS = 1000 // RATE_HZ


def read_recording(path):
    """Return the list of (n, ax, ay, az) of one recording file."""
    rows = []
    with open(path, encoding="ascii", errors="replace") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.strip().split(",")
            if len(fields) != 8 or fields[0] == "n":
                continue
            rows.append((int(fields[0]), float(fields[2]), float(fields[3]),
                         float(fields[4])))
    return rows


def convert(source, target):
    """Write one file in the Edge Impulse format. Return the lost samples."""
    rows = read_recording(source)
    lost = (rows[-1][0] - rows[0][0] + 1) - len(rows)
    with open(target, "w", encoding="ascii") as handle:
        handle.write("timestamp,accX,accY,accZ\n")
        for index, (_, ax, ay, az) in enumerate(rows):
            handle.write("%d,%.4f,%.4f,%.4f\n"
                         % (index * PERIOD_MS, ax * G_TO_MS2, ay * G_TO_MS2,
                            az * G_TO_MS2))
    return lost


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", default="data",
                        help="folder with the recordings (default: data)")
    parser.add_argument("--out", default="ei_upload",
                        help="output folder (default: ei_upload)")
    parser.add_argument("--test-sessions", nargs="+", metavar="SESSION",
                        help="sessions for the test set. Without this "
                             "option, the program reads split.json.")
    args = parser.parse_args()

    if not os.path.isdir(args.data):
        raise SystemExit("The folder %s/ does not exist." % args.data)
    names = sorted(name for name in os.listdir(args.data)
                   if name.endswith(".csv") and len(name.split(".")) == 4)
    if not names:
        raise SystemExit("No recording in %s/" % args.data)

    if args.test_sessions:
        test_sessions = set(args.test_sessions)
    else:
        split_file = os.path.join(args.data, "split.json")
        if not os.path.exists(split_file):
            raise SystemExit("%s does not exist. Run the notebook first, or "
                             "give --test-sessions." % split_file)
        with open(split_file, encoding="utf-8") as handle:
            test_sessions = set(json.load(handle)["test_sessions"])

    sessions = {name.split(".")[1] for name in names}
    unknown = test_sessions - sessions
    if unknown:
        raise SystemExit("No recording has the session %s" % sorted(unknown))
    if test_sessions == sessions:
        raise SystemExit("All sessions are test sessions. The training set "
                         "is empty.")

    counts = {"training": 0, "testing": 0}
    for category in counts:
        os.makedirs(os.path.join(args.out, category), exist_ok=True)
    for name in names:
        session = name.split(".")[1]
        category = "testing" if session in test_sessions else "training"
        lost = convert(os.path.join(args.data, name),
                       os.path.join(args.out, category, name))
        counts[category] += 1
        if lost:
            print("WARNING: %s has %d lost samples. Its time stamps are not "
                  "correct." % (name, lost))

    print("Training: %d files in %s/training/" % (counts["training"], args.out))
    print("Testing:  %d files in %s/testing/ (sessions: %s)"
          % (counts["testing"], args.out, ", ".join(sorted(test_sessions))))
    print()
    print("Upload with the Edge Impulse CLI:")
    print("  edge-impulse-uploader --category training %s/training/*.csv"
          % args.out)
    print("  edge-impulse-uploader --category testing %s/testing/*.csv"
          % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
