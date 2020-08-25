import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)  # Read output from PIR motion sensor

while True:
    i = GPIO.input(6)

    motion_array = []
    for interval in range(0, 120):

        if i == 0:  # When output from motion sensor is LOW
            time.sleep(0.5)
            motion_array.append(False)
        elif i == 1:  # When output from motion sensor is HIGH
            time.sleep(0.5)
            motion_array.append(True)

    if True in motion_array:
        print("motion was detected")
    else:
        print("no motion detected")
