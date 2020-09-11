"""
This file contains the control logic
"""

import RPi.GPIO as GPIO
import time
import numpy as np
import datetime as dt
from sqlite3 import Error

import VARIABLES
import db_handler
import my_logger

# create logger
logger = my_logger.init_logger("light_controller.log")

# previous day number, needed to turn on lights at midnight
previous_day = 9999

lights_dict = {
    "top": {
        "current_state": 0,
        "previous_state": 0,
        "time_on": 0,
        "max_time_on": VARIABLES.max_time_on_lights_top,
        "pin": 19,
        "ctr_signal": 0,
        "occupancy_detected": True,
    },
    "desk": {
        "current_state": 0,
        "previous_state": 0,
        "time_on": 0,
        "max_time_on": VARIABLES.max_time_on_lights_desk,
        "pin": 26,
        "ctr_signal": 0,
        "occupancy_detected": True,
    },
}

room_light = {
    "current_state": 0,
    "time_on": 0,
    "max_time_on": VARIABLES.max_time_on_lights_top,
    "hours_on": VARIABLES.hours_on,
    "days_on": VARIABLES.days_on,
    "pin": 22,
    "completed_hourly_cycle": 0,  # hour number when cycle completed
}

all_off_light_pin = 13

# set up board configuration RPI
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# https://pinout.xyz

# set pin role
GPIO.setup(lights_dict["desk"]["pin"], GPIO.OUT)  # green
GPIO.setup(lights_dict["top"]["pin"], GPIO.OUT)  # yellow
GPIO.setup(room_light["pin"], GPIO.OUT)  # yellow
GPIO.setup(all_off_light_pin, GPIO.OUT)  # red

# wait for few seconds before the script starts so sensors can start collecting data
time.sleep(5)


def ultrasonic_control():

    try:
        # query the last entries
        conn = db_handler.connect_db()

        # query only last entry by beacon id
        query = f"SELECT std FROM ultrasonic ORDER BY time_stamp DESC LIMIT 1"
        rows = db_handler.read_db(conn, query)

        conn.close()

        std = rows[0][0]

        if std > VARIABLES.threshold_ultrasonic_std:
            return False
        else:
            return True

    except IndexError:
        return True

    except Error as e:
        print(e)
        return True


def kill_switch_control():

    try:
        # query the last entries
        conn = db_handler.connect_db()

        # query only last entry by beacon id
        query = f"SELECT time_stamp FROM button ORDER BY time_stamp DESC LIMIT 1"
        rows = db_handler.read_db(conn, query)

        conn.close()

        time_button_pressed = rows[0][0]

        if time.time() - time_button_pressed < VARIABLES.delay_kill_switch:
            return False
        else:
            return True

    except IndexError:
        return True

    except Error as e:
        print(e)
        return True


def pir_control():

    try:
        # query the last entries
        conn = db_handler.connect_db()

        # query only last entry by beacon id
        query_last_entry_by_id = (
            f"SELECT presence, MAX(time_stamp), sensor_id FROM pir GROUP BY sensor_id;"
        )
        rows = db_handler.read_db(conn, query_last_entry_by_id)

        conn.close()

        presence = []
        time_elapsed = []

        for row in rows:
            presence.append(row[0])
            time_elapsed.append(time.time() - row[1])

        if (1 in presence) or (min(time_elapsed) < VARIABLES.delay_pir):
            return False
        else:
            return True

    except (IndexError, ValueError):
        return True

    except Error as e:
        print(e)
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
        if row[0] in VARIABLES.beacons_to_track.keys():

            # check against time threshold
            if time.time() - row[2] < VARIABLES.delay_beacons:

                # if not enough time has elapsed check signal strength
                if row[1] < VARIABLES.beacons_to_track[row[0]]:

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


def send_ctr_relay(signal=0, light_key="top"):

    GPIO.output(lights_dict[light_key]["pin"], signal)


def control_room_light():
    _now = dt.datetime.now()

    if (
        (_now.weekday() in room_light["days_on"])
        and (_now.hour in room_light["hours_on"])
        and (_now.hour != room_light["completed_hourly_cycle"])
    ):

        if room_light["current_state"] == 0:  # light was off

            GPIO.output(room_light["pin"], 1)  # turn on light

            room_light["time_on"] = time.time()
            room_light["current_state"] = 1

            _values = (
                int(time.time()),
                "timer",
                "room",
                1,
            )

            write_control_to_db(_values)

        elif time.time() - room_light["time_on"] > room_light["max_time_on"]:

            GPIO.output(room_light["pin"], 0)  # turn on light

            room_light["current_state"] = 0
            room_light["completed_hourly_cycle"] = _now.hour

            _values = (
                int(time.time()),
                "timer",
                "room",
                0,
            )

            write_control_to_db(_values)


def write_control_to_db(_values):
    # write control signal to database
    connection = db_handler.connect_db(_values)

    sql = (
        " INSERT INTO control_signals(time_stamp, sensor, light_type, "
        "signal) "
        "VALUES(?,?,?,?) "
    )

    db_handler.write_db(connection, sql, _values)

    connection.close()

    logger.info(
        f"light control -- {dt.datetime.now().isoformat()} - light: "
        f"{_values[2]}, light_state: {_values[3]}"
    )


if __name__ == "__main__":

    db_handler.create_controller_table()

    control_room_light()

    while True:

        # get the control signal from each sensor
        ctr_beacon = beacons_control()
        ctr_pir = pir_control()
        ctr_ultrasonic = ultrasonic_control()
        ctr_kill_switch = kill_switch_control()

        # a positive control (True) means that light can be turned on
        if ctr_kill_switch:

            if ctr_ultrasonic:

                if ctr_pir:

                    # this variable specifies which sensor controlled the light
                    sensor = "beacon"

                    # control desk light
                    lights_dict["desk"]["ctr_signal"] = int(ctr_beacon["desk"])

                    # control top light
                    lights_dict["top"]["ctr_signal"] = int(ctr_beacon["top"])

                # turn off the lights if pir detected occupancy
                else:

                    sensor = "pir"

                    for light_type in lights_dict.keys():

                        lights_dict[light_type]["ctr_signal"] = 0

            # turn off the lights if ultrasonic detected motion
            else:

                sensor = "ultrasonic"

                for light_type in lights_dict.keys():

                    lights_dict[light_type]["ctr_signal"] = 0

        # turn off the lights if kill switch was pressed
        else:

            sensor = "switch"

            for light_type in lights_dict.keys():

                lights_dict[light_type]["ctr_signal"] = 0

        # turn off lights if occupancy was detected
        for light_type in lights_dict.keys():

            if lights_dict[light_type]["ctr_signal"] == 0:

                send_ctr_relay(signal=0, light_key=light_type)

                lights_dict[light_type]["current_state"] = 0

                lights_dict[light_type]["occupancy_detected"] = True

        # finally turn on lights if needed
        for light_type in lights_dict.keys():

            now = time.time()

            # function that decides whether or not lights needs to be turned on
            if lights_dict[light_type]["occupancy_detected"]:

                if (lights_dict[light_type]["ctr_signal"] == 1) and (
                    lights_dict[light_type]["current_state"] == 0
                ):

                    lights_dict[light_type]["current_state"] = 1
                    lights_dict[light_type]["time_on"] = now

                    send_ctr_relay(signal=1, light_key=light_type)

                    # print(
                    #     f"{dt.datetime.now().isoformat()} - " f"{light_type} turned on"
                    # )

                elif (
                    (now - lights_dict[light_type]["time_on"])
                    > lights_dict[light_type]["max_time_on"]
                ) and (lights_dict[light_type]["current_state"] == 1):

                    lights_dict[light_type]["current_state"] = 0
                    send_ctr_relay(signal=0, light_key=light_type)

                    logger.info(
                        f"{dt.datetime.now().isoformat()} - "
                        f"{light_type} turned off since was on for too long"
                    )

                    lights_dict[light_type]["occupancy_detected"] = False

        # reset everything at midnight
        if dt.datetime.now().hour == 0 and dt.datetime.now().day != previous_day:

            previous_day = dt.datetime.now().day

            for light_type in lights_dict.keys():

                lights_dict[light_type]["occupancy_detected"] = True

        # turn on red led if all lights are off
        if 1 not in [lights_dict[x]["current_state"] for x in lights_dict.keys()]:

            GPIO.output(all_off_light_pin, 1)

        else:

            GPIO.output(all_off_light_pin, 0)

        for light_type in lights_dict.keys():

            light_info = lights_dict[light_type]

            if light_info["current_state"] != light_info["previous_state"]:

                lights_dict[light_type]["previous_state"] = light_info["current_state"]

                values = (
                    int(time.time()),
                    sensor,
                    light_type,
                    light_info["current_state"],
                )

                write_control_to_db(values)

        time.sleep(1)
