#!/usr/bin/env python3
"""A simulated board: send IMU lines over UDP, as board/imu_wifi.py does.

Runs on: the laptop, Python 3.10 or later, with the package numpy.

Use this program to test host/logger.py when no board is available. The
signals come from host/motion_sim.py. They are simulated.

Start the logger in one terminal:
    python3 host/logger.py --udp 5005 --label lift --session s1 --count 2

Start the simulated board in a second terminal:
    python3 host/sim_board.py --label lift --session s1

The program sends 50 samples each second, with the lines of 5 samples in
one packet. Press Ctrl-C to stop it.
"""

import argparse
import socket
import sys
import time

import motion_sim


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--label", default="terrestrial",
                        choices=motion_sim.CLASSES)
    parser.add_argument("--session", default="s1")
    parser.add_argument("--host", default="127.0.0.1",
                        help="address of the logger (default: this computer)")
    parser.add_argument("--port", type=int, default=5005)
    parser.add_argument("--seconds", type=float, default=0.0,
                        help="stop after this time (default: no limit)")
    parser.add_argument("--lose", type=int, default=0,
                        help="lose one packet in this number, for a test "
                             "(default: lose no packet)")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target = (args.host, args.port)
    period = 1.0 / motion_sim.RATE_HZ
    period_us = 1000000 // motion_sim.RATE_HZ
    print("Sending class '%s', session '%s' to %s, port %d"
          % (args.label, args.session, args.host, args.port))

    n = 0
    packets = 0
    block = 0
    lines = []
    start = time.monotonic()
    try:
        while args.seconds <= 0 or n < args.seconds * motion_sim.RATE_HZ:
            # One block of 10 s of signal. The index changes for each block.
            signal = motion_sim.simulate(args.label, args.session,
                                         "sim%d" % block)
            block += 1
            for row in signal:
                lines.append(motion_sim.csv_line(n, n * period_us, row))
                n += 1
                if len(lines) == 5:
                    packets += 1
                    if not (args.lose and packets % args.lose == 0):
                        sock.sendto(("\n".join(lines) + "\n").encode(), target)
                    lines = []
                # Wait for the deadline of the next sample.
                wait = start + n * period - time.monotonic()
                if wait > 0:
                    time.sleep(wait)
                if args.seconds > 0 and n >= args.seconds * motion_sim.RATE_HZ:
                    break
    except KeyboardInterrupt:
        pass
    print("Stopped after %d samples" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
