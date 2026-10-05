"""Day 8 lab: shared code of the live application and of the benchmark.

The scripts pi/live_detect.py and pi/bench_detect.py import this file. It
has three parts: the source of the frames (the camera or image files), the
model, and the temperature of the processor.
"""
import glob
import os
import re
import sys
import time

os.environ.setdefault("YOLO_VERBOSE", "False")      # no status lines of the package

try:
    import cv2
    from ultralytics import YOLO
except ImportError:
    sys.exit("ERROR: the package ultralytics is not available. "
             "Start the environment: source ~/yolo/bin/activate")

IMAGE_TYPES = (".jpg", ".jpeg", ".png", ".bmp")


class CameraSource:
    """Frames of the Raspberry Pi camera, as arrays in the order blue, green, red."""

    name = "camera"

    def __init__(self, width, height):
        try:
            from picamera2 import Picamera2
        except ImportError:
            sys.exit("ERROR: the package picamera2 is not available. Run this script on the "
                     "Raspberry Pi, or give image files with --source.")
        self.camera = Picamera2()
        # The format "RGB888" of picamera2 gives the bytes in the order blue,
        # green, red. OpenCV and the package ultralytics use this order.
        config = self.camera.create_preview_configuration(
            main={"size": (width, height), "format": "RGB888"})
        self.camera.configure(config)
        self.camera.start()
        time.sleep(2)       # the camera sets its exposure (source script)

    def read(self):
        return self.camera.capture_array()

    def close(self):
        self.camera.stop()


class FileSource:
    """Frames from one image file or from all images of a folder, again and again."""

    name = "files"

    def __init__(self, path, width, height):
        if os.path.isdir(path):
            files = sorted(name for name in glob.glob(os.path.join(path, "*"))
                           if name.lower().endswith(IMAGE_TYPES))
        else:
            files = [path]
        if not files or not all(os.path.isfile(name) for name in files):
            sys.exit("ERROR: no image file at %s" % path)
        self.files = files
        self.size = (width, height)
        self.index = 0

    def read(self):
        # Read and decode the file each time, so that the step "capture" has
        # a cost. The frame gets the size of a camera frame.
        frame = cv2.imread(self.files[self.index])
        self.index = (self.index + 1) % len(self.files)
        if frame is None:
            sys.exit("ERROR: cannot read an image file of the source.")
        return cv2.resize(frame, self.size)

    def close(self):
        pass


def open_source(source, width=640, height=480):
    """source is the word "camera", an image file, or a folder with images."""
    if source == "camera":
        return CameraSource(width, height)
    return FileSource(source, width, height)


def set_litert_threads(threads):
    """Set the number of threads that the package uses for a LiteRT file.

    The package uses the number of cores minus 1 for LiteRT (3 on the
    Raspberry Pi 5), and NCNN uses all cores. For a fair comparison, the
    scripts of this lab give LiteRT the same number as NCNN. Call this
    function before load_model. Return True if the setting works.
    """
    try:
        import ultralytics.nn.backends.litert as litert_backend
        litert_backend.NUM_THREADS = threads
        return True
    except (ImportError, AttributeError):
        return False


def describe(path):
    """Return (runtime, precision, image size) from the name of a model."""
    name = os.path.basename(os.path.normpath(path))
    if name.endswith("_ncnn_model"):
        runtime, precision = "NCNN", "float32"
    elif name.endswith(".tflite"):
        runtime = "LiteRT"
        precision = "int8" if "_int8" in name else "float32"
    elif name.endswith(".onnx"):
        runtime, precision = "ONNX Runtime", "float32"
    else:
        runtime, precision = "PyTorch", "float32"
    match = re.search(r"_(\d{3,4})(?:_|\.|$)", name)
    return runtime, precision, int(match.group(1)) if match else None


def load_model(path):
    if not os.path.exists(path):
        sys.exit("ERROR: the model %s does not exist." % path)
    return YOLO(path, task="detect")


def detect(model, frame, imgsz, conf=0.25, iou=0.7):
    """Run the model on one frame. Return the result of the package.

    result.speed has the time in ms of three steps: "preprocess",
    "inference", and "postprocess". result.boxes has the detections.
    """
    return model.predict(frame, imgsz=imgsz, conf=conf, iou=iou, save=False, verbose=False)[0]


def temperature():
    """Return the temperature of the processor in degrees Celsius, or None."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as handle:
            return int(handle.read().strip()) / 1000.0
    except (OSError, ValueError):
        return None
