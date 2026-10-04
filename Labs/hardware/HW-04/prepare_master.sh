#!/usr/bin/env bash
# prepare_master.sh - clean the master card before you copy it
#
# Run on: the master Raspberry Pi, as the last step before the shutdown.
# Use:    bash prepare_master.sh
#
# The script removes the data that must be different on each copy:
# package files, the command history, and the machine identity.
# set_hostname.sh makes the identity again on each copy.
#
# Hardware status: new script, not tested on a Raspberry Pi
# (prepared on 2026-10-01).

set -euo pipefail

echo "This script prepares the card for a copy. The Raspberry Pi shuts down."
read -r -p "Continue? (yes/no) " answer
[ "$answer" = "yes" ] || { echo "Stopped."; exit 1; }

# Free space. A smaller card image is faster to copy.
sudo apt-get clean
rm -rf "$HOME/.cache/pip"
sudo journalctl --rotate
sudo journalctl --vacuum-time=1s

# Remove the command history of the master.
rm -f "$HOME/.bash_history"

# Remove the machine identity. Two computers with the same identity can
# get the same address from the router.
sudo truncate -s 0 /etc/machine-id
sudo rm -f /var/lib/dbus/machine-id

echo "Ready. The Raspberry Pi shuts down now."
echo "Wait until the green LED is off. Then remove the power."
sudo shutdown -h now
