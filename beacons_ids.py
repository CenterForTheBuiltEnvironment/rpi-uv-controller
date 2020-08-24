"""
This Python file contains a list of all the Beacons we want to track.

The keys in the dictionary are the beacon ids,
while the values are the rssi threshold for that beacon.

With the rssi threshold decreasing as the BLE beacon moves away.
The rssi values are negative values.
"""

beacons_to_track = {
    "DA:f7:89:c4:54:5f": -90,
    }
