#!/usr/bin/env python
# coding: utf-8

# In[3]:


from __future__ import annotations
import pandas as pd

GAS_LABEL = "Gas oil automobile Automotive gas oil Dieselkraftstoff (I)"
EURO_LABEL = "Euro-super 95 (I)"


def gasolineEU_yearly_filtered_table(
    csv_path_fuel: str,
    start_year: int = 2019,
    end_year: int = 2024,
    sep: str = ";",
    decimal: str = ",",
    thousands: str = ".",
    print_table: bool = True,
) -> pd.DataFrame:
    raw = pd.read_csv(
        csv_path_fuel,
        sep=sep,
        header=[0, 1, 2],
        decimal=decimal,
        thousands=thousands,
        skipinitialspace=True,
    )

    def _normalise(text: str | float | int | None) -> str:
        if not isinstance(text, str):
            return ""
        return " ".join(text.strip().split())

    raw.columns = pd.MultiIndex.from_tuples(
        tuple(_normalise(level) for level in col) for col in raw.columns
    )

    # find date column (3rd level == "Date")
    date_col = next(col for col in raw.columns if col[2] == "Date")
    dates = pd.to_datetime(
    raw[date_col],
    format="%d.%m.%y",
    errors="coerce",
    )

    mask = dates.notna()
    raw = raw.loc[mask]
    dates = dates.loc[mask]

    data: dict[str, pd.Series] = {"Date": dates}

    current_entity = ""
    rename_overrides = {
        "EU_price_with_tax_euro95": "European Union",
        "EUR_price_with_tax_euro95": "Euro Area",
    }

    # build per-liter diesel series per entity
    for column in raw.columns:
        top_level, product, _unit = column

        # track entity based on euro95 columns
        if product == EURO_LABEL and top_level not in {"", "CTR"}:
            current_entity = top_level

        # pick diesel columns and map them to the last seen entity (or itself)
        if product == GAS_LABEL and top_level not in {"", "CTR"}:
            label_source = current_entity or top_level
            entity_label = rename_overrides.get(label_source, label_source)

            prices_per_1000l = pd.to_numeric(raw[column], errors="coerce")
            data[entity_label] = prices_per_1000l / 1000.0  # convert to per liter

    gasolineEU_df = pd.DataFrame(data).set_index("Date").sort_index()

    # yearly average
    yearly = gasolineEU_df.resample("YE").mean()

    # make index like 2019, 2020, ... (same vibe as your other output)
    yearly.index = yearly.index.year
    yearly.index.name = "Year"

    # filter 2019–2024
    filtered = yearly.loc[start_year:end_year]

    if print_table:
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_colwidth", None)
        pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

        print(f"Average automotive diesel price (per liter) by country and year ({start_year}–{end_year}):\n")
        print(filtered)

    return filtered

# In[ ]:




