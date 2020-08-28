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
* the top lights turn on if the beacon is further than the predefined threshold while the desk light turn on only if the beacon was not detected.

Only after occupancy is not detected for a predefined amount of time (see section below to change this value). Then the RPI turns on lights based on the above mentioned control logic. Light can stay on only for a predefined amount of time after which they automatically turn off. Light will turn on again either at midnight, on a daily basis or after that a new person enter and leaves the space. 

## Parameters (variables) that can be changed

You can change them by editing the file `VARIABLES.py`.

### beacons_to_track

Is a dictionary of all the the Beacons that the RPI needs to track.

**The ids of the beacons should be lowercase**

The keys are the beacon ids, while the values are the rssi threshold for that beacon. Note that rssi values are always negative values, with decreasing values as the beacon moves away from the RPI.

### other variables

See `VARIABLES.py` for more information.

### database.db

Is an SQLite3 database that stores all the data collected by the sensors and the control commands for the lights

## How to get started

Clone this repository on the RPI using the following code:
```
git clone https://github.com/FedericoTartarini/rpi-uv-controller.git
```

cd into the project repository using the following command:
```
cd rpi-uv-controller
```

Create a virtual environment and activate it
```
python3 -m venv venv
. venv/bin/activate
```

Install the required packages
```
pip install -r requirements.txt
``` 

Run the file `run_code.sh` using the following command:
```
bash run_code.sh
```

This will run automatically all the Python scripts needed.

You can selectively kill a Python script using the following command:
```
sudo pkill -f <name_python_file>
```

Alternatively run the following command to kill them all at once.
```
bash stop_code.sh
```

## How to install new packages

* cd into the project repository
* activate virtual environment
```
. venv/bin/activate
```
* install the new package
* use `pipreqs` to generate `requirements.txt` file, alternatively manually add new package to `requirements.txt`
