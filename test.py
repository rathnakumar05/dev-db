import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
try:
    server = '192.168.1.5'
    database = 'AQMS' 
    username = 'sa' 
    password = '$erver2012'
    port='1433'
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    cnxn = pyodbc.connect('DRIVER={FreeTDS};SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

# CONVERT(Date, updatetime)
    cursor.execute("SELECT TOP 7 min(AQI) AS AQI, FORMAT(CONVERT(Date, updatetime), 'MMM/dd') as date FROM ALT_TblAQI_History WHERE devicename='AQMS-1' and updatetime>= DATEADD(day,-10000, GETDATE()) GROUP BY CONVERT(Date, updatetime)") 
# cursor.execute("SELECT min(AQI) AS AQI, FORMAT(CONVERT(Date, updatetime), 'MMM/dd') as date FROM ALT_TblAQI_History WHERE devicename='AQMS-1' and updatetime>= DATEADD(day,-10000, GETDATE()) GROUP BY CONVERT(Date, updatetime)")
    row = cursor.fetchone() 
except:
    print("edednednend")
# print(row)
# print("Hello")
# count = 0
# while row: 
#     print(row)
#     row = cursor.fetchone()
#     count = count + 1

# print(count)
