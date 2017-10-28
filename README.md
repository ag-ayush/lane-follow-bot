# lane-follow-bot
The concept here is to use OpenCv in python to detect white lines on grass and send signal to arduino to move accordingly.


I have been unable to build a robot to test this, therefore the output currently is in form of LEDs connected to PWMs on an Arduino Mega 2560.

## OpenCv
Takes an image and does the following:
1. Blur the image
2. HSV Color Filter
3. Dilations and Erosions
4. Canny Edge Detection
5. Hough Line Transform P

## Python-Arduino Bridge
This file takes a value between -1 and 1, where -1 is left and 1 is right. Currently it has a threshold between -0.1 and 0.1 for going straight (no LEDs on).

The file outputs to Arduino serial in form of a string: `<direction, float>` where direction is either RIGHT, LEFT, or STRAIGHT and float is the value to turn between 0 and 1.

_It should be noted that serial port and baud rate are hard coded, and will need to be changed for other boards and computers._

## Arduiono
The Arduino file looks for the message from PC, decodes it, and turns on LED based on the motor output (0 to 1, where 0 is off and 1 is full power).

## Hardward and Software
* OpenCv 3.3.0
* Python 2.7.12
* Arduino IDE 1.8.5
* Arduino Mega 2560
