
#Author: Tariq Islam

# My thought process for the algorithm to track object is:
# Detect the object & measure it's area.
# For moving close to the object, I used the area of the object(Larger it is, closer it is)
# For it being sideways, I set up a midpoint and everytime it went past 320(center of frame),
# my robot would pan towards it.

import cv2
import numpy as np
# import os
import sys
# import termios
# import fcntl
import RPi.GPIO as gpio
import time

# My webcam

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


# Screen size smaller will make it faster

def track():
    import sys
    init()
    # Create a Frame to be read
    _, frame = cap.read()

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color defined in ranges from low to high red
    lower_red = np.array([117, 40, 115], dtype=np.uint8)
    upper_red = np.array([180, 255, 255], dtype=np.uint8)

    # With mask we should only detect red object
    # Get red mask
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # Image mask is derived so we can measure the image moment
    # Moment is the weighted average taken from the mask.
    moments = cv2.moments(mask)
    # Area of object can be found with moments 'm00'
    area = moments['m00']
    # To cancel out unnecessary similar pigments
    if (area > 100000):
        # X and Y coordinates can be found from moments through:
        # M (m10) / M(m00)
        x = moments['m10'] / area
        y = moments['m01'] / area

        # We can see continuous update of x,y coordinates and area.
        print('x: ' + str(int(x)) + ' y: ' + str(int(y)) + ' area: ' + str(area))

        move_elee(round(x, -1), y, round(area, -5))
        time.sleep(0.15)

    # Display mask
    cv2.imshow('mask', mask)
    # Set up escape key with q.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        clean_up()
        sys.exit()
# From the image moments, if I want to move my robot, I can do the following:
# Take x,y and area for function

def move_elee(x, y, area):
    # If x is greater than 350, not 320 on purpose for lax
    # Or else it keeps moving all the time
    # More the difference, more time it takes to turn was my logic.
    # 3600, 1600000, 2600000 are just calibrated numbers.
    if x > 350:
        turn_right((x - 320) / 3600)
    elif x < 290:
        turn_left((320 - x) / 3600)
    elif ((290 <= x <= 350) and area < 1600000):
        forward(0.10)
    elif ((290 <= x <= 250) and area > 2600000):
        reverse(0.05)

# 4 DC motors, 2 L298N controllers.
def init():
    gpio.setmode(gpio.BOARD)
    # Front motors & controller
    gpio.setup(18, gpio.OUT)
    gpio.setup(16, gpio.OUT)
    gpio.setup(15, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    #ENA & ENB
    gpio.output(22, True)
    gpio.output(11, True)

    # Rear motors & controller
    gpio.setup(36, gpio.OUT)
    gpio.setup(29, gpio.OUT)
    gpio.setup(31, gpio.OUT)
    gpio.setup(33, gpio.OUT)
    gpio.setup(32, gpio.OUT)
    gpio.setup(37, gpio.OUT)
    # ENA & ENB
    gpio.output(32, True)
    gpio.output(37, True)


def forward(tf):

    gpio.output(18, True)
    gpio.output(16, False)
    gpio.output(15, True)
    gpio.output(13, False)

    gpio.output(36, True)
    gpio.output(29, False)
    gpio.output(31, True)
    gpio.output(33, False)

    time.sleep(tf)
    clean_up()


def reverse(tf):

    gpio.output(18, False)
    gpio.output(16, True)
    gpio.output(15, False)
    gpio.output(13, True)

    gpio.output(36, False)
    gpio.output(29, True)
    gpio.output(31, False)
    gpio.output(33, True)
    time.sleep(tf)
    clean_up()

def turn_right(tf):

    gpio.output(18, False)
    gpio.output(16, True)
    gpio.output(15, True)
    gpio.output(13, False)

    gpio.output(36, True)
    gpio.output(29, False)
    gpio.output(31, False)
    gpio.output(33, True)
    time.sleep(tf)
    clean_up()


def turn_left(tf):

    gpio.output(18, True)
    gpio.output(16, False)
    gpio.output(15, False)
    gpio.output(13, True)

    gpio.output(36, False)
    gpio.output(29, True)
    gpio.output(31, True)
    gpio.output(33, False)
    time.sleep(tf)
    clean_up()


def clean_up():
    gpio.output(18, False)
    gpio.output(16, False)
    gpio.output(15, False)
    gpio.output(13, False)
    gpio.output(22, False)
    gpio.output(11, False)

    gpio.output(36, False)
    gpio.output(29, False)
    gpio.output(31, False)
    gpio.output(33, False)
    gpio.output(32, False)
    gpio.output(37, False)

    gpio.cleanup()

# Run the program, and ensure to destroy windows after use.
def main():
    while True:
        track()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()