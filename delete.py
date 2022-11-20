import csv
import json
import re
import time
import sys
import math
from os.path import exists  
import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
from time import mktime

def dbConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("DB CONNECTION ERROR")
    return conn

def dbDelete(conn):
    now = datetime.now()
    hours_48 = now - timedelta(hours=48)
    hours_48 = str(mktime(hours_48.timetuple()))
    try:
        sql = 'DELETE FROM backup WHERE created_date_int < "'+hours_48+'"'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except Exception as err:
        print("DB ERROR DELETE")

def dbBackup():
    database = r"/home/pi/dev-db/db/parse.db"
    conn = dbConnection(database)
    with conn:
        dbDelete(conn)

def main():
    dbBackup()

if __name__ == '__main__':
    main()

