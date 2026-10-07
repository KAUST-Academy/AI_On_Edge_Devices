#!/usr/bin/env python3
"""Make the fallback dataset of the MC-3 lab.

Runs on: the laptop, Python 3.10 or later, with the package numpy.

Use the fallback dataset only if you have no recordings of your own. The
signals come from host/motion_sim.py. They are simulated, so a model that
learns from them does not work on the real kit.

    python3 host/make_dataset.py

The program writes 48 files into the folder fallback_data/: 4 classes,
3 sessions, 4 recordings of 10 s for each class and session. The files have
the format of the logger of the course, so your own recordings of the XIAOML
Kit can replace them. The program always makes the same files.

Put your own recordings in the folder data/ instead. The notebook reads
data/ when it has files, and fallback_data/ when it has none.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import motion_sim

SESSIONS = ("s1", "s2", "s3")
RECORDINGS = 4
SECONDS = 10.0


def write_recording(folder, label, session, number):
    """Write one file and return its name."""
    name = "%s.%s.%02d.csv" % (label, session, number)
    signal = motion_sim.simulate(label, session, number, SECONDS)
    period_us = 1000000 // motion_sim.RATE_HZ
    with open(os.path.join(folder, name), "w", encoding="ascii") as handle:
        handle.write("# device: simulation (host/motion_sim.py), not a "
                     "recording\n")
        handle.write("# rate_hz: %d\n" % motion_sim.RATE_HZ)
        handle.write("# accel_range_g: %d\n" % motion_sim.ACCEL_RANGE_G)
        handle.write("# gyro_range_dps: %d\n" % motion_sim.GYRO_RANGE_DPS)
        handle.write("# label: %s\n" % label)
        handle.write("# session: %s\n" % session)
        handle.write("# person: simulation\n")
        handle.write("# source: simulation\n")
        handle.write("n,t_us,ax,ay,az,gx,gy,gz\n")
        for n, row in enumerate(signal):
            handle.write(motion_sim.csv_line(n, n * period_us, row) + "\n")
    return name


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="fallback_data",
                        help="output folder (default: fallback_data)")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    count = 0
    for label in motion_sim.CLASSES:
        for session in SESSIONS:
            for number in range(1, RECORDINGS + 1):
                write_recording(args.out, label, session, number)
                count += 1
    print("Wrote %d files to %s/" % (count, args.out))
    print("These signals are simulated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())