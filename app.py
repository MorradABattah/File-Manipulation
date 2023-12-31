import os
import logging
from flask import Flask, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from prometheus_flask_exporter import PrometheusMetrics
import pandas as pd

# Constants
APP_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_DIR, 'uploads')
DOWNLOAD_FOLDER = os.path.join(APP_DIR, 'downloads')
ALLOWED_EXTENSIONS = {'csv'}

# Ensure upload and download directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# App configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Initialize the metrics after the Flask app has been configured
metrics = PrometheusMetrics(app)

logging.basicConfig(filename='app.log', level=logging.INFO)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.info('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            logging.info('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logging.info('File saved successfully')
            csv_to_txt(filepath)
            return redirect('/downloads/' + filename.rsplit('.', 1)[0] + '.txt')
    return '''
    <!doctype html>
    <title>Upload CSV file</title>
    <h1>Upload CSV file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def csv_to_txt(filepath):
    try:
        df = pd.read_csv(filepath)  # Use pandas to read the CSV
        txt_filename = filepath.rsplit('.', 1)[0] + '.txt'
        df.to_csv(txt_filename, sep='\t', index=False)  # Use pandas to write the TXT
        logging.info('File converted to txt')
    except Exception as e:
        logging.error('Failed to convert file: ' + str(e))


@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(port=5000)
