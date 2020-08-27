"""
This file contains the control logic
"""

import RPi.GPIO as GPIO
import time
import numpy as np

import beacons_ids
from db_handler import connect_db, read_db

# delay between last signal and lights can be turned on
delay_beacons = 30  # in seconds
delay_pir = 30  # in seconds

# define the GPIOs pin that control the light
top_light_pin = 19
desk_light_pin = 26
all_off_light_pin = 13

# threshold for ultrasonic sensor to detect movement
threshold_ultrasonic_std = 0.02 # calculated using the calibration data, this is the std

# set up board configuration RPI
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# https://pinout.xyz

# set pin role
GPIO.setup(desk_light_pin, GPIO.OUT)  # green
GPIO.setup(top_light_pin, GPIO.OUT)  # yellow
GPIO.setup(all_off_light_pin, GPIO.OUT)  # red


def ultrasonic_control():

    try:
        # query the last entries
        conn = connect_db()

        # query only last entry by beacon id
        query = f"SELECT std FROM ultrasonic ORDER BY time_stamp DESC LIMIT 1"
        rows = read_db(conn, query)

        conn.close()

        std = rows[0][0]

        # print("standard deviation", std)

        if std > threshold_ultrasonic_std:
            return False
        else:
            return True
    except:
        return False


def pir_control():

    # query the last entries
    conn = connect_db()

    now = int(time.time()) - delay_pir

    # query only last entry by beacon id
    query_last_entry_by_id = f"SELECT * FROM pir WHERE time_stamp > {now}"
    rows = read_db(conn, query_last_entry_by_id)

    conn.close()

    occupancy_array = [row[2] for row in rows]

    if 1 in occupancy_array:
        return False
    else:
        return True


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
            if time.time() - row[2] < delay_beacons:

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


def all_lights_off():

    desk_light_off()
    top_light_off()
    GPIO.output(all_off_light_pin, 1)


def desk_light_on():

    GPIO.output(desk_light_pin, 1)


def desk_light_off():

    GPIO.output(desk_light_pin, 0)


def top_light_on():

    GPIO.output(desk_light_pin, 1)


def top_light_off():

    GPIO.output(desk_light_pin, 0)


if __name__ == '__main__':

    while True:

        # get the control signal from each sensor
        ctr_beacon = beacons_control()
        ctr_pir = pir_control()
        ctr_ultrasonic = ultrasonic_control()

        # a positive control (True) means that light can be turned on
        if ctr_ultrasonic:

            if ctr_pir:

                # turn on all lights
                if ctr_beacon["desk_light"]:
                    desk_light_on()
                else:
                    print("desk light turned off by beacon")
                    desk_light_off()

                # turn of the desk light but on the top light if beacon farther then threshold
                if ctr_beacon["top_light"]:
                    top_light_on()

                else:
                    print("top light turned off by beacon")
                    top_light_off()

            # turn of the lights if pir detected occupancy
            else:
                print("turned off by pir")
                all_lights_off()

        # turn of the lights if ultrasonic detected motion
        else:
            print("turned off by ultrasonic")
            all_lights_off()

        # todo write control signal to database

        time.sleep(5)
