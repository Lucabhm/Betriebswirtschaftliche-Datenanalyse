import pandas as pd

def fuel_yearly_avg_table(csv_path, start_year, end_year):
    raw = pd.read_csv(
        csv_path,
        sep=";",
        decimal=",",
        thousands=".",
    )

    month_cols = [
        col
        for col in raw.columns
        if "-" in col
    ]

    df = raw.melt(
        id_vars=["Country"],
        value_vars=month_cols,
        var_name="Month",
        value_name="Price",
    )

    df["Year"] = pd.to_datetime(df["Month"], format="%b-%y").dt.year

    yearly_avg = (
        df.groupby(["Year", "Country"])["Price"]
          .mean()
          .unstack()
          .loc[start_year:end_year]
    )

    return yearly_avg