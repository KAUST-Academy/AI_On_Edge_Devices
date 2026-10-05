#!/usr/bin/env python3
"""Local decision on the Raspberry Pi: keyword events to an LED command.

Day 12 lab, Part C. Runs on: the Raspberry Pi of the group, in ~/yolo.
Needs: paho-mqtt 2.0 or later, the Mosquitto broker of the Raspberry Pi.

Use:
    ~/yolo/bin/python decide.py --group g07
    ~/yolo/bin/python decide.py --group g07 --on-seconds 30 --threshold 0.8

The program subscribes to the events and the status of the XIAO and runs a
state machine with three states:

    OFF    the light is off
    ON     the light is on; it goes off 60 s after the last "yes"
    FAULT  the XIAO is offline (its last will); the light is off

For each change of state, it sends the command "led=1" or "led=0" to the
XIAO, and it publishes one decision message. Each 10 s it publishes a
summary. The forwarder of Part D sends these two message types to the cloud.

Topics (<group> is the value of --group):
    in   edgeai/<group>/xiao/result    {"seq":3,"ms":81234,"label":"yes","score":0.91}
    in   edgeai/<group>/xiao/status    "online" or "offline" (retained)
    out  edgeai/<group>/xiao/cmd       "led=1" or "led=0" (QoS 1)
    out  edgeai/<group>/pi/decision    {"seq":5,"t":1791012345.123,"state":"ON",
                                        "reason":"yes 0.91","source_seq":3}
    out  edgeai/<group>/pi/summary     {"seq":12,"t":...,"state":"OFF",
                                        "events":7,"commands":4}
    out  edgeai/<group>/pi/status      "online" or "offline" (retained, last will)

Task C1 of the lab is the function next_state(). The program checks it at
the start with a table of transitions and prints "Task C1: complete" or
"Task C1: not complete".

Credits: new work of this course. The state machine follows Part 1 of the
Day 12 lecture.
"""

import argparse
import json
import threading
import time

import paho.mqtt.client as mqtt

OFF, ON, FAULT = "OFF", "ON", "FAULT"
COMMAND = {OFF: "led=0", ON: "led=1", FAULT: "led=0"}


def next_state(state, event, now, last_yes, settings):
    """Return the next state of the light.

    state     the current state: OFF, ON, or FAULT
    event     one of these dictionaries:
                {"type": "keyword", "label": "yes", "score": 0.91}
                {"type": "status", "online": False}
                {"type": "tick"}             (the program sends one each second)
    now       the time now, in seconds (time.monotonic())
    last_yes  the time of the last accepted "yes", in seconds, or None
    settings  {"threshold": 0.8, "on_seconds": 60}

    The rules, in this order:
      1. A status "offline" gives FAULT, from each state.
      2. In FAULT, a status "online" gives OFF. Other events change nothing.
      3. A keyword with a score below the threshold changes nothing.
      4. "yes" gives ON. "no" gives OFF.
      5. In ON, a tick more than on_seconds after last_yes gives OFF.
      6. Each other event changes nothing.
    """
    # TODO (student), Task C1: apply the six rules of the docstring, in
    # their order, and return the new state (OFF, ON, or FAULT).
    # event["type"] is "keyword", "status", or "tick".
    return state


# Table of the check: (state, event, now, last_yes, expected state).
CHECKS = [
    (OFF, {"type": "keyword", "label": "yes", "score": 0.9}, 10, None, ON),
    (OFF, {"type": "keyword", "label": "yes", "score": 0.5}, 10, None, OFF),
    (ON, {"type": "keyword", "label": "no", "score": 0.9}, 10, 5, OFF),
    (ON, {"type": "keyword", "label": "unknown", "score": 0.9}, 10, 5, ON),
    (ON, {"type": "tick"}, 30, 5, ON),
    (ON, {"type": "tick"}, 70, 5, OFF),
    (OFF, {"type": "tick"}, 70, 5, OFF),
    (ON, {"type": "status", "online": False}, 10, 5, FAULT),
    (OFF, {"type": "status", "online": False}, 10, None, FAULT),
    (FAULT, {"type": "keyword", "label": "yes", "score": 0.9}, 10, None, FAULT),
    (FAULT, {"type": "status", "online": True}, 10, None, OFF),
    (ON, {"type": "status", "online": True}, 10, 5, ON),
]


def check_task(settings):
    for state, event, now, last_yes, expected in CHECKS:
        if next_state(state, event, now, last_yes, settings) != expected:
            return False
    return True


class Decider:
    def __init__(self, args):
        self.args = args
        self.settings = {"threshold": args.threshold,
                         "on_seconds": args.on_seconds}
        base = "edgeai/" + args.group
        self.t_result = base + "/xiao/result"
        self.t_status = base + "/xiao/status"
        self.t_cmd = base + "/xiao/cmd"
        self.t_decision = base + "/pi/decision"
        self.t_summary = base + "/pi/summary"
        self.t_pi_status = base + "/pi/status"
        self.state = OFF
        self.last_yes = None
        self.lock = threading.Lock()
        self.seq_decision = 0
        self.seq_summary = 0
        self.events = 0
        self.commands = 0
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                  client_id="decide-" + args.group)
        self.client.will_set(self.t_pi_status, "offline", qos=1, retain=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason, props):
        print("Connected to the broker %s" % self.args.broker, flush=True)
        client.publish(self.t_pi_status, "online", qos=1, retain=True)
        client.subscribe([(self.t_result, 1), (self.t_status, 1)])

    def on_message(self, client, userdata, msg):
        t_in = time.monotonic()
        text = msg.payload.decode("utf-8", "replace")
        if msg.topic == self.t_status:
            event = {"type": "status", "online": text == "online"}
            reason, source = "status " + text, None
        else:
            try:
                data = json.loads(text)
                event = {"type": "keyword", "label": str(data["label"]),
                         "score": float(data["score"])}
            except (ValueError, KeyError, TypeError):
                print("Dropped a bad message: %s" % text[:80], flush=True)
                return
            self.events += 1
            reason = "%s %.2f" % (event["label"], event["score"])
            source = data.get("seq")
            print("event   %-8s score %.2f  seq %s" % (
                event["label"], event["score"], source), flush=True)
        self.apply(event, reason, source, t_in)

    def apply(self, event, reason, source, t_in):
        with self.lock:
            now = time.monotonic()
            new = next_state(self.state, event, now, self.last_yes,
                             self.settings)
            if (event["type"] == "keyword" and new == ON
                    and event["label"] == "yes"
                    and event["score"] >= self.settings["threshold"]):
                self.last_yes = now
            # After the XIAO is online again, send the command of the state
            # again: a command is a state, so a second copy does no harm.
            resend = (event["type"] == "status" and event["online"])
            if new == self.state and not resend:
                return
            old, self.state = self.state, new
            self.client.publish(self.t_cmd, COMMAND[new], qos=1)
            self.commands += 1
            local_ms = (time.monotonic() - t_in) * 1000
            self.seq_decision += 1
            decision = {"seq": self.seq_decision, "t": round(time.time(), 3),
                        "state": new, "reason": reason,
                        "source_seq": source}
            self.client.publish(self.t_decision, json.dumps(decision), qos=1)
        print("state   %-5s -> %-5s  %s  command %s  (%.2f ms)" % (
            old, new, reason, COMMAND[new], local_ms), flush=True)

    def tick(self):
        """One tick each second, and one summary each 10 s."""
        last_summary = time.monotonic()
        while True:
            time.sleep(1.0)
            self.apply({"type": "tick"}, "no yes for %d s"
                       % self.settings["on_seconds"], None, time.monotonic())
            if time.monotonic() - last_summary >= self.args.summary_seconds:
                last_summary = time.monotonic()
                with self.lock:
                    self.seq_summary += 1
                    summary = {"seq": self.seq_summary,
                               "t": round(time.time(), 3),
                               "state": self.state, "events": self.events,
                               "commands": self.commands}
                    self.client.publish(self.t_summary, json.dumps(summary),
                                        qos=1)
                print("summary %s" % json.dumps(summary), flush=True)

    def run(self):
        self.client.connect(self.args.broker, self.args.port, keepalive=15)
        threading.Thread(target=self.tick, daemon=True).start()
        self.client.loop_forever()      # reconnects after a lost link


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--broker", default="localhost")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--threshold", type=float, default=0.8)
    parser.add_argument("--on-seconds", type=float, default=60.0)
    parser.add_argument("--summary-seconds", type=float, default=10.0)
    args = parser.parse_args()
    settings = {"threshold": args.threshold, "on_seconds": args.on_seconds}
    if check_task({"threshold": 0.8, "on_seconds": 60}):
        print("Task C1: complete", flush=True)
    else:
        print("Task C1: not complete. The state never changes.", flush=True)
    print("Settings: threshold %.2f, light on for %.0f s after a yes"
          % (settings["threshold"], settings["on_seconds"]), flush=True)
    try:
        Decider(args).run()
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()
