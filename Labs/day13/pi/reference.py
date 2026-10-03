#!/usr/bin/env python3
"""Day 13 lab, Part C: a threshold from a reference period.

Runs on: the Raspberry Pi 5 or the laptop. Needs only Python 3.
Use:     python3 reference.py --csv ../dashboard/metrics_log/metrics_2026-10-05.csv --last-minutes 10
         python3 reference.py --csv FILE --start 10:20 --end 10:30 --metric brightness

The dashboard writes one row for each summary of the detector (one each
10 s) into a CSV file for each day. This script takes the rows of the
reference period, makes the means of `--window` rows in a row (6 rows: 60 s,
the window of the alert rule), and gives the threshold mean - 3 standard
deviations of these means (Task C1). It also prints how many windows of the
reference period are below the threshold, and the command for alert.py.

A reference with almost no variation (a still scene, or the same images
again and again) gives a threshold very near the mean: a small normal change
then fires the alert. The script warns when 3 standard deviations are less
than 5 percent of the mean. Then record a longer reference with normal
activity, or give a minimum distance with --min-margin (for example 0.05 for
the confidence). With a margin m, the threshold is mean - m and the clear
value is mean - m / 3.

The reference period must be a normal period: the usual light, the usual
objects in front of the camera, and no person who moves the camera.

Hardware status: not tested on hardware (prepared on 2026-10-03). The script
ran on the work computer of the course with the CSV file of a test.

Credits: the method follows Part 3 of the Day 13 lecture of this course. All
code is new code of this course.
"""
import argparse
import csv
import statistics
import sys
import time


# ------------------------------------------------------------- Task C1
def threshold_from_history(values, window, k=3.0):
    """Return a dict with the threshold of an alert rule for low values.

    values: the values of the reference period, in time order.
    window: the number of values in one mean (the window of the rule).

    1. Make the means of `window` values in a row: one mean for each end
       position, so len(values) - window + 1 means.
    2. mean = the mean of these means; sd = their standard deviation
       (statistics.stdev).
    3. threshold = mean - k * sd; clear = mean - 1 * sd (the value that
       ends the alert: hysteresis).
    Return {"means": [...], "mean": ..., "sd": ..., "threshold": ...,
    "clear": ...}.
    """
    # TODO (student), Task C1: make the means of `window` values in a row,
    # then return the dictionary of the docstring.
    return {"means": [], "mean": 0.0, "sd": 0.0, "threshold": 0.0, "clear": 0.0}


def check_task():
    values = [0.70, 0.74, 0.72, 0.76, 0.71, 0.75, 0.73, 0.77]
    try:
        got = threshold_from_history(values, 2)
        ok = (len(got["means"]) == 7 and abs(got["means"][0] - 0.72) < 1e-9
              and abs(got["mean"] - 0.735) < 1e-9
              and abs(got["threshold"] - (got["mean"] - 3 * got["sd"])) < 1e-9
              and abs(got["sd"] - statistics.stdev(got["means"])) < 1e-9
              and abs(got["clear"] - (got["mean"] - got["sd"])) < 1e-9)
    except Exception:
        ok = False
    print("Task C1: %s" % ("complete" if ok else "not complete"))
    return ok


def read_rows(path, metric):
    rows = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                rows.append((float(row["ts"]), float(row[metric])))
            except (KeyError, TypeError, ValueError):
                continue                  # a row with no value of the metric
    return rows


def clock(text, day):
    hour, minute = (int(x) for x in text.split(":"))
    return time.mktime(day[:3] + (hour, minute, 0, 0, 0, -1))


def main():
    parser = argparse.ArgumentParser(description="A threshold from a reference period.")
    parser.add_argument("--csv", required=True, help="CSV file of the dashboard")
    parser.add_argument("--metric", default="confidence", help="column (default confidence)")
    parser.add_argument("--window", type=int, default=6, help="rows in one mean (default 6: 60 s)")
    parser.add_argument("--k", type=float, default=3.0, help="number of standard deviations (3)")
    parser.add_argument("--last-minutes", type=float, default=0, help="the last N minutes of the file")
    parser.add_argument("--start", help="start of the period, HH:MM (local time)")
    parser.add_argument("--end", help="end of the period, HH:MM (local time)")
    parser.add_argument("--min-margin", type=float, default=0.0,
                        help="smallest distance of the threshold from the mean (default 0)")
    parser.add_argument("--group", default="gNN", help="group name for the printed command")
    args = parser.parse_args()

    if not check_task():
        print("Complete Task C1 first.")
        return 1
    rows = read_rows(args.csv, args.metric)
    if not rows:
        print("ERROR: no row with the column %s in %s" % (args.metric, args.csv))
        return 2
    if args.start and args.end:
        day = time.localtime(rows[0][0])
        lo, hi = clock(args.start, day), clock(args.end, day)
    elif args.last_minutes:
        hi = rows[-1][0]
        lo = hi - 60 * args.last_minutes
    else:
        lo, hi = rows[0][0], rows[-1][0]
    values = [v for t, v in rows if lo <= t <= hi]
    if len(values) < args.window + 2:
        print("ERROR: only %d rows in the period. Record a longer reference period." % len(values))
        return 2

    result = threshold_from_history(values, args.window, args.k)
    margin = result["mean"] - result["threshold"]
    if margin < 0.05 * abs(result["mean"]):
        print("WARNING: the reference has almost no variation (%.0f sd = %.4f). A small"
              " normal change fires the alert. Record a longer reference with normal"
              " activity, or use --min-margin." % (args.k, margin))
    if args.min_margin > margin:
        margin = args.min_margin
        result["threshold"] = result["mean"] - margin
        result["clear"] = result["mean"] - margin / 3.0
        print("Margin: %.3f from --min-margin" % margin)
    below = sum(m < result["threshold"] for m in result["means"])
    print("Reference: %d rows from %s to %s, metric %s" % (
        len(values), time.strftime("%H:%M:%S", time.localtime(lo)),
        time.strftime("%H:%M:%S", time.localtime(hi)), args.metric))
    print("Rows:      mean %.3f  sd %.3f  min %.3f  max %.3f" % (
        statistics.mean(values), statistics.stdev(values), min(values), max(values)))
    print("Means of %d rows: %d means, mean %.3f  sd %.3f" % (
        args.window, len(result["means"]), result["mean"], result["sd"]))
    print("Threshold: %.3f   clear: %.3f   (mean - %.3f, mean - %.3f)" % (
        result["threshold"], result["clear"], result["mean"] - result["threshold"],
        result["mean"] - result["clear"]))
    print("Means of the reference below the threshold: %d of %d" % (below, len(result["means"])))
    print("Command: python alert.py --group %s --metric %s --threshold %.3f --clear %.3f --window %d"
          % (args.group, args.metric, result["threshold"], result["clear"], args.window))
    return 0


if __name__ == "__main__":
    sys.exit(main())
