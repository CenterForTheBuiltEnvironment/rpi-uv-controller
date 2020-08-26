from gpiozero import DistanceSensor
import time
import numpy as np

import db_handler

db_handler.create_ultrasonic_calibration_table()

sql = """ INSERT INTO calibration_ultrasonic 
        (time_stamp, distance, mean, std) 
        VALUES(?,?,?,?) """

conn = db_handler.connect_db()

distances = []

ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=2)

while True:

    distance = ultrasonic.distance

    distances.append(distance)

    if len(distances) > 360:

        del distances[0]

        mean = np.mean(distances)
        std = np.std(distances)

        print(round(distance, 3), round(mean, 3), round(std, 3))

        values = (int(time.time()), round(distance, 3),
                  round(mean, 3), round(std, 3))

        index = db_handler.write_db(conn, sql, values)

    time.sleep(0.5)
