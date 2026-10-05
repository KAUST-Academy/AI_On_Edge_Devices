#!/usr/bin/env python3
"""Day 9 lab, Part C: one benchmark harness for the Raspberry Pi 5.

Runs on: the Raspberry Pi 5, from the folder ~/edgeai/day09/.
         Suites "classification" and "tiny": the environment ~/tflite_env.
         Suite "detection": the environment ~/yolo, which has the package ncnn.
         The script also runs on a laptop with the same packages.
Use:     python pi/bench.py --suite classification
         python pi/bench.py --suite detection
         python pi/bench.py --suite tiny
         python pi/bench.py --model FILE --threads 1 4 --warmup 20 --runs 200
         python pi/bench.py --sustain 180 --model FILE --threads 4
         python pi/bench.py --idle 30
Output:  one line for each case, one new row for each case in the file
         results_pi.csv, and one JSON file for each case in the folder raw/
         with each measured time.

A case is one model file with one runtime and one number of threads. The
script starts a new process for each case, so that the load time, the first
inference, and the peak memory belong to this case only. In each case:

    1. Load the model and make one fixed input.
    2. Measure the first inference alone.
    3. Do the other warm-up inferences with no measurement.
    4. Measure each of the timed inferences with time.perf_counter_ns().
    5. Read the temperature and the clock of the processor before the timed
       runs, between them, and after them. A read is never in a timed run.

The timed window is the call of the runtime: the model only. The input is
ready before the clock starts.

The suites use the model files of the earlier labs:

    classification   ../day07/models/   MobileNetV2: LiteRT and ONNX Runtime,
                                        float32 and int8
    detection        ../day08/models/   your detector at 320 pixels: NCNN and
                                        LiteRT, float32 and int8
    tiny             models/            the four models of the kit sketch,
                                        with the test input of the sketch

Credits: the run rules (warm-up, repetitions, percentiles, one window, the
system description) follow Parts 1 and 2 of the Day 9 lecture and chapter 12
"Benchmarking" of "Machine Learning Systems" by Vijay Janapa Reddi and
contributors (mlsysbook.ai, CC BY-NC-SA 4.0). The power estimate from the
command "vcgencmd pmic_read_adc", with its linear correction, follows the
script avg_temp_power.sh of the chapter "Setup" of "Edge AI Engineering:
Raspberry Pi" by Marcelo Rovai (github.com/Mjrovai/EdgeML_Made_Ease_ebook).
The script is new code of this course.
"""
import argparse
import csv
import json
import math
import os
import platform
import re
import statistics
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
if os.path.basename(LAB) == "solutions":
    LAB = os.path.dirname(LAB)
LABS = os.path.dirname(LAB)

# task, file, runtime, precision
SUITES = {
    "classification": (os.path.join(LABS, "day07", "models"), [
        ("classification", "mnv2.tflite", "litert", "float32"),
        ("classification", "mnv2_int8.tflite", "litert", "int8"),
        ("classification", "mnv2_static.onnx", "onnxruntime", "float32"),
        ("classification", "mnv2_int8.onnx", "onnxruntime", "int8"),
    ]),
    "detection": (os.path.join(LABS, "day08", "models"), [
        ("detection", "cupbottle_320_ncnn_model", "ncnn", "float32"),
        ("detection", "cupbottle_320.tflite", "litert", "float32"),
        ("detection", "cupbottle_320_int8.tflite", "litert", "int8"),
    ]),
    "tiny": (os.path.join(LAB, "models"), [
        ("kws", "kws_int8.tflite", "litert", "int8"),
        ("kws", "kws_float32.tflite", "litert", "float32"),
        ("ic", "ic_int8.tflite", "litert", "int8"),
        ("ic", "ic_float32.tflite", "litert", "float32"),
    ]),
}
DEFAULT_THREADS = {"classification": [1, 4], "detection": [1, 4], "tiny": [1]}

# The test input of the kit sketch (sketches/kit_bench/bench_cases.h): the
# seed of each task, and the class that LiteRT gives for it.
KIT_SEEDS = {"kws": 8, "ic": 5}
KIT_CLASSES = {"kws": 8, "ic": 6}
KWS_INPUT_SCALE, KWS_INPUT_ZERO = 0.5847029089927673, 83

# Linear correction of the power sum of "vcgencmd pmic_read_adc" (source:
# the script avg_temp_power.sh of the book "Edge AI Engineering").
PMIC_CORRECTION_A, PMIC_CORRECTION_B = 1.1451, 0.5879

FIELDS = ["device", "task", "model", "runtime", "precision", "threads", "window", "input",
          "warmup", "runs", "load_ms", "first_ms", "min_ms", "median_ms", "p95_ms",
          "max_ms", "mean_ms", "peak_rss_mb", "model_bytes", "temp_start_c", "temp_max_c",
          "freq_min_mhz", "throttled", "power_w", "check"]


# ----------------------------------------------------------------- statistics
def percentile(values, percent):
    """Task C1. Return the percentile of a list with the nearest-rank rule.

    The result is the smallest value with at least `percent` percent of the
    values at or below it. percent is an integer from 1 to 100. The median is
    the percentile 50.

    Sort the values. rank = percent x n / 100, rounded up. The result is the
    value with this rank. The first value has the rank 1.
    Examples: n = 20 and percent = 95 give the rank 19. n = 7 and percent = 50
    give the rank 4 (3.5 rounded up).
    """
    ordered = sorted(values)
    rank = math.ceil(percent * len(ordered) / 100)
    return ordered[max(rank, 1) - 1]


def check_task_c1():
    """Test percentile() with four examples."""
    twenty = [10.0 * (i + 1) for i in range(20)]
    seven = [21.0, 3.0, 55.0, 8.0, 34.0, 5.0, 13.0]       # not sorted
    try:
        return (percentile(twenty, 50) == 100.0 and percentile(twenty, 95) == 190.0
                and percentile(seven, 50) == 13.0 and percentile(seven, 100) == 55.0)
    except Exception:
        return False


# -------------------------------------------------------------------- sensors
def read_temperature():
    """The temperature of the processor in degrees Celsius, or None."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as handle:
            return int(handle.read().strip()) / 1000.0
    except (OSError, ValueError):
        return None


def read_frequency_mhz():
    """The clock of core 0 in MHz, or None."""
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") as handle:
            return int(handle.read().strip()) / 1000.0
    except (OSError, ValueError):
        return None


def vcgencmd(*arguments):
    """The output of the Raspberry Pi tool vcgencmd, or None."""
    try:
        return subprocess.run(["vcgencmd"] + list(arguments), capture_output=True,
                              text=True, check=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return None


def read_throttled():
    """The throttle state as text, for example "0x0", or an empty text.

    0x0 means: no low voltage and no limit of the clock since the start of
    the board. A different value means that the firmware limited the clock,
    or that the supply voltage was too low.
    """
    text = vcgencmd("get_throttled")
    return text.strip().replace("throttled=", "") if text else ""


def parse_pmic(text):
    """Return the sum of voltage x current of all rails in watts, or None.

    The output of "vcgencmd pmic_read_adc" has one line for the current and
    one line for the voltage of each rail, for example:
        3V3_SYS_A current(1)=0.06245952A
        3V3_SYS_V volt(13)=3.29687500V
    """
    currents, volts = {}, {}
    for match in re.finditer(r"(\S+)_A\s+current\(\d+\)=([0-9.]+)A", text):
        currents[match.group(1)] = float(match.group(2))
    for match in re.finditer(r"(\S+)_V\s+volt\(\d+\)=([0-9.]+)V", text):
        volts[match.group(1)] = float(match.group(2))
    rails = [name for name in currents if name in volts]
    if not rails:
        return None
    return sum(currents[name] * volts[name] for name in rails)


def read_power_w():
    """The estimated power of the board in watts, or None.

    The sum of the rails is the power of the main chips. The linear
    correction of the source gives an estimate of the power of the board.
    """
    text = vcgencmd("pmic_read_adc")
    rails = parse_pmic(text) if text else None
    if rails is None:
        return None
    return PMIC_CORRECTION_A * rails + PMIC_CORRECTION_B


def peak_rss_mb():
    """The peak resident memory of this process in MB (1 MB = 1024 KB), or None."""
    try:
        with open("/proc/self/status") as handle:
            for line in handle:
                if line.startswith("VmHWM:"):
                    return int(line.split()[1]) / 1024.0
    except OSError:
        pass
    return None


def device_name():
    try:
        with open("/proc/device-tree/model") as handle:
            return handle.read().strip("\0\n ")
    except OSError:
        return "%s (%s)" % (platform.node(), platform.machine())


# --------------------------------------------------------------------- inputs
def kit_input(task, dtype):
    """The test input of the kit sketch, as an array with one dimension."""
    import numpy as np
    count = 490 if task == "kws" else 3072
    state = KIT_SEEDS[task]
    values = np.empty(count, np.int64)
    for i in range(count):
        state = (state * 1664525 + 1013904223) & 0xFFFFFFFF
        values[i] = state >> 24
    if task == "kws":
        q = KWS_INPUT_ZERO + np.trunc((values - 128) / 12.0).astype(np.int64)
        q[np.arange(count) % 10 == 0] -= 60
        q = np.clip(q, -128, 127)
        if np.dtype(dtype) == np.int8:
            return q.astype(np.int8)
        return ((q - KWS_INPUT_ZERO) * KWS_INPUT_SCALE).astype(np.float32)
    if np.dtype(dtype) == np.int8:
        return (values - 128).astype(np.int8)
    return values.astype(np.float32)


def random_input(shape, dtype):
    """A fixed random tensor with the shape and the type of the model input."""
    import numpy as np
    rng = np.random.default_rng(0)
    shape = [int(v) if str(v).isdigit() and int(v) > 0 else 1 for v in shape]
    if np.dtype(dtype) == np.uint8:
        return rng.integers(0, 256, size=shape, dtype=np.uint8)
    if np.dtype(dtype) == np.int8:
        return rng.integers(-128, 128, size=shape, dtype=np.int8)
    return rng.random(shape, dtype=np.float32)


# ------------------------------------------------------------------- runtimes
def make_litert(path, threads, task):
    import numpy as np
    from ai_edge_litert.interpreter import Interpreter
    interpreter = Interpreter(model_path=path, num_threads=threads)
    interpreter.allocate_tensors()
    detail = interpreter.get_input_details()[0]
    output = interpreter.get_output_details()[0]
    if task in KIT_SEEDS:
        data = kit_input(task, detail["dtype"]).reshape(detail["shape"])
        note = "kit test input"
    else:
        data = random_input(detail["shape"], detail["dtype"])
        note = "random, seed 0"

    def run():
        interpreter.set_tensor(detail["index"], data)
        interpreter.invoke()
        return interpreter.get_tensor(output["index"])
    return run, note


def make_onnxruntime(path, threads, task):
    import numpy as np
    import onnxruntime as ort
    options = ort.SessionOptions()
    options.intra_op_num_threads = threads
    options.inter_op_num_threads = 1
    session = ort.InferenceSession(path, options, providers=["CPUExecutionProvider"])
    detail = session.get_inputs()[0]
    data = random_input(detail.shape, np.float32 if "float" in detail.type else np.uint8)

    def run():
        return session.run(None, {detail.name: data})[0]
    return run, "random, seed 0"


def make_ncnn(path, threads, task):
    import glob
    import ncnn
    import numpy as np
    if os.path.isdir(path):
        files = sorted(glob.glob(os.path.join(path, "*.param")))
        if not files:
            raise FileNotFoundError("no .param file in " + path)
        param = files[0]
    else:
        param = path
    match = re.search(r"_(\d{3,4})(?:_|\.|$)", os.path.basename(os.path.normpath(path)))
    size = int(match.group(1)) if match else 640
    net = ncnn.Net()
    net.opt.num_threads = threads
    net.opt.use_vulkan_compute = False
    net.load_param(param)
    net.load_model(param[:-len(".param")] + ".bin")
    data = random_input([3, size, size], np.float32)
    name_in = net.input_names()[0]
    names_out = sorted(net.output_names())

    def run():
        extractor = net.create_extractor()
        extractor.input(name_in, ncnn.Mat(data).clone())
        return [np.array(extractor.extract(name)[1]) for name in names_out]
    return run, "random, seed 0"


MAKERS = {"litert": make_litert, "onnxruntime": make_onnxruntime, "ncnn": make_ncnn}


def guess_runtime(path):
    name = os.path.basename(os.path.normpath(path))
    if name.endswith(".tflite"):
        return "litert"
    if name.endswith(".onnx"):
        return "onnxruntime"
    if name.endswith("_ncnn_model") or name.endswith(".param"):
        return "ncnn"
    raise SystemExit("ERROR: no runtime for the file %s" % name)


def model_bytes(path):
    if os.path.isdir(path):
        return sum(os.path.getsize(os.path.join(path, name)) for name in os.listdir(path)
                   if name.endswith((".param", ".bin")))
    return os.path.getsize(path)


# ----------------------------------------------------------------- one case
def run_case(case):
    """Measure one case in this process. Return the results as a dictionary."""
    import numpy as np
    start = time.perf_counter_ns()
    run, note = MAKERS[case["runtime"]](case["path"], case["threads"], case["task"])
    load_ms = (time.perf_counter_ns() - start) / 1e6

    def timed():
        begin = time.perf_counter_ns()
        output = run()
        return (time.perf_counter_ns() - begin) / 1e6, output

    first_ms, output = timed()
    for _ in range(case["warmup"] - 1):
        run()

    temperatures = [read_temperature()]
    frequencies = [read_frequency_mhz()]
    powers = [read_power_w()]
    times = []
    limit = time.perf_counter() + case["max_seconds"]
    while len(times) < case["runs"] and time.perf_counter() < limit:
        elapsed, output = timed()
        times.append(elapsed)
        if len(times) % 20 == 0:                 # a read is not in a timed run
            temperatures.append(read_temperature())
            frequencies.append(read_frequency_mhz())
            powers.append(read_power_w())
    temperatures.append(read_temperature())
    frequencies.append(read_frequency_mhz())

    check = ""
    if case["task"] in KIT_CLASSES:
        best = int(np.asarray(output).reshape(-1).argmax())
        check = "class %d, %s" % (best, "same as the kit sketch"
                                  if best == KIT_CLASSES[case["task"]] else "NOT THE SAME")
    temperatures = [t for t in temperatures if t is not None]
    frequencies = [f for f in frequencies if f is not None]
    powers = [p for p in powers if p is not None]
    return {"input": note, "load_ms": load_ms, "first_ms": first_ms, "times_ms": times,
            "peak_rss_mb": peak_rss_mb(),
            "temp_start_c": temperatures[0] if temperatures else None,
            "temp_max_c": max(temperatures) if temperatures else None,
            "freq_min_mhz": min(frequencies) if frequencies else None,
            "throttled": read_throttled(),
            "power_w": statistics.fmean(powers) if powers else None, "check": check}


def run_child(case):
    """Start a new process for one case and return its result."""
    process = subprocess.run([sys.executable, os.path.abspath(__file__), "--child",
                              json.dumps(case)], capture_output=True, text=True)
    lines = [line for line in process.stdout.splitlines() if line.startswith("{")]
    if process.returncode != 0 or not lines:
        message = (process.stderr.strip().splitlines() or ["no output"])[-1]
        return {"error": message}
    return json.loads(lines[-1])


def show(value, form="%.2f"):
    return "" if value is None else form % value


def summary_row(case, result):
    """One row of results_pi.csv from the times of one case."""
    times = result["times_ms"]
    return {
        "device": device_name(), "task": case["task"],
        "model": os.path.basename(os.path.normpath(case["path"])),
        "runtime": case["runtime"], "precision": case["precision"],
        "threads": case["threads"], "window": "model only", "input": result["input"],
        "warmup": case["warmup"], "runs": len(times),
        "load_ms": show(result["load_ms"], "%.1f"), "first_ms": show(result["first_ms"], "%.3f"),
        "min_ms": show(min(times), "%.3f"), "median_ms": show(percentile(times, 50), "%.3f"),
        "p95_ms": show(percentile(times, 95), "%.3f"), "max_ms": show(max(times), "%.3f"),
        "mean_ms": show(statistics.fmean(times), "%.3f"),
        "peak_rss_mb": show(result["peak_rss_mb"], "%.1f"),
        "model_bytes": model_bytes(case["path"]),
        "temp_start_c": show(result["temp_start_c"], "%.1f"),
        "temp_max_c": show(result["temp_max_c"], "%.1f"),
        "freq_min_mhz": show(result["freq_min_mhz"], "%.0f"),
        "throttled": result["throttled"], "power_w": show(result["power_w"], "%.2f"),
        "check": result["check"],
    }


def append_rows(path, rows):
    new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if new:
            writer.writeheader()
        writer.writerows(rows)


def save_raw(folder, case, result):
    os.makedirs(folder, exist_ok=True)
    name = "%s_%s_t%d.json" % (os.path.basename(os.path.normpath(case["path"])),
                               case["runtime"], case["threads"])
    with open(os.path.join(folder, name), "w", encoding="utf-8") as handle:
        json.dump({"case": case, "result": result}, handle, indent=1)


# ----------------------------------------------------------- the three modes
def run_cases(cases, args):
    print("%-15s %-28s %-12s %-8s %7s | %8s %8s %8s %8s | %7s %6s %6s %s"
          % ("task", "model", "runtime", "type", "threads", "first", "median", "p95", "max",
             "RSS MB", "temp", "watt", "check"))
    rows = []
    for case in cases:
        name = os.path.basename(os.path.normpath(case["path"]))
        if not os.path.exists(case["path"]):
            print("%-15s %-28s not found" % (case["task"], name))
            continue
        result = run_child(case)
        if "error" in result:
            print("%-15s %-28s %-12s ERROR: %s" % (case["task"], name, case["runtime"],
                                                    result["error"]))
            continue
        row = summary_row(case, result)
        print("%-15s %-28s %-12s %-8s %7d | %8s %8s %8s %8s | %7s %6s %6s %s"
              % (row["task"], row["model"], row["runtime"], row["precision"], row["threads"],
                 row["first_ms"], row["median_ms"], row["p95_ms"], row["max_ms"],
                 row["peak_rss_mb"], row["temp_max_c"], row["power_w"], row["check"]),
              flush=True)
        rows.append(row)
        save_raw(args.raw, case, result)
    if rows:
        append_rows(args.output, rows)
        print()
        print("%d rows added to %s. Times in ms. Each case: %d inferences to warm up, then "
              "%d timed inferences or %d seconds." % (len(rows), args.output, args.warmup,
                                                      args.runs, args.max_seconds))


def run_sustain(args):
    """Run one model for a long time and print one line for each window."""
    path = args.model
    runtime = args.runtime or guess_runtime(path)
    threads = args.threads[0]
    run, _ = MAKERS[runtime](path, threads, "sustain")
    for _ in range(args.warmup):
        run()
    print("Sustained run: %s, %s, %d threads, %d seconds, one line for each %d seconds"
          % (os.path.basename(os.path.normpath(path)), runtime, threads, args.sustain,
             args.window))
    print("%8s %10s %10s %10s %8s %9s %10s %7s"
          % ("second", "inferences", "median ms", "p95 ms", "temp C", "clock MHz",
             "throttled", "watt"))
    rows = []
    begin = time.perf_counter()
    while time.perf_counter() - begin < args.sustain:
        times = []
        window_end = time.perf_counter() + args.window
        while time.perf_counter() < window_end:
            start = time.perf_counter_ns()
            run()
            times.append((time.perf_counter_ns() - start) / 1e6)
        row = {"second": round(time.perf_counter() - begin), "inferences": len(times),
               "median_ms": show(percentile(times, 50), "%.3f"),
               "p95_ms": show(percentile(times, 95), "%.3f"),
               "temp_c": show(read_temperature(), "%.1f"),
               "freq_mhz": show(read_frequency_mhz(), "%.0f"),
               "throttled": read_throttled(), "power_w": show(read_power_w(), "%.2f")}
        print("%8d %10d %10s %10s %8s %9s %10s %7s"
              % (row["second"], row["inferences"], row["median_ms"], row["p95_ms"],
                 row["temp_c"], row["freq_mhz"], row["throttled"], row["power_w"]), flush=True)
        rows.append(row)
    with open(args.sustain_output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    first, last = float(rows[0]["median_ms"]), float(rows[-1]["median_ms"])
    print()
    print("Median latency: %.3f ms in the first window, %.3f ms in the last window "
          "(%+.1f percent)." % (first, last, 100.0 * (last / first - 1.0)))
    print("Saved: %s" % args.sustain_output)


def run_idle(args):
    """Read the temperature and the power for some seconds with no load."""
    temperatures, powers = [], []
    for _ in range(args.idle):
        temperatures.append(read_temperature())
        powers.append(read_power_w())
        time.sleep(1)
    temperatures = [t for t in temperatures if t is not None]
    powers = [p for p in powers if p is not None]
    print("Idle for %d seconds." % args.idle)
    print("Temperature: %s" % (show(statistics.fmean(temperatures), "%.1f C")
                               if temperatures else "no value on this computer"))
    print("Estimated power: %s" % (show(statistics.fmean(powers), "%.2f W")
                                   if powers else "no value on this computer"))


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--child":
        print(json.dumps(run_case(json.loads(sys.argv[2]))))
        return
    parser = argparse.ArgumentParser(description="Benchmark harness of the Day 9 lab.")
    parser.add_argument("--suite", choices=sorted(SUITES),
                        help="measure the model files of one suite")
    parser.add_argument("--model", help="measure one model file or one NCNN folder")
    parser.add_argument("--runtime", choices=sorted(MAKERS),
                        help="runtime for --model (default: from the file name)")
    parser.add_argument("--threads", type=int, nargs="+", default=None,
                        help="thread counts (default: 1 and 4, or 1 for the suite tiny)")
    parser.add_argument("--warmup", type=int, default=20,
                        help="inferences before the timed runs (default 20)")
    parser.add_argument("--runs", type=int, default=200,
                        help="timed inferences for each case (default 200)")
    parser.add_argument("--max-seconds", type=int, default=30,
                        help="time limit of the timed runs of one case (default 30)")
    parser.add_argument("--sustain", type=int, default=0,
                        help="run --model for this number of seconds")
    parser.add_argument("--window", type=int, default=10,
                        help="seconds for one line of the sustained run (default 10)")
    parser.add_argument("--idle", type=int, default=0,
                        help="read temperature and power for this number of seconds")
    parser.add_argument("--output", default="results_pi.csv")
    parser.add_argument("--sustain-output", default="sustain.csv")
    parser.add_argument("--raw", default="raw")
    args = parser.parse_args()
    if args.warmup < 1 or args.runs < 1:
        parser.error("--warmup and --runs must be 1 or more")

    import numpy as np
    print("Device: %s" % device_name())
    print("Python %s, NumPy %s, %d cores" % (platform.python_version(), np.__version__,
                                             os.cpu_count()))
    for package in ("ai_edge_litert", "onnxruntime", "ncnn"):
        try:
            module = __import__(package)
            print("%s %s" % (package, getattr(module, "__version__", "installed")))
        except ImportError:
            print("%s is not installed in this environment" % package)
    temperature = read_temperature()
    if temperature is not None:
        print("Temperature: %.1f C, clock: %s MHz, throttled: %s"
              % (temperature, show(read_frequency_mhz(), "%.0f"), read_throttled()))

    if args.idle:
        run_idle(args)
        return
    if not check_task_c1():
        print("Task C1: not complete. Write the function percentile() in pi/bench.py.")
        sys.exit(1)
    print("Task C1: complete.")
    print()
    if args.sustain:
        if not args.model:
            parser.error("--sustain needs --model")
        args.threads = args.threads or [4]
        run_sustain(args)
        return
    if args.suite:
        folder, entries = SUITES[args.suite]
        threads = args.threads or DEFAULT_THREADS[args.suite]
        cases = [{"task": task, "path": os.path.join(folder, name), "runtime": runtime,
                  "precision": precision, "threads": count}
                 for task, name, runtime, precision in entries for count in threads]
    elif args.model:
        runtime = args.runtime or guess_runtime(args.model)
        precision = "int8" if "int8" in os.path.basename(args.model) else "float32"
        cases = [{"task": "custom", "path": args.model, "runtime": runtime,
                  "precision": precision, "threads": count}
                 for count in (args.threads or [1, 4])]
    else:
        parser.error("give --suite, --model, or --idle")
    for case in cases:
        case.update({"warmup": args.warmup, "runs": args.runs,
                     "max_seconds": args.max_seconds})
    run_cases(cases, args)


if __name__ == "__main__":
    main()
