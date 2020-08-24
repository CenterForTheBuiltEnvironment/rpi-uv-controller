# nvim configuration http://vim.fisadev.com/#features-and-help

from bluepy.btle import Scanner, DefaultDelegate
import time
import sqlite3
import datetime
import sys

# Connection to the local database
conn = sqlite3.connect("database.db")

# Create a cursor
c = conn.cursor()

try:
    c.execute("""CREATE TABLE beacons (
            time_stamp text,
            device_id text,
            rssi integer,
            )
            """)
    conn.commit()

    print("table successfully created")
except:
    print(sys.exc_info()[0])

# conn.close()

# BLE Scanning class
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(Self, dev, isNewDev, isNewData):
        pass
        # if isNewDev:
            # pass
            # print ("Discovered Device", dev.addr)
        # elif isNewData:
            # pass
            # print ("Received new data from:", dev.addr)


# initialize the scanner
scanner = Scanner().withDelegate(ScanDelegate())


# Main Loop that scans for the beacons
i = 0

while i < 1:
#   i = i + 1
#   print(time.time())
    print("Scanning ... ")
    devices = scanner.scan(5.0)
    # print("Finished scan for devices")

    for dev in devices:

        # for (adtype, desc, value) in dev.getScanData():

            # print(adtype, desc, value)
            # print(dev.addr)

        if dev.addr == ('DA:f7:89:c4:54:5f').lower():

            print("beacon in range")
            print(dev.addr, dev.addrType, dev.rssi)

            now = datetime.datetime.now().isoformat()

            c.execute(f"INSERT INTO beacons VALUES ( '2020-08-24T11:12:31', 'aa:bb', 20)")

            c.commit()

            #if ((desc == 'Complete Local Name') & (value == "ESP32")):
                # print(desc, value)
                # ID=str(dev.addr)
                # print('ID (MAC addr): %s' % (ID))
                # MQTTID=ID.replace(":","")

