#!/usr/bin/env python3
"""Publish system metrics and model metrics of one device with MQTT.

Runs on: the Raspberry Pi 5 (environment ~/yolo), or a laptop for a test.
Needs:   paho-mqtt 2.0 or later, psutil.

Use:
    python3 metrics_publisher.py --group g07 --simulate
    python3 metrics_publisher.py --group g07 --simulate --drift-after 60

Topic:   edgeai/<group>/pi/metrics
Payload: {"seq": 12, "ts": 1790000000.5, "latency_ms": 41.3, "fps": 22.8,
          "confidence": 0.84, "cpu_temp_c": 58.2, "cpu_percent": 71.0,
          "ram_used_mb": 1830.4}

The system metrics are real. With --simulate, the model metrics (latency,
frame rate, confidence) are random numbers. They let you test a dashboard
before the detector is ready. The option --drift-after lowers the simulated
confidence after some seconds, so that you can test an alert rule.

To send the metrics of a real model, import the class MetricsPublisher:

    from metrics_publisher import MetricsPublisher
    publisher = MetricsPublisher("localhost", "g07")
    publisher.publish(latency_ms=41.3, fps=22.8, confidence=0.84)

Credits: the temperature command comes from the lab "Small Language Models"
of "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0).
"""

import argparse
import json
import pathlib
import random
import subprocess
import sys
import time

import paho.mqtt.client as mqtt
import psutil


def cpu_temperature():
    """Return the CPU temperature in degrees Celsius, or None."""
    try:
        text = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True,
                              text=True, timeout=2, check=True).stdout
        return float(text.strip().replace("temp=", "").replace("'C", ""))
    except (OSError, subprocess.SubprocessError, ValueError):
        pass
    try:
        zone = pathlib.Path("/sys/class/thermal/thermal_zone0/temp")
        return int(zone.read_text()) / 1000.0
    except (OSError, ValueError):
        return None


class MetricsPublisher:
    """Send one JSON message for each call of publish()."""

    def __init__(self, broker, group, device="pi", port=1883):
        self.topic = "edgeai/%s/%s/metrics" % (group, device)
        self.status_topic = "edgeai/%s/%s/status" % (group, device)
        self.sequence = 0
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.will_set(self.status_topic, "offline", qos=1, retain=True)
        self.client.connect(broker, port, keepalive=15)
        self.client.loop_start()          # connects again without help
        self.client.publish(self.status_topic, "online", qos=1, retain=True)
        psutil.cpu_percent(interval=None)  # start the CPU measurement

    def publish(self, latency_ms=None, fps=None, confidence=None, **more):
        """Send the model metrics and the system metrics of this moment."""
        message = {
            "seq": self.sequence,
            "ts": round(time.time(), 3),
            "latency_ms": latency_ms,
            "fps": fps,
            "confidence": confidence,
            "cpu_temp_c": cpu_temperature(),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "ram_used_mb": round(psutil.virtual_memory().used / 1048576.0, 1),
        }
        message.update(more)
        self.client.publish(self.topic, json.dumps(message), qos=0)
        self.sequence += 1
        return message

    def close(self):
        self.client.publish(self.status_topic, "offline", qos=1, retain=True)
        time.sleep(0.2)
        self.client.loop_stop()
        self.client.disconnect()


def simulated_model(elapsed, drift_after):
    """Return (latency_ms, fps, confidence) of a model that does not exist."""
    latency = random.gauss(40.0, 4.0)
    confidence = min(0.99, max(0.05, random.gauss(0.85, 0.04)))
    if drift_after and elapsed >= drift_after:
        # Drift event: the confidence goes down, the latency stays.
        confidence = min(0.99, max(0.05, random.gauss(0.45, 0.08)))
    return round(latency, 1), round(1000.0 / latency, 1), round(confidence, 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--broker", default="localhost")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--device", default="pi")
    parser.add_argument("--period", type=float, default=1.0,
                        help="seconds between two messages (default: 1)")
    parser.add_argument("--seconds", type=float, default=0,
                        help="stop after this time (default: run until Ctrl-C)")
    parser.add_argument("--simulate", action="store_true",
                        help="add random model metrics")
    parser.add_argument("--drift-after", type=float, default=0,
                        help="lower the simulated confidence after this time")
    args = parser.parse_args()

    try:
        publisher = MetricsPublisher(args.broker, args.group, args.device,
                                     args.port)
    except OSError as error:
        print("ERROR: cannot connect to %s:%d: %s" % (args.broker, args.port, error))
        return 2
    print("Publishing to %s each %.1f s" % (publisher.topic, args.period))

    start = time.monotonic()
    try:
        while not args.seconds or time.monotonic() - start < args.seconds:
            elapsed = time.monotonic() - start
            if args.simulate:
                latency, fps, confidence = simulated_model(elapsed, args.drift_after)
                message = publisher.publish(latency, fps, confidence)
            else:
                message = publisher.publish()
            print(json.dumps(message), flush=True)
            time.sleep(args.period)
    except KeyboardInterrupt:
        pass
    publisher.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
