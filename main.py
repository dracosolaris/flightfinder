import sqlite3, requests
from sqlite3 import Error

url = "test.api.amadeus.com"
api_key = "hmIQI2iCWjsIngmMrLsNgZYnm0u6YS3Y"
api_secret = "C2mAhApDP3DO2YDJ"

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"./db.db")