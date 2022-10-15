import csv
import json
import re
import time
import sys
import math
from os.path import exists  
import sqlite3
from sqlite3 import Error

def dbConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("DB CONNECTION ERROR")
    return conn

def dbInsert(conn, task):
    try:
        sql = ''' INSERT INTO backup(pm25,pm10,co,co2,so2,no2,o3,created_date,created_date_int)
                 VALUES(?,?,?,?,?,?,?,datetime('now'),strftime('%s','now')) '''
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
    except Exception as err:
        print("DB ERROR INSERT")

def dbBackup(data):
    database = r"D:\00-workstation\flask\dev-db\db\parse.db"

    conn = dbConnection(database)

    with conn:
        dbInsert(conn, data)


def main():
    try:
        file = open('./json.txt')
        content = file.read()
        pattern = r"{(?:[^{}]*|)*}"
        match = re.search(pattern, content)
        match = match.group()
        match = match.replace("\n", "")
        data = json.loads(match)
        data =  {k.upper(): v for k, v in data.items()}
        backup_data = [data["PM2_5"], data["PM10"], data["CO"], data["CO2"], data["SO2"], data["NO2"], data["O3"]]
        print(backup_data)
        for i in range(len(backup_data)):
            try:
                if(math.isnan(float(backup_data[i]))):
                    raise ValueError("Not a number")
                backup_data[i] = float(backup_data[i])
            except ValueError:
                print("VALUE ERROR")
                backup_data[i] = 0.00
        
        print(backup_data)
        dbBackup(backup_data)
        file.close()
    except Exception as err:
        print(err)
        print("ERROR")
        data = {}

    if(bool(data)!=False):
        headers = data.keys()
        file_exists = exists('backup.csv')
        try:
            with open('backup.csv', 'a',newline='\n', encoding='UTF8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = headers)
                if(file_exists != True):
                    writer.writeheader()
                writer.writerows([data])
        except Exception as  err:
            print(err)
            print("ERROR CSV")
        print("DONE")

if __name__ == '__main__':
    try:
        while True:
            main()
            time.sleep(5)
    except KeyboardInterrupt:
        sys.exit(0)
