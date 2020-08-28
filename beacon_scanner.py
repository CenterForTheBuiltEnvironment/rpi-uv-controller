# nvim configuration http://vim.fisadev.com/#features-and-help

from bluepy.btle import Scanner, DefaultDelegate
import time
import VARIABLES
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

    # Main Loop that scans for the beacons
    while True:

        devices = scanner.scan(VARIABLES.beacon_scanning_interval)

        conn = db_handler.connect_db()

        for dev in devices:

            if dev.addr in VARIABLES.beacons_to_track.keys():

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
