# rpi-uv-controller

This repository contains the code to automatically control the UV lights in a space using a RPI and the following sensors:

* occupancy sensors
* ble beacons
* manual switch

## How to get started

Clone this repository on the RPI using the following code:
```
git clone https://github.com/FedericoTartarini/rpi-uv-controller.git
```

cd into the project repository using the following command:
```
cd rpi-uv-controller
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