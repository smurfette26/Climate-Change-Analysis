from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from filter_data import Filter

app = Flask(__name__)

conn = sqlite3.connect('climate.db')

df = pd.read_sql_query("select * from climate", conn)


@app.route("/")
def myApp():
  return render_template('home.html')


@app.route("/filter_data", methods=["GET", "POST"])
def filter_data():
  print("running in filter_data")
  if request.method == "POST":
    print("running in post request")
    country = request.form.get("country")
    if country == "None":
      country = None
    sector = request.form.get("sector")
    if sector == "None":
      sector = None
    gas = request.form.get("gas")
    if gas == "None":
      gas = None

    fil = Filter(country, sector, gas)

    i = fil.FilterByCountry(df)
    filtered_data = fil.FilterBySector(i)

    # Pass the filtered DataFrame to the template for rendering
    return render_template('home.html',
                           tables=[filtered_data.to_html(classes='data')])

  else:
    return render_template('home.html', tables=df.to_html(classes='data'))


@app.route("/climate")
def climate():
  return render_template('climate.html',
                         tables=[df.to_html(classes='data')],
                         titles=df.columns.values)


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
