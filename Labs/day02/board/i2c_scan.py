# i2c_scan.py - list the I2C devices of the XIAOML Kit
#
# Board:   XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
# Runs on: MicroPython v1.29.0 for SEEED_XIAO_ESP32S3
# Run:     mpremote run board/i2c_scan.py
#
# Pins: SDA = GPIO5 (D4), SCL = GPIO6 (D5). Source: pins_arduino.h of the
# board XIAO_ESP32S3 in the Arduino core "esp32" 3.3.12.
# Addresses: IMU 0x6A, display 0x3C. Source: the XIAOML Kit setup chapter of
# "Machine Learning Systems" (mlsysbook.ai, CC BY-NC-SA 4.0).

from machine import I2C, Pin

NAMES = {0x3C: "OLED display (SSD1306)", 0x6A: "IMU (LSM6DS3TR-C)"}

i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)
found = i2c.scan()
print("Found %d device(s)" % len(found))
for address in found:
    print("  0x%02X  %s" % (address, NAMES.get(address, "unknown")))
