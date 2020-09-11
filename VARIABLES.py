"""
This Python file contains all the variables that can be changed. Please refer to README.md
"""

# dictionary of beacons to track
beacons_to_track = {
    "da:f7:89:c4:54:5f": -75,
}

# time after which lights turn on after last occupancy was detected by the relative sensor
delay_beacons = 1 * 60
delay_pir = 1 * 60
delay_kill_switch = 1 * 60

# max time lights can stay on after person leaves the space
max_time_on_lights_top = 20 * 60
max_time_on_lights_desk = 20 * 60
max_time_on_lights_room = 20 * 60

# room light variables
hours_on = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
days_on = [0, 1, 2, 3, 4]  # where 0 is Monday

# std of distance below which it is believe there is not occupancy
threshold_ultrasonic_std = 0.02  # calculated using data collected by Federico

# other variables (all times are in seconds)
beacon_scanning_interval = 3.0  # amount of seconds the RPI scans for beacons
