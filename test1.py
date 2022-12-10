import pymssql  

conn = pymssql.connect(server='LAPTOP-2C9DB9N1', user='test', password='test', database='AQMS')  
cursor = conn.cursor()  
cursor.execute("SELECT * FROM ALT_TblAQI_History WHERE devicename='AQMS-1'")  
row = cursor.fetchone()  
while row:  
    print(row)     
    row = cursor.fetchone()