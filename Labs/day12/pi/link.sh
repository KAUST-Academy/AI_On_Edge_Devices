#!/bin/bash
# link.sh - cut and restore the link from the Raspberry Pi to the cloud broker
#
# Day 12 lab, Part D. Runs on: the Raspberry Pi of the group.
#
# Use:
#   bash link.sh down 192.168.8.10     # cut the link to this address
#   bash link.sh up 192.168.8.10       # restore the link
#   bash link.sh show 192.168.8.10     # show the route to this address
#
# "down" adds a blackhole route for the one address of the cloud broker. The
# kernel then drops each packet to this address, with no answer: the same
# effect as a lost Wi-Fi link or a lost internet link. The TCP connection
# stays open until the keep-alive of the forwarder finds the loss. All other
# traffic of the lab network continues: the XIAO, the local broker, and SSH.

set -u
ACTION="${1:-}"
ADDRESS="${2:-}"
if [ -z "$ACTION" ] || [ -z "$ADDRESS" ]; then
  echo "Use: bash link.sh down|up|show <address of the cloud broker>"
  exit 1
fi

case "$ACTION" in
  down)
    sudo ip route add blackhole "$ADDRESS/32" && echo "Link to $ADDRESS: DOWN"
    ;;
  up)
    sudo ip route del blackhole "$ADDRESS/32" && echo "Link to $ADDRESS: UP"
    ;;
  show)
    ;;
  *)
    echo "Unknown action: $ACTION (use down, up, or show)"
    exit 1
    ;;
esac
ip route get "$ADDRESS" 2>&1 | head -1
