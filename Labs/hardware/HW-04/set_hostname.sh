#!/usr/bin/env bash
# set_hostname.sh - give one copy of the master card its own identity
#
# Run on: each Raspberry Pi, at its first start with a copied card.
# Use:    sudo bash set_hostname.sh 07        the group number, 01 to 99
#
# The script sets the host name pi-NN, makes new SSH host keys, makes a new
# machine identity, and starts the Raspberry Pi again.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: run this script with sudo."
    exit 1
fi

if ! [[ "${1:-}" =~ ^[0-9]{2}$ ]]; then
    echo "Use: sudo bash set_hostname.sh NN    (NN = group number, two digits)"
    exit 1
fi

NEW_NAME="pi-$1"
OLD_NAME="$(hostname)"

echo "Host name: $OLD_NAME -> $NEW_NAME"
if command -v raspi-config >/dev/null 2>&1; then
    raspi-config nonint do_hostname "$NEW_NAME"
else
    hostnamectl set-hostname "$NEW_NAME"
    sed -i "s/\b$OLD_NAME\b/$NEW_NAME/g" /etc/hosts
fi

echo "New SSH host keys"
rm -f /etc/ssh/ssh_host_*
ssh-keygen -A

echo "New machine identity"
rm -f /etc/machine-id /var/lib/dbus/machine-id
systemd-machine-id-setup

echo "Complete. The Raspberry Pi starts again in 5 seconds."
echo "Then connect with: ssh $(logname 2>/dev/null || echo USER)@$NEW_NAME.local"
sleep 5
reboot
