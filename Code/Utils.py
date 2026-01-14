import pandas as pd

def mergeDf(gasolineDf: pd.DataFrame, gasolineEUDf: pd.DataFrame, inflation: pd.DataFrame, continents: dict):
    gasolineDfLong = gasolineDf.reset_index().melt(id_vars="Year", var_name="Country", value_name="GasolinePrice")
    gasolineEUDfLong = gasolineEUDf.reset_index().melt(id_vars="Year", var_name="Country", value_name="GasolinePrice")

    inflation = inflation.rename(columns={"country_name": "Country"})
    inflationLong = inflation.reset_index().melt(id_vars="Year", var_name="Country", value_name="Inflation")

    combinedGasoline = pd.concat([gasolineDfLong, gasolineEUDfLong], ignore_index=True)

    res = pd.merge(combinedGasoline, inflationLong, on=["Country", "Year"], how="inner")

    countryToContinent = {
        country: continent
        for continent, countries in continents.items()
        for country in countries
    }

    res["Continent"] = res["Country"].map(countryToContinent)

    return res

def diffGasoline(data: pd.DataFrame):
    data["GasolinePriceDiff"] = data.groupby("Country")["GasolinePrice"].pct_change() * 100