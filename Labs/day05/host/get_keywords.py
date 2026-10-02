#!/usr/bin/env python3
"""Get the keyword dataset for Part A of the Day 5 lab.

Runs on: the laptop, Python 3.10 or later. No package is necessary.

Use, from the folder Labs/day05/:
    python3 host/get_keywords.py
    python3 host/get_keywords.py --each 300 --zip downloads/keywords2.zip

The script downloads the file keywords2.zip of Edge Impulse (139 MB) into the
folder downloads/, one time. Then it writes some clips of each class into
the folder keywords/:

    keywords/yes/      keywords/no/      keywords/unknown/      keywords/noise/

Each clip has 1 s at 16 kHz with 16 bits. The name of a clip starts with
its class, so Edge Impulse Studio reads the label from the name.

Credits: the dataset is the "keyword spotting pre-built dataset" of Edge
Impulse (docs.edgeimpulse.com). Its words come from the dataset "Speech
Commands" by Pete Warden (Google, CC BY 4.0). The kit lab "Keyword Spotting
(KWS)" of "Machine Learning Systems" uses the same file.
"""

import argparse
import pathlib
import sys
import urllib.request
import zipfile

URL = "https://cdn.edgeimpulse.com/datasets/keywords2.zip"
CLASSES = ["yes", "no", "unknown", "noise"]


def download(url, target):
    """Download a file and print the progress."""
    target.parent.mkdir(parents=True, exist_ok=True)
    print("download", url)
    with urllib.request.urlopen(url) as response, open(target, "wb") as out:
        total = int(response.headers.get("Content-Length", 0))
        done = 0
        while True:
            block = response.read(1 << 20)
            if not block:
                break
            out.write(block)
            done += len(block)
            if total:
                print(f"\r  {100 * done // total} percent", end="", flush=True)
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--each", type=int, default=300,
                        help="number of clips of each class (default: 300)")
    parser.add_argument("--zip", default="downloads/keywords2.zip",
                        help="place of the ZIP file")
    parser.add_argument("--out", default="keywords",
                        help="output folder (default: keywords)")
    args = parser.parse_args()

    archive = pathlib.Path(args.zip)
    if not archive.exists():
        download(URL, archive)

    out = pathlib.Path(args.out)
    with zipfile.ZipFile(archive) as bundle:
        for label in CLASSES:
            names = sorted(name for name in bundle.namelist()
                           if name.startswith(label + "/")
                           and name.endswith(".wav"))
            if not names:
                print(f"ERROR: the ZIP file has no clips of the class {label}")
                return 1
            folder = out / label
            folder.mkdir(parents=True, exist_ok=True)
            # The names are in the order of the speaker codes. A step through
            # the list gives clips of many speakers.
            step = max(1, len(names) // args.each)
            picked = names[::step][:args.each]
            for name in picked:
                (folder / pathlib.Path(name).name).write_bytes(bundle.read(name))
            print(f"{label:<8} {len(picked)} of {len(names)} clips "
                  f"-> {folder}")
    print("Upload the four folders in Edge Impulse Studio: Data acquisition.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
