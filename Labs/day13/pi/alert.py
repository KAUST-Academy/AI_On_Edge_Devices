#!/usr/bin/env python3
"""Day 13 lab, Part D: one alert rule on the metrics of the detector.

Runs on: the Raspberry Pi 5, in the environment ~/yolo (paho-mqtt 2.x).
Use:     python alert.py --group g07 --threshold 0.612 --clear 0.655
         python alert.py --group g07 --threshold 0.612 --clear 0.655 --for-seconds 60 --xiao-led

The program subscribes to edgeai/<group>/pi/metrics (one summary each 10 s
from monitor_detect.py). For each summary it takes the value of --metric
and gives it to the rule (Task D1):

  - the mean of the last --window values (6 values: 60 s),
  - the alert fires when this mean stays below --threshold for
    --for-seconds,
  - the alert clears when this mean is above --clear (hysteresis).

At each change, the program prints one line and publishes a retained JSON
message on edgeai/<group>/pi/alert/<metric>. The dashboard shows it in its
state bar. Two copies of the program can watch two metrics.
With --xiao-led, it also sends led=1 and led=0 to the XIAO of the Day 12
lab (topic edgeai/<group>/xiao/cmd).
"""
import argparse
import collections
import json
import sys
import time


class AlertRule:
    """An alert for a low value: window, duration, and hysteresis."""

    def __init__(self, threshold, clear, window=6, for_seconds=60.0):
        self.threshold = threshold
        self.clear = clear
        self.values = collections.deque(maxlen=window)
        self.for_seconds = for_seconds
        self.active = False          # True while the alert fires
        self.below_since = None      # time of the first mean below the threshold
        self.mean = None             # the mean of the last window

    # --------------------------------------------------------- Task D1
    def update(self, t, value):
        """Add one value at the time t (seconds). Return "fire", "clear", or None.

        1. Append value to self.values. When the deque is not full, set
           self.mean = None and return None.
        2. self.mean = the mean of self.values.
        3. If the alert is not active:
           - mean below self.threshold: remember the first time (set
             self.below_since if it is None). When t - self.below_since is
             self.for_seconds or more, set self.active = True and return
             "fire".
           - else: self.below_since = None.
        4. If the alert is active and the mean is above self.clear: set
           self.active = False and self.below_since = None, and return
           "clear".
        5. Return None.
        """
        # TODO (student), Task D1: follow the five steps of the docstring.
        self.values.append(value)
        return None


def check_task():
    """Run the rule on a known sequence. Print whether Task D1 is complete."""
    seq = [0.8] * 6 + [0.4] * 12 + [0.8] * 8
    try:
        rule = AlertRule(threshold=0.6, clear=0.7, window=3, for_seconds=30)
        events = [(10 * i, rule.update(10 * i, v)) for i, v in enumerate(seq)]
        events = [(t, e) for t, e in events if e]
        ok = events == [(100, "fire"), (200, "clear")]
        # no alert for a short drop
        rule = AlertRule(threshold=0.6, clear=0.7, window=3, for_seconds=30)
        short = [rule.update(10 * i, v) for i, v in enumerate([0.8] * 6 + [0.3] * 2 + [0.8] * 6)]
        ok = ok and not any(short)
    except Exception:
        ok = False
    print("Task D1: %s" % ("complete" if ok else "not complete"))
    return ok


def main():
    parser = argparse.ArgumentParser(description="One alert rule on the metrics of the detector.")
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--broker", default="localhost")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--metric", default="confidence", help="field of the summary (confidence)")
    parser.add_argument("--threshold", type=float, required=True, help="fire below this mean")
    parser.add_argument("--clear", type=float, required=True, help="clear above this mean")
    parser.add_argument("--window", type=int, default=6, help="summaries in the mean (6: 60 s)")
    parser.add_argument("--for-seconds", type=float, default=60.0, help="duration before it fires (60)")
    parser.add_argument("--xiao-led", action="store_true", help="also switch the LED of the Day 12 XIAO")
    parser.add_argument("--seconds", type=float, default=0, help="stop after this time")
    args = parser.parse_args()

    if not check_task():
        print("Complete Task D1 first.")
        return 1
    if args.clear <= args.threshold:
        print("ERROR: --clear must be larger than --threshold (hysteresis).")
        return 2
    import paho.mqtt.client as mqtt

    rule = AlertRule(args.threshold, args.clear, args.window, args.for_seconds)
    topic = "edgeai/%s/pi/metrics" % args.group
    alert_topic = "edgeai/%s/pi/alert/%s" % (args.group, args.metric)
    led_topic = "edgeai/%s/xiao/cmd" % args.group
    counts = {"messages": 0, "fire": 0, "clear": 0}

    def state_message(state, data):
        return json.dumps({"state": state, "metric": args.metric,
                           "mean": None if rule.mean is None else round(rule.mean, 3),
                           "threshold": args.threshold, "clear": args.clear,
                           "window_s": 10 * args.window, "for_s": args.for_seconds,
                           "ts": round(time.time(), 3), "source_seq": data.get("seq")})

    def on_connect(client, userdata, flags, reason_code, properties):
        client.subscribe(topic, qos=0)
        print("Broker connected. Subscribe to %s" % topic, flush=True)

    def on_message(client, userdata, message):
        try:
            data = json.loads(message.payload.decode("utf-8"))
            value = float(data[args.metric])
        except (ValueError, KeyError, TypeError):
            return
        counts["messages"] += 1
        event = rule.update(float(data.get("ts", time.time())), value)
        if event is None:
            return
        counts[event] += 1
        state = "firing" if event == "fire" else "ok"
        client.publish(alert_topic, state_message(state, data), qos=1, retain=True)
        if args.xiao_led:
            client.publish(led_topic, "led=1" if event == "fire" else "led=0", qos=1)
        print("%s ALERT %-5s %s: mean of %d s %.3f, threshold %.3f, clear %.3f" % (
            time.strftime("%H:%M:%S"), "ON" if event == "fire" else "OFF", args.metric,
            10 * args.window, rule.mean, args.threshold, args.clear), flush=True)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                         client_id="alert-%s-%s" % (args.group, args.metric))
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(args.broker, args.port, keepalive=30)
    except OSError as error:
        print("ERROR: cannot connect to %s:%d: %s" % (args.broker, args.port, error))
        return 2
    client.publish(alert_topic, state_message("ok", {}), qos=1, retain=True)
    client.loop_start()
    print("Rule: mean of %d summaries of %s below %.3f for %.0f s; clear above %.3f" % (
        args.window, args.metric, args.threshold, args.for_seconds, args.clear), flush=True)
    start = time.monotonic()
    try:
        while not args.seconds or time.monotonic() - start < args.seconds:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    client.loop_stop()
    client.disconnect()
    print("Messages %d, alerts %d, clears %d" % (counts["messages"], counts["fire"], counts["clear"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
