from gpiozero import DistanceSensor
import time

ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=2)

while True:
    print(ultrasonic.distance)

    time.sleep(1)