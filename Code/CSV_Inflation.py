import pandas as pd

def inflation_yearly_table(csv_path, start_year, end_year):
    raw = pd.read_csv(
        csv_path,
        sep=",",
        decimal=".",
    )

    # nur Jahre, die wirklich als Spalten existieren
    year_cols = [
        str(year)
        for year in range(start_year, end_year + 1)
        if str(year) in raw.columns
    ]

    #raw zu neuem dataframe zusammensetzen
    df = raw.melt(
        id_vars=["country_name"],
        value_vars=year_cols,
        var_name="Year",
        value_name="Inflation",
    )

    #Errors streichen aus df
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Inflation"] = pd.to_numeric(df["Inflation"], errors="coerce")

    #df neu annordenen
    yearly = (
        df.groupby(["Year", "country_name"])["Inflation"]
          .mean()
          .unstack()
          .loc[start_year:end_year]
    )

    return yearly
