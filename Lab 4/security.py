# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import qwiic
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


# initial center of the circle
center_x = 63
center_y = 15
# how fast does it move in each direction
x_inc = 1
y_inc = 1
# what is the starting radius of the circle
radius = 8

# start with a blank screen
oled.fill(0)
# we just blanked the framebuffer. to push the framebuffer onto the display, we call show()
oled.show()


print("VL53L1X Qwiic Test\n")
ToF = qwiic.QwiicVL53L1X()
if (ToF.sensor_init() == None):         # Begin returns 0 on a good init
    print("Sensor online!\n")


firstDistFeet = 0.0
while True:
    try:
        ToF.start_ranging()             # Write configuration bytes to initiate measurement
        time.sleep(.005)
        distance = ToF.get_distance()   # Get the result of the measurement from the sensor
        time.sleep(.005)
        ToF.stop_ranging()

        distanceInches = distance / 25.4
        distanceFeet = distanceInches / 12.0
        if firstDistFeet == 0.0:
            firstDistFeet = distanceFeet
            
        elif abs(firstDistFeet - distanceFeet) > 0.2 * firstDistFeet:
            oled.fill(1)

        else:
            oled.fill(0)

        print(firstDistFeet, distanceFeet, abs(firstDistFeet - distanceFeet))
        oled.show()
        

    except Exception as e:
        print(e)


while True:
    oled.fill(1)
    oled.show()
