#!/usr/bin/env python3
"""Convert a LiteRT model file (.tflite) to a C header for an Arduino sketch.

Runs on: the laptop, Python 3.10 or later. No package is necessary.

Use:
    python3 tflite_to_header.py model.tflite sketches/my_sketch/model.h

The header defines the array g_model and the length g_model_len. The array
has an alignment of 16 bytes, because TensorFlow Lite Micro reads the model
in place.

The command "xxd -i model.tflite" gives the same bytes. This script adds the
alignment, the const qualifier, and a fixed array name.
"""

import argparse
import pathlib
import sys

TFLITE_IDENTIFIER = b"TFL3"   # bytes 4 to 7 of each LiteRT flatbuffer


def make_header(data, source_name, name="g_model", notice=""):
    """Return the text of the header for the model bytes."""
    lines = []
    if notice:
        lines.append("/* " + notice.strip().replace("*/", "* /") + " */")
        lines.append("")
    lines.append("// Model: %s (%d bytes)" % (source_name, len(data)))
    lines.append("// Made by tflite_to_header.py. Do not change this file by hand.")
    lines.append("")
    lines.append("#ifndef MODEL_H_")
    lines.append("#define MODEL_H_")
    lines.append("")
    lines.append("alignas(16) const unsigned char %s[] = {" % name)
    for start in range(0, len(data), 12):
        chunk = data[start:start + 12]
        lines.append("    " + ", ".join("0x%02x" % byte for byte in chunk) + ",")
    lines.append("};")
    lines.append("")
    lines.append("const int %s_len = sizeof(%s);" % (name, name))
    lines.append("")
    lines.append("#endif  // MODEL_H_")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("model", help="input file, for example model.tflite")
    parser.add_argument("header", help="output file, for example model.h")
    parser.add_argument("--name", default="g_model",
                        help="name of the C array (default: g_model)")
    parser.add_argument("--notice",
                        help="text file with a licence notice for the header")
    args = parser.parse_args()

    data = pathlib.Path(args.model).read_bytes()
    if len(data) < 8 or data[4:8] != TFLITE_IDENTIFIER:
        print("ERROR: %s is not a LiteRT model (no TFL3 identifier)" % args.model)
        return 1

    notice = pathlib.Path(args.notice).read_text() if args.notice else ""
    text = make_header(data, pathlib.Path(args.model).name, args.name, notice)
    pathlib.Path(args.header).write_text(text)
    print("Wrote %s: %d model bytes" % (args.header, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
