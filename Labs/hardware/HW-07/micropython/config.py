# config.py - network settings of the group for mqtt_imu.py
#
# Change the four values. Copy the file to the board:
#   mpremote connect PORT fs cp micropython/config.py :config.py

WIFI_SSID = "edgeai-lab"        # name of the lab Wi-Fi
WIFI_PASSWORD = "change-me"     # password of the lab Wi-Fi
MQTT_BROKER = "192.168.8.101"   # IP address of your Raspberry Pi
GROUP_ID = "g00"                # your group: g01, g02, ...
