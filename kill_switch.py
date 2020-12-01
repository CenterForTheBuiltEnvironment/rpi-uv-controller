import RPi.GPIO as GPIO
import time
import db_handler
import datetime as dt
import VARIABLES

# Set warnings off (optional)
import my_logger

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set Button and LED pins
button_pin = VARIABLES.pin_manual_switch

previous_state = 0

# Setup Button and LED
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create table to store button presses data
db_handler.create_button_table()

# sql statement to add new entries to table
sql = """ INSERT INTO button (time_stamp, status) VALUES(?,?) """

# create logger
logger = my_logger.init_logger("kill_switch.log")

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

        logger.info(
            f"button -- {dt.datetime.now().isoformat()} - button state: {reading}"
        )

        # close connection
        conn.close()

    previous_state = reading
