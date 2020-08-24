"""
This Python file contains a list of all the Beacons we want to track.

The keys in the dictionary are the beacon ids,
while the values are the rssi threshold for that beacon.

With the rssi threshold decreasing as the BLE beacon moves away.
The rssi values are negative values.

The ids should be lowercase
"""

beacons_to_track = {
    "da:f7:89:c4:54:5f": -75,
    "dd:bb:cc": -10,
}
