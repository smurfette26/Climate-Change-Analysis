from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

####Data processing libraries
from pandas import read_csv, DataFrame
from statistics import mean, stdev
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from statistics import mode, mean, median, stdev, variance
from collections import Counter
from statistics import variance, stdev
from numpy import  transpose
import numpy as np


app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = '/static/uploads'
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


def data_processing(filename):
  
  

@app.route("/preprocessing/<filename>")
def preprocessing(filename):
  print(filename)
  data = {}
  return render_template('pre_processing.html', context=data)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    #f.save(secure_filename(f.filename))
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('preprocessing', filename=filename))
  else:
    return redirect(url_for('myApp'))


@app.route("/")
def myApp():
  data = {}
  return render_template('home.html', context=data)


print(__name__)
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
