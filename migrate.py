import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


# delete from backup where created_date_int < '1665745209'; 
def main():
    database = r"D:\00-workstation\flask\dev-db\db\parse.db"

    sql_create_backup_table = """CREATE TABLE IF NOT EXISTS backup (
                                        pm25 VARCHAR(100) DEFAULT NULL,
                                        pm10 VARCHAR(100) DEFAULT NULL,
                                        co VARCHAR(100) DEFAULT NULL,
                                        co2 VARCHAR(100) DEFAULT NULL,
                                        so2 VARCHAR(100) DEFAULT NULL,
                                        no2 VARCHAR(100) DEFAULT NULL,
                                        o3 VARCHAR(100) DEFAULT NULL,
                                        created_date VARCHAR(100) DEFAULT NULL,
                                        created_date_int INT DEFAULT NULL
                                    );"""


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_backup_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
