import RPi.GPIO as GPIO
import time
import datetime as dt

import db_handler
import light_controller

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)  # Read output from PIR motion sensor

motion_array = []

# create the table
db_handler.create_pir_table()

sql = " INSERT INTO pir(time_stamp, presence) VALUES(?,?) "

if __name__ == "__main__":

    while True:

        pir_signal = GPIO.input(6)

        if pir_signal == 0:  # When output from motion sensor is LOW
            motion_array.append(False)
        elif pir_signal == 1:  # When output from motion sensor is HIGH

            # turn off all lights immediately
            light_controller.all_lights_off()

            motion_array.append(True)

            values = (int(time.time()), 1)

            conn = db_handler.connect_db()
            index = db_handler.write_db(conn, sql, values)
            conn.close()

            print(
                f"pir_sensor -- {dt.datetime.now().isoformat()} - index_db: {index}, value: {values[1]}"
            )

        if len(motion_array) > 60:

            conn = db_handler.connect_db()

            if True in motion_array:
                values = (int(time.time()), 1)
            else:
                values = (int(time.time()), 0)

            index = db_handler.write_db(conn, sql, values)
            conn.close()

            print(
                f"pir_sensor -- {dt.datetime.now().isoformat()} - index_db: {index}, value: {values[1]}"
            )

            motion_array = []

        time.sleep(0.5)
