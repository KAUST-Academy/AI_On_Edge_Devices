#!/usr/bin/env python3
"""Day 8 lab, Part C: live detection with the camera.

Runs on: the Raspberry Pi 5 with the camera, in the environment ~/yolo, from
         the folder ~/edgeai/day08/.
Use:     python pi/live_detect.py --model models/cupbottle_320_ncnn_model
         python pi/live_detect.py --model models/cupbottle_320_int8.tflite --conf 0.4
         python pi/live_detect.py --model models/cupbottle_320.tflite --source images/ --no-web --frames 20
View:    open http://pi-NN.local:5000 in the browser of the laptop.
Stop:    Ctrl+C.

The script takes a frame, runs the model, draws the boxes, and gives the
image to a small web server. It prints one line in each second: the frame
rate, the time of each step, and the objects of the last frame.

The image size comes from the name of the model: cupbottle_320... runs with
320 pixels. For a different name, give --imgsz.

Credits: the web server, the camera thread, and the page follow the script
object_detection_app.py of "EdgeML with Raspberry Pi" by Marcelo Rovai
(github.com/Mjrovai/EdgeML-with-Raspberry-Pi, GPL-3.0), which the kit lab
"Object Detection" of "Machine Learning Systems" (mlsysbook.ai,
CC BY-NC-SA 4.0) describes. Changes: the model is a YOLO model of the
package ultralytics (AGPL-3.0) in place of the SSD model, the camera gives
arrays, the page needs no file from the internet, and the script measures
each step.
"""
import argparse
import collections
import statistics
import sys
import threading
import time

from detector import cv2, describe, detect, load_model, open_source, set_litert_threads, temperature

STEPS = ["capture", "pre-processing", "inference", "post-processing", "draw"]

PAGE = """<!DOCTYPE html>
<html>
<head>
<title>Day 8 lab: live detection</title>
<style>
body { font-family: sans-serif; margin: 20px; }
td, th { padding: 2px 12px; text-align: right; }
</style>
</head>
<body>
<h2>Day 8 lab: live detection</h2>
<p id="model"></p>
<img src="/video" alt="live image">
<table id="stats"></table>
<p id="objects"></p>
<script>
function update() {
  fetch("/stats").then(function (reply) { return reply.json(); }).then(function (s) {
    document.getElementById("model").textContent =
      s.model + ", " + s.runtime + ", " + s.precision + ", image size " + s.imgsz;
    var rows = "<tr><th>frames in each second</th><td>" + s.fps.toFixed(1) + "</td></tr>";
    for (var name in s.steps_ms) {
      rows += "<tr><th>" + name + " (ms)</th><td>" + s.steps_ms[name].toFixed(1) + "</td></tr>";
    }
    document.getElementById("stats").innerHTML = rows;
    document.getElementById("objects").textContent = "Last frame: " + s.objects;
  });
}
setInterval(update, 1000);
update();
</script>
</body>
</html>
"""


class State:
    """The values that the worker thread gives to the web server."""

    def __init__(self):
        self.lock = threading.Lock()
        self.jpeg = None
        self.frames = 0
        self.stats = {}
        self.stop = False


def count_objects(result):
    """Return a text such as "2 cup, 1 bottle" for the detections of a frame."""
    counts = collections.Counter(result.names[int(c)] for c in result.boxes.cls.tolist())
    return ", ".join("%d %s" % (n, name) for name, n in sorted(counts.items())) or "no object"


def worker(args, state, info):
    """Take a frame, detect, draw, and store the result. Repeat."""
    model = load_model(args.model)
    source = open_source(args.source, args.width, args.height)
    detect(model, source.read(), info["imgsz"], args.conf, args.iou)    # the first run is slow
    window = collections.deque(maxlen=30)       # the last 30 frames
    last_print = time.perf_counter()
    frames = 0
    try:
        while not state.stop and (args.frames == 0 or frames < args.frames):
            t0 = time.perf_counter()
            frame = source.read()
            t1 = time.perf_counter()
            result = detect(model, frame, info["imgsz"], args.conf, args.iou)
            t2 = time.perf_counter()
            image = result.plot()
            ok, jpeg = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 80])
            t3 = time.perf_counter()
            frames += 1
            window.append({
                "capture": (t1 - t0) * 1000,
                "pre-processing": result.speed["preprocess"],
                "inference": result.speed["inference"],
                "post-processing": result.speed["postprocess"],
                "draw": (t3 - t2) * 1000,
                "frame": (t3 - t0) * 1000,
            })
            steps = {name: statistics.median(row[name] for row in window) for name in STEPS}
            fps = 1000.0 / statistics.median(row["frame"] for row in window)
            objects = count_objects(result)
            with state.lock:
                if ok:
                    state.jpeg = jpeg.tobytes()
                    state.frames = frames
                state.stats = dict(info, fps=fps, steps_ms=steps, objects=objects, frames=frames)
            if t3 - last_print >= 1.0 or frames == args.frames:
                last_print = t3
                degrees = temperature()
                print("%5.1f frames/s | capture %5.1f  pre %4.1f  inference %6.1f  post %4.1f  draw %4.1f ms"
                      " | %s%s" % (fps, steps["capture"], steps["pre-processing"], steps["inference"],
                                   steps["post-processing"], steps["draw"], objects,
                                   "" if degrees is None else " | %.0f C" % degrees), flush=True)
    finally:
        source.close()
        state.stop = True


def make_app(state):
    from flask import Flask, Response, jsonify

    app = Flask(__name__)

    @app.route("/")
    def index():
        return PAGE

    @app.route("/stats")
    def stats():
        with state.lock:
            return jsonify(state.stats)

    @app.route("/video")
    def video():
        def frames():
            sent = 0
            while not state.stop:
                with state.lock:
                    jpeg, number = state.jpeg, state.frames
                if jpeg is not None and number != sent:     # send each frame one time
                    sent = number
                    yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"
                time.sleep(0.01)
        return Response(frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

    return app


def main():
    parser = argparse.ArgumentParser(description="Live detection with the camera.")
    parser.add_argument("--model", required=True, help="model file or NCNN folder")
    parser.add_argument("--imgsz", type=int, default=0, help="image size (default: from the name)")
    parser.add_argument("--conf", type=float, default=0.25, help="score threshold (default 0.25)")
    parser.add_argument("--iou", type=float, default=0.7, help="IoU threshold (default 0.7)")
    parser.add_argument("--source", default="camera",
                        help='"camera", an image file, or a folder with images (default camera)')
    parser.add_argument("--width", type=int, default=640, help="width of a frame (default 640)")
    parser.add_argument("--height", type=int, default=480, help="height of a frame (default 480)")
    parser.add_argument("--threads", type=int, default=4, help="threads for a LiteRT file (default 4)")
    parser.add_argument("--port", type=int, default=5000, help="port of the web server (default 5000)")
    parser.add_argument("--frames", type=int, default=0, help="stop after this number of frames")
    parser.add_argument("--no-web", action="store_true", help="no web server, print only")
    args = parser.parse_args()

    runtime, precision, size = describe(args.model)
    imgsz = args.imgsz or size
    if not imgsz:
        sys.exit("ERROR: the name of the model gives no image size. Use --imgsz.")
    if not set_litert_threads(args.threads) and runtime == "LiteRT":
        print("NOTE: cannot set the threads for LiteRT. The package uses its default.")
    info = {"model": args.model.rstrip("/").split("/")[-1], "runtime": runtime,
            "precision": precision, "imgsz": imgsz}
    print("Model: %(model)s, %(runtime)s, %(precision)s, image size %(imgsz)d" % info)

    state = State()
    thread = threading.Thread(target=worker, args=(args, state, info), daemon=True)
    thread.start()
    try:
        if args.no_web:
            while thread.is_alive():
                thread.join(0.5)
        else:
            try:
                app = make_app(state)
            except ImportError:
                sys.exit("ERROR: the package flask is not available. Use --no-web, or install "
                         "it: pip install flask")
            print("Open http://<name of this board>:%d in a browser. Stop with Ctrl+C." % args.port)
            import logging
            logging.getLogger("werkzeug").setLevel(logging.ERROR)   # no line for each request
            app.run(host="0.0.0.0", port=args.port, threaded=True)
    except KeyboardInterrupt:
        pass
    finally:
        state.stop = True
        thread.join(5)
        print("Stopped.")


if __name__ == "__main__":
    main()
