#!/usr/bin/env bash
# check_pi.sh - check one Raspberry Pi 5 of the course
#
# Run on: the Raspberry Pi, after setup_pi.sh.
# Use:    bash check_pi.sh
#
# The script prints one line for each check: PASS, FAIL, or INFO.
# It changes nothing. Its exit code is the number of failed checks.

FAILED=0

pass() { echo "PASS  $*"; }
fail() { echo "FAIL  $*"; FAILED=$((FAILED + 1)); }
info() { echo "INFO  $*"; }

# check "text" command...   PASS when the command has exit code 0
check() {
    local text="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        pass "$text"
    else
        fail "$text"
    fi
}

# Find the camera tool. Its name changed from libcamera-* to rpicam-*.
camera_tool() {
    local name
    for name in "rpicam-$1" "libcamera-$1"; do
        if command -v "$name" >/dev/null 2>&1; then
            echo "$name"
            return 0
        fi
    done
    return 1
}

echo "Check of $(hostname) on $(date -Is)"
echo

# --- System -----------------------------------------------------------------
MODEL="unknown"
if [ -r /proc/device-tree/model ]; then
    MODEL=$(tr -d '\0' < /proc/device-tree/model)
fi
info "Model:   $MODEL"
info "OS:      $(. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME")"
info "Kernel:  $(uname -r) $(uname -m)"
info "Python:  $(python3 --version 2>&1)"
info "Host:    $(hostname), addresses: $(hostname -I 2>/dev/null)"

check "64-bit operating system (aarch64)" test "$(uname -m)" = "aarch64"

MEM_KB=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
info "RAM:     $((MEM_KB / 1024)) MB"
if [ "$MEM_KB" -gt 7000000 ]; then
    pass "RAM is 8 GB or more"
else
    fail "RAM is less than 8 GB. Day 10 needs 8 GB."
fi

FREE_GB=$(df --output=avail -BG "$HOME" | tail -1 | tr -dc '0-9')
info "Disk:    ${FREE_GB} GB free in $HOME"
if [ "${FREE_GB:-0}" -ge 20 ]; then
    pass "20 GB or more are free"
else
    fail "Less than 20 GB are free. The models of Day 10 need space."
fi

# --- Temperature and power --------------------------------------------------
if command -v vcgencmd >/dev/null 2>&1; then
    info "Temperature: $(vcgencmd measure_temp)"
    THROTTLED=$(vcgencmd get_throttled)
    info "Power state: $THROTTLED"
    if [ "$THROTTLED" = "throttled=0x0" ]; then
        pass "No low voltage and no throttling since the start"
    else
        fail "Low voltage or throttling occurred. Check the power supply and the cooler."
    fi
else
    fail "vcgencmd not found"
fi

# --- Network ----------------------------------------------------------------
check "SSH server is active" systemctl is-active ssh
check "avahi-daemon is active (name $(hostname).local)" systemctl is-active avahi-daemon

# --- Camera -----------------------------------------------------------------
if HELLO=$(camera_tool hello); then
    CAMERAS=$("$HELLO" --list-cameras 2>&1)
    if echo "$CAMERAS" | grep -q "^ *0 :"; then
        pass "Camera found: $(echo "$CAMERAS" | grep "^ *0 :" | head -1 | sed 's/^ *//')"
        if JPEG=$(camera_tool jpeg); then
            SHOT="/tmp/check_pi_camera.jpg"
            rm -f "$SHOT"
            "$JPEG" --output "$SHOT" --width 640 --height 480 --nopreview -t 1000 \
                >/dev/null 2>&1
            if [ -s "$SHOT" ]; then
                pass "Camera image saved: $SHOT ($(stat -c %s "$SHOT") bytes)"
            else
                fail "The camera saved no image"
            fi
        fi
    else
        fail "No camera found. Check the cable and its direction."
    fi
else
    fail "Camera tool not found (rpicam-hello or libcamera-hello)"
fi

# --- Python environments ------------------------------------------------------
# check_import <environment> <module> [<module> ...]
check_import() {
    local env="$1"
    shift
    local py="$HOME/$env/bin/python"
    if [ ! -x "$py" ]; then
        fail "Environment ~/$env not found"
        return
    fi
    local module
    for module in "$@"; do
        local version
        if version=$("$py" -c "import $module as m; print(getattr(m, '__version__', 'ok'))" 2>/dev/null); then
            pass "~/$env: $module $version"
        else
            fail "~/$env: cannot import $module"
        fi
    done
}

check_import tflite_env numpy PIL cv2 picamera2 ai_edge_litert onnxruntime
check_import yolo numpy torch ultralytics ncnn ai_edge_litert flask cv2 picamera2 paho.mqtt psutil prometheus_client
check_import ollama ollama pydantic

# --- Tools --------------------------------------------------------------------
for tool in git ffmpeg iperf3 mosquitto_pub mosquitto_sub ollama; do
    check "Tool: $tool" command -v "$tool"
done
check "Mosquitto broker is active" systemctl is-active mosquitto

echo
if [ "$FAILED" -eq 0 ]; then
    echo "RESULT: PASS - all checks passed"
else
    echo "RESULT: FAIL - $FAILED check(s) failed"
fi
exit "$FAILED"
