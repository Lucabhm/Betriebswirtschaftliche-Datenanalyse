#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import annotations
import pandas as pd


def fuel_yearly_avg_table(
    csv_path_fuel: str,
    start_year: int = 2019,
    end_year: int = 2024,
    sep: str = ";",
    decimal: str = ",",
    thousands: str = ".",
    encoding: str = "utf-8",
    print_table: bool = True,
) -> pd.DataFrame:
    # read raw csv
    raw = pd.read_csv(
        csv_path_fuel,
        sep=sep,
        header=0,
        decimal=decimal,
        thousands=thousands,
        skipinitialspace=True,
        encoding=encoding,
    )

    # month columns like "Dec-15", "Jan-16", ...
    month_cols = [
        col for col in raw.columns
        if isinstance(col, str) and "-" in col and col[:3].isalpha()
    ]

    # wide -> long
    id_vars = [
        "Regular Gasoline (LCU/liter)",
        "Country",
        "Country Code",
        "Original Units",
        "Converted Units",
        "Default MAP (1 to show)",
    ]

    long_df = raw.melt(
        id_vars=id_vars,
        value_vars=month_cols,
        var_name="Month",
        value_name="Price",
    )

    # parse month to datetime, drop invalid
    long_df["Date"] = pd.to_datetime(long_df["Month"], format="%b-%y", errors="coerce")
    long_df = long_df.dropna(subset=["Date"])

    # year + yearly average per country
    long_df["Year"] = long_df["Date"].dt.year
    yearly_avg = (
        long_df.groupby(["Country", "Country Code", "Year"], as_index=False)["Price"]
        .mean()
    )

    # filter years
    yearly_filtered = yearly_avg[(yearly_avg["Year"] >= start_year) & (yearly_avg["Year"] <= end_year)]

    # pivot to wide format (Year rows, Country columns)
    yearly_wide = (
        yearly_filtered.pivot(index="Year", columns="Country", values="Price")
        .sort_index()
    )

    if print_table:
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_colwidth", None)
        pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

        print(f"Average automotive gasoline price (per liter) by country and year ({start_year}–{end_year}):\n")
        print(yearly_wide)

    return yearly_wide

# In[ ]:




