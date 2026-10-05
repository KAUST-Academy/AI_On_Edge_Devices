#!/usr/bin/env bash
# setup_pi.sh - install the course software on a Raspberry Pi 5
#
# Run on: the Raspberry Pi 5 (8 GB), Raspberry Pi OS (64-bit), after the
#         first start. The Raspberry Pi needs an internet connection.
# Use:    bash setup_pi.sh            install all parts
#         bash setup_pi.sh base yolo  install the named parts only
# Parts:  base  litert  yolo  slm  network
#
# Credits: the packages and the three virtual environments follow the setup
# steps of "Edge AI Engineering: Raspberry Pi" by Marcelo Rovai
# (mjrovai.github.io/EdgeML_Made_Ease_ebook) and of the Raspberry Pi kit labs
# of "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0).
#
# The script is safe to run again. It does not delete a file.

set -euo pipefail

PARTS=("$@")
if [ ${#PARTS[@]} -eq 0 ]; then
    PARTS=(base litert yolo slm network)
fi

LOG="$HOME/setup_pi.log"
COURSE_DIR="$HOME/edgeai"

say() { echo; echo "=== $* ==="; }

want() {
    local part
    for part in "${PARTS[@]}"; do
        [ "$part" = "$1" ] && return 0
    done
    return 1
}

# Make a virtual environment that can see the system packages.
# picamera2 comes from apt, so the environment must see it.
make_venv() {
    local path="$1"
    if [ ! -x "$path/bin/python" ]; then
        python3 -m venv "$path" --system-site-packages
    fi
    "$path/bin/pip" install --upgrade pip
}

if [ "$(uname -m)" != "aarch64" ]; then
    echo "ERROR: this script needs a 64-bit operating system (aarch64)."
    echo "Found: $(uname -m). Write Raspberry Pi OS (64-bit) to the card."
    exit 1
fi

{
echo "setup_pi.sh started: $(date -Is), parts: ${PARTS[*]}"

if want base; then
    say "Part base: system update and system packages"
    sudo apt-get update
    sudo apt-get -y full-upgrade
    # Camera and Python tools (book: sections "Installing a Camera" and
    # "Updating and Installing Software").
    sudo apt-get install -y \
        python3-pip python3-venv python3-picamera2 \
        libcamera-dev libcamera-tools libcamera-apps \
        git htop curl wget ffmpeg
    mkdir -p "$COURSE_DIR/models" "$COURSE_DIR/images" "$COURSE_DIR/logs"
fi

if want litert; then
    say "Part litert: environment ~/tflite_env (Days 7 and 9)"
    make_venv "$HOME/tflite_env"
    "$HOME/tflite_env/bin/pip" install numpy pillow matplotlib opencv-python
    "$HOME/tflite_env/bin/pip" install ai-edge-litert onnx onnxruntime
    "$HOME/tflite_env/bin/pip" install jupyter jupyterlab notebook
fi

if want yolo; then
    say "Part yolo: environment ~/yolo (Days 8, 11, and 13)"
    make_venv "$HOME/yolo"
    "$HOME/yolo/bin/pip" install torch torchvision \
        --index-url https://download.pytorch.org/whl/cpu
    # The Day 8 lab exports its models on the laptop with this version of
    # the package. ncnn and ai-edge-litert run the exported files.
    "$HOME/yolo/bin/pip" install "ultralytics==8.4.171" ncnn ai-edge-litert
    "$HOME/yolo/bin/pip" install paho-mqtt psutil prometheus-client flask
    "$HOME/yolo/bin/pip" install jupyter jupyterlab notebook
fi

if want slm; then
    say "Part slm: Ollama and environment ~/ollama (Day 10)"
    if ! command -v ollama >/dev/null 2>&1; then
        curl -fsSL https://ollama.com/install.sh | sh
    fi
    make_venv "$HOME/ollama"
    "$HOME/ollama/bin/pip" install ollama requests pydantic
    "$HOME/ollama/bin/pip" install jupyter jupyterlab notebook
    echo "The models are not downloaded here. See Labs/hardware/HW-05."
fi

if want network; then
    say "Part network: tools for Days 11 to 13"
    # iperf3 asks a question during the installation. Answer "no" in advance.
    echo "iperf3 iperf3/start_daemon boolean false" | sudo debconf-set-selections
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
        iperf3 mosquitto mosquitto-clients avahi-utils
    echo "MediaMTX: see Labs/hardware/HW-06."
    echo "Broker settings: see Labs/hardware/HW-07."
    echo "Prometheus and Grafana: see Labs/hardware/HW-08."
fi

say "Complete"
echo "Next: bash check_pi.sh"
echo "setup_pi.sh ended: $(date -Is)"
} 2>&1 | tee -a "$LOG"
