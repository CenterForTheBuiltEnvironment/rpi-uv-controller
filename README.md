# rpi-uv-controller

This repository contains the code to automatically control the UV lights in a space using a RPI and the following sensors:

* occupancy sensor
* ble beacons
* ultrasonic sensor
* manual switch

In a nutshell the control logic works as follows:

* if the kill switch was not pressed; and
* if the ultrasonic sensor did not detect movement; and
* if the PIR sensor did not detect movement;
* the top lights turn on if the beacon is further than the predefined threshold while the desk light turn on only if the beacon was not detected at all.

Only after occupancy is not detected for a predefined amount of time (see section below to change these values) which can be set differently for each sensor. Then the RPI turns on the lights based on the above mentioned control logic. Light can stay on only for a predefined amount of time after which they automatically turn off. Light will turn on again either at midnight (each day) or after that a person enter and then leaves the space. 

## Project schematic

![alt text](https://github.com/FedericoTartarini/rpi-uv-controller/tree/master/images/schematic.png)

If you wire the sensors as shown in the image above please change the variables in the `VARIABLES.py` file as follows:

### pins
pin_manual_switch = 22
pin_pir_1 = 27
pin_pir_2 = 18
pin_ultrasonic_echo = 4
pin_ultrasonic_trigger = 17
pin_light_desk = 10
pin_light_room = 24
pin_light_top = 23

## Parts

Below a list of all the parts needed and their estimated cost.

| Command | Unit price | Quantity |
| --- | --- | --- |
| BreadBoard - Half Size | $4.5 | 1 |
| BLE beacon | $20 | 1 |
| Raspberry Pi 3 or 4 | $40 | 1 |
| Relay Module 4-Ch | $2.69 | 1 |
| PIR (motion) sensor | $9.95 | 2 |
| USB micro-B Cable - 6 Foot | $2.98 | 1 |
| Ultrasonic Sensor - HC-SR04 | $3.95 | 1 |
| 470 Ohm Resistor | $0.1 | 1 |
| 1K Ohm Resistor | $0.1 | 1 |
| Mini Pushbutton Switch | $0.1 | 1 |
| 10K Ohm Resistor | $0.1 | 1 |
| Jumper Wires Pack - M/M | $1.95 | 1 |
| Jumper Wires Pack - M/F | $1.95 | 1 |

## Parameters (variables) that can be changed

You can change them by editing the file `VARIABLES.py`.

Please also change the pin numbers in this file if you are connecting the sensors as shown in the schematic image.

### beacons_to_track

Is a dictionary of all the the Beacons that the RPI needs to track.

**The ids of the beacons should be lowercase!**

The keys are the beacon ids, while the values are the rssi threshold for that beacon. This threshold is used to turn on the top lights. Note that rssi values are always negative values, with decreasing values as the beacon moves away from the RPI.

### other variables

See `VARIABLES.py` for more information.

### database.db

SQLite3 database that stores all the data collected by the sensors and the control commands for the lights

## How to get started

* Clone this repository on the RPI using the following code:
```
git clone https://github.com/FedericoTartarini/rpi-uv-controller.git
```

or this code if you use SSH.
```
git@github.com:FedericoTartarini/rpi-uv-controller.git
```

* cd into the project repository using the following command:
```
cd rpi-uv-controller
```

* Create a virtual environment and activate it
```
python3 -m venv venv
. venv/bin/activate
```

* Install the required packages
```
pip install -r requirements.txt
``` 

* Run the file `run_code.sh` using the following command:
```
bash run_code.sh &
```

This will run automatically all the Python scripts needed.

To kill them all at once.
```
bash stop_code.sh
```

Alternative, you can selectively kill a Python script using the following command:
```
sudo pkill -f <name_python_file>
```

## How to install new packages

* cd into the project repository
* activate virtual environment
```
. venv/bin/activate
```
* install the new package
* use `pipreqs` to generate `requirements.txt` file, alternatively manually add new package to `requirements.txt`

## How to access the PI remotely
You can SSH into the PI if you are connected to the same Wi-Fi network by using the following command
```
ssh pi@10.25.174.66
```

## How to commit and push new local changes to GitHub
```
git add .
git commit -m "your commmit message"
git push
```

## How to analyse the control signal data
You need to first SSH into the pi. Then type the following commands to update the csv file and push it to GitHub
```
cd Desktop/rpi-uv-controller
python3 db_handler.py

git add .
git commit -m "your commmit message"
git push
```

Then on your computer open anaconda, navigate to the `rpi-uv-controller` folder and type:
```
git pull
python3 control_signals_analysis/analyze_control_signals.py
```

This should generate the chart.

