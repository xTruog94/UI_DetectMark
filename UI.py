from flask import Flask, render_template, request, send_file,redirect,url_for,send_from_directory
from model import *
import os
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone

app = Flask(__name__)
dropzone = Dropzone(app)

UPLOAD_FOLDER='E:/20201/flask_calculator_app/input/'
filename=''
output_dir='E:/20201/flask_calculator_app/output/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'home'
@app.route('/') 
def home():  
    return render_template("index.html")
@app.route('/upload',methods=['GET','POST'])  
def upload():
    global filename
    upload=False
    f = request.files['file']
    file_path = UPLOAD_FOLDER + f.filename
    filename = f.filename
    f.save(file_path)
    print(filename)
    return render_template('upload.html', upload=True,file=f.filename)
    
@app.route('/process', methods=['GET', 'POST'])
def process():

    try:
        finish = False
        run()
        return render_template('process.html',finish=True)
    except Exception as e:
        print(e)
        return render_template('error.html')

@app.route('/download', methods=['GET','POST'])
def download():
    global filename
    file_name = filename + '_result.xls'
    print(file_name)
    return send_from_directory(directory=output_dir
    ,filename= file_name)

if __name__ == '__main__':  
    app.run(debug = True)  