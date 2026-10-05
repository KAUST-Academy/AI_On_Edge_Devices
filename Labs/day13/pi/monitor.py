"""Day 13 lab, Part A: measurements, logs, and metrics of the detector.

The script pi/monitor_detect.py imports this file. It has five parts:
  1. input_stats(frame)       brightness and sharpness of one frame (Task A1)
  2. summarize(records, s)    one summary of the frames of a window (Task A2)
  3. system_metrics()         temperature, CPU, RAM, disk of the device
  4. make_logger(folder)      a JSON log with a size limit (rotation)
  5. Publisher                sends each summary with MQTT

Runs on: the Raspberry Pi 5, in the environment ~/yolo (numpy, OpenCV,
         paho-mqtt 2.x, psutil).

Credits: the brightness and sharpness statistics, the summary, the JSON log,
and the rotation follow Parts 1 and 2 of the Day 13 lecture. The message
format is the format of Labs/hardware/HW-08/metrics_publisher.py of this
course, with more fields. The temperature command comes from the lab "Small
Language Models" of "Machine Learning Systems" (mlsysbook.ai,
CC BY-NC-SA 4.0), through HW-08. All code is new code of this course.
"""
import json
import logging
import logging.handlers
import math
import os
import shutil
import subprocess
import time

import cv2
import numpy as np

try:
    import psutil
except ImportError:          # the summary works without it; RAM and CPU are None
    psutil = None


# ------------------------------------------------------------- Task A1
def input_stats(frame):
    """Return (brightness, sharpness) of one frame.

    frame: an array of height x width x 3 values (0 to 255), in the order
    blue, green, red (the order of OpenCV and of the camera of the lab).

    brightness: the mean of the grey image (0 to 255).
    sharpness:  the variance of the Laplacian of the grey image. A frame that
                is not sharp has a small value.
    Use cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) and cv2.Laplacian(grey,
    cv2.CV_64F). Return two floats.
    """
    # TODO (student), Task A1: convert the frame to grey, then return the
    # mean of the grey image and the variance of its Laplacian (two floats).
    return 0.0, 0.0


# ------------------------------------------------------------- Task A2
def percentile(values, p):
    """Nearest-rank percentile (Day 9): the smallest value with at least p
    percent of the values at or below it."""
    ordered = sorted(values)
    rank = max(1, math.ceil(p / 100.0 * len(ordered)))
    return ordered[rank - 1]


def summarize(records, seconds):
    """Return one summary (a dict) of the frame records of one window.

    records: a list of dicts, one for each frame, with the keys latency_ms,
             top_score, objects, brightness, sharpness.
    seconds: the length of the window in seconds.

    The summary has these keys:
      frames          the number of records
      fps             frames / seconds
      latency_ms      the mean of latency_ms
      latency_p95_ms  the 95th percentile of latency_ms (use percentile())
      latency_max_ms  the largest latency_ms
      confidence      the mean of top_score
      low_conf        the part of the frames with a top_score below 0.5
      objects         the mean of objects
      brightness      the mean of brightness
      sharpness       the mean of sharpness
    Round each float to 3 decimals (round(x, 3)). For an empty list, return
    {"frames": 0, "fps": 0.0}.
    """
    # TODO (student), Task A2: return the summary of the docstring.
    # Use percentile(latencies, 95) for latency_p95_ms.
    return {"frames": len(records), "fps": 0.0}


# ------------------------------------------------------- system metrics
def cpu_temperature():
    """Temperature of the processor in degrees Celsius, or None."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as handle:
            return int(handle.read().strip()) / 1000.0
    except (OSError, ValueError):
        return None


def throttled():
    """The value of `vcgencmd get_throttled` as an integer, or None."""
    try:
        text = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True,
                              text=True, timeout=2, check=True).stdout
        return int(text.strip().split("=")[1], 16)
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return None


def system_metrics(folder="."):
    """Return the system metrics of this moment (a dict)."""
    metrics = {"cpu_temp_c": cpu_temperature(), "throttled": throttled(),
               "cpu_percent": None, "ram_used_mb": None, "rss_mb": None}
    if psutil is not None:
        metrics["cpu_percent"] = psutil.cpu_percent(interval=None)
        metrics["ram_used_mb"] = round(psutil.virtual_memory().used / 1048576.0, 1)
        metrics["rss_mb"] = round(psutil.Process().memory_info().rss / 1048576.0, 1)
    usage = shutil.disk_usage(folder)
    metrics["disk_free_pct"] = round(100.0 * usage.free / usage.total, 1)
    return metrics


# --------------------------------------------------------------- the log
class JsonFormatter(logging.Formatter):
    """One JSON object on each line: ts (UTC), level, event, and the fields."""

    def format(self, record):
        data = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created))
                + ".%03dZ" % int(record.msecs),
                "level": record.levelname, "event": record.getMessage()}
        data.update(getattr(record, "fields", {}))
        return json.dumps(data, separators=(",", ":"))


def make_logger(folder, name="detector", max_bytes=1024 * 1024, backups=5):
    """A logger that writes folder/<name>.jsonl, at most 1 MB, 5 old files."""
    os.makedirs(folder, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        os.path.join(folder, name + ".jsonl"), maxBytes=max_bytes, backupCount=backups)
    handler.setFormatter(JsonFormatter())
    log = logging.getLogger("day13." + name)
    log.handlers[:] = [handler]
    log.setLevel(logging.INFO)
    log.propagate = False
    return log


# ------------------------------------------------------------ the sender
class Publisher:
    """Send each summary as one JSON message with MQTT.

    Topic edgeai/<group>/pi/metrics, the topic of HW-08. The message has the
    fields of HW-08 (seq, ts, latency_ms, fps, confidence, cpu_temp_c,
    cpu_percent, ram_used_mb) and the other fields of the summary.
    """

    def __init__(self, broker, group, port=1883, device="pi"):
        import paho.mqtt.client as mqtt
        self.topic = "edgeai/%s/%s/metrics" % (group, device)
        self.status_topic = "edgeai/%s/%s/status" % (group, device)
        self.sequence = 0
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                  client_id="monitor-%s" % group)
        self.client.will_set(self.status_topic, "offline", qos=1, retain=True)
        self.client.connect(broker, port, keepalive=15)
        self.client.loop_start()          # connects again without help
        self.client.publish(self.status_topic, "online", qos=1, retain=True)

    def publish(self, summary):
        message = {"seq": self.sequence, "ts": round(time.time(), 3)}
        message.update(summary)
        self.client.publish(self.topic, json.dumps(message), qos=0)
        self.sequence += 1
        return message

    def close(self):
        self.client.publish(self.status_topic, "offline", qos=1, retain=True)
        time.sleep(0.2)
        self.client.loop_stop()
        self.client.disconnect()


# ----------------------------------------------------- check of the tasks
def check_tasks():
    """Print whether Task A1 and Task A2 are complete. Return True if both are."""
    frame = np.zeros((40, 60, 3), dtype=np.uint8)
    frame[:, 30:] = 200                        # a dark half and a bright half
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    want_b = float(grey.mean())
    want_s = float(cv2.Laplacian(grey, cv2.CV_64F).var())
    try:
        b, s = input_stats(frame)
        a1 = abs(b - want_b) < 1e-6 and abs(s - want_s) < 1e-6
    except Exception:                          # the placeholder can fail
        a1 = False
    records = [{"latency_ms": float(v), "top_score": t, "objects": o,
                "brightness": 100.0, "sharpness": 50.0}
               for v, t, o in zip(range(1, 21), [0.9, 0.3] * 10, [1, 2] * 10)]
    want = {"frames": 20, "fps": 2.0, "latency_ms": 10.5, "latency_p95_ms": 19.0,
            "latency_max_ms": 20.0, "confidence": 0.6, "low_conf": 0.5,
            "objects": 1.5, "brightness": 100.0, "sharpness": 50.0}
    try:
        got = summarize(records, 10.0)
        a2 = all(abs(got.get(k, -1) - v) < 1e-6 for k, v in want.items())
    except Exception:
        a2 = False
    print("Task A1: %s" % ("complete" if a1 else "not complete"))
    print("Task A2: %s" % ("complete" if a2 else "not complete"))
    return a1 and a2


if __name__ == "__main__":
    check_tasks()
