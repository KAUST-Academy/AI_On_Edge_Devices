#!/usr/bin/env bash
# Download the MicroPython firmware for the XIAO ESP32S3 and check the file.
#
# Source of the file: micropython.org/download/SEEED_XIAO_ESP32S3/
# The checksum was computed on 2026-10-01 from a download of that page.
#
# Use:  bash get_firmware.sh
set -euo pipefail

FILE="SEEED_XIAO_ESP32S3-20260824-v1.29.0.bin"
URL="https://micropython.org/resources/firmware/${FILE}"
SHA256="07a24ab9ee2bc393fb2ed99eed71bb538364b8297924a1daf6e7d7eaf4c85a0b"

# Git ignores the folder "downloads".
cd "$(dirname "$0")"
mkdir -p downloads

if [ ! -f "downloads/${FILE}" ]; then
    echo "Download ${URL}"
    curl -fL --retry 3 -o "downloads/${FILE}" "${URL}"
fi

echo "${SHA256}  downloads/${FILE}" | sha256sum --check -
echo "Firmware file: $(pwd)/downloads/${FILE}"
