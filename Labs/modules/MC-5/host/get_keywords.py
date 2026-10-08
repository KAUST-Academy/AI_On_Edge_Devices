#!/usr/bin/env python3
"""Get the keyword clips that the MC-5 lab uses.

Runs on: the laptop, Python 3.10 or later. No package is necessary.

Use, from the folder Labs/modules/MC-5/:
    python3 host/get_keywords.py
    python3 host/get_keywords.py --each 240

The script downloads the file keywords2.zip of Edge Impulse (139 MB) into
the folder downloads/, one time. Then it writes some clips of each class
into the folder keywords/:

    keywords/yes/  keywords/no/  keywords/unknown/  keywords/noise/

Each clip has 1 s of audio at 16 kHz with 16 bits. The first four files of
the archive are the class names, the rest are the clips. The script
converts each clip to the folder keywords/clips/ as one CSV file of
amplitude values, so that the notebook needs no audio package.
"""

import argparse
import pathlib
import sys
import urllib.request
import wave
import zipfile

URL = "https://cdn.edgeimpulse.com/datasets/keywords2.zip"
CLASSES = ["yes", "no", "unknown", "noise"]


def download(url, target):
    """Download a file and print the progress."""
    target.parent.mkdir(parents=True, exist_ok=True)
    print("download", url, flush=True)
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
    print(flush=True)


def read_clip(raw):
    """Read a WAV clip of the archive and return the amplitudes as int16."""
    with wave.open(raw, "rb") as handle:
        frames = handle.readframes(handle.getnframes())
    count = len(frames) // 2
    values = [int.from_bytes(frames[2 * i:2 * i + 2], "little", signed=True)
              for i in range(count)]
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--each", type=int, default=240,
                        help="number of clips of each class (default: 240)")
    parser.add_argument("--zip", default="downloads/keywords2.zip",
                        help="place of the ZIP file")
    parser.add_argument("--out", default="keywords",
                        help="output folder (default: keywords)")
    args = parser.parse_args()

    archive = pathlib.Path(args.zip)
    if not archive.exists():
        download(URL, archive)

    out = pathlib.Path(args.out)
    clips = out / "clips"
    for label in CLASSES:
        (out / label).mkdir(parents=True, exist_ok=True)
    clips.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(archive) as bundle:
        for label in CLASSES:
            names = sorted(name for name in bundle.namelist()
                           if name.startswith(label + "/")
                           and name.endswith(".wav"))
            if not names:
                print(f"ERROR: the ZIP file has no clips of the class {label}")
                return 1
            # The names are in the order of the speaker codes, so a step
            # through the list gives clips of many speakers.
            step = max(1, len(names) // args.each)
            picked = names[::step][:args.each]
            for name in picked:
                short = pathlib.Path(name).name
                (out / label / short).write_bytes(bundle.read(name))
                values = read_clip(bundle.open(name))
                text = "\n".join(str(v) for v in values)
                (clips / f"{label}.{short}").write_text(text + "\n",
                                                         encoding="utf-8")
            print(f"{label:<8} {len(picked)} of {len(names)} clips "
                  f"-> {out / label}", flush=True)
    print("The notebook reads the folder keywords/clips/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())