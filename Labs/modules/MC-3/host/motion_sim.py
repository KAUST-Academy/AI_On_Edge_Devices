"""Simulated IMU signals for the four motion classes of the MC-5 lab.

Runs on: the laptop, Python 3.10 or later, with the package numpy.

This module is adapted from the file host/motion_sim.py of the lab of Day 2
of this course. The signals are the same in form. They are simulated, so a
model that learns from them does not work on the real kit.

Use the simulated signals in two cases only:

- host/make_dataset.py: a fallback dataset for a group that has no
  recordings of the motion of a package.
- a check of the notebook when no recording is in the folder data/.

The values have the units of the logger of the course: g for the
acceleration and degrees per second for the angular rate. The kit lies with
the display up, so the z axis shows gravity (about +1 g).

Each session has its own speed, amplitude, direction, and tilt. Recordings
of one session are similar. Recordings of different sessions are different.
A real dataset has the same property: one person in one position makes
similar motions.
"""

import math
import zlib

import numpy as np

CLASSES = ("idle", "terrestrial", "lift", "maritime")
RATE_HZ = 50
ACCEL_RANGE_G = 16.0
GYRO_RANGE_DPS = 2000.0


def _rng(*parts):
    """Return a random generator that depends only on the given text parts."""
    seed = zlib.crc32("/".join(str(p) for p in parts).encode())
    return np.random.default_rng(seed)


def session_parameters(session):
    """Return the parameters that all recordings of one session share."""
    rng = _rng("mc3-session", session)
    return {
        "speed": rng.uniform(0.7, 1.4),         # factor on each frequency
        "amplitude": rng.uniform(0.6, 1.5),     # factor on each amplitude
        "direction": rng.uniform(-35.0, 35.0),  # degrees in the x-y plane
        "roll": rng.normal(0.0, 6.0),           # tilt of the kit, degrees
        "pitch": rng.normal(0.0, 6.0),
        "sway": rng.uniform(0.02, 0.15),        # side motion, in g
        "noise": rng.uniform(0.008, 0.02),      # sensor and hand noise, in g
    }


def simulate(label, session, index, seconds=10.0, rate=RATE_HZ):
    """Return an array with one row for each sample: ax, ay, az, gx, gy, gz.

    label is one of CLASSES. session is the session name, for example "s1".
    index is the number of the recording in the session. The same three
    values always give the same signal.
    """
    if label not in CLASSES:
        raise ValueError("label must be one of %s" % (CLASSES,))
    par = session_parameters(session)
    rng = _rng("mc3-recording", label, session, index)
    count = int(round(seconds * rate))
    t = np.arange(count) / rate

    # Small changes from one recording to the next.
    speed = par["speed"] * rng.uniform(0.9, 1.1)
    amplitude = par["amplitude"] * rng.uniform(0.9, 1.1)
    phase = rng.uniform(0.0, 2.0 * math.pi, size=6)

    def wave(frequency, k):
        return np.sin(2.0 * math.pi * frequency * speed * t + phase[k])

    ax = np.zeros(count)
    ay = np.zeros(count)
    az = np.zeros(count)
    gx = np.zeros(count)
    gy = np.zeros(count)
    gz = np.zeros(count)
    tilt = 1.0

    if label == "idle":
        tilt = 0.2                              # the kit lies on the table
    elif label == "terrestrial":
        # Motion in the horizontal plane, in the direction of the session.
        angle = math.radians(par["direction"])
        motion = 0.55 * amplitude * wave(1.2, 0)
        ax += motion * math.sin(angle)
        ay += motion * math.cos(angle)
        az += par["sway"] * wave(2.4, 1)
        gz += 25.0 * amplitude * wave(1.2, 2)
    elif label == "lift":
        # Motion up and down, with some side motion.
        az += 0.45 * amplitude * wave(0.8, 0)
        ax += par["sway"] * wave(0.8, 1)
        ay += par["sway"] * wave(1.6, 2)
        gx += 8.0 * wave(0.8, 3)
    else:
        # Maritime: slow motion on all axes, with rotation.
        ax += 0.30 * amplitude * wave(0.45, 0)
        ay += 0.35 * amplitude * wave(0.60, 1)
        az += 0.25 * amplitude * wave(0.50, 2)
        gx += 45.0 * amplitude * wave(0.45, 3)
        gy += 40.0 * amplitude * wave(0.60, 4)
        gz += 10.0 * wave(0.50, 5)

    # Gravity in the axes of a kit with a small tilt.
    roll = math.radians(par["roll"] * tilt)
    pitch = math.radians(par["pitch"] * tilt)
    ax += -math.sin(pitch)
    ay += np.sin(roll) * np.cos(pitch)
    az += np.cos(roll) * np.cos(pitch)

    noise = par["noise"] if label != "idle" else 0.004
    data = np.stack([ax, ay, az, gx, gy, gz], axis=1)
    data[:, 0:3] += rng.normal(0.0, noise, size=(count, 3))
    data[:, 3:6] += rng.normal(0.0, 0.6, size=(count, 3))

    # The sensor cuts each value at the limit of its range.
    data[:, 0:3] = np.clip(data[:, 0:3], -ACCEL_RANGE_G, ACCEL_RANGE_G)
    data[:, 3:6] = np.clip(data[:, 3:6], -GYRO_RANGE_DPS, GYRO_RANGE_DPS)
    return data


def csv_line(n, t_us, row):
    """Return one line in the format of the logger of the course."""
    return "%d,%d,%.4f,%.4f,%.4f,%.2f,%.2f,%.2f" % (n, t_us, *row)