import RPi.GPIO as GPIO
import time
import db_handler
import datetime as dt

# Set warnings off (optional)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set Button and LED pins
button_pin = 2

previous_state = 0

# Setup Button and LED
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create table to store button presses data
db_handler.create_button_table()

# sql statement to add new entries to table
sql = """ INSERT INTO button 
        (time_stamp, status) 
        VALUES(?,?) """

while True:

    reading = GPIO.input(button_pin)

    # I am inverting 0 with 1 and 1 with 0 since for button pressed reading == 0
    reading = reading ^ 1

    if (reading != previous_state) and (previous_state == 0):

        # connect to db
        conn = db_handler.connect_db()

        # prepare values to be stored
        values = (
            int(time.time()),
            reading,
        )

        # write to db
        index = db_handler.write_db(conn, sql, values)

        print(
            f"button -- {dt.datetime.now().isoformat()} - index_db: "
            f"{index}, button state: {reading}"
        )

        # close connection
        conn.close()

    previous_state = reading
