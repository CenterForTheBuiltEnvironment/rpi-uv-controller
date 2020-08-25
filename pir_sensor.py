import RPi.GPIO as GPIO
import time
import datetime as dt

import db_handler

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)  # Read output from PIR motion sensor

motion_array = []

# create the table
db_handler.create_pir_table()

sql = """ INSERT INTO pir(time_stamp, presence)
          VALUES(?,?) """

while True:

    i = GPIO.input(6)

    if i == 0:  # When output from motion sensor is LOW
        time.sleep(0.5)
        motion_array.append(False)
    elif i == 1:  # When output from motion sensor is HIGH
        motion_array.append(True)
        time.sleep(5)

        values = (int(time.time()), 1)

        conn = db_handler.connect_db()
        index = db_handler.write_db(conn, sql, values)
        conn.close()

        print(f"pir_sensor -- {dt.datetime.now().isoformat()} - index_db: {index}, value: {values[1]}")

    if len(motion_array) > 60:

        conn = db_handler.connect_db()

        if True in motion_array:
            values = (int(time.time()), 1)
        else:
            values = (int(time.time()), 0)

        index = db_handler.write_db(conn, sql, values)
        conn.close()

        print(f"pir_sensor -- {dt.datetime.now().isoformat()} - index_db: {index}, value: {values[1]}")

        motion_array = []
