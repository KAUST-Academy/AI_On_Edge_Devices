# blink_timer.py - switch the LED with a hardware timer, and read the button
#
# Board:   XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
# Runs on: MicroPython v1.29.0 for SEEED_XIAO_ESP32S3
# Run:     mpremote connect PORT run board/blink_timer.py
#
# Hardware status: new code, not tested on hardware (prepared on 2026-10-02).
#
# Pins: the LED is on GPIO21 and it is on when the pin is low. The boot
# button is on GPIO0 and it connects the pin to 0 V. Source: the XIAOML Kit
# setup chapter of "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0)
# and the Seeed Studio wiki of the XIAO ESP32S3.
#
# The timer calls tick() two times each second. The main loop does no
# timing. It only prints what the two handlers counted.

import time
from machine import Pin, Timer

led = Pin(21, Pin.OUT, value=1)          # 1 = LED off
button = Pin(0, Pin.IN, Pin.PULL_UP)     # 0 = pressed

ticks = 0
presses = 0


def tick(timer):
    """Timer handler. Keep it short: change the LED and count."""
    global ticks
    led.value(not led.value())
    ticks += 1


def on_press(pin):
    """Pin handler. It runs when the button goes from high to low."""
    global presses
    presses += 1


timer = Timer(0)
timer.init(freq=2, mode=Timer.PERIODIC, callback=tick)
button.irq(trigger=Pin.IRQ_FALLING, handler=on_press)

print("The LED changes two times each second. Press the boot button.")
print("Press Ctrl-C to stop.")
try:
    while True:
        print("ticks = %d, presses = %d" % (ticks, presses))
        time.sleep(1)
except KeyboardInterrupt:
    timer.deinit()
    button.irq(handler=None)
    led.value(1)
    print("stopped")
