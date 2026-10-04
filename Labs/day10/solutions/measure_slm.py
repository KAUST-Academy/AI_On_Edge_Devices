#!/usr/bin/env python3
"""Part A of the Day 10 lab: measure small language models with Ollama.

Runs on: the Raspberry Pi 5, in the environment ~/ollama (Labs/hardware/HW-04).
         It also runs on a laptop that has Ollama.
Needs:   the Python package "ollama", and a running Ollama server.

Use:
    python measure_slm.py                                  both models
    python measure_slm.py --models llama3.2:1b --num-thread 2
    python measure_slm.py --memory-only --models llama3.2:3b --num-ctx 8192

The method follows the Day 9 lab:
  1. One request loads the model. The script does not count it.
  2. One request to warm up. The script does not count it.
  3. The timed requests: each prompt of prompts.txt, --runs times.
  4. The statistic: the median of the rates. The script also prints the
     lowest rate and the mean number of prompt tokens.
  5. The window: the counters of Ollama. They measure the model only, not
     the HTTP time and not the Python time.
The context and the threads are set in each request (Part 2 of the lecture).

Task A1 is in the function token_rate.

Hardware status: not tested on hardware (prepared on 2026-10-03). Tested on
the work computer of the course with Ollama 0.32.6.

Credits: the metrics and prompts 1 to 3 come from the lab "Small Language
Models" of "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0). The
script grows from Labs/hardware/HW-05/measure_slm.py of this course.
"""

import argparse
import csv
import os
import pathlib
import statistics
import subprocess
import sys
import time

import ollama

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE.parent if HERE.name == "solutions" else HERE
NS = 1e9   # Ollama gives each duration in nanoseconds


def token_rate(count, duration_ns):
    """Task A1: return the rate in tokens for each second.

    count:       a number of tokens, for example eval_count
    duration_ns: the time of these tokens in nanoseconds, for example
                 eval_duration
    Return None if the count or the duration is 0 or None.
    """
    if not count or not duration_ns:
        return None
    return count / (duration_ns / NS)


def read_prompts(path):
    """Return the prompts of the file. Skip comments and empty lines."""
    prompts = []
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            prompts.append(line)
    return prompts


def cpu_temperature():
    """Return the CPU temperature in degrees Celsius, or None."""
    try:
        text = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True,
                              text=True, timeout=5, check=True).stdout
        return float(text.strip().replace("temp=", "").replace("'C", ""))
    except (OSError, subprocess.SubprocessError, ValueError):
        pass
    try:
        text = pathlib.Path("/sys/class/thermal/thermal_zone0/temp").read_text()
        return int(text) / 1000.0
    except (OSError, ValueError):
        return None


def throttled():
    """Return the text of "vcgencmd get_throttled", or None."""
    try:
        return subprocess.run(["vcgencmd", "get_throttled"], capture_output=True,
                              text=True, timeout=5, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def memory_available_mb():
    """Return the available system memory in MB (Linux), or None."""
    try:
        for line in pathlib.Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) / 1024.0
    except OSError:
        pass
    return None


def model_memory_mb(client, model):
    """Return the memory that Ollama reports for the loaded model, in MB."""
    for entry in client.ps().models:
        if entry.model == model or entry.name == model:
            return entry.size / 1e6
    return None


def make_options(args):
    """The options of each request. Give the context and the threads."""
    options = {"num_predict": args.num_predict, "num_ctx": args.num_ctx,
               "temperature": 0, "seed": 0}
    if args.num_thread:
        options["num_thread"] = args.num_thread
    # The course tested the script on a computer with a GPU.
    # EDGEAI_CPU=1 keeps the model on the CPU, as on the Raspberry Pi.
    if os.environ.get("EDGEAI_CPU"):
        options["num_gpu"] = 0
    return options


def measure(client, model, prompts, args):
    """Run the method of the module docstring on one model."""
    options = make_options(args)
    free_before = memory_available_mb()
    temp_before = cpu_temperature()

    start = time.monotonic()
    client.generate(model=model, prompt="Hello.", options=dict(options, num_predict=1),
                    keep_alive="10m")
    load_s = time.monotonic() - start
    client.generate(model=model, prompt=prompts[0], options=options, keep_alive="10m")

    prompt_rates, eval_rates, prompt_tokens = [], [], []
    temp_max = temp_before
    for _ in range(args.runs):
        for prompt in prompts:
            reply = client.generate(model=model, prompt=prompt, options=options,
                                    keep_alive="10m")
            p = token_rate(reply.prompt_eval_count, reply.prompt_eval_duration)
            e = token_rate(reply.eval_count, reply.eval_duration)
            if p is not None:
                prompt_rates.append(p)
                prompt_tokens.append(reply.prompt_eval_count)
            if e is not None:
                eval_rates.append(e)
            t = cpu_temperature()
            if t is not None and (temp_max is None or t > temp_max):
                temp_max = t

    result = {
        "model": model,
        "num_ctx": args.num_ctx,
        "num_thread": args.num_thread or "default",
        "requests": len(eval_rates),
        "load_s": round(load_s, 2),
        "prompt_tokens_mean": round(statistics.fmean(prompt_tokens), 1) if prompt_tokens else None,
        "prompt_rate_median": round(statistics.median(prompt_rates), 2) if prompt_rates else None,
        "eval_rate_median": round(statistics.median(eval_rates), 2) if eval_rates else None,
        "eval_rate_min": round(min(eval_rates), 2) if eval_rates else None,
        "model_mb": round(model_memory_mb(client, model) or 0),
        "free_before_mb": round(free_before) if free_before else None,
        "free_loaded_mb": round(memory_available_mb() or 0),
        "temp_before_c": temp_before,
        "temp_max_c": temp_max,
        "throttled": throttled() or "no vcgencmd",
    }
    client.generate(model=model, prompt="", keep_alive=0)
    return result


def memory_only(client, model, args):
    """Load the model with the context of --num-ctx and read its memory."""
    options = make_options(args)
    client.generate(model=model, prompt="", keep_alive=0)
    time.sleep(2)
    client.generate(model=model, prompt="Hello.", options=dict(options, num_predict=1),
                    keep_alive="10m")
    mb = model_memory_mb(client, model)
    client.generate(model=model, prompt="", keep_alive=0)
    return mb


def show(value):
    return "-" if value is None else str(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--models", nargs="+", default=["llama3.2:1b", "llama3.2:3b"])
    parser.add_argument("--prompts", default=str(LAB / "prompts.txt"))
    parser.add_argument("--runs", type=int, default=2,
                        help="timed runs of each prompt (default: 2)")
    parser.add_argument("--num-predict", type=int, default=128,
                        help="largest number of generated tokens (default: 128)")
    parser.add_argument("--num-ctx", type=int, default=2048,
                        help="context length in tokens (default: 2048)")
    parser.add_argument("--num-thread", type=int, default=0,
                        help="threads (default: the choice of Ollama)")
    parser.add_argument("--memory-only", action="store_true",
                        help="only load each model and print its memory")
    parser.add_argument("--csv", default=str(LAB / "results.csv"),
                        help="add one row for each model to this file")
    args = parser.parse_args()

    if token_rate(100, 2 * NS) != 50 or token_rate(0, NS) is not None:
        print("Task A1 is not complete: token_rate(100, 2e9) must be 50.0.")
        return 1
    print("Task A1: complete")

    client = ollama.Client()
    installed = {entry.model for entry in client.list().models}
    models = [m for m in args.models if m in installed or m + ":latest" in installed]
    for m in args.models:
        if m not in models:
            print("SKIP %s: not downloaded. Run: ollama pull %s" % (m, m))
    if not models:
        return 1

    if args.memory_only:
        for m in models:
            mb = memory_only(client, m, args)
            print("%-14s num_ctx %6d: model memory %s MB" % (m, args.num_ctx, show(round(mb) if mb else None)))
        return 0

    prompts = read_prompts(args.prompts)
    results = []
    for m in models:
        print("Measure %s: %d prompts x %d runs, num_ctx %d, threads %s ..."
              % (m, len(prompts), args.runs, args.num_ctx, args.num_thread or "default"), flush=True)
        results.append(measure(client, m, prompts, args))
        time.sleep(2)

    print()
    print("%-13s %7s %6s %9s %11s %10s %9s %8s %13s" % (
        "model", "threads", "load s", "prompt tk", "prompt tk/s", "eval tk/s",
        "min tk/s", "model MB", "temp C"))
    for r in results:
        print("%-13s %7s %6s %9s %11s %10s %9s %8s %13s" % (
            r["model"], r["num_thread"], show(r["load_s"]), show(r["prompt_tokens_mean"]),
            show(r["prompt_rate_median"]), show(r["eval_rate_median"]), show(r["eval_rate_min"]),
            show(r["model_mb"]), "%s -> %s" % (show(r["temp_before_c"]), show(r["temp_max_c"]))))
    for r in results:
        print("%s: free memory %s MB -> %s MB with the model, %s"
              % (r["model"], show(r["free_before_mb"]), show(r["free_loaded_mb"]), r["throttled"]))

    path = pathlib.Path(args.csv)
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        if new_file:
            writer.writeheader()
        writer.writerows(results)
    print("Results added to %s" % path.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
