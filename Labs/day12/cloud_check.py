#!/usr/bin/env python3
"""Count the messages of one group on the cloud broker.

Day 12 lab, Part D. Runs on: the laptop of the group.
Needs: paho-mqtt 2.0 or later.

Use:
    python3 cloud_check.py --broker 192.168.8.10 --group g07 --seconds 300

The program subscribes to edgeai/<group>/# on the cloud broker (the
instructor laptop) and prints each message that has a sequence number
"seq". A message with a time stamp "t" that is more than 5 s old is marked
"late": it waited in the queue of the forwarder. At the end, the program
prints a table for each topic: the messages, the different sequence
numbers, the lost numbers, and the double copies. The result is PASS when no
topic has a lost number.

Task D1 of the lab is the function count_sequence(). The program checks it
at the start and prints "Task D1: complete" or "Task D1: not complete".

Hardware status: new code, tested on the work computer with a broker and a
forwarder. Not tested in the lab network (prepared on 2026-10-03).
Credits: new work of this course. It extends the counter of
Labs/hardware/HW-07/host/mqtt_check.py.
"""

import argparse
import json
import threading
import time

import paho.mqtt.client as mqtt


def count_sequence(seqs):
    """Count a list of sequence numbers, in the order of arrival.

    Return a dictionary with four values:
      "received"  the number of messages (the length of the list)
      "unique"    the number of different sequence numbers
      "double"    received minus unique: the second copies
      "lost"      the numbers that are missing between the smallest and the
                  largest number of the list

    Example: [1, 2, 4, 4, 5] gives received 5, unique 4, double 1, lost 1
    (the number 3 is missing). An empty list gives four zeros.
    """
    # TODO (student), Task D1: return the dictionary of the docstring.
    # Hint: set(seqs) gives the different numbers. The lost numbers are
    # (largest - smallest + 1) minus the number of different numbers.
    return {"received": len(seqs), "unique": 0, "double": 0, "lost": 0}


def check_task():
    cases = [
        ([1, 2, 4, 4, 5], {"received": 5, "unique": 4, "double": 1, "lost": 1}),
        ([], {"received": 0, "unique": 0, "double": 0, "lost": 0}),
        ([7, 9, 8, 10], {"received": 4, "unique": 4, "double": 0, "lost": 0}),
        ([3, 3, 3], {"received": 3, "unique": 1, "double": 2, "lost": 0}),
        ([10, 14], {"received": 2, "unique": 2, "double": 0, "lost": 3}),
    ]
    try:
        return all(count_sequence(list(s)) == want for s, want in cases)
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--broker", required=True)
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--seconds", type=float, default=300.0)
    args = parser.parse_args()
    task_ok = check_task()
    print("Task D1: %s" % ("complete" if task_ok else "not complete"),
          flush=True)

    seqs, lock = {}, threading.Lock()

    def on_connect(client, userdata, flags, reason, props):
        client.subscribe("edgeai/%s/#" % args.group, qos=1)
        print("Connected to %s, topics edgeai/%s/#" % (args.broker, args.group),
              flush=True)

    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            seq = int(data["seq"])
        except (ValueError, KeyError, TypeError):
            return
        age = ""
        if isinstance(data.get("t"), (int, float)):
            late = time.time() - data["t"]
            if late > 5:
                age = "  late %.0f s" % late
        with lock:
            seqs.setdefault(msg.topic, []).append(seq)
        print("%-30s seq %5d%s" % (msg.topic, seq, age), flush=True)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                         client_id="cloud-check-" + args.group)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.broker, args.port, keepalive=30)
    client.loop_start()
    try:
        time.sleep(args.seconds)
    except KeyboardInterrupt:
        pass
    client.disconnect()
    client.loop_stop()

    print()
    print("%-30s %8s %8s %6s %6s" % ("topic", "received", "unique", "lost",
                                      "double"))
    lost = 0
    with lock:
        for topic in sorted(seqs):
            c = count_sequence(seqs[topic])
            lost += c["lost"]
            print("%-30s %8d %8d %6d %6d" % (topic, c["received"], c["unique"],
                                             c["lost"], c["double"]))
    if not task_ok:
        print("RESULT: not valid - Task D1 is not complete")
    elif not seqs:
        print("RESULT: FAIL - no message with a sequence number")
    elif lost:
        print("RESULT: FAIL - %d lost messages" % lost)
    else:
        print("RESULT: PASS - no lost message")


if __name__ == "__main__":
    main()
