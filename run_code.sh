#!/bin/sh
# pull request to update files
git pull &
pid=$!
wait $pid

# start beacon scanner
sudo python3 beacon_scanner.py &
idBeaconScanner=$!
echo idBeaconScanner