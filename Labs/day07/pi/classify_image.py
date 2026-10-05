#!/usr/bin/env python3
"""Day 7 lab, Part B: classify one image with LiteRT.

Run on: the Raspberry Pi 5, in the environment ~/tflite_env. The script also
        runs on a laptop with the packages ai-edge-litert, numpy, and pillow.
Use:    python pi/classify_image.py images/Cat03.jpg
        python pi/classify_image.py images/Cat03.jpg --model models/mnv2.tflite
        python pi/classify_image.py images/Cat03.jpg --threads 4 --runs 20

The script reads the input details of the model and prepares the image for
three types of file:

    uint8 input     raw pixels from 0 to 255 (the model of the kit lab)
    float32 input   pixels with the mean and the standard deviation of
                    ImageNet (the model that you export in Part C)
    int8 input      the float32 values, quantized with the scale and the zero
                    point of the input (models/mnv2_int8.tflite)
"""
import argparse
import os
import statistics
import time

import numpy as np
from PIL import Image

from ai_edge_litert.interpreter import Interpreter

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
if os.path.basename(LAB) == "solutions":
    LAB = os.path.dirname(LAB)
MODELS = os.path.join(LAB, "models")

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def load_labels(filename):
    with open(filename, "r", encoding="utf-8") as handle:
        return [line.strip() for line in handle.readlines()]


def labels_for(model_path, number_of_outputs):
    """The kit model has 1001 outputs. A model from PyTorch has 1000."""
    name = "labels.txt" if number_of_outputs == 1001 else "imagenet_classes.txt"
    return load_labels(os.path.join(os.path.dirname(model_path), name))


def preprocess(image, input_details):
    """Return the input tensor of the model for one PIL image."""
    shape = input_details["shape"]
    channels_first = shape[1] == 3
    height, width = (shape[2], shape[3]) if channels_first else (shape[1], shape[2])
    pixels = np.asarray(image.convert("RGB").resize((width, height)))
    dtype = input_details["dtype"]
    if dtype == np.uint8:
        data = pixels
    else:
        data = (pixels.astype(np.float32) / 255.0 - IMAGENET_MEAN) / IMAGENET_STD
        if dtype == np.int8:
            scale, zero_point = input_details["quantization"]
            data = np.clip(np.round(data / scale + zero_point), -128, 127)
    if channels_first:
        data = data.transpose(2, 0, 1)
    return np.expand_dims(data, axis=0).astype(dtype)


def dequantize_and_softmax(raw, scale, zero_point):
    """Task B1. Return the probabilities for the raw output of the model.

    raw is a NumPy array with one value for each class. For a quantized
    model, the values are integers, and scale is not 0. For a float32 model,
    scale is 0, and the values are the real outputs.
    """
    # TODO (student), Task B1: three steps.
    # 1. Change raw to float32.
    # 2. If scale is not 0: real value = (integer - zero_point) * scale.
    # 3. Softmax: subtract the largest value, apply np.exp, and divide by
    #    the sum. Return the result.
    return None


def classify(image_path, model_path, threads=4, runs=10):
    """Run the model on one image. Return the probabilities and the times."""
    start = time.perf_counter()
    interpreter = Interpreter(model_path=model_path, num_threads=threads)
    interpreter.allocate_tensors()
    load_ms = 1000 * (time.perf_counter() - start)
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    input_data = preprocess(Image.open(image_path), input_details)

    times = []
    for _ in range(runs):
        start = time.perf_counter()
        interpreter.set_tensor(input_details["index"], input_data)
        interpreter.invoke()
        raw = interpreter.get_tensor(output_details["index"])[0]
        times.append(1000 * (time.perf_counter() - start))

    scale, zero_point = output_details["quantization"]
    probabilities = dequantize_and_softmax(raw, scale, zero_point)
    return {
        "raw": raw,
        "probabilities": probabilities,
        "input_shape": [int(v) for v in input_details["shape"]],
        "input_dtype": np.dtype(input_details["dtype"]).name,
        "output_dtype": np.dtype(output_details["dtype"]).name,
        "load_ms": load_ms,
        "first_ms": times[0],
        "median_ms": statistics.median(times[1:]) if runs > 1 else times[0],
    }


def print_result(result, labels, top=5):
    print("Input:  shape %s, type %s" % (result["input_shape"], result["input_dtype"]))
    print("Output: %d values, type %s" % (len(result["raw"]), result["output_dtype"]))
    print("Load: %.1f ms. First inference: %.1f ms. Median of the next runs: %.1f ms."
          % (result["load_ms"], result["first_ms"], result["median_ms"]))
    probabilities = result["probabilities"]
    if probabilities is None:
        print("Task B1: not complete. The list shows the raw output values.")
        order = np.argsort(result["raw"])[::-1][:top]
        print("\n\t[PREDICTION]        [Raw value]\n")
        for index in order:
            print("\t{:20}: {}".format(labels[index], result["raw"][index]))
        return
    print("Task B1: complete.")
    order = np.argsort(probabilities)[::-1][:top]
    print("\n\t[PREDICTION]        [Prob]\n")
    for index in order:
        print("\t{:20}: {}%".format(labels[index], int(probabilities[index] * 100)))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("image", help="path of a JPEG or PNG file")
    parser.add_argument("--model",
                        default=os.path.join(MODELS, "mobilenet_v2_1.0_224_quant.tflite"))
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()

    print("Model:  %s (%d bytes)" % (os.path.relpath(args.model),
                                    os.path.getsize(args.model)))
    print("Image:  %s, threads: %d" % (args.image, args.threads))
    result = classify(args.image, args.model, args.threads, args.runs)
    labels = labels_for(args.model, len(result["raw"]))
    print_result(result, labels, args.top)


if __name__ == "__main__":
    main()
