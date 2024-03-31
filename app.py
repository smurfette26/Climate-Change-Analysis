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


def data_processing(filename):
  data = read_csv(filename)
  X = data.drop(["sales"], axis=1)
  y = data['sales']
  k = DataFrame(y)

  #X = data.drop(["sales"] , axis = 1)
  LE = OrdinalEncoder(categories=[['Mega', 'Micro', 'Nano', 'Macro']])
  Encoded = LE.fit_transform(X[['influencer']])
  D_influencer = DataFrame(Encoded)
  D_influencer.columns = ['encoded influencer']
  D_influencer.join(X[['influencer']])

  ##Normalization
  normal_f = StandardScaler()

  X = data.drop(["sales", 'influencer'], axis=1)
  K = normal_f.fit_transform(X)
  header = X.columns
  K = DataFrame(K)
  K.columns = header

  ##Missing value detection
  data.isnull().sum()
  data.fillna(0, inplace=True)
  print(data.isnull().sum())

  correlation = data.corr()


@app.route("/preprocessing/<filename>")
def preprocessing(filename=None):
  if not filename:
    data = {}
    print(filename)
    file_name_with_path = os.path.join(app.config['UPLOAD_PATH'], filename)
    df = read_csv(file_name_with_path)
    return jsonify(df.to_dict())
    return render_template("pre_processing.html", context=data)

  return render_template('pre_processing.html')


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
