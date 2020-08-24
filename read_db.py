import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def query_db(conn, query_str):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(query_str)

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = r"database.db"

    # create a database connection
    conn = create_connection(database)
    with conn:

        query = "SELECT * from beacons"
        query_db(conn, query)


if __name__ == '__main__':
    main()