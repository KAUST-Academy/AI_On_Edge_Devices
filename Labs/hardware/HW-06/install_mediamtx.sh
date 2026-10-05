#!/usr/bin/env bash
# install_mediamtx.sh - install the RTSP server MediaMTX in ~/mediamtx
#
# Run on: the Raspberry Pi 5 (64-bit), or a Linux laptop for a test.
# Use:    bash install_mediamtx.sh
#
# The script downloads the release v1.21.1 from
# github.com/bluenviron/mediamtx and checks its SHA-256. The checksums come
# from the file checksums.sha256 of that release (read on 2026-10-01).
# The script needs no administrator right.
set -euo pipefail

VERSION="v1.21.1"
case "$(uname -m)" in
    aarch64)
        ARCH="linux_arm64"
        SHA256="6a3aa635fb60ea9b8d566ec306f0a42ff1b6b52a3942bc2baffbe55880d4c3dd"
        ;;
    x86_64)
        ARCH="linux_amd64"
        SHA256="653abc672a3e693f8d3b2717752492fdcfb8072291ec108d03d3dd857411b0ee"
        ;;
    *)
        echo "ERROR: no download for the architecture $(uname -m)."
        exit 1
        ;;
esac

FILE="mediamtx_${VERSION}_${ARCH}.tar.gz"
URL="https://github.com/bluenviron/mediamtx/releases/download/${VERSION}/${FILE}"
TARGET="${MEDIAMTX_DIR:-$HOME/mediamtx}"
HERE="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$TARGET"
cd "$TARGET"

if [ ! -f "$FILE" ]; then
    echo "Download $URL"
    curl -fL --retry 3 -o "$FILE" "$URL"
fi
echo "${SHA256}  ${FILE}" | sha256sum --check -

# The archive holds: mediamtx, mediamtx.yml (all default values), LICENSE.
tar -xzf "$FILE"

# Copy the course settings next to the program.
cp "$HERE/mediamtx_cam.yml" "$TARGET/mediamtx_cam.yml"

echo
echo "Installed: $("$TARGET/mediamtx" --version) in $TARGET"
echo "Start the camera stream:"
echo "  cd $TARGET && ./mediamtx mediamtx_cam.yml"
