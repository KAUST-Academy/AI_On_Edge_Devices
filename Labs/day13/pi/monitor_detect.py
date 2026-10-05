#!/usr/bin/env python3
"""Day 13 lab, Parts A to C: the Day 8 detector with measurements and logs.

Runs on: the Raspberry Pi 5 with the camera, in the environment ~/yolo, from
         the folder ~/edgeai/day13/pi/. The Day 8 lab folder must be at
         ~/edgeai/day08/ (this script uses its file pi/detector.py and its
         models).
Use:     python monitor_detect.py --model ../../day08/models/cupbottle_320_ncnn_model --group g07
         python monitor_detect.py --model ... --group g07 --web
         python monitor_detect.py --model ... --group g07 --dim-after 120 --dim-gain 0.25
Stop:    Ctrl+C.

For each frame, the script measures the time, the largest box score (the
"top score"), the number of objects, and the brightness and the sharpness of
the frame (Task A1 in monitor.py). Each 10 s it makes one summary (Task A2),
adds the system metrics, writes the summary to the log, sends it with MQTT
to edgeai/<group>/pi/metrics, and prints one line.

The log logs/detector.jsonl has one JSON object on each line: the start, a
WARNING for each slow frame, an ERROR for a failed camera read, each
summary, and the stop. It has at most 1 MB and 5 old files.

The model runs with a low score threshold (0.05), so that the top score of
a frame is also known when the model is not sure. The objects count only
the boxes at or above --conf (0.25).

--dim-after S multiplies each frame by --dim-gain after S seconds, for
--dim-seconds seconds: a simulated drift for a test with no lamp.
"""
import argparse
import os
import signal
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
for folder in (os.path.join(HERE, "..", "..", "day08", "pi"),
               os.path.expanduser("~/edgeai/day08/pi")):
    if os.path.isfile(os.path.join(folder, "detector.py")):
        sys.path.insert(0, os.path.abspath(folder))
        break
else:
    sys.exit("ERROR: the Day 8 file pi/detector.py is not found. Copy the Day 8 "
             "lab folder to ~/edgeai/day08/.")
sys.path.insert(0, HERE)

import numpy as np                                                  # noqa: E402
from detector import cv2, describe, detect, load_model, open_source, set_litert_threads  # noqa: E402
import monitor                                                      # noqa: E402

MONITOR_CONF = 0.05          # score threshold of the model for the top score


def run(args, info, web_state=None):
    log = monitor.make_logger(args.log_dir)
    publisher = None
    if not args.no_mqtt:
        try:
            publisher = monitor.Publisher(args.broker, args.group, args.port)
        except OSError as error:
            sys.exit("ERROR: cannot connect to the broker %s:%d: %s" % (args.broker, args.port, error))
    model = load_model(args.model)
    source = open_source(args.source, args.width, args.height)
    detect(model, source.read(), info["imgsz"], MONITOR_CONF, args.iou)   # the first run is slow
    monitor.system_metrics(args.log_dir)       # starts the CPU measurement
    log.info("start", extra={"fields": dict(info, group=args.group, conf=args.conf,
                                            summary_s=args.summary_seconds,
                                            slow_ms=args.slow_ms)})
    print("Log: %s" % os.path.join(args.log_dir, "detector.jsonl"))
    if publisher:
        print("MQTT: %s on %s:%d" % (publisher.topic, args.broker, args.port))

    state = {"window": [], "errors": 0, "dim": False, "last": time.monotonic()}

    def maybe_summary():
        now = time.monotonic()
        if now - state["last"] < args.summary_seconds:
            return
        summary = monitor.summarize(state["window"], now - state["last"])
        summary.update(monitor.system_metrics(args.log_dir))
        summary.update(errors=state["errors"], dimmed=state["dim"])
        log.info("summary", extra={"fields": summary})
        if publisher:
            publisher.publish(summary)
        print("%s %5.1f frames/s  latency %s/%s ms  confidence %s  low %s  objects %s"
              "  brightness %s  sharpness %s  %s C  rss %s MB%s" % (
                  time.strftime("%H:%M:%S"), summary.get("fps", 0),
                  summary.get("latency_ms"), summary.get("latency_p95_ms"),
                  summary.get("confidence"), summary.get("low_conf"),
                  summary.get("objects"), summary.get("brightness"),
                  summary.get("sharpness"), summary.get("cpu_temp_c"),
                  summary.get("rss_mb"), "  (dimmed)" if state["dim"] else ""), flush=True)
        state.update(window=[], errors=0, last=now)

    frames, error_streak = 0, 0
    start = time.monotonic()
    try:
        while True:
            now = time.monotonic()
            if (args.seconds and now - start >= args.seconds) or (args.frames and frames >= args.frames):
                break
            if web_state is not None and web_state.stop:
                break
            t0 = time.perf_counter()
            try:
                frame = source.read()
            except Exception as error:               # a camera that fails
                state["errors"] += 1
                error_streak += 1
                if error_streak == 1:                # log the first error of a streak only
                    log.error("camera_read_failed", extra={"fields": {"error": str(error)[:200]}})
                time.sleep(0.1)
                maybe_summary()
                continue
            error_streak = 0
            elapsed = now - start
            state["dim"] = bool(args.dim_after) and args.dim_after <= elapsed < args.dim_after + args.dim_seconds
            if state["dim"]:
                frame = np.clip(frame * args.dim_gain, 0, 255).astype(np.uint8)
            brightness, sharpness = monitor.input_stats(frame)
            result = detect(model, frame, info["imgsz"], MONITOR_CONF, args.iou)
            scores = result.boxes.conf.tolist()
            t1 = time.perf_counter()
            frames += 1
            record = {"latency_ms": (t1 - t0) * 1000.0,
                      "top_score": max(scores) if scores else 0.0,
                      "objects": sum(s >= args.conf for s in scores),
                      "brightness": brightness, "sharpness": sharpness}
            state["window"].append(record)
            if record["latency_ms"] > args.slow_ms:
                log.warning("slow_frame", extra={"fields": {
                    "frame": frames, "latency_ms": round(record["latency_ms"], 1),
                    "inference_ms": round(result.speed["inference"], 1)}})
            if web_state is not None:
                shown = result[result.boxes.conf >= args.conf]
                ok, jpeg = cv2.imencode(".jpg", shown.plot(), [cv2.IMWRITE_JPEG_QUALITY, 80])
                with web_state.lock:
                    if ok:
                        web_state.jpeg = jpeg.tobytes()
                        web_state.frames = frames
                    web_state.stats = dict(info, fps=1000.0 / record["latency_ms"],
                                           steps_ms={"frame": record["latency_ms"]},
                                           objects="%d objects, top score %.2f"
                                           % (record["objects"], record["top_score"]))
            maybe_summary()
    except KeyboardInterrupt:
        pass
    finally:
        source.close()
        log.info("stop", extra={"fields": {"frames": frames,
                                           "seconds": round(time.monotonic() - start, 1)}})
        if publisher:
            publisher.close()
        if web_state is not None:
            web_state.stop = True
    print("Stopped after %d frames." % frames)


def main():
    parser = argparse.ArgumentParser(description="The Day 8 detector with measurements and logs.")
    parser.add_argument("--model", required=True, help="model file or NCNN folder of Day 8")
    parser.add_argument("--imgsz", type=int, default=0, help="image size (default: from the name)")
    parser.add_argument("--conf", type=float, default=0.25, help="score threshold of an object (0.25)")
    parser.add_argument("--iou", type=float, default=0.7, help="IoU threshold (default 0.7)")
    parser.add_argument("--source", default="camera", help='"camera", an image file, or a folder')
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--threads", type=int, default=4, help="threads for a LiteRT file (4)")
    parser.add_argument("--group", required=True, help="for example g07")
    parser.add_argument("--broker", default="localhost", help="MQTT broker (default localhost)")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--no-mqtt", action="store_true", help="write the log only")
    parser.add_argument("--summary-seconds", type=float, default=10.0, help="seconds between two summaries (10)")
    parser.add_argument("--slow-ms", type=float, default=250.0, help="a frame above this time is slow (250)")
    parser.add_argument("--log-dir", default=os.path.normpath(os.path.join(HERE, "..", "logs")),
                        help="folder of the log (default ../logs)")
    parser.add_argument("--seconds", type=float, default=0, help="stop after this time")
    parser.add_argument("--frames", type=int, default=0, help="stop after this number of frames")
    parser.add_argument("--dim-after", type=float, default=0, help="simulated drift: start after S seconds")
    parser.add_argument("--dim-gain", type=float, default=0.25, help="simulated drift: pixel factor (0.25)")
    parser.add_argument("--dim-seconds", type=float, default=180.0, help="simulated drift: duration (180)")
    parser.add_argument("--web", action="store_true", help="show the image on port 5000 (Day 8 page)")
    args = parser.parse_args()

    if not monitor.check_tasks():
        print("NOTE: complete the tasks in monitor.py. The values of an incomplete task are wrong.")
    runtime, precision, size = describe(args.model)
    imgsz = args.imgsz or size
    if not imgsz:
        sys.exit("ERROR: the name of the model gives no image size. Use --imgsz.")
    set_litert_threads(args.threads)
    info = {"model": args.model.rstrip("/").split("/")[-1], "runtime": runtime,
            "precision": precision, "imgsz": imgsz}
    print("Model: %(model)s, %(runtime)s, %(precision)s, image size %(imgsz)d" % info)

    if not args.web:
        run(args, info)
        return
    from live_detect import State, make_app            # the Day 8 page
    state = State()

    def worker():
        run(args, info, state)
        os.kill(os.getpid(), signal.SIGINT)        # the end of the run stops the web server

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    print("Open http://<name of this board>:5000 in a browser. Stop with Ctrl+C.")
    try:
        make_app(state).run(host="0.0.0.0", port=5000, threaded=True)
    except KeyboardInterrupt:
        pass
    finally:
        state.stop = True
        thread.join(5)


if __name__ == "__main__":
    main()
