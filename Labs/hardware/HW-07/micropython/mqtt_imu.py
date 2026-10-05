# mqtt_imu.py - send IMU telemetry from the XIAOML Kit with MQTT
#
# Board:   XIAOML Kit (XIAO ESP32S3 Sense with the expansion board)
# Runs on: MicroPython v1.29.0 for SEEED_XIAO_ESP32S3
# Needs:   config.py and lsm6ds3.py (from Labs/hardware/HW-01) on the board,
#          and the module umqtt.simple
# Broker:  Mosquitto on the Raspberry Pi of the group (port 1883)
# Run:     mpremote connect PORT run micropython/mqtt_imu.py
#
# Credits: the telemetry and command design follows chapter 3.5 of
# "XIAO: Big Power, Small Board" by Lei Feng and Marcelo Rovai
# (github.com/Mjrovai/XIAO_Big_Power_Small_Board-ebook, GPL-3.0).
# The chapter has Arduino code only. This MicroPython version is new.
#
# Topics:
#   edgeai/<group>/xiao/status   "online" or "offline", retained, last will
#   edgeai/<group>/xiao/imu      telemetry, each 200 ms
#   edgeai/<group>/xiao/cmd      command to the board: "led=1" or "led=0"

import time
import network
from machine import I2C, Pin
from umqtt.simple import MQTTClient

import config
from lsm6ds3 import LSM6DS3

PERIOD_MS = 200          # 5 messages each second
RETRY_MS = 5000

BASE = "edgeai/%s/xiao" % config.GROUP_ID
TOPIC_STATUS = (BASE + "/status").encode()
TOPIC_IMU = (BASE + "/imu").encode()
TOPIC_CMD = (BASE + "/cmd").encode()

# The built-in LED is on GPIO21. The value 0 turns it on.
led = Pin(21, Pin.OUT, value=1)


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


def on_message(topic, message):
    """The client calls this function for each message on the command topic."""
    print("Message arrived [%s] %s" % (topic.decode(), message.decode()))
    if message == b"led=1":
        led.value(0)     # on
    elif message == b"led=0":
        led.value(1)     # off


def connect_broker():
    """Return a connected client. Raise OSError when the broker is not there."""
    client = MQTTClient("xiao-" + config.GROUP_ID, config.MQTT_BROKER,
                        port=1883, keepalive=15)
    # Last will: the broker sends "offline" when the board disappears.
    client.set_last_will(TOPIC_STATUS, b"offline", retain=True, qos=1)
    client.set_callback(on_message)
    client.connect()
    client.publish(TOPIC_STATUS, b"online", retain=True)
    client.subscribe(TOPIC_CMD, qos=1)
    print("Connected to the broker", config.MQTT_BROKER)
    return client


def main():
    print("IP address:", connect_wifi())
    imu = LSM6DS3(I2C(0, sda=Pin(5), scl=Pin(6), freq=400000))

    client = None
    sequence = 0
    deadline = time.ticks_ms()
    while True:
        if client is None:
            try:
                client = connect_broker()
            except OSError as error:
                print("No broker:", error, "- next try in", RETRY_MS, "ms")
                time.sleep_ms(RETRY_MS)
                continue

        ax, ay, az, gx, gy, gz = imu.read()
        payload = ('{"seq":%d,"ms":%d,"ax":%.3f,"ay":%.3f,"az":%.3f,'
                   '"gx":%.2f,"gy":%.2f,"gz":%.2f}'
                   % (sequence, time.ticks_ms(), ax, ay, az, gx, gy, gz))
        try:
            client.publish(TOPIC_IMU, payload)
            client.check_msg()        # read a command, if one arrived
        except OSError as error:
            print("Connection lost:", error)
            client = None
            continue
        sequence += 1

        deadline = time.ticks_add(deadline, PERIOD_MS)
        wait = time.ticks_diff(deadline, time.ticks_ms())
        if wait > 0:
            time.sleep_ms(wait)
        else:
            deadline = time.ticks_ms()


main()
