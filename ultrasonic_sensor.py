from gpiozero import DistanceSensor
import time
import datetime as dt
import numpy as np

import db_handler

# variables
import my_logger

time_wrote_to_db = time.time()
logging_time = 10
sampling_time = 0.5
previous_std = 9999

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

# create logger
logger = my_logger.init_logger("ultrasonic_sensor.log")

# sql statement to add new entries to table
sql = """ INSERT INTO ultrasonic 
        (time_stamp, distance, mean, std) 
        VALUES(?,?,?,?) """

# store distances measured
distances = []

# initialize the sensor
ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=3.5)

while True:

    # measure distance
    distance = round(ultrasonic.distance, 4)

    # append to the array of previously measured distances
    distances.append(distance)

    # wait until I have three minutes of data
    if len(distances) > 60 / sampling_time * 3:

        # delete first entry
        del distances[0]

    # calculate mean and std
    mean = round(np.mean(distances), 4)
    std = round(np.std(distances), 4)

    # # save data to calibration table
    # print(round(distance, 3), round(mean, 3), round(std, 3))
    #
    # values = (int(time.time()), round(distance, 3),
    #           round(mean, 3), round(std, 3))
    #
    # index = db_handler.write_db(conn, sql, values)

    # if enough time has elapsed since last time data were written to db
    if (time.time() - time_wrote_to_db > logging_time) and (previous_std != std):

        # update value
        previous_std = std

        # update timestamp
        time_wrote_to_db = time.time()

        # connect to db
        conn = db_handler.connect_db()

        # prepare values to be stored
        values = (
            int(time_wrote_to_db),
            distance,
            mean,
            std,
        )

        # write to db
        index = db_handler.write_db(conn, sql, values)

        # close connection
        conn.close()

        logger.info(
            f"ultrasonic -- {dt.datetime.now().isoformat()} -  dist: {distance}, std: {std}"
        )

    # pause script
    time.sleep(sampling_time)
