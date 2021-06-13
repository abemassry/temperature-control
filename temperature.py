#!/usr/bin/python3
#
# Temperature Control
#
import os
import glob
import time
from datetime import datetime
from syslog import syslog


syslog("Temperature Control starting up")
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
run_dir = '/home/pi/temperature-control'
time_counter = 0
on_counter = 0
set_temp = 98
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        syslog(f'TC: current temp {temp_f}')
        return temp_f

def get_power_state():
    os.system(f'{run_dir}/getstate.sh')
    power_state = os.popen(f'cat {run_dir}/powerstate.txt').read()
    syslog(f'TC: getting power state: {power_state}')
    try:
        return int(power_state)
    except ValueError:
        return 0

def switch_on():
    os.system(f'{run_dir}/switchon.sh')
    syslog('TC: switching on')

def switch_off():
    os.system(f'{run_dir}/switchoff.sh')
    syslog('TC: switching off')

def check_network():
    network_state = os.popen(f'{run_dir}/networkconnected.sh').read()
    network_state = int(network_state)
    syslog(f'TC: checking networking state: {network_state}')
    if network_state != 0:
        syslog('TC: network state not good, restarting networking')
        os.system(f'{run_dir}/restartnetwork.sh')
        


while True:
    check_network()
    if datetime.now() > datetime.now().replace(hour=7) and datetime.now() < datetime.now().replace(hour=20):
        current_temp = read_temp()
        power_state = get_power_state()

        if current_temp >= set_temp and power_state == 0:
            switch_on()
            power_state = get_power_state()
        if current_temp < set_temp and power_state == 1:
            switch_off()
            power_state = get_power_state()
        

        if time_counter > 10 and power_state == 0:
            switch_on()
            power_state = get_power_state()
            time_counter = 0

        if power_state == 0:
            on_counter = 0
        else:
            on_counter += 1

        time.sleep(30)
        
        if on_counter > 8:
            switch_off()
            on_counter = 0

        if time_counter == 0 and power_state == 1:
            current_temp = read_temp()
            if current_temp < set_temp:
                switch_off()

        time.sleep(30)
        time_counter += 1
    else:
        power_state = get_power_state()
        if power_state == 1:
            switch_off()
        time.sleep(30)
