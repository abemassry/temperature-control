#!/bin/bash
# replace IP with IP of RaspberryPiZeroW
sudo ip link set wlan0 up; sudo ip addr add 192.168.1.172/24 dev wlan0
