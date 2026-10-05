# imu_stream.py - send IMU samples to the serial port at a fixed rate
#
# Board:   XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
# Runs on: MicroPython v1.29.0 for SEEED_XIAO_ESP32S3
# Needs:   lsm6ds3.py on the board (mpremote cp board/lsm6ds3.py :)
# Run:     mpremote run board/imu_stream.py
#
# Output: one CSV line for each sample.
#   n      sample number, starts at 0
#   t_us   time since the first sample, in microseconds
#   ax..az acceleration in g
#   gx..gz angular rate in degrees per second

import time
from machine import I2C, Pin
from lsm6ds3 import LSM6DS3

RATE_HZ = 50                       # the kit lab uses 50 Hz
PERIOD_US = 1000000 // RATE_HZ

i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)
imu = LSM6DS3(i2c)

print("n,t_us,ax,ay,az,gx,gy,gz")

n = 0
late = 0
elapsed_us = 0
last = time.ticks_us()
deadline = last

try:
    while True:
        # Measure the time first, then read the sensor.
        now = time.ticks_us()
        elapsed_us += time.ticks_diff(now, last)
        last = now
        ax, ay, az, gx, gy, gz = imu.read()
        print("%d,%d,%.4f,%.4f,%.4f,%.2f,%.2f,%.2f"
              % (n, elapsed_us, ax, ay, az, gx, gy, gz))
        n += 1

        # Wait for the next deadline. The deadline does not depend on the
        # time that the read and the print need, so the rate does not drift.
        deadline = time.ticks_add(deadline, PERIOD_US)
        wait = time.ticks_diff(deadline, time.ticks_us())
        if wait > 0:
            time.sleep_us(wait)
        else:
            # The loop is too slow for this rate. Start a new time base.
            late += 1
            deadline = time.ticks_us()
except KeyboardInterrupt:
    print("# stopped after %d samples, %d late" % (n, late))
