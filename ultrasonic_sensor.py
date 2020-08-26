from gpiozero import DistanceSensor
import time
import numpy as np

distances = []

ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=2)

while True:

    distance = ultrasonic.distance

    distances.append(distance)

    if len(distances) > 120:

        del distances[0]

        mean = np.mean(distances)
        std = np.std(distances)

        print(mean, std)

    time.sleep(1)
