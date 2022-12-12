from flask import Flask, render_template
import json
import re
import math
import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
from time import mktime
import copy
import pyodbc 
from waitress import serve

app = Flask(__name__)

def getChartData():
    chart_label = []
    chart_data = []
    try:
        server = '192.168.1.5'
        database = 'AQMS' 
        username = 'sa' 
        password = '$erver2012'
        port='1433'
        cnxn = pyodbc.connect('DRIVER={FreeTDS};SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        cursor.execute("SELECT TOP 7 min(AQI) AS AQI, FORMAT(CONVERT(Date, updatetime), 'dd/MMM') as date FROM ALT_TblAQI_History WHERE devicename='AQMS-1' and updatetime>= DATEADD(day,-7, GETDATE()) GROUP BY CONVERT(Date, updatetime)") 
        row = cursor.fetchone() 
        while row: 
            chart_label.append(row[1])
            chart_data.append(int(row[0]))
            row = cursor.fetchone()
    except:
        print("MSSQL ERROR")

    return chart_label, chart_data

def dbConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("DB ERROR")
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
        'hours_8' : 'SELECT SUM(co),SUM(o3),count(*) FROM backup WHERE created_date_int>="'+hours_8+'"',
        'hours_1' : 'SELECT SUM(so2),SUM(no2),count(*) FROM backup WHERE created_date_int>="'+hours_1+'"',
    }

    record = {}
    for i in sql:
        cur = conn.cursor()
        cur.execute(sql[i])
        rows = cur.fetchall()
        for row in rows:
            try:
                if(i=="hours_24"):
                    pm25 = float(row[0] or 0)
                    pm10 = float(row[1] or 0)
                    count = int(row[2] or 0)
                    if(count>0):
                        record["PM25"] = round(pm25/count, 2)
                        record["PM10"] = round(pm10/count, 2)
                    else:
                        record["PM25"] = 0.00
                        record["PM10"] = 0.00
                elif(i=="hours_8"):
                    co = float(row[0] or 0)
                    o3 = float(row[1] or 0)
                    count = int(row[2] or 0)
                    if(count>0):
                        record["CO"] = round(co/count, 2)
                        record["O3"] = round(o3/count, 2)
                    else:
                        record["CO"] = 0.00
                        record["O3"] = 0.00
                elif(i=="hours_1"):
                    so2 = float(row[0] or 0)
                    no2 = float(row[1] or 0)
                    count = int(row[2] or 0)
                    if(count>0):
                        record["SO2"] = round(so2/count, 2)
                        record["NO2"] = round(no2/count, 2)
                    else:
                        record["SO2"] = 0.00
                        record["NO2"] = 0.00
            except:
                print("RECORD ERROR")
    return record


def getAverage():
    database = r"/home/pi/dev-db/db/parse.db"
    conn = dbConnection(database)
    records = {}
    if(conn!=None):
        with conn:
            records = getRecord(conn)
    return records

def getAQICalc(BPLo, BPHi, ILo, IHi, avg):
    aqi_value = (((IHi-ILo)/(BPHi-BPLo))*(avg-BPLo)) + ILo
    return abs(aqi_value)
    

def getAQIValue(averages):
    aqi_values = []
    for key, value in averages.items():
        value = float(value)
        if(key=="PM25"):
            if(value>=0.00 and value<=30.00):
                aqi_value = getAQICalc(BPLo = 0.00, BPHi = 30.00, ILo = 0.00, IHi = 50.00, avg = value)
            elif(value>30.00 and value<=60.00):
                aqi_value = getAQICalc(BPLo = 30.1, BPHi = 60, ILo = 51, IHi = 100, avg = value)
            elif(value>60.00 and value<=90.00):
                aqi_value = getAQICalc(BPLo = 60.1, BPHi = 90, ILo = 101, IHi = 200, avg = value)
            elif(value>90.00 and value<=120.00):
                aqi_value = getAQICalc(BPLo = 91, BPHi = 120, ILo = 201, IHi = 300, avg = value)
            elif(value>120.00 and value<=250.00):
                aqi_value = getAQICalc(BPLo = 120.1, BPHi = 250, ILo = 301, IHi = 400, avg = value)
            elif(value>250.00 and value<=10000.00):
                aqi_value = getAQICalc(BPLo = 250.1, BPHi = 1000, ILo = 401, IHi = 500, avg = value)
            elif(value>10000.00):
                aqi_value = getAQICalc(BPLo = 250.1, BPHi = 1000, ILo = 401, IHi = 500, avg = value)
                # aqi_value = getAQICalc(BPLo = , BPHi = , ILo = , IHi = , avg = value)

        elif(key=="PM10"):
            if(value>=0.00 and value<=50.00):
                aqi_value = getAQICalc(BPLo = 0, BPHi = 50, ILo = 0, IHi = 50, avg = value)
            elif(value>50.00 and value<=100.00):
                aqi_value = getAQICalc(BPLo = 50.1, BPHi = 100, ILo = 51, IHi = 100, avg = value)
            elif(value>100.00 and value<=250.00):
                aqi_value = getAQICalc(BPLo = 100.1, BPHi = 250, ILo = 101, IHi = 200, avg = value)
            elif(value>250.00 and value<=350.00):
                aqi_value = getAQICalc(BPLo = 250.1, BPHi = 350, ILo = 201, IHi = 300, avg = value)
            elif(value>350.00 and value<=430.00):
                aqi_value = getAQICalc(BPLo = 351.1, BPHi = 430, ILo = 301, IHi = 400, avg = value)
            elif(value>430.00 and value<=10000.00):
                aqi_value = getAQICalc(BPLo = 431.1, BPHi = 1000, ILo = 401, IHi = 500, avg = value)
            elif( value>10000.00):
                aqi_value = getAQICalc(BPLo = 431.1, BPHi = 1000, ILo = 401, IHi = 500, avg = value)
        
        elif(key=="CO"):
            if(value>=0.00 and value<=4.4):
                aqi_value = getAQICalc(BPLo = 0, BPHi = 4.4, ILo = 0, IHi = 50, avg = value)
            elif(value>4.4 and value<=9.4):
                aqi_value = getAQICalc(BPLo = 4.5, BPHi = 9.4, ILo = 51, IHi = 100, avg = value)
            elif(value>9.4 and value<=12.4):
                aqi_value = getAQICalc(BPLo = 9.5, BPHi = 12.4, ILo = 101, IHi = 200, avg = value)
            elif(value>12.4 and value<=15.4):
                aqi_value = getAQICalc(BPLo = 12.5, BPHi = 15.4, ILo = 201, IHi = 300, avg = value)
            elif(value>15.4 and value<=30.4):
                aqi_value = getAQICalc(BPLo = 15.5, BPHi = 30.4, ILo = 301, IHi = 400, avg = value)
            elif(value>30.4 and value<=50.4):
                aqi_value = getAQICalc(BPLo = 30.5, BPHi = 50.4, ILo = 401, IHi = 500, avg = value)
            elif(value>50.4):
                aqi_value = getAQICalc(BPLo = 30.5, BPHi = 50.4, ILo = 401, IHi = 500, avg = value)
        
        elif(key=="SO2"):
            if(value>=0 and value<=40):
                aqi_value = getAQICalc(BPLo = 0, BPHi = 40, ILo = 0, IHi = 50, avg = value)
            elif(value>40 and value<=80):
                aqi_value = getAQICalc(BPLo = 41, BPHi = 80, ILo = 51, IHi = 100, avg = value)
            elif(value>80 and value<=380):
                aqi_value = getAQICalc(BPLo = 81, BPHi = 380, ILo = 101, IHi = 200, avg = value)
            elif(value>380 and value<=800):
                aqi_value = getAQICalc(BPLo = 381, BPHi = 800, ILo = 201, IHi = 300, avg = value)
            elif(value>800 and value<=1600):
                aqi_value = getAQICalc(BPLo = 801, BPHi = 1600, ILo = 301, IHi = 400, avg = value)
            elif(value>1600 and value<=2000):
                aqi_value = getAQICalc(BPLo = 1601, BPHi = 2000, ILo = 401, IHi = 500, avg = value)
            elif(value>2000):
                aqi_value = getAQICalc(BPLo = 1601, BPHi = 2000, ILo = 401, IHi = 500, avg = value)

        elif(key=="NO2"):
            if(value>=0.00 and value<=0.053):
                aqi_value = getAQICalc(BPLo = 0, BPHi = 0.053, ILo = 0, IHi = 50, avg = value)
            elif(value>0.053 and value<=0.1):
                aqi_value = getAQICalc(BPLo = 0.054, BPHi = 0.1, ILo = 51, IHi = 100, avg = value)
            elif(value>0.1 and value<=0.36):
                aqi_value = getAQICalc(BPLo = 0.101, BPHi = 0.36, ILo = 101, IHi = 200, avg = value)
            elif(value>0.36 and value<=0.649):
                aqi_value = getAQICalc(BPLo = 0.361, BPHi = 0.649, ILo = 201, IHi = 300, avg = value)
            elif(value>0.649 and value<=1.249):
                aqi_value = getAQICalc(BPLo = 0.65, BPHi = 1.249, ILo = 301, IHi = 400, avg = value)
            elif(value>1.249 and value<=2.049):
                aqi_value = getAQICalc(BPLo = 1.25, BPHi = 2.049, ILo = 401, IHi = 500, avg = value)
            elif(value>2.049):
                aqi_value = getAQICalc(BPLo = 1.25, BPHi = 2.049, ILo = 401, IHi = 500, avg = value)
        
        elif(key=="O3"):
            if(value>=0.00 and value<=50.00):
                aqi_value = getAQICalc(BPLo = 0, BPHi = 50, ILo = 0, IHi = 50, avg = value)
            elif(value>50.00 and value<=100.00):
                aqi_value = getAQICalc(BPLo = 51, BPHi = 100, ILo = 51, IHi = 100, avg = value)
            elif(value>100.00 and value<=168.00):
                aqi_value = getAQICalc(BPLo = 101, BPHi = 168, ILo = 101, IHi = 200, avg = value)
            elif(value>168.00 and value<=208.00):
                aqi_value = getAQICalc(BPLo = 169, BPHi = 208, ILo = 201, IHi = 300, avg = value)
            elif(value>208.00 and value<=748.00):
                aqi_value = getAQICalc(BPLo = 209, BPHi = 748, ILo = 301, IHi = 400, avg = value)
            elif(value>748.00 and value<=10000.00):
                aqi_value = getAQICalc(BPLo = 748.1, BPHi = 1000, ILo = 401, IHi = 500, avg = value)
            elif(value>10000.00):
                aqi_value = getAQICalc(BPLo = 748.1, BPHi = 1000, ILo = 401, IHi = 500, avg = value)
        
        else:
            aqi_value = 0
        
        aqi_values.append(aqi_value)
    return round(max(aqi_values), 2)

@app.route('/')
def home():
    try:
        with open('/home/pi/sensor/aqms/json.txt', encoding="utf8", errors='ignore') as file:
            content = file.read()
        pattern = r"{(?:[^{}]*|)*}"
        match = re.search(pattern, content)
        match = match.group()
        match = match.replace("\n", "")
        data = json.loads(match)
        averages = getAverage()
        if averages==None:
            averages = {}
            aqi = 0
        else:
           aqi = getAQIValue(averages) 
        
    except:
        print("ERROR")
        data = {}
        averages = {}
        aqi = 0
    final_data = {}
    data =  {k.upper(): v for k, v in data.items()}
    for key in data:
        key = key.upper()
        if(key.endswith("ID") and key!="DEVICENAME" and key!="UPDATETIME"):
            try:
                value_finder = key[:-2]
                if(value_finder=="PM25"):
                    value_finder = "PM2_5"
                if(value_finder=="TEMPERATURE"):
                    value_finder = "TEMP"
                if(value_finder=="LUX"):
                    value_finder = "AMBIENT"

                fi_value = data[value_finder]
                fi_key = data[key]
                fi_key = key+"-"+fi_key
                if(math.isnan(float(fi_value))):
                    raise ValueError("Not a number")
                final_data[fi_key] = [key[:-2], float(fi_value)]
            except KeyError:
                print("KEY ERROR")
                continue
            except ValueError:
                print("VALUE ERROR")
                final_data[fi_key] = [key.replace("ID", ""), 0.00]

        elif(key=="DEVICENAME" or key=="UPDATETIME"):
            final_data[key] = data[key]
    
    final_data_avg = copy.deepcopy(final_data)
    if len(averages.keys()) > 0:
        for key, value in final_data_avg.items(): 
            try:
                if(value[0]=="PM25"):
                    value[1] = averages["PM25"]
                elif(value[0]=="PM10"):
                    value[1] = averages["PM10"]
                elif(value[0]=="CO"):
                    value[1] = averages["CO"]
                elif(value[0]=="CO2"):
                    value[1] = averages["CO2"]
                elif(value[0]=="O3"):
                    value[1] = averages["O3"]
                elif(value[0]=="SO2"):
                    value[1] = averages["SO2"]
                elif(value[0]=="NO2"):
                    value[1] = averages["NO2"]
            except KeyError:
                print("KEY ERROR")
            except:
                print("ERROR")
                
        # print("AVERAGE ONLY")
        # print(averages)
        # print("REAL TIME")
        # print(final_data)
        # print("AVERAGE")
        # print(final_data_avg)
        # print("AQI")
        # print(aqi)
        chart_label, chart_data = getChartData()
    return render_template('index.html', values=final_data, values_avg=final_data_avg, aqi=aqi, chart_label=chart_label, chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
    # serve(app, host='0.0.0.0', port=5000)