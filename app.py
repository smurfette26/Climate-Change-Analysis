from flask import Flask, render_template, request, redirect, url_for, template_rendered
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'


@app.route("/preprocessing")
def preprocessing():
  data = {}
  return render_template('pre_processing.html', context=data)


@app.route("/")
def myApp():
  data = {}
  return render_template('home.html', context=data)


print(__name__)
if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
