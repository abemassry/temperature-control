#!/bin/bash
# replace IP address with IP of wireless Router
ping 192.168.1.1 -c 1 > /dev/null 2>&1
echo $?
