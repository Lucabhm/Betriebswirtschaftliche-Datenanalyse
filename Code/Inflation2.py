from __future__ import annotations
import pandas as pd


def inflation_yearly_table(
    csv_path_inflation: str,
    start_year: int = 2019,
    end_year: int = 2024,
    sep: str = ",",
    decimal: str = ".",
    thousands: str | None = None,
    encoding: str = "utf-8",
    indicator_contains: str = "consumer prices",
    print_table: bool = True,
) -> pd.DataFrame:

    raw = pd.read_csv(
        csv_path_inflation,
        sep=sep,
        decimal=decimal,
        thousands=thousands,
        encoding=encoding,
        skipinitialspace=True,
    )

    year_cols = [c for c in raw.columns if str(c).isdigit()]

    if indicator_contains:
        raw = raw[
            raw["indicator_name"]
            .astype(str)
            .str.contains(indicator_contains, case=False, na=False)
        ]

    wanted_years = [str(y) for y in range(start_year, end_year + 1)]
    existing_years = [y for y in wanted_years if y in raw.columns]

    long_df = raw.melt(
        id_vars=["country_name", "indicator_name"],
        value_vars=existing_years,
        var_name="Year",
        value_name="Inflation",
    )

    long_df["Year"] = pd.to_numeric(long_df["Year"], errors="coerce")
    long_df["Inflation"] = pd.to_numeric(long_df["Inflation"], errors="coerce")

    yearly_avg = (
        long_df.groupby(["country_name", "Year"], as_index=False)["Inflation"]
        .mean()
    )

    yearly_wide = yearly_avg.pivot(
        index="Year", columns="country_name", values="Inflation"
    ).sort_index()

    if print_table:
        print(yearly_wide)

    return yearly_wide
