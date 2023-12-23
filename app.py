from flask import Flask, render_template, request, redirect, session, url_for, jsonify, abort
# from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import secrets
import os, sys
from utils import dbconn, emails, crypt, sql_statements, formdata, commons
import utils
from sqlalchemy.util import deprecations
deprecations.SILENCE_UBER_WARNING = True

app = Flask(__name__)
app.secret_key = utils.get_secret()
static_path = os.path.abspath("./static")
app.config['UPLOAD_FOLDER'] = os.path.join(static_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
max_upload_size = 5 #in MB
print(app.config['UPLOAD_FOLDER'])
server_name = 'localhost'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_data/<sensor_type>/',methods=["GET", "POST"])
def send_data(sensor_type):
    if(request.method=='GET'):
        if(sensor_type == 'force_sensor'):
            data_get = request.args.get('data')
            data_json = json.loads(data_get)
            x = data_json['value']
            return data_json
        else:
            return redirect('index.html')

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=8008)