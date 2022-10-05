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
    sql = ''' INSERT INTO backup(pm25,pm10,co,co2,so2,no2,o3,created_date,created_date_int)
             VALUES(?,?,?,?,?,?,?,datetime('now'),strftime('%s','now')) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def dbBackup(data):
    database = r"D:\00-workstation\flask\dev-db\db\parse.db"
    
    try:
        conn = dbConnection(database)
    except Exception as err:
        print("DB ERROR")

    with conn:
        try:
            dbInsert(conn, data)
        except Exception as err:
            print("DB ERROR INSERT")

def main():
    try:
        file = open('./json.txt')
        content = file.read()
        pattern = r"{(?:[^{}]*|)*}"
        match = re.search(pattern, content)
        match = match.group()
        match = match.replace("\n", "")
        data = json.loads(match)
        backup_data = [data["PM25Value"], data["PM10Value"], data["COValue"], data["CO2Value"], data["SO2Value"], data["NO2Value"], data["O3Value"]]
        for i in range(len(backup_data)):
            try:
                if(math.isnan(float(backup_data[i]))):
                    raise ValueError("Not a number")
                backup_data[i] = float(backup_data[i])
            except ValueError:
                print("VALUE ERROR")
                backup_data[i] = 0.00
                
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
