#!/usr/bin/env python3
import configparser
from easyhid import Enumeration
from urllib.request import urlopen
import psutil
import GPUtil

def init_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

def getdevice():
    # Stores an enumeration of all the connected USB HID devices
    en = Enumeration()

    #List of known working devices, add your PID here if it works
    #                Apex 7,  7 TKL, Pro     Apex 5
    supported_pid = (0x1612, 0x1618, 0x1610, 0x161c)

    # Return a list of devices based on the search parameters
    devices = en.find(vid=0x1038, interface=1)
    if not devices:
        exit("No SteelSeries devices found, exiting.")
    # Need to figure out how to handle multiple devices gracefully
    # for now we pick the first one that shows up
    for device in devices:
        if device.product_id in supported_pid:
            return device

    exit("No compatible SteelSeries devices found, exiting.")

def load1():
    round(psutil.getloadavg()[0], 3)

def load5():
    round(psutil.getloadavg()[1], 3)

def load15():
    round(psutil.getloadavg()[1], 3)

def core_temp():
    psutil.sensors_temperatures()['coretemp'][0].current

def gpu_temp():
    try:
        GPUtil.getGPUs()[0].temperature
    except:
        print("No GPU")

def swap_use():
    round(psutil.swap_memory()[1]/1048576)

def swap_percent():
    psutil.swap_memory()[3]

def mem_used():
    round(psutil.virtual_memory()[3]/1048576)

def mem_used_percent():
    psutil.virtual_memory()[2]

def mem_total():
    round(psutil.virtual_memory()[0]/1048576)

def cpu_freq():
    psutil.cpu_freq()[0]

def cpu_count():
    psutil.cpu_count()

def ext_ip():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

def draw_init():
    draw.rectangle([(0,0),(128,40)], fill=0)

def draw_text_3(stat_one, stat_two, stat_three):

def draw_text_4(stat_one, stat_two, stat_three, stat_four):

        
