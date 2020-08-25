import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)  # Read output from PIR motion sensor

while True:
    i = GPIO.input(6)
    if i == 0:  # When output from motion sensor is LOW
        print ("No motion detected", i)
        time.sleep(1)
    elif i == 1:  # When output from motion sensor is HIGH
        print ("motion detected")
        time.sleep(1)
