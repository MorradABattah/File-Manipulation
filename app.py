from flask import Flask, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from prometheus_flask_exporter import PrometheusMetrics
import pandas as pd
import os
import logging

app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/upload/directory'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the metrics after the Flask app has been configured
metrics = PrometheusMetrics(app)

logging.basicConfig(filename='app.log', level=logging.INFO)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # rest of your code...
