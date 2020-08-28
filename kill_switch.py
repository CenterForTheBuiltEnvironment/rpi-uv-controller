import RPi.GPIO as GPIO
import time

#Set warnings off (optional)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Set Button and LED pins
Button = 2

#Setup Button and LED
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
    button_state = GPIO.input(Button)
    print(button_state)
    time.sleep(0.5)