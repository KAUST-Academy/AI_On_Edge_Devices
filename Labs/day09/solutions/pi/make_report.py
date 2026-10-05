#!/usr/bin/env python3
"""Day 9 lab, Part D: the tables of the benchmark report.

Runs on: the laptop or the Raspberry Pi. It needs Python 3.8 or later and no
         extra package.
Use:     python pi/make_report.py
         python pi/make_report.py --period-ms 500 --battery-mah 2000
Input:   results_kit.csv   the lines "CSV,..." of the Serial Monitor (Part B)
         results_pi.csv    the rows of pi/bench.py (Part C)
         power.csv         the power of each board: active, idle, sleep
Output:  the tables on the screen and in the file report_tables.md. Copy the
         tables into report.md.

The script calculates no latency. It reads the measured values of the two
result files and adds the energy for one inference and a battery estimate.

Credits: the energy of one inference and the mean power of a duty cycle
follow Part 3 of the Day 9 lecture and the section "Battery and thermal
benchmarking" of chapter 12 "Benchmarking" of "Machine Learning Systems" by
Vijay Janapa Reddi and contributors (mlsysbook.ai, CC BY-NC-SA 4.0). The
script is new code of this course.
"""
import argparse
import csv
import os
import sys

KIT_FIELDS = ["device", "task", "precision", "model_bytes", "arena_bytes", "arena_memory",
              "cpu_mhz", "warmup", "runs", "first_us", "min_us", "median_us", "p95_us",
              "max_us", "same_as_litert", "temp_c"]
TASK_NAMES = {"kws": "Keyword spotting", "ic": "Image classification",
              "classification": "Image classification (MobileNetV2)",
              "detection": "Object detection", "custom": "Other model"}


# ----------------------------------------------------------------- the tasks
def energy_mj(power_w, latency_ms):
    """Task D1. Return the energy of one inference in millijoules.

    power_w:    the power of the board during the inference, in watts
    latency_ms: the time of one inference, in milliseconds

    Energy = power x time. 1 W x 1 ms = 1 mJ.
    """
    return power_w * latency_ms


def mean_power_w(active_w, rest_w, latency_ms, period_ms):
    """Task D2. Return the mean power of a device with a duty cycle, in watts.

    The device does one inference in each period. During the inference it
    uses active_w. For the rest of the period it uses rest_w (idle or sleep).

    duty cycle = latency / period, and not more than 1.
    mean power = duty cycle x active_w + (1 - duty cycle) x rest_w
    """
    duty = min(latency_ms / period_ms, 1.0)
    return duty * active_w + (1.0 - duty) * rest_w


def check_tasks():
    """Return the list of the tasks that are not complete."""
    missing = []
    try:
        if abs(energy_mj(0.2, 150.0) - 30.0) > 1e-9 or abs(energy_mj(5.0, 4.0) - 20.0) > 1e-9:
            missing.append("D1")
    except Exception:
        missing.append("D1")
    try:
        first = mean_power_w(0.2, 0.001, 100.0, 1000.0)        # duty cycle 0.1
        second = mean_power_w(4.0, 3.0, 2000.0, 1000.0)        # duty cycle limited to 1
        if abs(first - 0.0209) > 1e-9 or abs(second - 4.0) > 1e-9:
            missing.append("D2")
    except Exception:
        missing.append("D2")
    return missing


# ------------------------------------------------------------------- inputs
def read_kit(path):
    """Read the lines "CSV,kit,..." that the sketch kit_bench prints."""
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if "CSV," in line:                  # a Serial Monitor can add a time
                line = line[line.index("CSV,") + 4:]
            values = [value.strip() for value in line.strip().split(",")]
            if len(values) != len(KIT_FIELDS) or values[0] in ("device", ""):
                continue
            row = dict(zip(KIT_FIELDS, values))
            try:
                for key in ("model_bytes", "arena_bytes", "cpu_mhz", "warmup", "runs",
                            "first_us", "min_us", "median_us", "p95_us", "max_us"):
                    row[key] = int(row[key])
            except ValueError:
                continue
            rows.append(row)
    return rows


def read_pi(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_power(path):
    """Return {(device, state): (power in watts or None, method)}."""
    table = {}
    if not os.path.exists(path):
        return table
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                value = float(row["power_w"])
            except (TypeError, ValueError):
                value = None
            table[(row["device"].strip(), row["state"].strip())] = (value, row["method"])
    return table


def number(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def show(value, form="%.2f"):
    return "no value" if value is None else form % value


def table(header, rows):
    """Return a Markdown table as a list of lines."""
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return lines


# ------------------------------------------------------------------- report
def pi_power(row, power):
    """The active power for one row of the Raspberry Pi, and its method."""
    value, method = power.get(("pi", "active"), (None, ""))
    if value is not None:
        return value, "power.csv"
    value = number(row.get("power_w"))
    return value, "power_w of results_pi.csv" if value is not None else "no value"


def build(kit, pi, power, period_ms, battery_mah, battery_v):
    lines = ["# Tables of the benchmark report", ""]
    kit_active, kit_method = power.get(("kit", "active"), (None, ""))
    kit_idle = power.get(("kit", "idle"), (None, ""))[0]
    kit_sleep = power.get(("kit", "sleep"), (None, ""))[0]
    pi_idle = power.get(("pi", "idle"), (None, ""))[0]

    lines += ["## 1. XIAOML Kit: TensorFlow Lite Micro, the model only", ""]
    rows = []
    for row in kit:
        median_ms = row["median_us"] / 1000.0
        energy = None if kit_active is None else energy_mj(kit_active, median_ms)
        rows.append([TASK_NAMES.get(row["task"], row["task"]), row["precision"],
                     row["model_bytes"], "%d (%s)" % (row["arena_bytes"], row["arena_memory"]),
                     row["cpu_mhz"], "%d + %d" % (row["warmup"], row["runs"]),
                     "%.2f" % (row["first_us"] / 1000.0), "%.2f" % median_ms,
                     "%.2f" % (row["p95_us"] / 1000.0), row["same_as_litert"],
                     show(energy, "%.3f")])
    lines += table(["Task", "Precision", "Flash of the model in bytes",
                    "Arena in bytes (memory)", "Clock in MHz", "Warm-up + timed runs",
                    "First inference in ms", "Median in ms", "p95 in ms",
                    "Same result as LiteRT", "Energy in mJ"], rows) if rows else [
        "No row in the file of the kit."]
    lines += ["", "Power for the energy: %s W (%s)." % (show(kit_active, "%.3f"),
                                                       kit_method or "no value"), ""]

    lines += ["## 2. Raspberry Pi: the model only", ""]
    rows = []
    for row in pi:
        median_ms = number(row["median_ms"])
        watts, _ = pi_power(row, power)
        energy = None if watts is None or median_ms is None else energy_mj(watts, median_ms)
        rows.append([TASK_NAMES.get(row["task"], row["task"]), row["model"], row["runtime"],
                     row["precision"], row["threads"],
                     "%s + %s" % (row["warmup"], row["runs"]), row["first_ms"],
                     row["median_ms"], row["p95_ms"], row["peak_rss_mb"] or "no value",
                     row["temp_max_c"] or "no value", show(watts), show(energy, "%.3f")])
    lines += table(["Task", "Model file", "Runtime", "Precision", "Threads",
                    "Warm-up + timed runs", "First inference in ms", "Median in ms",
                    "p95 in ms", "Peak RAM in MB", "Highest temperature in C", "Power in W",
                    "Energy in mJ"], rows) if rows else ["No row in the file of the board."]
    lines += [""]

    lines += ["## 3. The same model file on the two boards", ""]
    rows = []
    for kit_row in kit:
        match = [row for row in pi
                 if row["task"] == kit_row["task"] and row["precision"] == kit_row["precision"]
                 and row["threads"] == "1" and row["runtime"] == "litert"]
        if not match:
            continue
        pi_row = match[-1]                      # the newest row of this model
        kit_ms = kit_row["median_us"] / 1000.0
        pi_ms = number(pi_row["median_ms"])
        watts, _ = pi_power(pi_row, power)
        kit_mj = None if kit_active is None else energy_mj(kit_active, kit_ms)
        pi_mj = None if watts is None else energy_mj(watts, pi_ms)
        ratio = None if kit_mj is None or not pi_mj else kit_mj / pi_mj
        rows.append([TASK_NAMES.get(kit_row["task"], kit_row["task"]), kit_row["precision"],
                     "%.2f" % kit_ms, "%.3f" % pi_ms, "%.0f" % (kit_ms / pi_ms),
                     show(kit_mj, "%.3f"), show(pi_mj, "%.3f"), show(ratio, "%.2f")])
    lines += table(["Task", "Precision", "Kit: median in ms", "Raspberry Pi: median in ms",
                    "Latency of the kit divided by the latency of the Raspberry Pi",
                    "Kit: energy in mJ", "Raspberry Pi: energy in mJ",
                    "Energy of the kit divided by the energy of the Raspberry Pi"],
                   rows) if rows else [
        "No model is in the two files. Run the sketch kit_bench and "
        "`python pi/bench.py --suite tiny`."]
    lines += [""]

    lines += ["## 4. Battery estimate: one keyword inference in each %d ms" % period_ms, "",
              "Battery: %d mAh at %.1f V (%.2f Wh)."
              % (battery_mah, battery_v, battery_mah * battery_v / 1000.0), ""]
    battery_wh = battery_mah * battery_v / 1000.0
    rows = []
    kws_kit = [row for row in kit if row["task"] == "kws" and row["precision"] == "int8"]
    if kws_kit and kit_active is not None:
        latency = kws_kit[-1]["median_us"] / 1000.0
        for label, rest in (("idle between two inferences", kit_idle),
                            ("light sleep between two inferences", kit_sleep)):
            if rest is None:
                continue
            mean = mean_power_w(kit_active, rest, latency, period_ms)
            rows.append(["XIAOML Kit, " + label, "%.2f" % latency,
                         "%.1f" % (100.0 * min(latency / period_ms, 1.0)),
                         "%.3f" % kit_active, "%.5f" % rest, "%.5f" % mean,
                         "%.1f" % (battery_wh / mean)])
    kws_pi = [row for row in pi if row["task"] == "kws" and row["precision"] == "int8"]
    if kws_pi and pi_idle is not None:
        latency = number(kws_pi[-1]["median_ms"])
        watts, _ = pi_power(kws_pi[-1], power)
        if watts is not None:
            mean = mean_power_w(watts, pi_idle, latency, period_ms)
            rows.append(["Raspberry Pi 5, idle between two inferences", "%.3f" % latency,
                         "%.2f" % (100.0 * min(latency / period_ms, 1.0)), "%.3f" % watts,
                         "%.5f" % pi_idle, "%.5f" % mean, "%.1f" % (battery_wh / mean)])
    lines += table(["Device and rest state", "Latency in ms", "Duty cycle in percent",
                    "Active power in W", "Rest power in W", "Mean power in W",
                    "Battery life in hours"], rows) if rows else [
        "No estimate: the int8 keyword row or a power value is missing."]
    lines += ["", "The estimate has only the inference. A real product also reads the "
              "microphone and calculates the features."]
    return lines


def main():
    parser = argparse.ArgumentParser(description="Make the tables of the Day 9 report.")
    parser.add_argument("--kit", default="results_kit.csv")
    parser.add_argument("--pi", default="results_pi.csv")
    parser.add_argument("--power", default="power.csv")
    parser.add_argument("--output", default="report_tables.md")
    parser.add_argument("--period-ms", type=int, default=1000,
                        help="one keyword inference in each period (default 1000 ms)")
    parser.add_argument("--battery-mah", type=int, default=1000,
                        help="capacity of the battery (default 1000 mAh)")
    parser.add_argument("--battery-v", type=float, default=3.7,
                        help="voltage of the battery (default 3.7 V)")
    args = parser.parse_args()

    missing = check_tasks()
    if missing:
        print("Task %s: not complete. Complete pi/make_report.py."
              % " and Task ".join(missing))
        sys.exit(1)
    print("Tasks D1 and D2: complete.")
    kit, pi, power = read_kit(args.kit), read_pi(args.pi), read_power(args.power)
    print("%d rows of the kit, %d rows of the Raspberry Pi, %d power values."
          % (len(kit), len(pi), sum(1 for value, _ in power.values() if value is not None)))
    lines = build(kit, pi, power, args.period_ms, args.battery_mah, args.battery_v)
    text = "\n".join(lines) + "\n"
    print()
    print(text)
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(text)
    print("Saved: %s" % args.output)


if __name__ == "__main__":
    main()
