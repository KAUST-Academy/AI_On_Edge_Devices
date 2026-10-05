#!/usr/bin/env python3
"""Watch the MQTT messages of one group and count the lost messages.

Runs on: the laptop or the Raspberry Pi.
Needs:   paho-mqtt 2.0 or later.

Use:
    python3 host/mqtt_check.py --broker pi-07.local --group g07
    python3 host/mqtt_check.py --broker pi-07.local --group g07 --seconds 30
    python3 host/mqtt_check.py --broker pi-07.local --group g07 --send led=1

The script subscribes to edgeai/<group>/# and prints each message. For the
topics with a "seq" field, it counts the messages and the gaps in the
sequence. A gap is a lost message.

"""

import argparse
import json
import sys
import time

import paho.mqtt.client as mqtt


class Counter:
    """Count the messages of one topic and the gaps in the sequence."""

    def __init__(self):
        self.count = 0
        self.lost = 0
        self.restarts = 0
        self.last_seq = None
        self.first_time = None
        self.last_time = None

    def add(self, seq, now):
        self.count += 1
        if self.first_time is None:
            self.first_time = now
        self.last_time = now
        if seq is not None:
            if self.last_seq is not None:
                if seq > self.last_seq + 1:
                    self.lost += seq - self.last_seq - 1
                elif seq <= self.last_seq:
                    self.restarts += 1        # the board started again
            self.last_seq = seq

    def rate(self):
        if self.count < 2 or self.last_time == self.first_time:
            return 0.0
        return (self.count - 1) / (self.last_time - self.first_time)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--broker", required=True,
                        help="host name or IP address of the broker")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--seconds", type=float, default=0,
                        help="stop after this time (default: run until Ctrl-C)")
    parser.add_argument("--send", metavar="COMMAND",
                        help="send this command to the board, then stop")
    parser.add_argument("--quiet", action="store_true",
                        help="do not print each message")
    args = parser.parse_args()

    base = "edgeai/%s" % args.group
    counters = {}

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code != 0:
            print("ERROR: the broker refused the connection: %s" % reason_code)
            return
        print("Connected to %s:%d" % (args.broker, args.port))
        client.subscribe(base + "/#", qos=1)

    def on_message(client, userdata, message):
        now = time.monotonic()
        text = message.payload.decode("utf-8", errors="replace")
        seq = None
        try:
            data = json.loads(text)
            if isinstance(data, dict) and isinstance(data.get("seq"), int):
                seq = data["seq"]
        except ValueError:
            pass
        counters.setdefault(message.topic, Counter()).add(seq, now)
        if not args.quiet:
            retained = " (retained)" if message.retain else ""
            print("%s%s  %s" % (message.topic, retained, text))

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(args.broker, args.port, keepalive=30)
    except OSError as error:
        print("ERROR: cannot connect to %s:%d: %s" % (args.broker, args.port, error))
        return 2

    if args.send:
        client.loop_start()
        info = client.publish(base + "/xiao/cmd", args.send, qos=1)
        info.wait_for_publish(timeout=5)
        print("Sent to %s/xiao/cmd: %s" % (base, args.send))
        client.loop_stop()
        client.disconnect()
        return 0

    client.loop_start()
    start = time.monotonic()
    try:
        while not args.seconds or time.monotonic() - start < args.seconds:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    client.loop_stop()
    client.disconnect()

    print()
    print("%-34s %8s %8s %8s %10s" % ("topic", "messages", "lost", "restarts",
                                      "rate 1/s"))
    total_lost = 0
    for topic in sorted(counters):
        counter = counters[topic]
        total_lost += counter.lost
        print("%-34s %8d %8d %8d %10.2f" % (topic, counter.count, counter.lost,
                                            counter.restarts, counter.rate()))
    if not counters:
        print("RESULT: FAIL - no message arrived")
        return 1
    if total_lost:
        print("RESULT: FAIL - %d message(s) lost" % total_lost)
        return 1
    print("RESULT: PASS - no gap in the sequence numbers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
