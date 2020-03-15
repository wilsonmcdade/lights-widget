"""
Python file to deploy to a raspi with a WS2812B LED strip connected
Author: Wilson McDade
"""

import RPi.GPIO as gpio
from flask import Flask, request
import time
import sys
import board
from neopixel import *

app = Flask(__name__)

COLORS_DICT = {'aquamarine': (112, 219, 147), 'mediumaquamarine': (50, 204, 153), 'MediumAquamarine': (50, 204, 153),
               'black': (0, 0, 0), 'blue': (0, 0, 255), 'cadetblue': (95, 159, 159), 'CadetBlue': (95, 159, 159),
               'cornflowerblue': (66, 66, 111), 'CornflowerBlue': (66, 66, 111), 'darkslateblue': (107, 35, 142),
               'DarkSlateBlue': (107, 35, 142), 'lightblue': (191, 216, 216), 'LightBlue': (191, 216, 216),
               'lightsteelblue': (143, 143, 188), 'LightSteelBlue': (143, 143, 188), 'mediumblue': (50, 50, 204),
               'MediumBlue': (50, 50, 204), 'mediumslateblue': (127, 0, 255), 'MediumSlateBlue': (127, 0, 255),
               'midnightblue': (47, 47, 79), 'MidnightBlue': (47, 47, 79), 'navyblue': (35, 35, 142),
               'NavyBlue': (35, 35, 142), 'navy': (35, 35, 142), 'skyblue': (50, 153, 204), 'SkyBlue': (50, 153, 204),
               'slateblue': (0, 127, 255), 'SlateBlue': (0, 127, 255), 'steelblue': (35, 107, 142),
               'SteelBlue': (35, 107, 142), 'coral': (255, 127, 0), 'cyan': (0, 255, 255), 'purple': (176, 0, 255),
               'firebrick': (142, 35, 35), 'brown': (165, 42, 42), 'sandybrown': (244, 164, 96),
               'SandyBrown': (244, 164, 96), 'gold': (204, 127, 50), 'goldenrod': (219, 219, 112),
               'mediumgoldenrod': (234, 234, 173), 'MediumGoldenrod': (234, 234, 173), 'green': (0, 255, 0),
               'darkgreen': (47, 79, 47), 'DarkGreen': (47, 79, 47), 'darkolivegreen': (79, 79, 47),
               'DarkOliveGreen': (79, 79, 47), 'forestgreen': (35, 142, 35), 'ForestGreen': (35, 142, 35),
               'limegreen': (50, 204, 50), 'LimeGreen': (50, 204, 50), 'mediumforestgreen': (107, 142, 35),
               'MediumForestGreen': (107, 142, 35), 'mediumseagreen': (66, 111, 66), 'MediumSeaGreen': (66, 111, 66),
               'mediumspringgreen': (127, 255, 0), 'MediumSpringGreen': (127, 255, 0), 'palegreen': (143, 188, 143),
               'PaleGreen': (143, 188, 143), 'seagreen': (35, 142, 107), 'SeaGreen': (35, 142, 107),
               'springgreen': (0, 255, 127), 'SpringGreen': (0, 255, 127), 'yellowgreen': (153, 204, 50),
               'YellowGreen': (153, 204, 50), 'darkslategrey': (47, 79, 79), 'DarkSlateGrey': (47, 79, 79),
               'darkslategray': (47, 79, 79), 'DarkSlateGray': (47, 79, 79), 'dimgrey': (84, 84, 84),
               'DimGrey': (84, 84, 84), 'dimgray': (84, 84, 84), 'DimGray': (84, 84, 84),
               'lightgrey': (168, 168, 168), 'LightGrey': (168, 168, 168), 'lightgray': (168, 168, 168),
               'LightGray': (168, 168, 168), 'gray': (192, 192, 192), 'grey': (192, 192, 192),
               'khaki': (159, 159, 95), 'magenta': (255, 0, 255), 'maroon': (142, 35, 107), 'orange': (204, 50, 50),
               'orchid': (219, 112, 219), 'darkorchid': (153, 50, 204), 'DarkOrchid': (153, 50, 204),
               'mediumorchid': (147, 112, 219), 'MediumOrchid': (147, 112, 219), 'pink': (188, 143, 143),
               'plum': (234, 173, 234), 'red': (255, 0, 0), 'indianred': (79, 47, 47), 'IndianRed': (79, 47, 47),
               'mediumvioletred': (219, 112, 147), 'MediumVioletRed': (219, 112, 147), 'orangered': (255, 0, 127),
               'OrangeRed': (255, 0, 127), 'violetred': (204, 50, 153), 'VioletRed': (204, 50, 153),
               'salmon': (111, 66, 66), 'sienna': (142, 107, 35), 'tan': (219, 147, 112), 'thistle': (216, 191, 216),
               'turquoise': (173, 234, 234), 'darkturquoise': (112, 147, 219), 'DarkTurquoise': (112, 147, 219),
               'mediumturquoise': (112, 219, 219), 'MediumTurquoise': (112, 219, 219), 'violet': (79, 47, 79),
               'blueviolet': (159, 95, 159), 'BlueViolet': (159, 95, 159), 'wheat': (216, 216, 191),
               'white': (255, 255, 255), 'yellow': (255, 255, 0), 'greenyellow': (147, 219, 112),
               'GreenYellow': (147, 219, 112)}

def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

@app.route('/color&<name>', methods=['GET'])
def set_color(name):
    if setup == True:
        if name in COLORS_DICT:
            strip.fill(COLORS_DICT[name])
            return "True"
        else:
            return "not in dict"
    else:
        return "setup first"

@app.route('/rgb&<red>&<green>&<blue>', methods=['GET'])
def rgb(red,green,blue):
    if setup == True:
        red = int(red)
        green = int(green)
        blue = int(blue)

        if red < 256 and green < 256 and blue < 256:
            strip.fill((red,green,blue))
            return "True"
        else:
            return "False"
    else:
        return "False"

@app.route('/off', methods=['GET'])
def off():
    strip.fill((0,0,0))
    return "True"

@app.route('/setup&<num>', methods=['GET'])
def setup(num):

    print("beginning setup...")
    #inits strip
    global strip
    strip = NeoPixel(board.D12,int(num))

    global num_pixels
    num_pixels = int(num)

    #flashes strip red
    for i in range(0,4):
        strip.fill((255,0,0))
        strip.show()
        time.sleep(.2)
        strip.fill((0,0,0))
        strip.show()
        time.sleep(.2)

    global setup
    setup = True

    print("finished setup.")

    return "True"

@app.route('/rainbow')
def rainbow():
    if setup == True:
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                strip[i] = wheel(pixel_index & 255)
            strip.show()
            time.sleep(20/1000)
        return "True"
    else:
        return "False"

if __name__ == "__main__":
    app.run("0.0.0.0",port="8080")
