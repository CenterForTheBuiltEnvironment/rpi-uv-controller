# nvim configuration http://vim.fisadev.com/#features-and-help

from bluepy.btle import Scanner, DefaultDelegate
import sqlite3
import datetime


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print("could not connect")

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except:
        print("could not create a table")


def add_entry(conn, data):
    """
    Create a new entry into the beacons table
    :param conn:
    :param data:
    :return: project id
    """
    sql = """ INSERT INTO beacons(device_id, time_stamp, rssi)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid


sql_create_beacons_table = (
    "CREATE TABLE IF NOT EXISTS beacons "
    "( id integer PRIMARY KEY, "
    "device_id text NOT NULL, "
    "time_stamp text, "
    "rssi int)"
)

connection = create_connection("database.db")

# create tables
if connection is not None:
    # create projects table
    create_table(connection, sql_create_beacons_table)

    # create tasks table
    create_table(connection, sql_create_beacons_table)
else:
    print("Error! cannot create the database connection.")

# conn.close()

# BLE Scanning class
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # def handleDiscovery(Self, dev, isNewDev, isNewData):
    #     if isNewDev:
    #         print ("Discovered Device", dev.addr)
    #     elif isNewData:
    #         print ("Received new data from:", dev.addr)


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

        if dev.addr == ("DA:f7:89:c4:54:5f").lower():

            print("beacon in range")
            print(dev.addr, dev.rssi)

            reading = (dev.addr, datetime.datetime.now().isoformat(), dev.rssi)

            index = add_entry(connection, reading)

            print(f"index new entry: {index}")

            # if ((desc == 'Complete Local Name') & (value == "ESP32")):
            # print(desc, value)
            # ID=str(dev.addr)
            # print('ID (MAC addr): %s' % (ID))
            # MQTTID=ID.replace(":","")
