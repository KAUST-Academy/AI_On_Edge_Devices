# imu_stream.py - send IMU samples to the serial port at a fixed rate
#
# Student version of the Day 2 lab. This version waits a fixed time after
# each sample. Task B1 of the lab replaces the wait with a deadline.
#
# Board:   XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
# Runs on: MicroPython v1.29.0 for SEEED_XIAO_ESP32S3
# Needs:   lsm6ds3.py on the board (mpremote fs cp board/lsm6ds3.py :lsm6ds3.py)
# Run:     mpremote connect PORT run board/imu_stream.py
#
# Output: one CSV line for each sample.
#   n      sample number, starts at 0
#   t_us   time since the first sample, in microseconds
#   ax..az acceleration in g
#   gx..gz angular rate in degrees per second
#
# Credits: the sampling rate of 50 Hz follows the data collection sketch of
# the motion classification chapter of "Machine Learning Systems"
# (mlsysbook.ai, CC BY-NC-SA 4.0).

import time
from machine import I2C, Pin
from lsm6ds3 import LSM6DS3

RATE_HZ = 50                       # the kit lab uses 50 Hz
PERIOD_US = 1000000 // RATE_HZ

i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)
imu = LSM6DS3(i2c)

print("n,t_us,ax,ay,az,gx,gy,gz")

n = 0
elapsed_us = 0
last = time.ticks_us()

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

        # TODO (student), task B1: this line waits one full period after the
        # work of the loop. The read time and the print time add to each
        # period, so the rate is lower than RATE_HZ.
        # Replace the line with a deadline:
        #   1. Keep a variable "deadline". Start it with time.ticks_us()
        #      before the loop.
        #   2. Add PERIOD_US to the deadline with time.ticks_add().
        #   3. Calculate the time to the deadline with time.ticks_diff().
        #   4. Sleep only for this time with time.sleep_us().
        #   5. If the time is negative, the loop is too slow. Start a new
        #      time base: deadline = time.ticks_us().
        time.sleep_us(PERIOD_US)
except KeyboardInterrupt:
    print("# stopped after %d samples" % n)
