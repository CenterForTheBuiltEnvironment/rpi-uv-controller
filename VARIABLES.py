"""
This Python file contains all the variables that can be changed. Please refer to README.md
"""

# dictionary of beacons to track
beacons_to_track = {
    "da:f7:89:c4:54:5f": -40,
    "f3:d8:17:3f:fd:9c": -40,
    "f4:d9:18:40:fe:9d": -40,
    "f0:d5:14:3c:fa:99": -40,
}

# minimum time that the light need to stay off, to prevent that the light fails
min_time_off = 5 * 60

# time after which lights turn on after last occupancy was detected by the relative sensor
delay_beacons = 1 * 60
delay_pir = 2 * 60
delay_kill_switch = 1 * 60

# max time lights can stay on after person leaves the space
max_time_on_lights_top = 10 * 60  # in reality is desk
max_time_on_lights_desk = 20 * 60  # ceiling light
max_time_on_lights_room = 10 * 60  # is actually room

# room light variables
hours_on = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
days_on = [0, 1, 2, 3, 4]  # where 0 is Monday

# std of distance below which it is believe there is not occupancy
threshold_ultrasonic_std = 0.02  # calculated using data collected by Federico

# other variables (all times are in seconds)
beacon_scanning_interval = 3.0  # amount of seconds the RPI scans for beacons
