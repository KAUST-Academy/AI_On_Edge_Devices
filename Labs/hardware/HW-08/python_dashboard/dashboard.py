#!/usr/bin/env python3
"""Live dashboard in the browser for the MQTT metrics of the course.

Runs on: the Raspberry Pi 5 (environment ~/yolo), or a laptop.
Needs:   paho-mqtt 2.0 or later. The web page needs no internet connection.

Use:
    python3 dashboard.py --group g07
    Then open http://pi-07.local:8080 in a browser.

What the program does:
  1. It subscribes to edgeai/<group>/+/metrics.
  2. It stores each message in a CSV file (one file for each day).
  3. It keeps the last 10 minutes in memory.
  4. It serves one web page that draws the metrics and updates each second.
  5. It applies one alert rule: the mean confidence of the last 20 messages
     is below a threshold.

Credits: the CSV log follows data_logger.py of "EdgeML with Raspberry Pi" by
Marcelo Rovai (github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0).
"""

import argparse
import collections
import csv
import json
import pathlib
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import paho.mqtt.client as mqtt

HERE = pathlib.Path(__file__).resolve().parent
FIELDS = ["ts", "device", "seq", "latency_ms", "fps", "confidence",
          "cpu_temp_c", "cpu_percent", "ram_used_mb"]
HISTORY_SECONDS = 600


class Store:
    """Keep the newest messages in memory and write all messages to CSV."""

    def __init__(self, log_dir, alert_threshold, alert_window):
        self.lock = threading.Lock()
        self.rows = collections.deque()
        self.log_dir = pathlib.Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.alert_threshold = alert_threshold
        self.alert_window = alert_window
        self.received = 0
        self.lost = 0
        self.last_seq = {}

    def add(self, device, message):
        row = {name: message.get(name) for name in FIELDS}
        row["device"] = device
        if not isinstance(row["ts"], (int, float)):
            row["ts"] = time.time()

        with self.lock:
            self.received += 1
            seq = message.get("seq")
            if isinstance(seq, int):
                last = self.last_seq.get(device)
                if last is not None and seq > last + 1:
                    self.lost += seq - last - 1
                self.last_seq[device] = seq
            self.rows.append(row)
            limit = time.time() - HISTORY_SECONDS
            while self.rows and self.rows[0]["ts"] < limit:
                self.rows.popleft()

        # One file for each day keeps each file small.
        path = self.log_dir / time.strftime("metrics_%Y-%m-%d.csv",
                                            time.localtime(row["ts"]))
        new_file = not path.exists()
        with path.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            if new_file:
                writer.writeheader()
            writer.writerow(row)

    def alert(self):
        """Return the state of the confidence alert."""
        with self.lock:
            values = [row["confidence"] for row in self.rows
                      if isinstance(row["confidence"], (int, float))]
        values = values[-self.alert_window:]
        if len(values) < self.alert_window:
            return {"active": False, "mean_confidence": None,
                    "threshold": self.alert_threshold,
                    "text": "not enough data"}
        mean = sum(values) / len(values)
        active = mean < self.alert_threshold
        return {"active": active, "mean_confidence": round(mean, 3),
                "threshold": self.alert_threshold,
                "text": "LOW CONFIDENCE" if active else "ok"}

    def snapshot(self):
        with self.lock:
            rows = list(self.rows)
            received, lost = self.received, self.lost
        age = time.time() - rows[-1]["ts"] if rows else None
        return {"rows": rows, "received": received, "lost": lost,
                "age_s": None if age is None else round(age, 1),
                "alert": self.alert()}


def make_handler(store, group):
    page = (HERE / "index.html").read_text(encoding="utf-8")
    page = page.replace("{{GROUP}}", group)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/data.json"):
                body = json.dumps(store.snapshot()).encode("utf-8")
                kind = "application/json"
            elif self.path in ("/", "/index.html"):
                body = page.encode("utf-8")
                kind = "text/html; charset=utf-8"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass                      # no line for each request

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--broker", default="localhost")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--http-port", type=int, default=8080)
    parser.add_argument("--log-dir", default="metrics_log",
                        help="folder for the CSV files (default: metrics_log)")
    parser.add_argument("--alert-threshold", type=float, default=0.6,
                        help="alert when the mean confidence is below this")
    parser.add_argument("--alert-window", type=int, default=20,
                        help="number of messages for the mean (default: 20)")
    parser.add_argument("--seconds", type=float, default=0,
                        help="stop after this time (default: run until Ctrl-C)")
    args = parser.parse_args()

    store = Store(args.log_dir, args.alert_threshold, args.alert_window)
    topic = "edgeai/%s/+/metrics" % args.group

    def on_connect(client, userdata, flags, reason_code, properties):
        print("Broker connected. Subscribe to %s" % topic, flush=True)
        client.subscribe(topic, qos=0)

    def on_message(client, userdata, message):
        try:
            data = json.loads(message.payload.decode("utf-8"))
        except ValueError:
            return
        if isinstance(data, dict):
            store.add(message.topic.split("/")[2], data)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(args.broker, args.port, keepalive=30)
    except OSError as error:
        print("ERROR: cannot connect to %s:%d: %s" % (args.broker, args.port, error))
        return 2
    client.loop_start()

    try:
        server = ThreadingHTTPServer(("0.0.0.0", args.http_port),
                                     make_handler(store, args.group))
    except OSError as error:
        print("ERROR: cannot use the port %d: %s. Select a different port "
              "with --http-port." % (args.http_port, error))
        client.loop_stop()
        return 2
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print("Dashboard: http://localhost:%d" % args.http_port, flush=True)

    start = time.monotonic()
    was_active = False
    try:
        while not args.seconds or time.monotonic() - start < args.seconds:
            time.sleep(1.0)
            state = store.alert()
            if state["active"] != was_active:
                print("%s ALERT %s: mean confidence %s, threshold %.2f" % (
                    time.strftime("%H:%M:%S"),
                    "ON" if state["active"] else "OFF",
                    state["mean_confidence"], state["threshold"]), flush=True)
                was_active = state["active"]
    except KeyboardInterrupt:
        pass
    server.shutdown()
    client.loop_stop()
    client.disconnect()
    print("Messages: %d received, %d lost" % (store.received, store.lost))
    return 0


if __name__ == "__main__":
    sys.exit(main())
