#!/usr/bin/env python3
"""Day 8 lab, Part B: train a YOLO11n model on the dataset cup and bottle.

Runs on: the laptop (or Colab), in the environment of this lab, from the
         folder Labs/day08/. The notebook custom_detector.ipynb starts this
         script in the background. You can also start it in a terminal.
Use:     python train_detector.py
         python train_detector.py --epochs 40
Output:  the folder runs/cupbottle/ with the curves and the weights, and
         the file models/cupbottle.pt (a copy of the best weights).

The training starts from the weights yolo11n.pt, which the package
downloads (5.4 MB). The option freeze=10 keeps the first 10 modules of the
model (the backbone) fixed. Only the neck and the head learn. An epoch is
then faster, and 240 images cannot damage the features of the backbone.
"""
import argparse
import json
import os
import shutil
import time

LAB = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser(description="Train the detector for cup and bottle.")
    parser.add_argument("--data", default=os.path.join(LAB, "data", "cup_bottle", "data.yaml"),
                        help="dataset file (default data/cup_bottle/data.yaml)")
    parser.add_argument("--epochs", type=int, default=25, help="epochs (default 25)")
    parser.add_argument("--imgsz", type=int, default=320, help="image size (default 320)")
    parser.add_argument("--batch", type=int, default=16, help="images in a batch (default 16)")
    parser.add_argument("--freeze", type=int, default=10,
                        help="number of fixed modules, 0 for none (default 10: the backbone)")
    parser.add_argument("--device", default="cpu",
                        help='"cpu", or the number of an accelerator, for example 0 (default cpu)')
    parser.add_argument("--name", default="cupbottle", help="name of the run (default cupbottle)")
    args = parser.parse_args()

    if not os.path.isfile(args.data):
        raise SystemExit("ERROR: %s does not exist. Run first: python get_dataset.py" % args.data)

    from ultralytics import YOLO        # the import needs some seconds

    os.makedirs(os.path.join(LAB, "models"), exist_ok=True)
    run = os.path.join(LAB, "runs", args.name)
    done = os.path.join(run, "done.json")
    if os.path.exists(done):
        os.remove(done)

    model = YOLO(os.path.join(LAB, "models", "yolo11n.pt"))
    start = time.time()
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        freeze=args.freeze or None,
        device=args.device,
        seed=0,                 # the same start values in each run
        workers=2,
        project=os.path.join(LAB, "runs"),
        name=args.name,
        exist_ok=True,          # a new run replaces the old run of this name
        plots=True,
    )
    minutes = (time.time() - start) / 60

    best = os.path.join(run, "weights", "best.pt")
    target = os.path.join(LAB, "models", "%s.pt" % args.name)
    shutil.copy(best, target)
    with open(done, "w", encoding="utf-8") as handle:
        json.dump({"minutes": round(minutes, 2), "epochs": args.epochs, "imgsz": args.imgsz,
                   "freeze": args.freeze, "weights": os.path.relpath(target, LAB)}, handle)
    print("Training time: %.1f minutes" % minutes)
    print("Best weights: %s" % os.path.relpath(target, LAB))


if __name__ == "__main__":
    main()
