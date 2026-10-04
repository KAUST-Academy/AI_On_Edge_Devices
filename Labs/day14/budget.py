#!/usr/bin/env python3
"""Budget calculator for the capstone proposal (Day 14 lab, Part B).

It calculates the five budgets of Day 14, Part 3 of the lecture. It needs
no board and only the Python standard library.

    python3 budget.py fit --flash-kb 3264 --ram-kb 298.68 --program-kb 300 \
        --params 1534 --bits 8 --peak-values 1028
    python3 budget.py latency window=2000 model=100 decision=400 mqtt=100 \
        --limit-ms 3000
    python3 budget.py power --work-mw 217 --rest-mw 19 --work-ms 50 \
        --period-ms 2000 --radio-mw 290.4 --radio-s-per-hour 3 \
        --battery-mah 1000 --days 30
    python3 budget.py data --bytes 147 --per-second 50
    python3 budget.py cost kit=40 pi=80 camera=25 other=40 --sites 100 \
        --spares 0.15

Units: 1 KB = 1024 bytes for memory. 1 GB = 10^9 bytes for a data volume
(as in Day 12, Part 3). Mark each value that you did not measure as an
estimate in the proposal.

Credits: the method follows Day 9, Part 3 (power and battery) and Day 14,
Part 3 (budgets) of this course. New code of this course.
"""
import argparse
import sys

DAY_S = 86400


def pairs(items):
    """Read name=value pairs into a list of (name, float)."""
    out = []
    for item in items:
        if "=" not in item:
            sys.exit(f"ERROR: '{item}' is not name=value")
        name, value = item.split("=", 1)
        out.append((name, float(value)))
    return out


def fit(a):
    model_bytes = a.params * a.bits / 8
    flash_used = a.program_kb * 1024 + model_bytes
    flash = a.flash_kb * 1024
    ram_used = a.peak_values * a.bits / 8 + a.other_ram_kb * 1024
    ram = a.ram_kb * 1024
    print(f"Model file (weights only): {model_bytes:,.0f} bytes")
    print(f"Flash: {flash_used:,.0f} of {flash:,.0f} bytes "
          f"({100 * flash_used / flash:.1f} percent)")
    print(f"RAM:   {ram_used:,.0f} of {ram:,.0f} bytes "
          f"({100 * ram_used / ram:.1f} percent)")
    ok_flash, ok_ram = flash_used <= flash, ram_used <= ram
    print("Result: " + ("fits" if ok_flash and ok_ram else
                        "does not fit: " + " and ".join(
                            n for n, ok in (("flash", ok_flash), ("RAM", ok_ram))
                            if not ok)))
    return {"model_bytes": model_bytes, "flash_used": flash_used, "ram_used": ram_used,
            "fits": ok_flash and ok_ram}


def latency(a):
    stages = pairs(a.stages)
    total = sum(v for _, v in stages)
    width = max(len(n) for n, _ in stages)
    for name, value in stages:
        print(f"  {name:<{width}}  {value:10.1f} ms  ({100 * value / total:4.1f} percent)")
    print(f"Total: {total:.1f} ms")
    if a.limit_ms:
        print(f"Requirement: {a.limit_ms:.1f} ms, margin {a.limit_ms - total:.1f} ms "
              + ("(met)" if total <= a.limit_ms else "(NOT met)"))
    return {"total_ms": total}


def power(a):
    duty = a.work_ms / a.period_ms
    model_mw = duty * a.work_mw + (1 - duty) * a.rest_mw
    radio_mw = a.radio_mw * a.radio_s_per_hour / 3600
    mean_mw = model_mw + radio_mw
    battery_mwh = a.battery_mah * a.battery_v
    hours = battery_mwh / mean_mw
    print(f"Duty cycle: {100 * duty:.2f} percent")
    print(f"Mean power: {mean_mw:.3f} mW (work and rest {model_mw:.3f} mW, "
          f"radio {radio_mw:.3f} mW)")
    print(f"Rest is {100 * (1 - duty) * a.rest_mw / mean_mw:.0f} percent of the energy")
    print(f"Battery {a.battery_mah:.0f} mAh at {a.battery_v} V = {battery_mwh:.0f} mWh: "
          f"{hours:.1f} h = {hours / 24:.1f} days")
    result = {"duty": duty, "mean_mw": mean_mw, "hours": hours}
    if a.days:
        need_wh = mean_mw * 24 * a.days / 1000
        print(f"{a.days:g} days need {need_wh:.2f} Wh: "
              f"{need_wh * 1000 / a.battery_v:.0f} mAh at {a.battery_v} V")
        result["need_wh"] = need_wh
    return result


def data(a):
    per_s = a.bytes * a.per_second
    day = per_s * DAY_S
    print(f"{per_s:,.1f} bytes each second = {per_s * 8 / 1000:,.2f} kbit/s")
    print(f"One hour: {per_s * 3600 / 1e6:,.3f} MB")
    print(f"One day: {day / 1e6:,.3f} MB")
    print(f"30 days: {day * 30 / 1e9:,.3f} GB")
    return {"day_bytes": day}


def cost(a):
    items = pairs(a.items)
    site = sum(v for _, v in items)
    sets = round(a.sites * (1 + a.spares))
    for name, value in items:
        print(f"  {name:<12} {value:10.2f}")
    print(f"One site: {site:.2f}")
    print(f"{a.sites} sites and {100 * a.spares:.0f} percent of spares: {sets} sets, "
          f"{sets * site:,.2f}")
    return {"site": site, "sets": sets, "total": sets * site}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("fit", help="does a model fit the flash and the RAM?")
    s.add_argument("--flash-kb", type=float, required=True)
    s.add_argument("--ram-kb", type=float, required=True)
    s.add_argument("--program-kb", type=float, default=0.0,
                   help="flash of the program without the model")
    s.add_argument("--params", type=float, required=True)
    s.add_argument("--bits", type=float, default=8.0)
    s.add_argument("--peak-values", type=float, required=True,
                   help="peak activation memory in values (Day 1 rule), or the arena size in bytes with --bits 8")
    s.add_argument("--other-ram-kb", type=float, default=0.0)
    s.set_defaults(func=fit)

    s = sub.add_parser("latency", help="sum of the stages of one path")
    s.add_argument("stages", nargs="+", help="name=milliseconds")
    s.add_argument("--limit-ms", type=float)
    s.set_defaults(func=latency)

    s = sub.add_parser("power", help="mean power and battery life")
    s.add_argument("--work-mw", type=float, required=True)
    s.add_argument("--rest-mw", type=float, required=True)
    s.add_argument("--work-ms", type=float, required=True)
    s.add_argument("--period-ms", type=float, required=True)
    s.add_argument("--radio-mw", type=float, default=0.0)
    s.add_argument("--radio-s-per-hour", type=float, default=0.0)
    s.add_argument("--battery-mah", type=float, default=1000.0)
    s.add_argument("--battery-v", type=float, default=3.7)
    s.add_argument("--days", type=float)
    s.set_defaults(func=power)

    s = sub.add_parser("data", help="data volume of one message stream")
    s.add_argument("--bytes", type=float, required=True,
                   help="bytes of one message (147 for an IMU JSON message with IP and TCP)")
    s.add_argument("--per-second", type=float, required=True)
    s.set_defaults(func=data)

    s = sub.add_parser("cost", help="hardware cost of one site and of all sites")
    s.add_argument("items", nargs="+", help="name=price")
    s.add_argument("--sites", type=int, default=1)
    s.add_argument("--spares", type=float, default=0.0)
    s.set_defaults(func=cost)

    a = p.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    main()
