"""
Python file to deploy to a raspi with a WS2812B LED strip connected
Author: Wilson McDade
"""

import RPi.GPIO as gpio
from flask import Flask, request
import time
import sys
from neopixel import *

def set_color(color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i,color)
        strip.show()

def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

@app.route('/setup&<pin>&<num>', methods=['GET'])
def setup(pin,num):

    #inits strip
    global strip = Adafruit_NeoPixel(int(num),int(pin),800000,10,False,255,0)
    strip.begin()

    #flashes strip red
    for i in range(0,4):
        set_color(Color(255,0,0))
        time.sleep(.2)
        set_color(Color(0,0,0))
        time.sleep(.2)

    global setup = True

    return True

@app.route('/rainbow')
def rainbow():
    if setup == True:
        for j in range(256*5):
            for i in range(strip.numPixels()+1):
                strip.setPixelColor(i, wheel((i+j) & 255))
            strip.show()
            time.sleep(20/1000.0)
        return True
    else:
        return False

if __name__ == "__main__":
    app.run("0.0.0.0",port="8080")
