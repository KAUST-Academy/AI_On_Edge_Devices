# imu_wifi.py - send IMU samples to the laptop over Wi-Fi (UDP)
#
# Board:   XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
# Runs on: MicroPython v1.29.0 for SEEED_XIAO_ESP32S3
# Needs:   config.py and lsm6ds3.py on the board, and the Wi-Fi antenna
# Run:     mpremote connect PORT run board/imu_wifi.py
# Laptop:  python3 host/logger.py --udp 5005 --label test --session wifi
#
# Hardware status: new code, not tested on hardware (prepared on 2026-10-02).
#
# The board sends the same CSV lines as imu_stream.py. One UDP packet holds
# the lines of 5 samples, so the board sends 10 packets each second. UDP has
# no repeat: a packet that the network loses does not arrive. The sample
# number n shows each lost sample.
#
# Credits: the sampling method (a deadline for each sample, 50 Hz) follows
# the data collection sketch of the motion classification chapter of
# "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0). The Wi-Fi
# connection follows Labs/hardware/HW-07/micropython/mqtt_imu.py.

import socket
import time
import network
from machine import I2C, Pin

import config
from lsm6ds3 import LSM6DS3

RATE_HZ = 50
PERIOD_US = 1000000 // RATE_HZ
SAMPLES_IN_PACKET = 5


def connect_wifi():
    """Connect to the lab Wi-Fi. Return the IP address of the board."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to", config.WIFI_SSID)
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep_ms(500)
    return wlan.ifconfig()[0]


print("Board address:", connect_wifi())
target = (config.LAPTOP_IP, config.UDP_PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Sending to %s, port %d" % target)

i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)
imu = LSM6DS3(i2c)

n = 0
late = 0
elapsed_us = 0
last = time.ticks_us()
deadline = last
lines = []

try:
    while True:
        now = time.ticks_us()
        elapsed_us += time.ticks_diff(now, last)
        last = now
        ax, ay, az, gx, gy, gz = imu.read()
        lines.append("%d,%d,%.4f,%.4f,%.4f,%.2f,%.2f,%.2f"
                     % (n, elapsed_us, ax, ay, az, gx, gy, gz))
        n += 1

        if len(lines) == SAMPLES_IN_PACKET:
            try:
                sock.sendto(("\n".join(lines) + "\n").encode(), target)
            except OSError:
                pass             # the network is busy: this packet is lost
            lines = []

        deadline = time.ticks_add(deadline, PERIOD_US)
        wait = time.ticks_diff(deadline, time.ticks_us())
        if wait > 0:
            time.sleep_us(wait)
        else:
            late += 1
            deadline = time.ticks_us()
except KeyboardInterrupt:
    sock.close()
    print("# stopped after %d samples, %d late" % (n, late))
