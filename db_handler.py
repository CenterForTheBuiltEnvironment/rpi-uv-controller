import sqlite3
from sqlite3 import Error
import time
import os
import csv


db_file_location = os.path.join(os.getcwd(), "database.db")


def connect_db():
    """ create a database connection to the SQLite database
        specified by the db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file_location)
    except Error as e:
        print(e)

    return conn


def read_db(conn, query_str):
    """
    Query all rows in the tasks table
    """
    cur = conn.cursor()
    cur.execute(query_str)

    rows = cur.fetchall()

    return rows


def write_db(conn, sql, values):
    """ Write to database """
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print("could not create a table")
        print(e)


def create_beacons_table():
    conn = connect_db()

    sql = (
        "CREATE TABLE IF NOT EXISTS beacons "
        "( id integer PRIMARY KEY, "
        "device_id text NOT NULL, "
        "time_stamp int, "
        "rssi int)"
    )

    create_table(conn, sql)

    conn.close()


def create_pir_table():
    conn = connect_db()

    sql = (
        "CREATE TABLE IF NOT EXISTS pir "
        "( id integer PRIMARY KEY, "
        "time_stamp int, "
        "presence int)"
    )

    create_table(conn, sql)

    conn.close()


def create_ultrasonic_calibration_table():
    conn = connect_db()

    sql = (
        "CREATE TABLE IF NOT EXISTS calibration_ultrasonic "
        "( id integer PRIMARY KEY, "
        "time_stamp int, "
        "distance real, "
        "mean real, "
        "std real)"
    )

    create_table(conn, sql)

    conn.close()


def create_ultrasonic_table():
    conn = connect_db()

    sql = (
        "CREATE TABLE IF NOT EXISTS ultrasonic "
        "( id integer PRIMARY KEY, "
        "time_stamp int, "
        "distance real, "
        "mean real, "
        "std real)"
    )

    create_table(conn, sql)

    conn.close()


def create_controller_table():
    conn = connect_db()

    sql = (
        "CREATE TABLE IF NOT EXISTS control_signals "
        "( id integer PRIMARY KEY, "
        "time_stamp int, "
        "sensor text, "
        "light_type text, "
        "signal int)"
    )

    create_table(conn, sql)

    conn.close()


def add_fake_beacons_reading(_id, rssi):

    sql = "INSERT INTO beacons(device_id, time_stamp, rssi) VALUES(?,?,?) "

    reading = (_id, int(time.time()), rssi)

    conn = connect_db()

    ix = write_db(conn, sql, reading)

    conn.close()

    print(ix)


def main():

    conn = connect_db()

    # # query all data
    # query = "SELECT * from beacons"
    # rows =  read_db(conn, query)

    # # query only last entry by beacon id
    # query_last_entry_by_id = (
    #     "SELECT device_id, rssi, MAX(time_stamp) " "FROM beacons " "GROUP BY device_id;"
    # )
    # rows = read_db(conn, query_last_entry_by_id)

    # # query last entries rpi
    # now = int(time.time()) - 60
    # query_last_entry_by_id = f"SELECT * FROM pir WHERE time_stamp > {now}"
    # rows = read_db(conn, query_last_entry_by_id)

    # query ultrasonic data
    query = f"SELECT * FROM calibration_ultrasonic"
    rows = read_db(conn, query)

    with open("ultrasonic_calibration.csv", "w", newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        for row in rows:
            writer.writerow(row)

    conn.close()


if __name__ == "__main__":
    main()
