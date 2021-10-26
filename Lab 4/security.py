# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import qwiic
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

def main():
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


    ToF = qwiic.QwiicVL53L1X()
    if (ToF.sensor_init() == None):         # Begin returns 0 on a good init
        print("Sensor online!")

    from adafruit_servokit import ServoKit
    from collections import deque
    kit = ServoKit(channels=16)
    servo = kit.servo[2]
    servo.set_pulse_width_range(500, 2500)

    # start it turned around towards outside world
    servo.angle = 180

    i = 1
    angles = deque([0.0])

    baseFeet = 0.0
    while True:
        try:
            ToF.start_ranging()             # Write configuration bytes to initiate measurement
            time.sleep(.005)
            distance = ToF.get_distance()   # Get the result of the measurement from the sensor
            time.sleep(.005)
            ToF.stop_ranging()

            distanceInches = distance / 25.4
            distanceFeet = distanceInches / 12.0

            if i % 50 == 0:
                servo.angle = 90
                baseFeet = angles.popleft()
                angles.append(distanceFeet)
                time.sleep(0.25)

            elif (i+25) % 50 == 0:
                servo.angle = 180
                baseFeet = angles.popleft()
                angles.append(distanceFeet)
                time.sleep(0.25)

            """
            distanceInches = distance / 25.4
            distanceFeet = distanceInches / 12.0
            """

            """
            if baseFeet == 0.0:
                baseFeet = distanceFeet
            """

            if abs(baseFeet - distanceFeet) > 0.3 * baseFeet:
                oled.fill(1)

            else:
                oled.fill(0)

            oled.show()
           
            """
            if i % 50 == 0:
                servo.angle = 115
                baseFeet = distanceFeet
                #print(f"left: {i}")

            elif (i+25) % 50 == 0:
                servo.angle = 180
                baseFeet = distanceFeet
                #print(f"right: {i}")
            """

            i += 1

        except Exception as e:
            print(e)
            servo.angle = 0

if __name__ == "__main__":
    main()
