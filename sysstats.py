#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw
from easyhid import Enumeration
from time import sleep
import signal
import sys
import psutil

def signal_handler(sig, frame):
    try:
        # Blank screen on shutdown
        dev.send_feature_report(bytearray([0x61] + [0x00] * 641))
        dev.close()
        print("\n")
        sys.exit(0)
    except:
        sys.exit(0)

# Set up ctrl-c handler
signal.signal(signal.SIGINT, signal_handler)

# Stores an enumeration of all the connected USB HID devices
en = Enumeration()
# Return a list of devices based on the search parameters / Hardcoded to Apex 7
devices = en.find(vid=0x1038, pid=0x161c, interface=1)
if not devices:
    devices = en.find(vid=0x1038, pid=0x1618, interface=1)
if not devices:
    print("No devices found, exiting.")
    sys.exit(0)

# Use first device found with vid/pid
dev = devices[0]

print("Press Ctrl-C to exit.\n")
dev.open()

im = Image.new('1', (128,40))
draw = ImageDraw.Draw(im)

while(1):
    # use a truetype font
    draw.rectangle([(0,0),(128,40)], fill=0)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 9)

    cpu_freq, cpu_min, cpu_max = psutil.cpu_freq()

    draw.text((0, 0), "CPU: {:2.0f}%, {:2d} cores".format(psutil.cpu_percent(interval=1), psutil.cpu_count()), font=font, fill=255)
    #draw.text((0, 10), "CPU Freq: {:4.0f}MHz".format(cpu_freq), font=font, fill=255)
    draw.text((0, 10), "Swap: {0}MiB".format(psutil.swap_memory()[1]/1048576), font=font, fill=255)
    draw.text((0, 20), "CPU temp: {0}C".format(psutil.sensors_temperatures()['coretemp'][0].current), font=font, fill=255)
    draw.text((0, 30), "Load: {0}".format(round(psutil.getloadavg()[0], 3)), font=font, fill=255)

    data = im.tobytes()
    # Set up feature report package
    data = bytearray([0x61]) + data + bytearray([0x00])

    dev.send_feature_report(data)

    sleep(1)

    dev.send_feature_report(bytearray([0x61] + [0x00] * 641))

    sleep(.05)
    draw.rectangle([(0,0),(128,40)], fill=0)
    swap_use = round(psutil.swap_memory()[1]/1048576)
    mem_use = round(psutil.virtual_memory()[3]/1048576)

    draw.text((0, 0), "CPU Freq: {:4.0f}MHz".format(cpu_freq), font=font, fill=255)
    draw.text((0, 10), "Below is a test for mirppc".format(), font=font, fill=255)
    draw.text((0, 20), "Swap: {0}MiB  Memory: {1}MiB".format(swap_use, mem_use), font=font, fill=255)
    
    data = im.tobytes()
    data = bytearray([0x61]) + data + bytearray([0x00])
    dev.send_feature_report(data)

    sleep(1)

dev.close()
