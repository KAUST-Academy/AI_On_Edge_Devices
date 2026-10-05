#!/usr/bin/env python3
"""Store and forward: messages of the local broker to the cloud broker.

Day 12 lab, Part D. Runs on: the Raspberry Pi of the group, in ~/yolo.
Needs: paho-mqtt 2.0 or later, the Mosquitto broker of the Raspberry Pi, and
the broker of the instructor laptop (the "cloud").

Use:
    ~/yolo/bin/python forwarder.py --group g07 --cloud 192.168.8.10
    ~/yolo/bin/python forwarder.py --group g07 --cloud 192.168.8.10 --reset

The program subscribes on the local broker to the topics of --topics (by
default the decisions and the summaries of decide.py, and the stats of the
XIAO). It writes each message into a queue on the disk (an SQLite file),
then sends the oldest messages to the cloud broker with QoS 1. It deletes a
message from the queue only after the PUBACK of the cloud broker. When the
link to the cloud fails, the queue grows. When the link comes back, the
program sends the queue, the oldest message first. Each 5 s it prints the
queue length and the state of the link.

Rules (Section 13 of the course plan, from the Day 12 lecture):
  - The row ID has AUTOINCREMENT: SQLite does not give a new message the ID
    of a deleted message.
  - At most 20 messages in flight. The receiver drops a second copy by the
    pair (topic, seq).
  - WAL and synchronous=NORMAL: a commit does not wait for the disk.

Credits: new work of this course.
"""

import argparse
import os
import sqlite3
import threading
import time

import paho.mqtt.client as mqtt

WINDOW = 20


class Forwarder:
    def __init__(self, args):
        self.args = args
        if args.reset:
            for ext in ("", "-wal", "-shm"):
                if os.path.exists(args.db + ext):
                    os.remove(args.db + ext)
        self.db = sqlite3.connect(args.db, check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=NORMAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS queue ("
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "topic TEXT, payload BLOB, stored REAL)")
        self.db.commit()
        self.lock = threading.Lock()
        self.inflight = {}        # message ID of paho -> row ID
        self.early = set()        # message IDs acked before they were recorded
        self.sent_rows = set()    # row IDs that are in flight
        self.stored = 0
        self.forwarded = 0
        topics = [t.replace("<group>", args.group) for t in args.topics]
        self.topics = [(t, 1) for t in topics]

        self.local = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                 client_id="fwd-local-" + args.group)
        self.local.on_connect = lambda c, u, f, r, p: c.subscribe(self.topics)
        self.local.on_message = self.store

        host, _, port = args.cloud.partition(":")
        self.cloud_host, self.cloud_port = host, int(port or 1883)
        self.cloud = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                 client_id="fwd-" + args.group,
                                 clean_session=False)
        self.cloud.reconnect_delay_set(1, 5)
        self.cloud.on_publish = self.acked
        self.cloud.on_connect = self.connected
        self.cloud.on_disconnect = self.disconnected
        self.link_up = False

    def connected(self, client, userdata, flags, reason, props):
        self.link_up = True
        print("Cloud broker: connected", flush=True)

    def disconnected(self, client, userdata, flags, reason, props):
        # paho also calls this function after each failed attempt.
        if self.link_up:
            self.link_up = False
            print("Cloud broker: link lost, the queue keeps the messages",
                  flush=True)

    def store(self, client, userdata, msg):
        """Write one local message into the queue."""
        with self.lock:
            self.db.execute("INSERT INTO queue (topic, payload, stored) "
                            "VALUES (?, ?, ?)",
                            (msg.topic, bytes(msg.payload), time.time()))
            self.db.commit()
            self.stored += 1

    def acked(self, client, userdata, mid, reason, props):
        """The cloud broker has the message: delete it from the queue."""
        with self.lock:
            row = self.inflight.pop(mid, None)
            if row is None:
                self.early.add(mid)   # the PUBACK came before the record
                return
            self.delete(row)

    def delete(self, row):
        self.db.execute("DELETE FROM queue WHERE id = ?", (row,))
        self.db.commit()
        self.sent_rows.discard(row)
        self.forwarded += 1

    def queue_length(self):
        with self.lock:
            return self.db.execute("SELECT COUNT(*) FROM queue").fetchone()[0]

    def send_loop(self):
        while True:
            if not self.cloud.is_connected():
                time.sleep(0.1)
                continue
            with self.lock:
                free = WINDOW - len(self.inflight)
                rows = []
                if free > 0:
                    rows = [r for r in self.db.execute(
                        "SELECT id, topic, payload FROM queue ORDER BY id "
                        "LIMIT ?", (2 * WINDOW,))
                        if r[0] not in self.sent_rows][:free]
                    self.sent_rows.update(r[0] for r in rows)
            for row, topic, payload in rows:
                info = self.cloud.publish(topic, payload, qos=1)
                with self.lock:
                    if info.mid in self.early:
                        self.early.discard(info.mid)
                        self.delete(row)
                    else:
                        self.inflight[info.mid] = row
            time.sleep(0.01)

    def report_loop(self):
        while True:
            time.sleep(5)
            print("queue %5d  stored %6d  forwarded %6d  link %s" % (
                self.queue_length(), self.stored, self.forwarded,
                "up" if self.cloud.is_connected() else "DOWN"), flush=True)

    def run(self):
        print("Queue file: %s (%d messages from an earlier run)" % (
            self.args.db, self.queue_length()), flush=True)
        print("Topics: %s" % ", ".join(t for t, _ in self.topics), flush=True)
        host, _, port = self.args.local.partition(":")
        self.local.connect(host, int(port or 1883), keepalive=15)
        self.local.loop_start()
        self.cloud.connect_async(self.cloud_host, self.cloud_port,
                                 keepalive=10)
        self.cloud.loop_start()
        threading.Thread(target=self.send_loop, daemon=True).start()
        threading.Thread(target=self.report_loop, daemon=True).start()
        while True:
            time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--cloud", required=True,
                        help="address of the cloud broker, host or host:port")
    parser.add_argument("--local", default="localhost",
                        help="address of the local broker, host or host:port")
    parser.add_argument("--db", default="forwarder.db")
    parser.add_argument("--reset", action="store_true",
                        help="start with an empty queue")
    parser.add_argument("--topics", nargs="+", default=[
        "edgeai/<group>/pi/decision", "edgeai/<group>/pi/summary",
        "edgeai/<group>/xiao/stats"])
    args = parser.parse_args()
    try:
        Forwarder(args).run()
    except KeyboardInterrupt:
        print("Stopped. The queue file keeps the messages that were not sent.")


if __name__ == "__main__":
    main()
