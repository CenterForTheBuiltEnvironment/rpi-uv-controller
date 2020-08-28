# nvim configuration http://vim.fisadev.com/#features-and-help

from bluepy.btle import Scanner, DefaultDelegate
import time
import beacons_ids
import db_handler
import datetime as dt

# BLE Scanning class
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # def handleDiscovery(Self, dev, isNewDev, isNewData):
    #     if isNewDev:
    #         print ("Discovered Device", dev.addr)
    #     elif isNewData:
    #         print ("Received new data from:", dev.addr)


def scan_beacons():

    # create the table
    db_handler.create_beacons_table()

    # # add some fake readings
    # db_handler.add_fake_beacons_reading("aa:aa:aa", -20, "database.db")

    # initialize the scanner
    scanner = Scanner().withDelegate(ScanDelegate())

    # devices to scan
    beacons = {}

    for beacon in beacons_ids.beacons_to_track.keys():
        beacons[beacon] = {}
        beacons[beacon]['previous_rssi'] = 9999

    # Main Loop that scans for the beacons
    while True:

        devices = scanner.scan(5.0)

        conn = db_handler.connect_db()

        for dev in devices:

            if dev.addr in beacons_ids.beacons_to_track.keys():

                if dev.rssi < beacons[dev.addr]['previous_rssi'] - 2 or dev.rssi > beacons[dev.addr]['previous_rssi'] + 2:

                    values = (dev.addr, int(time.time()), dev.rssi)

                    sql = """ INSERT INTO beacons(device_id, time_stamp, rssi)
                              VALUES(?,?,?) """

                    index = db_handler.write_db(conn, sql, values)

                    print(
                        f"beacon_scanner -- {dt.datetime.now().isoformat()} - index_db: {index}, ble_id: {dev.addr}, rssi: {dev.rssi}"
                    )

        conn.close()

    # todo implement a function that deletes old records


if __name__ == "__main__":
    scan_beacons()
