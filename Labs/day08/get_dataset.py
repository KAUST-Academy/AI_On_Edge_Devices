#!/usr/bin/env python3
"""Download the dataset "cup and bottle" of the Day 8 lab.

Runs on: the laptop. It needs Python 3.8 or later and no extra package.
Use:     python get_dataset.py              download all 400 images
         python get_dataset.py --check      check the files and count the labels

The file dataset/cup_bottle.csv has one row for each label. This script
downloads each image of that file from the server of COCO, and writes the
dataset in the format of YOLO:

    data/cup_bottle/data.yaml
    data/cup_bottle/train/images/*.jpg    data/cup_bottle/train/labels/*.txt
    data/cup_bottle/valid/images/*.jpg    data/cup_bottle/valid/labels/*.txt
    data/cup_bottle/test/images/*.jpg     data/cup_bottle/test/labels/*.txt

The download has about 65 MB. The script is safe to run again: it keeps
each image that is complete.
"""
import argparse
import collections
import concurrent.futures
import csv
import os
import sys
import time
import urllib.request

LAB = os.path.dirname(os.path.abspath(__file__))
LABELS = os.path.join(LAB, "dataset", "cup_bottle.csv")
OUT = os.path.join(LAB, "data", "cup_bottle")
SERVER = "http://images.cocodataset.org/"
NAMES = ["bottle", "cup"]
SPLITS = ["train", "valid", "test"]


def read_labels():
    """Return {split: {image: [label line, ...]}} from the CSV file."""
    dataset = {split: collections.OrderedDict() for split in SPLITS}
    with open(LABELS, encoding="utf-8") as handle:
        rows = csv.DictReader(line for line in handle if not line.startswith("#"))
        for row in rows:
            line = "%s %s %s %s %s" % (row["class"], row["cx"], row["cy"], row["w"], row["h"])
            dataset[row["split"]].setdefault(row["image"], []).append(line)
    return dataset


def is_jpeg(path):
    """A complete JPEG file starts with FF D8 and ends with FF D9."""
    if not os.path.isfile(path) or os.path.getsize(path) < 1000:
        return False
    with open(path, "rb") as handle:
        start = handle.read(2)
        handle.seek(-2, os.SEEK_END)
        end = handle.read(2)
    return start == b"\xff\xd8" and end == b"\xff\xd9"


def download(job):
    """Download one image. Return an error text, or None."""
    image, path = job
    if is_jpeg(path):
        return None
    error = "no attempt"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(SERVER + image, timeout=30) as reply:
                data = reply.read()
            with open(path + ".part", "wb") as handle:
                handle.write(data)
            os.replace(path + ".part", path)
            if is_jpeg(path):
                return None
            error = "the file is not a complete JPEG image"
        except Exception as exception:      # network errors have many types
            error = str(exception)
        time.sleep(2 * (attempt + 1))
    return "%s: %s" % (image, error)


def write_yaml():
    """data.yaml has no absolute path: the folder can move to a new place."""
    with open(os.path.join(OUT, "data.yaml"), "w", encoding="utf-8") as handle:
        handle.write("# Dataset cup and bottle of the Day 8 lab (images and labels of COCO 2017).\n")
        handle.write("# The three paths are relative to the folder of this file.\n")
        handle.write("train: train/images\nval: valid/images\ntest: test/images\n\n")
        handle.write("nc: %d\nnames: %s\n" % (len(NAMES), NAMES))


def report(dataset):
    """Print the table of the dataset. Return the number of missing images."""
    missing = 0
    print("%-6s %7s %7s %7s %8s" % ("split", "images", "bottle", "cup", "missing"))
    for split in SPLITS:
        counts = collections.Counter()
        gone = 0
        for image, lines in dataset[split].items():
            path = os.path.join(OUT, split, "images", os.path.basename(image))
            gone += not is_jpeg(path)
            counts.update(NAMES[int(line.split()[0])] for line in lines)
        missing += gone
        print("%-6s %7d %7d %7d %8d" % (split, len(dataset[split]), counts["bottle"], counts["cup"], gone))
    return missing


def main():
    parser = argparse.ArgumentParser(description="Download the dataset cup and bottle.")
    parser.add_argument("--check", action="store_true", help="check the files, download nothing")
    parser.add_argument("--workers", type=int, default=8, help="parallel downloads (default 8)")
    args = parser.parse_args()

    dataset = read_labels()
    if not args.check:
        jobs = []
        for split in SPLITS:
            os.makedirs(os.path.join(OUT, split, "images"), exist_ok=True)
            os.makedirs(os.path.join(OUT, split, "labels"), exist_ok=True)
            for image, lines in dataset[split].items():
                name = os.path.basename(image)
                with open(os.path.join(OUT, split, "labels", name[:-4] + ".txt"), "w") as handle:
                    handle.write("\n".join(lines) + "\n")
                jobs.append((image, os.path.join(OUT, split, "images", name)))
        write_yaml()
        print("Download of %d images from %s" % (len(jobs), SERVER))
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            for count, _ in enumerate(pool.map(download, jobs), 1):
                if count % 50 == 0 or count == len(jobs):
                    print("  %3d of %d" % (count, len(jobs)))
        # A network error can stop some images. Try these images again, one
        # after the other, in three more rounds.
        errors = []
        for round_number in range(3):
            missing = [job for job in jobs if not is_jpeg(job[1])]
            if not missing:
                break
            print("  %d images are not complete. Round %d of 3 for these images."
                  % (len(missing), round_number + 1))
            time.sleep(5)
            errors = [error for error in map(download, missing) if error]
        print("Time: %.0f s" % (time.time() - start))
        for error in errors[:10]:
            print("ERROR:", error)

    missing = report(dataset)
    if missing:
        print("RESULT: not complete. Missing images: %d. Run the script again." % missing)
        sys.exit(1)
    size = sum(os.path.getsize(os.path.join(root, name))
               for root, _, names in os.walk(OUT) for name in names if name.endswith(".jpg"))
    print("Size of the images: %.1f MB" % (size / 1e6))
    print("RESULT: complete. Dataset file:", os.path.relpath(os.path.join(OUT, "data.yaml")))


if __name__ == "__main__":
    main()
