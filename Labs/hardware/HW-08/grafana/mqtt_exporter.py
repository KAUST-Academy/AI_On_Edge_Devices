#!/usr/bin/env python3
"""Bridge from MQTT to Prometheus for the metrics of the course.

Runs on: the Raspberry Pi 5 (environment ~/yolo), or a laptop.
Needs:   paho-mqtt 2.0 or later, prometheus-client.

Use:
    python3 mqtt_exporter.py --group g07
    Then open http://localhost:9200/metrics

Prometheus cannot read MQTT. It reads numbers from a web address at a fixed
interval. This program subscribes to edgeai/<group>/+/metrics and shows the
newest value of each field at /metrics. Prometheus then stores the values,
and Grafana draws them.

"""

import argparse
import json
import sys
import time

import paho.mqtt.client as mqtt
from prometheus_client import Counter, Gauge, start_http_server

LABELS = ["group", "device"]

# JSON field -> Prometheus gauge
GAUGES = {
    "latency_ms": Gauge("edgeai_latency_ms", "Inference latency in milliseconds", LABELS),
    "fps": Gauge("edgeai_fps", "Processed frames per second", LABELS),
    "confidence": Gauge("edgeai_confidence", "Confidence of the newest result", LABELS),
    "cpu_temp_c": Gauge("edgeai_cpu_temp_celsius", "CPU temperature", LABELS),
    "cpu_percent": Gauge("edgeai_cpu_percent", "CPU load in percent", LABELS),
    "ram_used_mb": Gauge("edgeai_ram_used_mb", "RAM in use in megabytes", LABELS),
}
MESSAGES = Counter("edgeai_messages_total", "Messages received", LABELS)
LOST = Counter("edgeai_messages_lost_total", "Gaps in the sequence numbers", LABELS)
LAST_SEEN = Gauge("edgeai_last_message_timestamp_seconds",
                  "Time of the newest message (Unix time)", LABELS)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--broker", default="localhost")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--http-port", type=int, default=9200,
                        help="port of the /metrics page (default: 9200)")
    parser.add_argument("--seconds", type=float, default=0,
                        help="stop after this time (default: run until Ctrl-C)")
    args = parser.parse_args()

    topic = "edgeai/%s/+/metrics" % args.group
    last_seq = {}

    def on_connect(client, userdata, flags, reason_code, properties):
        print("Broker connected. Subscribe to %s" % topic, flush=True)
        client.subscribe(topic, qos=0)

    def on_message(client, userdata, message):
        try:
            data = json.loads(message.payload.decode("utf-8"))
        except ValueError:
            return
        if not isinstance(data, dict):
            return
        device = message.topic.split("/")[2]
        labels = (args.group, device)
        for field, gauge in GAUGES.items():
            value = data.get(field)
            if isinstance(value, (int, float)):
                gauge.labels(*labels).set(value)
        MESSAGES.labels(*labels).inc()
        LOST.labels(*labels).inc(0)       # make the series, also with no loss
        LAST_SEEN.labels(*labels).set(time.time())
        seq = data.get("seq")
        if isinstance(seq, int):
            last = last_seq.get(device)
            if last is not None and seq > last + 1:
                LOST.labels(*labels).inc(seq - last - 1)
            last_seq[device] = seq

    try:
        start_http_server(args.http_port)
    except OSError as error:
        print("ERROR: cannot use the port %d: %s" % (args.http_port, error))
        return 2

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(args.broker, args.port, keepalive=30)
    except OSError as error:
        print("ERROR: cannot connect to %s:%d: %s" % (args.broker, args.port, error))
        return 2
    client.loop_start()
    print("Metrics page: http://localhost:%d/metrics" % args.http_port, flush=True)

    start = time.monotonic()
    try:
        while not args.seconds or time.monotonic() - start < args.seconds:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    client.loop_stop()
    client.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
