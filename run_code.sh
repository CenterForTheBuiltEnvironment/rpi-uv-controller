#!/bin/sh
# pull request to update files
echo "Pull request"
git pull

# todo remove this line
echo "Removing the database file"
rm -f database.db

sleep 3

echo "Starting python scripts"
# start beacon scanner
sudo python3 beacon_scanner.py &
sudo python3 pir_sensor.py &
sudo python3 light_controller.py &
sudo python3 ultrasonic_sensor.py &
sudo python3 kill_switch.py &