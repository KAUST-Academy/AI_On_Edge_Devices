# config.py - network settings of the group for imu_wifi.py
#
# Change the three values. Copy the file to the board:
#   mpremote connect PORT fs cp board/config.py :config.py

WIFI_SSID = "edgeai-lab"        # name of the lab Wi-Fi
WIFI_PASSWORD = "change-me"     # password of the lab Wi-Fi
LAPTOP_IP = "192.168.8.150"     # IP address of your laptop in the lab Wi-Fi
UDP_PORT = 5005                 # port of host/logger.py --udp
