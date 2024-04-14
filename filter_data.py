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
