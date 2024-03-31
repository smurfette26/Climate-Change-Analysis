from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os

####Data processing libraries
from pandas import read_csv, DataFrame
from statistics import mean, stdev
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from statistics import mode, mean, median, stdev, variance
from collections import Counter
from statistics import variance, stdev
from numpy import transpose
import numpy as np

#Encoding Non-continous Value Using Ordinal encoder
from sklearn.preprocessing import OrdinalEncoder

app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = '/static/uploads'
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv']


def data_processing(filename):

  dataprocessed_values = {}
  
  data = read_csv(filename)
  X = data.drop(["sales"], axis=1)
  y = data['sales']
  k = DataFrame(y)

  #X = data.drop(["sales"] , axis = 1)
  LE = OrdinalEncoder(categories=[['Mega', 'Micro', 'Nano', 'Macro']])
  Encoded = LE.fit_transform(X[['influencer']])
  D_influencer = DataFrame(Encoded)
  D_influencer.columns = ['encoded influencer']
  encoded_data = D_influencer.join(X[['influencer']])
  dataprocessed_values['encoded_data'] =encoded_data
  
  # ##Normalization
  # normal_f = StandardScaler()

  # X = data.drop(["sales", 'influencer'], axis=1)
  # K = normal_f.fit_transform(X)
  # header = X.columns
  # K = DataFrame(K)
  # K.columns = header
  # dataprocessed_values["normalization"]=K
  
  # ##Missing value detection
  # data.isnull().sum()
  # data.fillna(0, inplace=True)
  # #print(data.isnull().sum())
  # dataprocessed_values["missing_value"] = data.isnull().sum()
  # correlation = data.corr()

  return dataprocessed_values
  

@app.route("/preprocessing/<filename>")
def preprocessing(filename=None):
  if filename:
    data = {}
    print(filename)
    file_name_with_path = os.path.join(app.config['UPLOAD_PATH'], filename)
    processed_data = data_processing(file_name_with_path)
    print(processed_data)
    #return jsonify(processed_data)
    return render_template("pre_processing.html", context=data)

  return render_template('pre_processing.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    filename = secure_filename(f.filename)
    if filename != '':
      file_ext = os.path.splitext(filename)[1]
      if file_ext not in app.config['UPLOAD_EXTENSIONS']:
        return f"{file_ext} file extensions not supported ", 400
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
