"""
This file contains the control logic
"""

import RPi.GPIO as GPIO
from db_handler import connect_db, read_db

import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(26,GPIO.OUT)     #Define pin 3 as an output pin
GPIO.setup(19,GPIO.OUT)     #Define pin 3 as an output pin
GPIO.setup(13,GPIO.OUT)     #Define pin 3 as an output pin

while True:
    GPIO.output(26,1)   #Outputs digital HIGH signal (5V) on pin 3
    GPIO.output(19,0)   #Outputs digital LOW signal (0V) on pin 3
    GPIO.output(13,0)   #Outputs digital LOW signal (0V) on pin 3

    time.sleep(1)

    GPIO.output(26,0)   #Outputs digital HIGH signal (5V) on pin 3
    GPIO.output(19,1)   #Outputs digital LOW signal (0V) on pin 3
    GPIO.output(13,0)   #Outputs digital LOW signal (0V) on pin 3

    time.sleep(1)

    GPIO.output(26,0)   #Outputs digital HIGH signal (5V) on pin 3
    GPIO.output(19,0)   #Outputs digital LOW signal (0V) on pin 3
    GPIO.output(13,1)   #Outputs digital LOW signal (0V) on pin 3

    time.sleep(1)

