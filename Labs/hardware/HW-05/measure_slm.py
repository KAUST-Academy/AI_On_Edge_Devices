#!/usr/bin/env python3
"""Measure small language models with Ollama: speed, memory, temperature.

Runs on: the Raspberry Pi 5, in the environment ~/ollama (see HW-04).
         It also runs on a laptop that has Ollama.
Needs:   the package "ollama", and a running Ollama server.

Use:
    python3 measure_slm.py --models llama3.2:1b llama3.2:3b
    python3 measure_slm.py --models llama3.2:1b --csv results.csv

For each model, the script does this:
  1. It loads the model and records the load time.
  2. It sends each prompt of prompts.txt and reads the counters of Ollama.
  3. It reads the memory of the model and the CPU temperature.

The numbers "prompt eval rate" and "eval rate" are the numbers that
"ollama run MODEL --verbose" prints.

Hardware status: tested on a laptop with Ollama. Not tested on a
Raspberry Pi (prepared on 2026-10-01).

Credits: the metrics and the first three prompts come from the lab "Small
Language Models" of "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0).
"""

import argparse
import csv
import pathlib
import statistics
import subprocess
import sys
import time

import ollama

HERE = pathlib.Path(__file__).resolve().parent
NS = 1e9   # Ollama reports each duration in nanoseconds


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
    zone = pathlib.Path("/sys/class/thermal/thermal_zone0/temp")
    try:
        return int(zone.read_text()) / 1000.0
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
            return entry.size / (1024.0 * 1024.0)
    return None


def unload(client, model):
    """Tell Ollama to remove the model from memory."""
    client.generate(model=model, prompt="", keep_alive=0)


def measure(client, model, prompts, num_predict, num_ctx):
    """Run all prompts on one model. Return a dictionary of results."""
    options = {"num_predict": num_predict, "temperature": 0, "seed": 1}
    if num_ctx:
        options["num_ctx"] = num_ctx

    free_before = memory_available_mb()
    temp_before = cpu_temperature()

    # An empty prompt loads the model and generates nothing.
    start = time.monotonic()
    client.generate(model=model, prompt="", keep_alive="10m")
    load_s = time.monotonic() - start

    prompt_rates = []
    eval_rates = []
    eval_tokens = 0
    first_answer = ""
    start = time.monotonic()
    for index, prompt in enumerate(prompts):
        reply = client.generate(model=model, prompt=prompt, options=options,
                                keep_alive="10m")
        if index == 0:
            first_answer = reply.response.strip().replace("\n", " ")
        if reply.eval_count and reply.eval_duration:
            eval_rates.append(reply.eval_count / (reply.eval_duration / NS))
            eval_tokens += reply.eval_count
        if reply.prompt_eval_count and reply.prompt_eval_duration:
            prompt_rates.append(reply.prompt_eval_count
                                / (reply.prompt_eval_duration / NS))
    run_s = time.monotonic() - start

    result = {
        "model": model,
        "prompts": len(prompts),
        "load_s": load_s,
        "run_s": run_s,
        "eval_tokens": eval_tokens,
        "eval_rate_mean": statistics.fmean(eval_rates) if eval_rates else None,
        "eval_rate_min": min(eval_rates) if eval_rates else None,
        "prompt_rate_mean": statistics.fmean(prompt_rates) if prompt_rates else None,
        "model_memory_mb": model_memory_mb(client, model),
        "free_before_mb": free_before,
        "free_loaded_mb": memory_available_mb(),
        "temp_before_c": temp_before,
        "temp_after_c": cpu_temperature(),
        "throttled": throttled(),
        "first_answer": first_answer[:80],
    }
    unload(client, model)
    return result


def show(value, pattern="%.1f"):
    return "-" if value is None else pattern % value


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--models", nargs="+",
                        default=["llama3.2:1b", "llama3.2:3b"])
    parser.add_argument("--prompts", default=str(HERE / "prompts.txt"),
                        help="file with one prompt on each line")
    parser.add_argument("--num-predict", type=int, default=128,
                        help="maximum number of generated tokens (default: 128)")
    parser.add_argument("--num-ctx", type=int, default=0,
                        help="context length in tokens (default: the model default)")
    parser.add_argument("--host", default=None,
                        help="address of the Ollama server (default: this computer)")
    parser.add_argument("--csv", help="add one row for each model to this file")
    args = parser.parse_args()

    client = ollama.Client(host=args.host) if args.host else ollama.Client()
    prompts = read_prompts(args.prompts)
    if not prompts:
        print("ERROR: no prompt in %s" % args.prompts)
        return 1

    installed = {entry.model for entry in client.list().models}
    results = []
    for model in args.models:
        if model not in installed and model + ":latest" not in installed:
            print("SKIP %s: not downloaded. Run: ollama pull %s" % (model, model))
            continue
        print("Measure %s with %d prompts ..." % (model, len(prompts)), flush=True)
        results.append(measure(client, model, prompts, args.num_predict,
                               args.num_ctx))
        time.sleep(2)   # let Ollama free the memory before the next model

    if not results:
        return 1

    print()
    print("%-18s %8s %12s %12s %10s %10s %14s" % (
        "model", "load s", "prompt tok/s", "eval tok/s", "min tok/s",
        "model MB", "temp C"))
    for r in results:
        temperature = "%s -> %s" % (show(r["temp_before_c"]), show(r["temp_after_c"]))
        print("%-18s %8s %12s %12s %10s %10s %14s" % (
            r["model"], show(r["load_s"]), show(r["prompt_rate_mean"]),
            show(r["eval_rate_mean"]), show(r["eval_rate_min"]),
            show(r["model_memory_mb"], "%.0f"), temperature))
    for r in results:
        print("%s: free memory %s MB -> %s MB, %s, first answer: %s" % (
            r["model"], show(r["free_before_mb"], "%.0f"),
            show(r["free_loaded_mb"], "%.0f"), r["throttled"] or "no vcgencmd",
            r["first_answer"]))

    if args.csv:
        path = pathlib.Path(args.csv)
        new_file = not path.exists()
        with path.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(results[0]))
            if new_file:
                writer.writeheader()
            writer.writerows(results)
        print("Results added to %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
