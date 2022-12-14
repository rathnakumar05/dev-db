import pyodbc 

try:
    server = '192.168.1.25'
    database = 'AQMS' 
    username = 'sa' 
    password = '$erver2012'
    port='1433'
    device_name = "AQMS-1"
    cnxn = pyodbc.connect('DRIVER={FreeTDS};SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+ password+';autocommit=True')
    cnxn.autocommit = True
    cursor = cnxn.cursor()
    cursor.execute("EXEC AQMS_Usp_AQIDailyUpdate @DeviceId='"+device_name+"'")
    row = cursor.fetchone()
    while row:
        row = cursor.fetchone()
        
    print("DONE")
    cnxn.close()
except:
    print("ERROR")

# cursor.execute("SELECT min(AQI) AS AQI, FORMAT(CONVERT(Date, updatetime), 'MMM/dd') as date FROM ALT_TblAQI_History WHERE devicename='AQMS-1' and updatetime>= DATEADD(day,-10000, GETDATE()) GROUP BY CONVERT(Date, updatetime)")



