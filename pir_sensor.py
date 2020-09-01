import RPi.GPIO as GPIO
import time
import datetime as dt

import db_handler
import my_logger

pir_pin_1 = 6
pir_pin_2 = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin_1, GPIO.IN)  # Read output from PIR motion sensor
GPIO.setup(pir_pin_2, GPIO.IN)  # Read output from PIR motion sensor

previous_pir_reading_1 = 0
previous_pir_reading_2 = 0

# create the table
db_handler.create_pir_table()

# create logger
logger = my_logger.init_logger("pir_sensor.log")

sql = " INSERT INTO pir (time_stamp, sensor_id, presence) VALUES(?, ?, ?) "

if __name__ == "__main__":

    while True:

        pir_signal_1 = GPIO.input(pir_pin_1)
        pir_signal_2 = GPIO.input(pir_pin_2)

        if pir_signal_1 != previous_pir_reading_1:

            logger.info(
                f"pir_sensor -- {dt.datetime.now().isoformat()} - id: 1, value: {pir_signal_1}"
            )

            previous_pir_reading_1 = pir_signal_1

            values = (int(time.time()), 1, pir_signal_1)

            conn = db_handler.connect_db()
            index = db_handler.write_db(conn, sql, values)
            conn.close()

        if pir_signal_2 != previous_pir_reading_2:

            logger.info(
                f"pir_sensor -- {dt.datetime.now().isoformat()} - id: 2, value: {pir_signal_2}"
            )

            previous_pir_reading_2 = pir_signal_2

            values = (int(time.time()), 2, pir_signal_2)

            conn = db_handler.connect_db()
            index = db_handler.write_db(conn, sql, values)
            conn.close()

        time.sleep(0.5)
