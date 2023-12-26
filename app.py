from flask import Flask, render_template, request, redirect, session, url_for, jsonify, abort
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
static_path = os.path.abspath("./static")
app.config['UPLOAD_FOLDER'] = os.path.join(static_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
max_upload_size = 5 #in MB
print(app.config['UPLOAD_FOLDER'])
server_name = 'localhost'

@app.route('/')
def index():
    sensor_data = utils.sql_utils.sql_to_html(utils.sql_utils.sql_1)
    print(sensor_data)
    return render_template('index.html',table_data = sensor_data)

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
        
if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=8008)