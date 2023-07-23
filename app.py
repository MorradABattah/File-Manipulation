from flask import Flask, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import os
import logging

app = Flask(__name__)

UPLOAD_FOLDER = '/Users/morradbattah/Documents/GitHub/File-Manipulation/Uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(filename='app.log', level=logging.INFO)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        df = pd.read_csv(filepath)
        txt_filename = filepath.rsplit('.', 1)[0] + '.txt'
        df.to_csv(txt_filename, sep='\t', index=False)
        logging.info('File converted to txt')
    except Exception as e:
        logging.error('Failed to convert file: ' + str(e))

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(port=5000)
