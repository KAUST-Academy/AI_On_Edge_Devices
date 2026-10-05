#!/usr/bin/env python3
"""Day 13 lab, Part B: live dashboard in the browser for the detector metrics.

Runs on: the Raspberry Pi 5 (environment ~/yolo), or a laptop.
Needs:   paho-mqtt 2.0 or later. The web page needs no internet connection.

Use:
    python dashboard.py --group g07
    Then open http://pi-07.local:8080 in a browser.

What the program does:
  1. It subscribes to edgeai/<group>/+/metrics (one summary each 10 s from
     pi/monitor_detect.py) and to edgeai/<group>/pi/alert/+ (the rules of
     pi/alert.py).
  2. It stores each summary in a CSV file (one file for each day) in the
     folder metrics_log/.
  3. It keeps the last 15 minutes in memory.
  4. It serves one web page that draws eight metrics and updates each second.
  5. Its state bar shows the state of the alert rules of pi/alert.py: red
     while a rule fires, yellow when no summary came for 25 s.
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
FIELDS = ["ts", "device", "seq", "frames", "fps", "latency_ms", "latency_p95_ms",
          "latency_max_ms", "confidence", "low_conf", "objects", "brightness",
          "sharpness", "cpu_temp_c", "throttled", "cpu_percent", "ram_used_mb",
          "rss_mb", "disk_free_pct", "errors", "dimmed"]
HISTORY_SECONDS = 900


class Store:
    """Keep the newest messages in memory and write all messages to CSV."""

    def __init__(self, log_dir):
        self.lock = threading.Lock()
        self.rows = collections.deque()
        self.log_dir = pathlib.Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.alert_states = {}         # metric: last message of pi/alert.py
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

    def set_alert(self, message):
        with self.lock:
            self.alert_states[str(message.get("metric"))] = message

    def alert(self):
        """Return the state of the rules of pi/alert.py."""
        with self.lock:
            states = dict(self.alert_states)
        if not states:
            return {"active": False, "thresholds": {}, "text": "no alert program"}
        firing = sorted(m for m, s in states.items() if s.get("state") == "firing")
        parts = ["%s mean %s, threshold %s" % (m, s.get("mean"), s.get("threshold"))
                 for m, s in sorted(states.items())]
        return {"active": bool(firing), "firing": firing,
                "thresholds": {m: s.get("threshold") for m, s in states.items()},
                "text": ("ALERT: LOW " + ", ".join(firing).upper() if firing else "ok")
                + " (" + "; ".join(parts) + ")"}

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
    parser.add_argument("--seconds", type=float, default=0,
                        help="stop after this time (default: run until Ctrl-C)")
    args = parser.parse_args()

    store = Store(args.log_dir)
    topic = "edgeai/%s/+/metrics" % args.group
    alert_topic = "edgeai/%s/pi/alert/+" % args.group

    def on_connect(client, userdata, flags, reason_code, properties):
        print("Broker connected. Subscribe to %s and %s" % (topic, alert_topic), flush=True)
        client.subscribe([(topic, 0), (alert_topic, 1)])

    def on_message(client, userdata, message):
        try:
            data = json.loads(message.payload.decode("utf-8"))
        except ValueError:
            return
        if not isinstance(data, dict):
            return
        if message.topic.startswith(alert_topic[:-1]):
            store.set_alert(data)
        else:
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
                print("%s ALERT %s: %s" % (time.strftime("%H:%M:%S"),
                                           "ON" if state["active"] else "OFF",
                                           state["text"]), flush=True)
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
