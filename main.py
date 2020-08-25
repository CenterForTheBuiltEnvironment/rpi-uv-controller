"""
This file contains the control logic
"""

import RPi.GPIO as GPIO
import time
import numpy as np
import datetime as dt
import dateutil.parser

import beacons_ids
from db_handler import connect_db, read_db

threshold_beacons = 60  # in seconds
threshold_pir = 60  # in seconds


def pir_control():

    # query the last entries
    conn = connect_db()

    # query only last entry by beacon id
    query_last_entry_by_id = (
        "SELECT * FROM rpi ORDER BY time_stamp DESC LIMIT 10"
    )
    rows = read_db(conn, query_last_entry_by_id)

    conn.close()



def beacons_control():

    # query the last entries
    conn = connect_db()

    # query only last entry by beacon id
    query_last_entry_by_id = (
        "SELECT device_id, rssi, MAX(time_stamp) FROM beacons GROUP BY device_id;"
    )
    rows = read_db(conn, query_last_entry_by_id)

    conn.close()

    zeros_array = np.zeros(len(rows))
    zeros_array[:] = False

    top_light_beacon_array = zeros_array.copy()
    desk_light_beacon_array = zeros_array.copy()

    for ix, row in enumerate(rows):

        # check that the index is among those to track
        if row[0] in beacons_ids.beacons_to_track.keys():

            # check against time threshold
            if ((
                dt.datetime.now() - dateutil.parser.parse(row[2])
            ).total_seconds() < threshold_beacons):

                # if not enough time has elapsed check signal strength
                if row[1] < beacons_ids.beacons_to_track[row[0]]:

                    top_light_beacon_array[ix] = True

            # if the threshold time has elapsed
            else:

                top_light_beacon_array[ix] = True
                desk_light_beacon_array[ix] = True

        # since I am not controlling for this beacon
        else:

            top_light_beacon_array[ix] = True
            desk_light_beacon_array[ix] = True

    if False in top_light_beacon_array:
        top_light_control = False
    else:
        top_light_control = True

    if False in desk_light_beacon_array:
        desk_light_control = False
    else:
        desk_light_control = True

    return {"top_light": top_light_control, "desk_light": desk_light_control}


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# https://pinout.xyz

GPIO.setup(26, GPIO.OUT)  # green
GPIO.setup(19, GPIO.OUT)  # yellow
GPIO.setup(13, GPIO.OUT)  # red

while True:

    ctr_beacon = beacons_control()

    print("beacon control", ctr_beacon)

    if ctr_beacon['desk_light']:
        GPIO.output(26, 1)
        GPIO.output(19, 0)
        GPIO.output(13, 0)
    elif ctr_beacon['top_light']:
        GPIO.output(26, 0)
        GPIO.output(19, 1)
        GPIO.output(13, 0)
    else:
        GPIO.output(26, 0)
        GPIO.output(19, 0)
        GPIO.output(13, 1)

    time.sleep(1)
