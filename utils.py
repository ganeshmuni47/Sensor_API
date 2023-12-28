import mysql.connector
import base64
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text
import pandas as pd

class dbconn:
    db_hostname = 'localhost'
    db_port = 3306 # defauls 3306
    db_username = 'admin'
    db_password = 'anubhabiitbbsr'
    db_name = 'sensors_database'

    def mysql(host=db_hostname, port=3306, username=db_username, password=db_password, database=db_name):
        connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_string)
        conn = engine.connect()
        print("== Mysql Database Connected ==")
        return conn
    
    def sql_transact(sql_query):
        print(sql_query)
        conn = dbconn.mysql()
        cursor = conn.execute(text(sql_query).execution_options(autocommit=True))
        conn.commit()
        conn.close()
        return cursor.rowcount

    def sql_select(sql_query):
        print(sql_query)
        conn = dbconn.mysql()
        cursor = conn.execute(text(sql_query).execution_options(autocommit=True))
        data = cursor.fetchall()
        keys = list(cursor.keys())
        conn.close()
        return keys,data

class sql_utils:
    def sql_to_dict(sql_query):
        keys,data = dbconn.sql_select(sql_query)
        result_dicts = [dict(zip(keys, row)) for row in data]
        return result_dicts

    def sql_to_html(sql_query,static_path=None):
        keys,data = dbconn.sql_select(sql_query)
        result_dicts = [dict(zip(keys, row)) for row in data]
        df = pd.DataFrame(result_dicts)
        df.columns = [items.upper() for items in list(df.columns)]
        html_str = df.to_html(index=False,table_id='data_table')
        if(static_path != None):
            df.to_csv(f"{static_path}\\temp_data\\temp.csv", index=False)
        return html_str
    
    sql_1 = """select * from sensor_data_v"""
    sql_2 = """select * from sensors_database.sensor_data_v
        where sensor_type like '{2}'
        and read_date >= '{0}'
        and read_date <= '{1}'"""
    sql_3 = """select * from sensors_database.sensor_data_v
        where sensor_type like '{0}' limit 50"""