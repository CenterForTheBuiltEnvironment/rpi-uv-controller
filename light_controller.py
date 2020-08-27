"""
This file contains the control logic
"""

import RPi.GPIO as GPIO
import time
import numpy as np
import datetime as dt

import beacons_ids
import db_handler

# delay between last signal and lights can be turned on
delay_beacons = 30  # in seconds
delay_pir = 30  # in seconds

# define the GPIOs pin that control the light
top_light_pin = 19
desk_light_pin = 26
all_off_light_pin = 13

# threshold for ultrasonic sensor to detect movement
threshold_ultrasonic_std = (
    0.02  # calculated using the calibration data, this is the std
)

# set up board configuration RPI
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# https://pinout.xyz

# set pin role
GPIO.setup(desk_light_pin, GPIO.OUT)  # green
GPIO.setup(top_light_pin, GPIO.OUT)  # yellow
GPIO.setup(all_off_light_pin, GPIO.OUT)  # red

# stores in memory if occupancy was detected
occupancy_detected = True

lights_dict = {
    "top": {
        "status": 0,
        "time_on": 0,
        "max_time_on": 60,
        "pin": 19  # todo replace top_light_pin with this
        },
    "desk": {
        "status": 0,
        "time_on": 0,
        "max_time_on": 60,
        "pin": 26  # todo replace desk_light_pin with this
        },
    }


def ultrasonic_control():

    try:
        # query the last entries
        conn = db_handler.connect_db()

        # query only last entry by beacon id
        query = f"SELECT std FROM ultrasonic ORDER BY time_stamp DESC LIMIT 1"
        rows = db_handler.read_db(conn, query)

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
    conn = db_handler.connect_db()

    now = int(time.time()) - delay_pir

    # query only last entry by beacon id
    query_last_entry_by_id = f"SELECT * FROM pir WHERE time_stamp > {now}"
    rows = db_handler.read_db(conn, query_last_entry_by_id)

    conn.close()

    occupancy_array = [row[2] for row in rows]

    if 1 in occupancy_array:
        return False
    else:
        return True


def beacons_control():

    # query the last entries
    conn = db_handler.connect_db()

    # query only last entry by beacon id
    query_last_entry_by_id = (
        "SELECT device_id, rssi, MAX(time_stamp) FROM beacons GROUP BY device_id;"
    )
    rows = db_handler.read_db(conn, query_last_entry_by_id)

    conn.close()

    zeros_array = np.zeros(len(rows))
    zeros_array[:] = False

    top_light_beacon_array = zeros_array.copy()
    desk_light_beacon_array = zeros_array.copy()

    for index, row in enumerate(rows):

        # check that the index is among those to track
        if row[0] in beacons_ids.beacons_to_track.keys():

            # check against time threshold
            if time.time() - row[2] < delay_beacons:

                # if not enough time has elapsed check signal strength
                if row[1] < beacons_ids.beacons_to_track[row[0]]:

                    top_light_beacon_array[index] = True

            # if the threshold time has elapsed
            else:

                top_light_beacon_array[index] = True
                desk_light_beacon_array[index] = True

        # since I am not controlling for this beacon
        else:

            top_light_beacon_array[index] = True
            desk_light_beacon_array[index] = True

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

    desk_light(signal=0)
    top_light(signal=0)
    GPIO.output(all_off_light_pin, 1)


# todo combine next two functions into one and get info from lights dict
def desk_light(signal):

    GPIO.output(desk_light_pin, signal)
    GPIO.output(all_off_light_pin, 0)


def top_light(signal):

    GPIO.output(top_light_pin, signal)
    GPIO.output(all_off_light_pin, 0)


def light_switch(signal=0, light_key='top'):

    GPIO.output(lights_dict[light_key]["pin"], signal)

    if signal == 1:

        GPIO.output(all_off_light_pin, 0)


if __name__ == "__main__":

    db_handler.create_controller_table()

    all_lights_off()

    while True:

        # get the control signal from each sensor
        ctr_beacon = beacons_control()
        ctr_pir = pir_control()
        ctr_ultrasonic = ultrasonic_control()

        # a positive control (True) means that light can be turned on
        if ctr_ultrasonic:

            if ctr_pir:

                sensor = "beacon"

                if occupancy_detected:

                    # control desk light
                    desk_light(signal=ctr_beacon["desk_light"])

                    # control top light
                    top_light(signal=ctr_beacon["top_light"])

                    signals = [int(ctr_beacon["desk_light"]), int(ctr_beacon["top_light"])]  # todo add this info to lights_dict

                if 1 not in signals:

                    all_lights_off()

            # turn of the lights if pir detected occupancy
            else:

                sensor = "pir"
                all_lights_off()

                signals = [0, 0]

        # turn of the lights if ultrasonic detected motion
        else:

            sensor = "ultrasonic"

            all_lights_off()

            signals = [0, 0]

        # control for how long UV lights were turned on
        for ix, light_type in enumerate(lights_dict.keys()):

            light_info = lights_dict[light_type]
            now = time.time()

            if (signals[ix] == 1) and (light_info['status'] == 0):

                print(f"{dt.datetime.now().isoformat()} - "
                      f"{light_type} turned on")

                light_info['status'] = 1

                light_info['time_on'] = now

            if (now - light_info['time_on']) > light_info['max_time_on']:

                light_switch(signal = 0, light_key=light_type)

                print(f"{dt.datetime.now().isoformat()} - "
                      f"{light_type} turned off")

                light_info['status'] = 0

                if light_type == 'top':

                    occupancy_detected = False

        if 0 in signals:

            occupancy_detected = True


        # write control signal to database
        connection = db_handler.connect_db()

        for ix, light_type in enumerate(["desk", "top"]):  # todo replace this array with keys lights dict

            values = (int(time.time()), sensor, light_type, signals[ix])
            sql = " INSERT INTO control_signals(time_stamp, sensor, light_type, signal) " \
                  "VALUES(?,?,?,?) "
            row_index = db_handler.write_db(connection, sql, values)

            # print(values)

        connection.close()

        time.sleep(5)

        # todo turn the lights on at midnight
