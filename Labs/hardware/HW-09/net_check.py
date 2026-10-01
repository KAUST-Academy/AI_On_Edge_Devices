#!/usr/bin/env python3
"""Check the lab network between this device and one other device.

Runs on: a laptop or a Raspberry Pi. Python 3.9 or later.
Needs:   no package for the basic checks.
         Optional: paho-mqtt for the MQTT check, the program iperf3 for the
         throughput check.

Use:
    python3 net_check.py pi-07.local
    python3 net_check.py 192.168.8.107 --mqtt --iperf
    python3 net_check.py --scan 192.168.8.0/24

Checks for one target:
  1. The name gives an IP address.
  2. The target answers to ping. The script reports the round-trip time.
  3. The TCP ports of the course are open (see PORTS below).
  4. --mqtt:  a message goes to the broker of the target and comes back.
  5. --iperf: the throughput to the target (the target runs "iperf3 -s").

A closed port is a FAIL only for the ports that you name with --need.
The other ports give INFO, because not each service runs on each day.

Hardware status: tested on one Linux computer against itself. Not tested
between two devices on the lab router (prepared on 2026-10-01).
"""

import argparse
import concurrent.futures
import ipaddress
import json
import platform
import re
import socket
import subprocess
import sys
import time

# Port -> service of the course
PORTS = {
    22: "SSH",
    1883: "MQTT broker (Mosquitto, Days 12 and 13)",
    5201: "iperf3 server (Day 11)",
    8080: "Python dashboard (Day 13)",
    8554: "RTSP server (MediaMTX, Day 11)",
    8888: "Jupyter",
    3000: "Grafana (Day 13)",
    9090: "Prometheus (Day 13)",
    11434: "Ollama (Day 10)",
}

FAILED = 0


def report(state, text):
    global FAILED
    if state == "FAIL":
        FAILED += 1
    print("%-5s %s" % (state, text), flush=True)


def resolve(target):
    """Return the IPv4 address of a name, or None."""
    try:
        infos = socket.getaddrinfo(target, None, family=socket.AF_INET)
        return infos[0][4][0]
    except OSError:
        return None


def ping(address, count=5, timeout_s=1):
    """Return (received, mean round-trip time in ms or None)."""
    if platform.system() == "Windows":
        command = ["ping", "-n", str(count), "-w", str(timeout_s * 1000), address]
    else:
        command = ["ping", "-c", str(count), "-W", str(timeout_s), address]
    try:
        output = subprocess.run(command, capture_output=True, text=True,
                                timeout=count * (timeout_s + 1) + 5).stdout
    except (OSError, subprocess.SubprocessError):
        return 0, None
    times = [float(value) for value in re.findall(r"time[=<]([0-9.]+)", output)]
    if not times:
        return 0, None
    return len(times), sum(times) / len(times)


def port_open(address, port, timeout_s=1.5):
    """Return True when a TCP connection to the port opens."""
    try:
        with socket.create_connection((address, port), timeout=timeout_s):
            return True
    except OSError:
        return False


def mqtt_round_trip(address, port, timeout_s=5):
    """Send one message to the broker and wait for it. Return ms or None."""
    try:
        import paho.mqtt.client as mqtt
    except ImportError:
        return "no paho-mqtt"

    topic = "edgeai/netcheck/%s/%d" % (socket.gethostname(), int(time.time()))
    state = {"sent": None, "delay": None}

    def on_connect(client, userdata, flags, reason_code, properties):
        client.subscribe(topic, qos=1)

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        state["sent"] = time.monotonic()
        client.publish(topic, "ping", qos=1)

    def on_message(client, userdata, message):
        if state["sent"] is not None and state["delay"] is None:
            state["delay"] = (time.monotonic() - state["sent"]) * 1000.0

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    try:
        client.connect(address, port, keepalive=10)
    except OSError:
        return None
    client.loop_start()
    end = time.monotonic() + timeout_s
    while state["delay"] is None and time.monotonic() < end:
        time.sleep(0.02)
    client.loop_stop()
    client.disconnect()
    return state["delay"]


def iperf(address, port, seconds):
    """Return the throughput in Mbit/s, or a text with the reason."""
    command = ["iperf3", "-c", address, "-p", str(port), "-t", str(seconds), "-J"]
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=seconds + 15)
    except FileNotFoundError:
        return "iperf3 is not installed on this device"
    except subprocess.SubprocessError:
        return "iperf3 did not end"
    try:
        data = json.loads(result.stdout)
    except ValueError:
        return "iperf3 gave no result"
    if "error" in data:
        return data["error"]
    return data["end"]["sum_received"]["bits_per_second"] / 1e6


def scan(network_text):
    """Ping each address of a network. Print the devices that answer."""
    network = ipaddress.ip_network(network_text, strict=False)
    hosts = [str(host) for host in network.hosts()]
    if len(hosts) > 1024:
        print("ERROR: the network has %d addresses. Use /22 or smaller." % len(hosts))
        return 1
    print("Scan of %s: %d addresses" % (network, len(hosts)), flush=True)

    def one(address):
        received, mean = ping(address, count=1, timeout_s=1)
        return address, received, mean

    found = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as pool:
        for address, received, mean in pool.map(one, hosts):
            if received:
                found += 1
                try:
                    name = socket.gethostbyaddr(address)[0]
                except OSError:
                    name = "-"
                print("%-16s %7.1f ms  %s" % (address, mean, name), flush=True)
    print("Devices that answer: %d" % found)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", nargs="?",
                        help="name or IP address, for example pi-07.local")
    parser.add_argument("--scan", metavar="NETWORK",
                        help="find the devices of a network, for example 192.168.8.0/24")
    parser.add_argument("--need", type=int, nargs="*", default=[22],
                        help="ports that must be open (default: 22)")
    parser.add_argument("--mqtt", action="store_true", help="do the MQTT check")
    parser.add_argument("--mqtt-port", type=int, default=1883)
    parser.add_argument("--iperf", action="store_true",
                        help="measure the throughput with iperf3")
    parser.add_argument("--iperf-port", type=int, default=5201)
    parser.add_argument("--iperf-seconds", type=int, default=5)
    args = parser.parse_args()

    if args.scan:
        return scan(args.scan)
    if not args.target:
        parser.error("give a target or --scan")

    print("From %s to %s" % (socket.gethostname(), args.target))

    address = resolve(args.target)
    if address is None:
        report("FAIL", "Name: %s gives no IP address" % args.target)
        print("RESULT: FAIL - 1 check failed")
        return 1
    report("PASS", "Name: %s is %s" % (args.target, address))

    received, mean = ping(address)
    if received:
        report("PASS", "Ping: %d of 5 answers, mean %.1f ms" % (received, mean))
    else:
        report("FAIL", "Ping: no answer. Check the client isolation of the router.")

    for port in sorted(PORTS):
        is_open = port_open(address, port)
        if is_open:
            report("PASS", "Port %5d open:   %s" % (port, PORTS[port]))
        elif port in args.need:
            report("FAIL", "Port %5d closed: %s" % (port, PORTS[port]))
        else:
            report("INFO", "Port %5d closed: %s" % (port, PORTS[port]))

    if args.mqtt:
        delay = mqtt_round_trip(address, args.mqtt_port)
        if delay == "no paho-mqtt":
            report("INFO", "MQTT: paho-mqtt is not installed on this device")
        elif delay is None:
            report("FAIL", "MQTT: no round trip through %s:%d" % (address, args.mqtt_port))
        else:
            report("PASS", "MQTT: round trip in %.1f ms" % delay)

    if args.iperf:
        value = iperf(address, args.iperf_port, args.iperf_seconds)
        if isinstance(value, float):
            report("PASS", "iperf3: %.1f Mbit/s to the target" % value)
        else:
            report("FAIL", "iperf3: %s" % value)

    if FAILED:
        print("RESULT: FAIL - %d check(s) failed" % FAILED)
    else:
        print("RESULT: PASS")
    return FAILED


if __name__ == "__main__":
    sys.exit(main())
