"""
 CREATE TABLE IF NOT EXISTS backup (,
                                        PM25 VARCHAR(100) DEFAULT NULL,
                                        PM10 VARCHAR(100) DEFAULT NULL,
                                        CO VARCHAR(100) DEFAULT NULL,
                                        CO2 VARCHAR(100) DEFAULT NULL,
                                        SO2 VARCHAR(100) DEFAULT NULL,
                                        NO2 VARCHAR(100) DEFAULT NULL,
                                        O3 VARCHAR(100) DEFAULT NULL,
                                        created_date VARCHAR(100) DEFAULT NULL,
                                        created_date_int INT DEFAULT NULL
                                    ); 
"""

"""
from timedate import datetime, timedelta
from time import mktime

unix time before 24 hours

time = datetime.now() - timedelta(hours=24)
time = mktime(time.timetuple())
"""