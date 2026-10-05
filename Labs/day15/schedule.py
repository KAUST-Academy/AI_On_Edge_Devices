#!/usr/bin/env python3
"""Demonstration schedule for the capstone (Day 15 lab, Part B).

The instructor publishes the schedule on Day 14. This script makes it from
a list of teams. It needs only the Python standard library.

    python3 schedule.py --start 13:00 --minutes 10 --part-minutes 70 \
        "Machine monitor" "Room counter" "Lab assistant"
    python3 schedule.py --start 13:00 --teams-file teams.txt --seed 1

Each slot has the demonstration time (default 10 minutes, as in the
syllabus) and a change time between two teams (default 0). With --seed, the
order is random but the same for the same seed. The script prints a
Markdown table and warns when the slots do not fit the time of Part B.
"""
import argparse
import random
import sys


def minutes(hhmm):
    hours, mins = hhmm.split(":")
    return int(hours) * 60 + int(mins)


def clock(total):
    return "%02d:%02d" % (total // 60 % 24, total % 60)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("teams", nargs="*", help="team names")
    p.add_argument("--teams-file", help="a text file with one team on each line")
    p.add_argument("--start", default="13:00", help="start of Part B, HH:MM")
    p.add_argument("--minutes", type=int, default=10, help="minutes for each team")
    p.add_argument("--change", type=int, default=0, help="minutes between two teams")
    p.add_argument("--part-minutes", type=int, default=70, help="length of Part B")
    p.add_argument("--seed", type=int, help="shuffle the order with this seed")
    a = p.parse_args(argv)

    teams = list(a.teams)
    if a.teams_file:
        with open(a.teams_file, encoding="utf-8") as handle:
            teams += [line.strip() for line in handle if line.strip()]
    if not teams:
        sys.exit("ERROR: no team. Give the names, or --teams-file.")
    if a.seed is not None:
        random.Random(a.seed).shuffle(teams)

    start = minutes(a.start)
    print("| Slot | Start | End | Team |")
    print("|---|---|---|---|")
    t = start
    for number, team in enumerate(teams, 1):
        print(f"| {number} | {clock(t)} | {clock(t + a.minutes)} | {team} |")
        t += a.minutes + a.change
    used = t - a.change - start
    print()
    print(f"{len(teams)} teams, {used} minutes of {a.part_minutes} minutes of Part B.")
    if used > a.part_minutes:
        fit = (a.part_minutes + a.change) // (a.minutes + a.change)
        print(f"WARNING: the slots need {used - a.part_minutes} minutes more than Part B. "
              f"Part B holds {fit} teams. Use two rooms, shorter slots, or start some "
              f"demonstrations in Part A.")
    return used


if __name__ == "__main__":
    main()
