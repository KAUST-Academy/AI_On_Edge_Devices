#!/usr/bin/env python3
"""Check that the IMU samples arrive at a constant rate.

Runs on: the laptop, Python 3.10 or later.
Input:   the CSV lines of board/imu_stream.py or of board/imu_wifi.py
         (columns n, t_us, ...).

Read from the serial port (needs the package pyserial):
    python3 host/check_rate.py --port /dev/ttyACM0 --seconds 20 --save run1.csv

Read from Wi-Fi, when board/imu_wifi.py runs on the board:
    python3 host/check_rate.py --udp 5005 --seconds 20

Read from a file:
    python3 host/check_rate.py --file run1.csv

This file is a copy of Labs/hardware/HW-01/host/check_rate.py with one
addition: the option --udp.

The script uses the time stamp of the board (t_us), not the arrival time on
the laptop. USB sends the lines in blocks, so the arrival time is not constant.
"""

import argparse
import socket
import statistics
import sys
import time


def read_serial(port, seconds, baud=115200):
    """Yield the text lines of the serial port for the given time."""
    import serial  # pyserial

    with serial.Serial(port, baud, timeout=1) as link:
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            raw = link.readline()
            if raw:
                yield raw.decode("ascii", errors="replace").strip()


def read_udp(port, seconds):
    """Yield the text lines of the UDP packets for the given time."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    sock.settimeout(1.0)
    end = time.monotonic() + seconds
    try:
        while time.monotonic() < end:
            try:
                packet, _ = sock.recvfrom(4096)
            except socket.timeout:
                continue
            for line in packet.decode("ascii", errors="replace").splitlines():
                yield line.strip()
    finally:
        sock.close()


def parse(lines):
    """Return the list of (n, t_us) and the list of all valid CSV lines."""
    stamps = []
    kept = []
    for line in lines:
        if not line or line.startswith("#"):
            continue
        fields = line.split(",")
        if fields[0] == "n":          # header line
            kept.append(line)
            continue
        if len(fields) != 8:
            continue                  # REPL text or a broken line
        try:
            stamps.append((int(fields[0]), int(fields[1])))
        except ValueError:
            continue
        kept.append(line)
    return stamps, kept


def analyse(stamps, nominal_hz, tolerance):
    """Return a dictionary with the rate statistics."""
    if len(stamps) < 3:
        raise SystemExit("Not enough samples: %d" % len(stamps))

    periods = []
    lost = 0
    for (n0, t0), (n1, t1) in zip(stamps, stamps[1:]):
        if n1 != n0 + 1:
            lost += n1 - n0 - 1       # lines that did not arrive
            continue
        periods.append(t1 - t0)

    nominal_us = 1e6 / nominal_hz
    outside = [p for p in periods if abs(p - nominal_us) > tolerance * nominal_us]
    mean_us = statistics.fmean(periods)
    return {
        "samples": len(stamps),
        "lost_lines": lost,
        "mean_period_us": mean_us,
        "mean_rate_hz": 1e6 / mean_us,
        "std_us": statistics.pstdev(periods),
        "min_us": min(periods),
        "max_us": max(periods),
        "outside": len(outside),
        "outside_percent": 100.0 * len(outside) / len(periods),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--port", help="serial port, for example /dev/ttyACM0")
    source.add_argument("--udp", type=int, metavar="PORT",
                        help="UDP port of board/imu_wifi.py, for example 5005")
    source.add_argument("--file", help="CSV file of an earlier run")
    parser.add_argument("--seconds", type=float, default=20.0,
                        help="recording time for --port and --udp (default: 20)")
    parser.add_argument("--rate", type=float, default=50.0,
                        help="nominal rate in Hz (default: 50)")
    parser.add_argument("--tolerance", type=float, default=0.10,
                        help="permitted error of one period (default: 0.10)")
    parser.add_argument("--save", help="write the valid CSV lines to this file")
    args = parser.parse_args()

    if args.port:
        lines = list(read_serial(args.port, args.seconds))
    elif args.udp:
        lines = list(read_udp(args.udp, args.seconds))
    else:
        with open(args.file, encoding="ascii", errors="replace") as handle:
            lines = [line.strip() for line in handle]

    stamps, kept = parse(lines)
    if args.save:
        with open(args.save, "w", encoding="ascii") as handle:
            handle.write("\n".join(kept) + "\n")

    result = analyse(stamps, args.rate, args.tolerance)
    print("Samples:            %d" % result["samples"])
    print("Lost lines:         %d" % result["lost_lines"])
    print("Mean rate:          %.2f Hz (nominal %.2f Hz)"
          % (result["mean_rate_hz"], args.rate))
    print("Period mean / std:  %.0f us / %.0f us"
          % (result["mean_period_us"], result["std_us"]))
    print("Period min / max:   %d us / %d us"
          % (result["min_us"], result["max_us"]))
    print("Periods outside +-%.0f%%: %d (%.2f%%)"
          % (100 * args.tolerance, result["outside"], result["outside_percent"]))

    rate_ok = abs(result["mean_rate_hz"] - args.rate) <= 0.01 * args.rate
    jitter_ok = result["outside_percent"] <= 1.0
    if rate_ok and jitter_ok and result["lost_lines"] == 0:
        print("RESULT: PASS - the sampling rate is constant")
        return 0
    print("RESULT: FAIL - mean rate within 1%%: %s, periods outside <= 1%%: %s, "
          "lost lines: %d" % (rate_ok, jitter_ok, result["lost_lines"]))
    return 1


if __name__ == "__main__":
    sys.exit(main())
