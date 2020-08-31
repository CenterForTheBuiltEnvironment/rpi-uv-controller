#!/bin/sh
# pull request to update files
echo "Pull request"
git pull

# todo remove this line
echo "Removing the database file"
rm -f database.db

echo "Starting python scripts"
# start python scripts
sudo python3 beacon_scanner.py &
python3 pir_sensor.py &
python3 ultrasonic_sensor.py &
python3 kill_switch.py &

sleep 10

# start controller
python3 light_controller.py &
