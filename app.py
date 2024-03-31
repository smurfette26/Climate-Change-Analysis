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


    
@app.route('/encoding')
def encoding():
    # Perform Encoding operation here
    filename = request.args.get('filename')
    file_name_with_path = os.path.join(app.config['UPLOAD_PATH'], filename)
    data = read_csv(file_name_with_path)
    X = data.drop(["sales"], axis=1)
    y = data['sales']
    k = DataFrame(y)

    #X = data.drop(["sales"] , axis = 1)
    LE = OrdinalEncoder(categories=[['Mega', 'Micro', 'Nano', 'Macro']])
    Encoded = LE.fit_transform(X[['influencer']])
    D_influencer = DataFrame(Encoded)
    D_influencer.columns = ['encoded influencer']
    encoded_data = D_influencer.join(X[['influencer']])
    table_html = encoded_data.to_html(classes='data')
  # Pass HTML string to template
    return render_template('data1.html', table=table_html,heading="Encoded Data")
    #return f"Encoding operation performed - {filename}"

@app.route('/missing_value_detection')
def missing_value_detection():
    # ##Missing value detection
  filename = request.args.get('filename')
  file_name_with_path = os.path.join(app.config['UPLOAD_PATH'], filename)
  print(file_name_with_path)
  data = read_csv(file_name_with_path)
  print(data)
  missing_Data = data.isnull().sum()
  filled_with_na_data = data.fillna(0, inplace=True)
  print(missing_Data)
  table_html = missing_Data.to_html(classes='data')
  #return table_html
  return render_template('data1.html', table=table_html)

@app.route('/normalization')
def normalization():
  filename = request.args.get('filename')
  file_name_with_path = os.path.join(app.config['UPLOAD_PATH'], filename)
  data = read_csv(file_name_with_path)
  X = data.drop(["sales"], axis=1)
  y = data['sales']
  k = DataFrame(y)
  # ##Normalization
  normal_f = StandardScaler()
  X = data.drop(["sales", 'influencer'], axis=1)
  K = normal_f.fit_transform(X)
  header = X.columns
  K = DataFrame(K)
  K.columns = header
  table_html = K.to_html(classes='data')
  return render_template('data1.html', table=table_html,heading="Normalised Data")


@app.route("/preprocessing/<filename>")
def preprocessing(filename=None):
  if filename:
    data = {"filename":filename}
    return render_template("pre_processing.html", context=data)
  else:
    return render_template('pre_processing.html',context={})


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
