#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw
from easyhid import Enumeration
from time import sleep
import signal
import sys
import psutil
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

def signal_handler(sig, frame):
    try:
        # Blank screen on shutdown
        dev.send_feature_report(bytearray([0x61] + [0x00] * 641))
        dev.close()
        print("\n")
        sys.exit(0)
    except:
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

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

# Use first device found with vid/pid
dev = getdevice()

if sys.stdout.isatty():
    print("Press Ctrl-C to exit.\n")

dev.open()

im = Image.new('1', (128,40))
draw = ImageDraw.Draw(im)

while(1):
    # use a truetype font
    draw.rectangle([(0,0),(128,40)], fill=0)
    font = ImageFont.truetype("SpaceMono-Regular.ttf", 12)

    cpu_freq, cpu_min, cpu_max = psutil.cpu_freq()

    draw.text((1, 1), "CPU: {:2.0f}%, {:2d} cores".format(psutil.cpu_percent(interval=1), psutil.cpu_count()), font=font, fill=255)
    #draw.text((0, 10), "CPU Freq: {:4.0f}MHz".format(cpu_freq), font=font, fill=255)
    #draw.text((1, 11), "Swap: {0}MiB".format(psutil.swap_memory()[1]/1048576), font=font, fill=255)
    draw.text((1, 11), "CPU temp: {0}C".format(psutil.sensors_temperatures()['coretemp'][0].current), font=font, fill=255)
    draw.text((1, 221), "Load: {0}".format(round(psutil.getloadavg()[0], 3)), font=font, fill=255)

    data = im.tobytes()
    # Set up feature report package
    data = bytearray([0x61]) + data + bytearray([0x00])

    dev.send_feature_report(data)

    sleep(2)

    dev.send_feature_report(bytearray([0x61] + [0x00] * 641))

    sleep(.05)
    draw.rectangle([(0,0),(128,40)], fill=0)
    swap_use = round(psutil.swap_memory()[1]/1048576)
    mem_use = round(psutil.virtual_memory()[3]/1048576)

    draw.text((1, 1), "CPU Freq: {:4.0f}MHz".format(cpu_freq), font=font, fill=255)
    draw.text((1, 11), "Memory: {0}MiB".format(mem_use), font=font, fill=255)
    draw.text((1, 21), "Swap: {0}MiB".format(swap_use), font=font, fill=255)
    
    data = im.tobytes()
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)

    sleep(2)

dev.close()
