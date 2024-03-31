from flask import Flask, render_template, request, redirect, url_for, template_rendered
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = '/static/uploads'
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


@app.route("/preprocessing")
def preprocessing():
  data = {}
  return render_template('pre_processing.html', context=data)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    #f.save(secure_filename(f.filename))
    filename = secure_filename(f.filename)
    print(filename)
    f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('preprocessing'))
  else:
    return redirect(url_for('myApp'))


@app.route("/")
def myApp():
  data = {}
  return render_template('home.html', context=data)


print(__name__)
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
