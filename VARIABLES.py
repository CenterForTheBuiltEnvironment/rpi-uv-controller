"""
This Python file contains all the variables that can be changed. Please refer to README.md
"""

# dictionary of beacons to track
beacons_to_track = {
    "f1:d6:15:3d:fb:9a": -50,
    "df:f8:6e:f6:b9:95": -50,
}

# minimum time that the light need to stay off, to prevent that the light fails
min_time_off = 1 * 60

# time after which lights turn on after last occupancy was detected by the relative sensor
delay_beacons = 1 * 60
delay_pir = 1 * 60
delay_kill_switch = 1 * 60

# max time lights can stay on after person leaves the space
max_time_on_lights_top = 5 * 60  # in reality is desk
max_time_on_lights_desk = 10 * 60  # ceiling light
max_time_on_lights_room = 5 * 60  # is actually room

# room light variables
hours_on = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
days_on = [0, 1, 2, 3, 4, 5, 6]  # where 0 is Monday

# std of distance below which it is believe there is not occupancy
threshold_ultrasonic_std = 0.05  # calculated using data collected by Federico

# other variables (all times are in seconds)
beacon_scanning_interval = 3.0  # amount of seconds the RPI scans for beacons
