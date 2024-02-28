# IMPORTANT
This is a fork of [steelseries-oled](https://github.com/edbgon/steelseries-oled) and is a work in progress. I plan to add more functionality, break a lot of stuff out into functions, add a config file, and a bit more. Right now it'll probably impregnate your cat, cause your fridge to make weird noises, give you an affinity for bears with Unix beards, and otherwise destroy your life. What follows is the original README.md which is probably not accurate at all right now.

# steelseries-oled
Python script for displaying images, arbitrary text, or system stuff on various Steelseries keyboard LEDs



# Installation
```
Use pip to install easyhid, pillow and if you want to use the statistics app, psutil.
Windows requires the hidapi.dll file which can be downloaded from the zip file here: https://github.com/libusb/hidapi/releases
```

# Usage
```
python oled.py image.gif
or
python sysstats.py
or
python profile.py [1-5]
  where [1-5] is the profile number
```
# Tools
Included are two extra tools, one that will display system stats on the OLED and one that will switch profiles.
