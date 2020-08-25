#!/bin/sh
# kill all the python scripts running
sudo pkill -f pir_sensor.py
sudo pkill -f beacon_scanner.py
sudo pkill -f light_controller.py
