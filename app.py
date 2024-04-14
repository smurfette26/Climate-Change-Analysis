from flask import Flask, render_template, request
import sqlite3
import pandas as pd
#from filter_data import Filter

app = Flask(__name__)

conn = sqlite3.connect('climate.db')

df = pd.read_sql_query("select * from climate", conn)


class Filter:

  def __init__(self,
               country=None,
               sector=None,
               gas=None,
               StartYear=None,
               EndYear=None):
    self.country = country
    self.sector = sector
    self.gas = gas
    self.StartYear = StartYear
    self.EndYear = EndYear

  def FilterByCountry(self, df):
    if self.country is not None:
      filtered_df_by_country = df[df['country'] == self.country]
      filtered_df_by_country.reset_index(drop=True, inplace=True)
      return filtered_df_by_country
    else:
      return df

  def FilterByYear(self, df):
    if self.StartYear is not None and self.EndYear is not None:
      fromYear = range(1990, self.StartYear)
      ToYear = range(self.EndYear + 1, 2021)
      sy = []
      ey = []
      for i in fromYear:
        sy.append(i)
      for k in ToYear:
        ey.append(k)
      sy.extend(ey)
      yearFilter = df.drop(columns=sy, axis=1)
      return yearFilter

    elif self.StartYear is not None:
      fromYear = range(1990, self.StartYear)
      sy = []
      for i in fromYear:
        sy.append(i)
      yearFilter = df.drop(columns=sy, axis=1)
      return yearFilter

    elif self.EndYear is not None:
      ToYear = range(self.EndYear + 1, 2021)
      ey = []
      for i in ToYear:
        ey.append(i)
      yearFilter = df.drop(columns=ey, axis=1)
      return yearFilter
    else:
      return df

  def FilterBySector(self, df):
    if self.sector is not None and self.gas is not None:
      filtered_df = df[(df['sector'] == self.sector) & (df['gas'] == self.gas)]
      filtered_df.reset_index(drop=True, inplace=True)
      return filtered_df
    elif self.sector is not None:
      filtered_df = df[df['sector'] == self.sector]
      filtered_df.reset_index(drop=True, inplace=True)
      return filtered_df
    elif self.gas is not None:
      filtered_df = df[df['gas'] == self.gas]
      filtered_df.reset_index(drop=True, inplace=True)
      return filtered_df

    else:
      return df


@app.route("/")
def myApp():
  return render_template('home.html')


@app.route("/filter_data", methods=["GET", "POST"])
def filter_data():
  print("running in filter_data")
  if request.method == "POST":
    print("running in post request")
    country = request.form.get("country")
    sector = request.form.get("sector")
    gas = request.form.get("gas")
    print("printing values")
    print(country, sector, gas)
    start_year = int(request.form.get("start_year"))
    start_year = int(start_year)
    end_year = int(request.form.get("end_year"))
    end_year = int(end_year)
    print(end_year, start_year)
    # fil = Filter(country, sector, gas, start_year, end_year)
    # i = fil.FilterByCountry(df)
    # j = fil.FilterBySector(i)
    # filtered_data = fil.FilterByYear(j)
    # print(filtered_data)
    fil = Filter("India", "Energy", None, 1990, 1995)

    i = fil.FilterByCountry(df)
    j = fil.FilterBySector(i)
    filtered_data = fil.FilterByYear(j)
    print(filtered_data)
    # Pass the filtered DataFrame to the template for rendering
    return render_template('home.html',
                           table=filtered_data.to_html(classes='data',
                                                       index=False))
  else:
    return render_template('home.html')


@app.route("/climate")
def climate():
  return render_template('climate.html',
                         tables=[df.to_html(classes='data')],
                         titles=df.columns.values)


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
