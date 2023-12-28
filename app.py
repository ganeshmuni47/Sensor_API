from flask import Flask, render_template, request, redirect, session, url_for, jsonify, abort, send_file
# from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import secrets
import os, sys
import utils
from utils import dbconn
from sqlalchemy.util import deprecations
deprecations.SILENCE_UBER_WARNING = True
from sqlalchemy import text
import pandas as pd

app = Flask(__name__)
app.secret_key = '1uybRXm+ZiS+L/yaoC4='
static_path = os.path.abspath("./static")
app.config['UPLOAD_FOLDER'] = os.path.join(static_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
max_upload_size = 5 #in MB
print(app.config['UPLOAD_FOLDER'])
server_name = 'localhost'

page_defaults = {
    "date_from" : datetime.today().strftime("%Y-%m-%d"),
    "date_to" : datetime.today().strftime("%Y-%m-%d"),
    "sensor_type" : "%"
}

@app.route('/',methods=["GET", "POST"])
def index():
    if(request.method=="POST"):
        print("#== Method POST ==#")
        if(request.form.get('submit')):
            date_from = request.form['date-from']
            date_to = request.form['date-to']
            sensor_type = request.form['sensor-type']
            sensor_data = utils.sql_utils.sql_to_html(utils.sql_utils.sql_2.format(date_from,date_to,sensor_type),static_path)
            if(sensor_type=='%'):
                sensor_type_file = 'All'
            else:
                sensor_type_file = sensor_type
            session['data']['date_from'] = date_from
            session['data']['date_to'] = date_to
            session['data']['sensor_type'] = sensor_type_file
            return render_template('index.html',table_data = sensor_data, data = session['data'])
        
        if(request.form.get('download')):
            date_from = request.form['date-from']
            date_to = request.form['date-to']
            sensor_type = request.form['sensor-type']
            sensor_data = utils.sql_utils.sql_to_html(utils.sql_utils.sql_2.format(date_from,date_to,sensor_type),static_path)
            path = static_path+"\\temp_data\\temp.csv"
            if(sensor_type=='%'):
                sensor_type_file = 'All'
            else:
                sensor_type_file = sensor_type
            file_name = f"SensorData_{sensor_type_file}_{date_from}_{date_to}.csv"
            return send_file(path, as_attachment=True, download_name=file_name)
    else:
        session['data'] = {}
        date_from = page_defaults['date_from']
        date_to = page_defaults['date_to']
        sensor_type = "%"
        sensor_data = utils.sql_utils.sql_to_html(utils.sql_utils.sql_2.format(date_from,date_to,sensor_type),static_path)
        sensor_type_file = ''
        if(sensor_type=='%'):
            sensor_type_file = 'All'
        else:
            sensor_type_file = sensor_type
        session['data']['date_from'] = date_from
        session['data']['date_to'] = date_to
        session['data']['sensor_type'] = sensor_type_file

        return render_template('index.html',table_data = sensor_data, data = session['data'])

# Reading Data
# http://localhost:8008/send_data/test_sensor/?data={%22value%22:30.1}
# http://localhost:8008/send_data/test_sensor/?data={"value":30.1}

@app.route('/send_data/<sensor_type>/',methods=["GET", "POST"])
def send_data(sensor_type):
    if(request.method=='GET'):
        if(sensor_type == 'test_sensor'):
            data_get = request.args.get('data')
            data_json = json.loads(data_get) # Get Sensor in JSON Data
            x = data_json['value'] # Get data of Key = "value"
            print("Sensor Value:", x)
            sql_insert = f"INSERT INTO sensors_database.sensors_read_f(sensor_id, read_value) VALUES(0, {x})"
            row_cnt = dbconn.sql_transact(sql_insert)
            print("Records inserted: ", row_cnt)
            # Success API
            response = {
                'status': 'success',
                'message': 'API call successful'
            }
            return jsonify(response), 200
        else:
            response = {
                'status': 'failed',
                'message': 'API call failed'
            }
            return jsonify(response), 400
        
@app.route('/live', methods=["GET","POST"])
def live():
    return render_template('live.html')

@app.route('/live_data/<sensor_type>/', methods=["GET","POST"])
def live_data(sensor_type):
    sensor_data = utils.sql_utils.sql_to_dict(utils.sql_utils.sql_3.format(sensor_type))
    return sensor_data


if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=8008)