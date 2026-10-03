#!/usr/bin/env python3
"""Part B of the Day 10 lab: the model calls a Python function.

Runs on: the Raspberry Pi 5 in ~/ollama, or a laptop with Ollama.
Needs:   the package "ollama", and a running Ollama server.

Use:
    python part_b/tools.py
    python part_b/tools.py --model llama3.2:3b

The model gets two tools: read_sensor and set_heater. For each request of
part_b/tool_prompts.txt, the model selects a tool and its arguments. The
function check_call (Task B2) checks the arguments before the code runs the
tool. The sensor values are simulated: this lab has no sensor.

Hardware status: not tested on hardware (prepared on 2026-10-03). Tested on
the work computer of the course with Ollama 0.32.6.

Credits: the tool-calling loop follows the chapter "SLM: Basic Optimization
Techniques" of "Edge AI Engineering" and the notebook
20-Ollama_Function_Calling_Pydantic.ipynb of "EdgeML with Raspberry Pi"
(Marcelo Rovai, GPL-3.0). The tools and the guard are new.
"""

import argparse
import os
import pathlib
import sys

import ollama

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE.parent.parent if HERE.parent.name == "solutions" else HERE.parent

ROOMS = ["kitchen", "bedroom", "garage", "office"]
HEATER_MIN, HEATER_MAX = 5, 30      # allowed set points in degrees Celsius
SENSORS = {"kitchen": (24.5, 41), "bedroom": (21.0, 48), "garage": (17.5, 63),
           "office": (19.0, 37)}      # simulated: (temperature in C, humidity in %)
HEATERS = {}

TOOLS = [
    {"type": "function", "function": {
        "name": "read_sensor",
        "description": "Read the temperature and the humidity of a room.",
        "parameters": {"type": "object", "required": ["room"],
                       "properties": {"room": {"type": "string", "enum": ROOMS}}}}},
    {"type": "function", "function": {
        "name": "set_heater",
        "description": "Set the heater of a room to a temperature in degrees Celsius.",
        "parameters": {"type": "object", "required": ["room", "celsius"],
                       "properties": {"room": {"type": "string", "enum": ROOMS},
                                      "celsius": {"type": "integer"}}}}},
]


def read_sensor(room):
    t, h = SENSORS[room]
    return "%s: %.1f degrees Celsius, %d percent humidity" % (room, t, h)


def set_heater(room, celsius):
    HEATERS[room] = celsius
    return "heater of the %s set to %d degrees Celsius" % (room, celsius)


FUNCTIONS = {"read_sensor": read_sensor, "set_heater": set_heater}


def check_call(name, arguments):
    """Task B2: check one tool call of the model before your code runs it.

    Return (True, clean_arguments) if the call is allowed, or (False, reason).
    Rules:
      - the name is a key of FUNCTIONS,
      - "room" is one of ROOMS,
      - for set_heater: "celsius" is an integer (the model can send the text
        "21") from HEATER_MIN to HEATER_MAX.
    """
    # Task B2: write the three rules here. This line allows every call.
    return True, arguments


def self_test():
    tests = [(("set_heater", {"room": "office", "celsius": "21"}), True),
             (("set_heater", {"room": "office", "celsius": 300}), False),
             (("read_sensor", {"room": "attic"}), False),
             (("open_door", {"room": "office"}), False),
             (("read_sensor", {"room": "Kitchen"}), True)]
    return all(check_call(*args)[0] == ok for args, ok in tests)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default="llama3.2:1b")
    parser.add_argument("--prompts", default=str(LAB / "part_b" / "tool_prompts.txt"))
    args = parser.parse_args()

    if not self_test():
        print("Task B2 is not complete: check_call does not follow the rules.")
        return 1
    print("Task B2: complete")

    options = {"temperature": 0, "seed": 0, "num_ctx": 2048, "num_predict": 64}
    if os.environ.get("EDGEAI_CPU"):   # the course tested on a computer with a GPU
        options["num_gpu"] = 0
    prompts = [l.strip() for l in pathlib.Path(args.prompts).read_text(encoding="utf-8").splitlines()
               if l.strip() and not l.startswith("#")]
    for prompt in prompts:
        reply = ollama.chat(model=args.model, messages=[{"role": "user", "content": prompt}],
                            tools=TOOLS, options=options, keep_alive="10m")
        calls = reply.message.tool_calls or []
        print("Request: %s" % prompt)
        if not calls:
            print("  no tool call. The model wrote: %s" % reply.message.content.strip()[:70])
        for call in calls:
            name, arguments = call.function.name, dict(call.function.arguments)
            ok, result = check_call(name, arguments)
            if ok:
                print("  %s(%s) -> %s" % (name, arguments, FUNCTIONS[name](**result)))
            else:
                print("  %s(%s) -> REFUSED: %s" % (name, arguments, result))
    print()
    print("Heaters that are set now: %s" % (HEATERS or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
