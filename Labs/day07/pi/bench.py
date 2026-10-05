#!/usr/bin/env python3
"""Day 7 lab, Part D: latency for each runtime, thread count, and precision.

Run on: the Raspberry Pi 5, in the environment ~/tflite_env. The script also
        runs on a laptop with the packages ai-edge-litert, onnxruntime, and
        numpy.
Use:    python pi/bench.py
        python pi/bench.py --threads 1 2 4 --runs 50 --out results.csv
        python pi/bench.py --only litert
        python pi/bench.py --levels

Credits: new code of this course. The method (some runs to warm up, then the
median of many runs, one thread setting for each runtime) follows Parts 2 and
3 of the Day 7 lecture.

The script measures each model file that it finds in the folder models/:

    mnv2.tflite                         LiteRT        float32  (from Part C)
    mnv2_int8.tflite                    LiteRT        int8
    mobilenet_v2_1.0_224_quant.tflite   LiteRT        uint8    (the kit model)
    mnv2_static.onnx                    ONNX Runtime  float32  (from Part C)
    mnv2_dynamic.onnx                   ONNX Runtime  float32  (from Part C)
    mnv2_int8.onnx                      ONNX Runtime  int8
    mnv2.ncnn.param                     NCNN          float16  (an option)

A file that is not there gives one line "not found" and no error. NCNN is
measured only if the Python package ncnn is installed.

With the option --levels, the script measures only the file
mnv2_unfused.onnx of Part C in ONNX Runtime, one time for each graph
optimization level: disabled, basic, extended, all.

The input of each run is a random tensor. The latency of these models does
not depend on the content of the image.
"""
import argparse
import csv
import os
import platform
import statistics
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
if os.path.basename(LAB) == "solutions":
    LAB = os.path.dirname(LAB)

# file, runtime, precision
FILES = [
    ("mnv2.tflite", "litert", "float32"),
    ("mnv2_int8.tflite", "litert", "int8"),
    ("mobilenet_v2_1.0_224_quant.tflite", "litert", "uint8"),
    ("mnv2_static.onnx", "onnxruntime", "float32"),
    ("mnv2_dynamic.onnx", "onnxruntime", "float32"),
    ("mnv2_int8.onnx", "onnxruntime", "int8"),
    ("mnv2.ncnn.param", "ncnn", "float16"),
]


def median_latency_ms(run, runs, warmup):
    """Task D1. Return the median time of one call of run(), in ms.

    Call run() warmup times first, and do not measure these calls. Then
    measure runs calls with time.perf_counter(), each call alone. Return the
    median of these times in milliseconds.
    """
    # TODO (student), Task D1: write the three steps of the text above.
    # Use statistics.median() for the median.
    return None


def random_input(shape, dtype):
    """A random tensor with the shape and the type of the model input."""
    rng = np.random.default_rng(0)
    # A dynamic dimension has a name or the value -1. Use 1 for it.
    shape = [int(v) if str(v).isdigit() and int(v) > 0 else 1 for v in shape]
    if np.dtype(dtype) == np.uint8:
        return rng.integers(0, 256, size=shape, dtype=np.uint8)
    if np.dtype(dtype) == np.int8:
        return rng.integers(-128, 128, size=shape, dtype=np.int8)
    return rng.standard_normal(shape).astype(np.float32)


def make_litert(path, threads):
    from ai_edge_litert.interpreter import Interpreter
    interpreter = Interpreter(model_path=path, num_threads=threads)
    interpreter.allocate_tensors()
    details = interpreter.get_input_details()[0]
    output = interpreter.get_output_details()[0]["index"]
    data = random_input(details["shape"], details["dtype"])

    def run():
        interpreter.set_tensor(details["index"], data)
        interpreter.invoke()
        return interpreter.get_tensor(output)
    return run


def make_onnxruntime(path, threads, level=None):
    import onnxruntime as ort
    options = ort.SessionOptions()
    options.intra_op_num_threads = threads
    options.inter_op_num_threads = 1
    if level is not None:
        options.graph_optimization_level = getattr(ort.GraphOptimizationLevel, level)
    session = ort.InferenceSession(path, options, providers=["CPUExecutionProvider"])
    details = session.get_inputs()[0]
    dtype = np.float32 if "float" in details.type else np.uint8
    data = random_input(details.shape, dtype)

    def run():
        return session.run(None, {details.name: data})[0]
    return run


def make_ncnn(path, threads):
    import ncnn
    net = ncnn.Net()
    net.opt.num_threads = threads
    net.opt.use_vulkan_compute = False
    net.load_param(path)
    net.load_model(path.replace(".param", ".bin"))
    data = random_input([3, 224, 224], np.float32)

    def run():
        extractor = net.create_extractor()
        extractor.input("in0", ncnn.Mat(data).clone())
        return np.array(extractor.extract("out0")[1])
    return run


MAKERS = {"litert": make_litert, "onnxruntime": make_onnxruntime, "ncnn": make_ncnn}

# name in the output, name of the level in ONNX Runtime
LEVELS = [("disabled", "ORT_DISABLE_ALL"), ("basic", "ORT_ENABLE_BASIC"),
          ("extended", "ORT_ENABLE_EXTENDED"), ("all", "ORT_ENABLE_ALL")]


def temperature():
    """The temperature of the processor, or an empty text on a laptop."""
    try:
        text = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True,
                              text=True, check=True).stdout.strip()
        return text.replace("temp=", "")
    except (OSError, subprocess.CalledProcessError):
        return ""


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--models", default=os.path.join(LAB, "models"))
    parser.add_argument("--threads", type=int, nargs="+", default=[1, 2, 4])
    parser.add_argument("--runs", type=int, default=50)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--only", choices=sorted(MAKERS), default=None,
                        help="measure one runtime only")
    parser.add_argument("--levels", action="store_true",
                        help="measure mnv2_unfused.onnx for each optimization level")
    parser.add_argument("--out", default="results.csv")
    args = parser.parse_args()

    print("Computer: %s, %s, %d cores" % (platform.node(), platform.machine(),
                                          os.cpu_count()))
    print("Python %s, NumPy %s" % (platform.python_version(), np.__version__))
    if temperature():
        print("Temperature at the start: %s" % temperature())

    if median_latency_ms(lambda: None, 3, 1) is None:
        print("Task D1: not complete. Write the function median_latency_ms() "
              "in pi/bench.py.")
        sys.exit(1)
    print("Task D1: complete.")
    print()
    print("%-12s %-34s %-8s %7s %9s %10s"
          % ("runtime", "file", "level" if args.levels else "type", "threads",
             "load ms", "median ms"))

    if args.levels:
        cases = [("mnv2_unfused.onnx", "onnxruntime", name, level)
                 for name, level in LEVELS]
    else:
        cases = [(name, runtime, precision, None) for name, runtime, precision in FILES
                 if not args.only or runtime == args.only]

    rows = []
    for name, runtime, precision, level in cases:
        path = os.path.join(args.models, name)
        if not os.path.exists(path):
            print("%-12s %-34s not found" % (runtime, name))
            continue
        for threads in args.threads:
            try:
                start = time.perf_counter()
                if level is None:
                    run = MAKERS[runtime](path, threads)
                else:
                    run = make_onnxruntime(path, threads, level)
                run()
                load_ms = 1000 * (time.perf_counter() - start)
                median = median_latency_ms(run, args.runs, args.warmup)
            except ImportError as error:
                print("%-12s %-34s package not installed (%s)" % (runtime, name, error.name))
                break
            print("%-12s %-34s %-8s %7d %9.1f %10.2f"
                  % (runtime, name, precision, threads, load_ms, median))
            rows.append({"runtime": runtime, "file": name, "precision": precision,
                         "threads": threads, "load_ms": round(load_ms, 1),
                         "median_ms": round(median, 2),
                         "bytes": os.path.getsize(path),
                         "temperature": temperature()})

    if rows:
        with open(args.out, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print()
        print("%d rows written to %s" % (len(rows), args.out))
    if temperature():
        print("Temperature at the end: %s" % temperature())


if __name__ == "__main__":
    main()
