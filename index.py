from flask import Flask, render_template
import json
import re
import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
from time import mktime

app = Flask(__name__)

def dbConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def getRecord(conn):
    now = datetime.now()

    hours_24 = now - timedelta(hours=24)
    hours_24 = str(mktime(hours_24.timetuple()))
    hours_8 = now - timedelta(hours=8)
    hours_8 = str(mktime(hours_8.timetuple()))
    hours_1 = now - timedelta(hours=1)
    hours_1 = str(mktime(hours_1.timetuple()))

    sql = {
        'hours_24' : 'SELECT SUM(pm25),SUM(pm10),count(*) FROM backup WHERE created_date_int>="'+hours_24+'"',
        'hours_8' : 'SELECT SUM(co),SUM(co2),SUM(o3),count(*) FROM backup WHERE created_date_int>="'+hours_8+'"',
        'hours_1' : 'SELECT SUM(so2),SUM(no2),count(*) FROM backup WHERE created_date_int>="'+hours_1+'"',
    }

    record = {}
    for i in sql:
        cur = conn.cursor()
        cur.execute(sql[i])
        rows = cur.fetchall()
        for row in rows:
            print(row)
            try:
                if(i=="hours_24"):
                    pm25 = float(row[0])
                    pm10 = float(row[1])
                    count = int(row[2])
                    if(count>0):
                        record["PM25"] = pm25/count
                        record["PM10"] = pm10/count
                elif(i=="hours_8"):
                    co = float(row[0])
                    co2 = float(row[1])
                    o3 = float(row[2])
                    count = int(row[3])
                    if(count>0):
                        record["CO"] = co/count
                        record["CO2"] = co2/count
                        record["O3"] = o3/count
                elif(i=="hours_1"):
                    so2 = float(row[0])
                    no2 = float(row[1])
                    count = int(row[2])
                    if(count>0):
                        record["SO2"] = so2/count
                        record["NO2"] = no2/count
            except Exception as err:
                print("RECORD ERROR")
    return record


def getAverage():
    database = r"D:\00-workstation\flask\dev\db\parse.db"
    try:
        conn = dbConnection(database)
    except Exception as err:
        print("DB ERROR")
    with conn:
        try:
            return getRecord(conn)
        except Exception as err:
            print(err)
            print("DB ERROR SELECT")
@app.route('/')
def home():
    try:
        with open('./json.txt', encoding="utf8", errors='ignore') as file:
            content = file.read()
        pattern = r"{(?:[^{}]*|)*}"
        match = re.search(pattern, content)
        match = match.group()
        match = match.replace("\n", "")
        data = json.loads(match)
        averages = getAverage()
        if averages==None:
            averages = {}
    except Exception as err:
        print("ERROR")
        data = {}
    final_data = {}
    for key in data:
        if(key.endswith("ID") and key!="DeviceID" and key!="CreatedDate"):
            try:
                value_finder = key.replace("ID", "Value")
                fi_value = data[value_finder]
                fi_key = data[key]
                fi_key = key+"-"+fi_key
                final_data[fi_key] = [key.replace("ID", ""), float(fi_value)]
            except KeyError:
                print("KEY ERROR")
                continue
            except ValueError:
                print("VALUE ERROR")
                final_data[fi_key] = [key.replace("ID", ""), -1.00]

        elif(key=="DeviceID" or key=="CreatedDate"):
            final_data[key] = data[key]
    
    return render_template('index.html', values=final_data, averages=averages)

if __name__ == '__main__':
    app.run(debug=True)