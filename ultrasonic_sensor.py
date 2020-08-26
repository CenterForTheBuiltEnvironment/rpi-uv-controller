from gpiozero import DistanceSensor
import time
import datetime as dt
import numpy as np

import db_handler

# variables
time_wrote_to_db = time.time()
logging_time = 10
sampling_time = 0.5

# # create calibration table
# db_handler.create_ultrasonic_calibration_table()
#
# sql = """ INSERT INTO calibration_ultrasonic
#         (time_stamp, distance, mean, std)
#         VALUES(?,?,?,?) """
#
# conn = db_handler.connect_db()

# create table to store ultrasonic sensor data
db_handler.create_ultrasonic_table()

# sql statement to add new entries to table
sql = """ INSERT INTO ultrasonic 
        (time_stamp, distance, mean, std) 
        VALUES(?,?,?,?) """

# store distances measured
distances = []

# initialize the sensor
ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=2)

while True:

    # measure disatnce
    distance = ultrasonic.distance

    # append to the array of previously measured distances
    distances.append(distance)

    # wait until I have three minutes of data
    if len(distances) > 60 / sampling_time * 3:

        # delete first entry
        del distances[0]

        # calculate mean and std
        mean = np.mean(distances)
        std = np.std(distances)

        # # save data to calibration table
        # print(round(distance, 3), round(mean, 3), round(std, 3))
        #
        # values = (int(time.time()), round(distance, 3),
        #           round(mean, 3), round(std, 3))
        #
        # index = db_handler.write_db(conn, sql, values)

        # if enough time has elapsed since last time data were written to db
        if time.time() - time_wrote_to_db > logging_time:

            # update timestamp
            time_wrote_to_db = time.time()

            # connect to db
            conn = db_handler.connect_db()

            # prepare values to be stored
            values = (int(time_wrote_to_db), round(distance, 3),
                      round(mean, 3), round(std, 3))

            # write to db
            index = db_handler.write_db(conn, sql, values)

            print(
                f"ultrasonic -- {dt.datetime.now().isoformat()} - index_db: "
                f"{index}, dist: {round(distance, 3)}, std: {round(std, 3)}"
                )

            # close connection
            conn.close()

    # pause script
    time.sleep(sampling_time)
