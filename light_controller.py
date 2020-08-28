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

# threshold for ultrasonic sensor to detect movement
threshold_ultrasonic_std = (
    0.02  # calculated using the calibration data, this is the std
)

# previous day number, needed to turn on lights at midnight
previous_day = 9999

lights_dict = {
    "top": {
        "status": 0,
        "time_on": 0,
        "max_time_on": 60,
        "pin": 19,
        "ctr_signal": 0,
        "occupancy_detected": True
        },
    "desk": {
        "status": 0,
        "time_on": 0,
        "max_time_on": 60,
        "pin": 26,
        "ctr_signal": 0,
        "occupancy_detected": True
        },
    }

# set up board configuration RPI
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# https://pinout.xyz

# set pin role
GPIO.setup(lights_dict['desk']["pin"], GPIO.OUT)  # green
GPIO.setup(lights_dict['top']["pin"], GPIO.OUT)  # yellow


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

    # query only last entry by beacon id
    query_last_entry_by_id = f"SELECT presence, time_stamp FROM pir ORDER BY time_stamp DESC LIMIT 1"
    rows = db_handler.read_db(conn, query_last_entry_by_id)

    conn.close()

    presence = rows[0][0]

    if (presence == 1) or (time.time() - rows[0][1] < delay_pir):
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

    return {"top": top_light_control, "desk": desk_light_control}


def light_switch(signal=0, _light_key='top'):

    GPIO.output(lights_dict[_light_key]["pin"], signal)


if __name__ == "__main__":

    db_handler.create_controller_table()

    while True:

        # get the control signal from each sensor
        ctr_beacon = beacons_control()
        ctr_pir = pir_control()
        ctr_ultrasonic = ultrasonic_control()

        # a positive control (True) means that light can be turned on
        if ctr_ultrasonic:

            if ctr_pir:

                sensor = "beacon"

                # control desk light
                lights_dict["desk"]['ctr_signal'] = int(ctr_beacon["desk"])

                # control top light
                lights_dict["top"]['ctr_signal'] = int(ctr_beacon["top"])

            # turn of the lights if pir detected occupancy
            else:

                sensor = "pir"

                for light_key in lights_dict.keys():

                    lights_dict[light_key]['ctr_signal'] = 0

        # turn of the lights if ultrasonic detected motion
        else:

            sensor = "ultrasonic"

            for light_key in lights_dict.keys():

                lights_dict[light_key]['ctr_signal'] = 0


        # turn off lights if occupancy was detected
        for light_key in lights_dict.keys():

            if lights_dict[light_type]['ctr_signal'] == 0:

                light_switch(signal= 0, _light_key=light_key)

                lights_dict[light_type]['status'] = 0

                lights_dict[light_type]['occupancy_detected'] = True


        # finally turn on lights if needed
        for light_type in lights_dict.keys():

            now = time.time()

            # function that decides whether or not lights needs to be turned on
            if lights_dict[light_type]['occupancy_detected']:

                if (lights_dict[light_type]['ctr_signal'] == 1) and (lights_dict[light_type]['status'] == 0):

                    lights_dict[light_type]['status'] = 1
                    lights_dict[light_type]['time_on'] = now

                    light_switch(signal=1, _light_key=light_type)

                    print(f"{dt.datetime.now().isoformat()} - "
                          f"{light_type} turned on")

                elif ((now - lights_dict[light_type]['time_on']) > lights_dict[light_type]['max_time_on']) and (lights_dict[light_type]['status'] == 1):

                    lights_dict[light_type]['status'] = 0
                    light_switch(signal = 0, _light_key=light_type)

                    print(f"{dt.datetime.now().isoformat()} - "
                          f"{light_type} turned off since was on for too long")

                    lights_dict[light_type]['occupancy_detected'] = False

        # reset everything at midnight
        if dt.datetime.now().hour == 0 and dt.datetime.now().day != previous_day:

            previous_day = dt.datetime.now().day

            for light_type in lights_dict.keys():

                lights_dict[light_type]['occupancy_detected'] = True


        # write control signal to database
        connection = db_handler.connect_db()

        for light_type in lights_dict.keys():

            values = (int(time.time()), sensor, light_type, lights_dict[light_type]['status'])
            sql = " INSERT INTO control_signals(time_stamp, sensor, light_type, signal) " \
                  "VALUES(?,?,?,?) "
            row_index = db_handler.write_db(connection, sql, values)

        connection.close()

        time.sleep(1)
