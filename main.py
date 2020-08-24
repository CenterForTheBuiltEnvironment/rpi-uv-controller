"""
This file contains the control logic
"""

import RPi.GPIO as GPIO
from db_handler import connect_db, read_db

import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)     #Define pin 3 as an output pin

while True:
    GPIO.output(3,1)   #Outputs digital HIGH signal (5V) on pin 3

    GPIO.output(3,0)   #Outputs digital LOW signal (0V) on pin 3