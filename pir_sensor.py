import RPi.GPIO as GPIO
import time
import datetime as dt

import db_handler
import light_controller

pir_pin = 6
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)  # Read output from PIR motion sensor

previous_pir_reading = 0

# create the table
db_handler.create_pir_table()
time.sleep(2)

sql = " INSERT INTO pir(time_stamp, presence) VALUES(?,?) "

if __name__ == "__main__":

    while True:

        pir_signal = GPIO.input(pir_pin)

        if pir_signal != previous_pir_reading:

            previous_pir_reading = pir_signal

            values = (int(time.time()), pir_signal)

            conn = db_handler.connect_db()
            index = db_handler.write_db(conn, sql, values)
            conn.close()

            print(
                f"pir_sensor -- {dt.datetime.now().isoformat()} - index_db: {index}, value: {values[1]}"
            )

        time.sleep(0.5)
