#!/bin/sh
# kill all the python scripts running
# https://stackoverflow.com/questions/40652793/how-to-kill-python-script-with-bash-script
# https://www.cyberciti.biz/faq/how-to-check-running-process-in-linux-using-command-line/
sudo pkill -f pir_sensor.py
sudo pkill -f beacon_scanner.py
sudo pkill -f light_controller.py
sudo pkill -f ultrasonic_sensor.py
sudo pkill -f kill_switch.py
