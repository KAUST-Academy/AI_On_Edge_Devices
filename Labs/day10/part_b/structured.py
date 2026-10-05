#!/usr/bin/env python3
"""Part B of the Day 10 lab: structured output with a schema.

Runs on: the Raspberry Pi 5 in ~/ollama, or a laptop with Ollama.
Needs:   the packages "ollama" and "pydantic", and a running Ollama server.

Use:
    python part_b/structured.py                       llama3.2:1b, with a schema
    python part_b/structured.py --model llama3.2:3b
    python part_b/structured.py --no-schema           the prompt only

The script converts each command of part_b/commands.txt into a JSON object
with three fields. It checks each answer with the Pydantic class Command and
compares it with the correct answer.

Task B1 is in the class Command.
"""

import argparse
import os
import pathlib
import sys
import time
from typing import Literal

import ollama
from pydantic import BaseModel, ValidationError

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE.parent.parent if HERE.parent.name == "solutions" else HERE.parent

PROMPT = ("You control a home. Convert the command into a JSON object with the keys "
          "\"device\" (one of lamp, fan, heater, door, pump), \"action\" (one of on, off, "
          "open, close), and \"room\" (one of kitchen, bedroom, garage, office). "
          "Reply with the JSON object only.\nCommand: %s")


class Command(BaseModel):
    """Task B1: the three fields of a command, with their allowed values.

    Use Literal[...] for each field, with the values of PROMPT.
    """
    # Task B1: replace each str with Literal[...] and the allowed values.
    device: str
    action: str
    room: str


def read_commands(path):
    rows = []
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            text, device, action, room = [x.strip() for x in line.split("|")]
            rows.append((text, {"device": device, "action": action, "room": room}))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default="llama3.2:1b")
    parser.add_argument("--commands", default=str(LAB / "part_b" / "commands.txt"))
    parser.add_argument("--no-schema", action="store_true", help="send the prompt only")
    args = parser.parse_args()

    if not Command.model_json_schema().get("properties", {}).get("room", {}).get("enum"):
        print("Task B1 is not complete: give each field of Command its allowed values.")
        return 1
    print("Task B1: complete")

    options = {"temperature": 0, "seed": 0, "num_ctx": 2048, "num_predict": 64}
    if os.environ.get("EDGEAI_CPU"):   # the course tested on a computer with a GPU
        options["num_gpu"] = 0
    schema = None if args.no_schema else Command.model_json_schema()
    rows = read_commands(args.commands)
    valid = correct = 0
    times = []
    for text, expected in rows:
        start = time.monotonic()
        reply = ollama.generate(model=args.model, prompt=PROMPT % text, format=schema,
                                options=options, keep_alive="10m")
        times.append(time.monotonic() - start)
        try:
            got = Command.model_validate_json(reply.response).model_dump()
            valid += 1
            ok = got == expected
            correct += ok
            mark = "correct" if ok else "WRONG, expected %s %s %s" % (
                expected["device"], expected["action"], expected["room"])
            answer = "%s %s %s" % (got["device"], got["action"], got["room"])
        except ValidationError:
            answer, mark = "not valid: " + reply.response.strip().replace("\n", " ")[:60], ""
        print("%-48s -> %-24s %s" % (text[:48], answer, mark))
    print()
    print("Model %s, %s: valid %d of %d, correct %d of %d, median time %.1f s"
          % (args.model, "prompt only" if args.no_schema else "with the schema",
             valid, len(rows), correct, len(rows), sorted(times)[len(times) // 2]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
