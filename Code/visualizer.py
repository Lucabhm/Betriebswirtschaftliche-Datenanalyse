import pandas as pd
import plotly.express as px
from typing import Optional, List

def diagramVisualizerOneParam(data: pd.DataFrame, title: str, yAxis: str, country: Optional[List[str]] = None, continent: Optional[List[str]] = None):
    if continent:
        filterData = data[data["Continent"].isin(continent)]
    else:
        filterData = data
    if country:
        filterData = filterData[filterData["Country"].isin(country)]
    fig = px.line(filterData, x='Year', y=yAxis, color='Country', title=title, markers=True, line_dash='Continent')
    fig.show()

def scatterPlotwithTrendline(data: pd.DataFrame, korrelation: pd.DataFrame, country: str = None):
    if country:
        filterData = data[data.Country == country]
        filterData = pd.merge(filterData, korrelation, on=["Country"], how="inner")
        fig = px.scatter(filterData, x="GasolinePriceDiff", y="Inflation", trendline="ols", hover_data="Year", title=f"Pearson Wert {korrelation.loc[korrelation["Country"] == country, "pearson"].values[0]}")
    else:
        filterData = data
        fig = px.scatter(filterData, x="GasolinePriceDiff", y="Inflation", trendline="ols", hover_data="Year")
    fig.show()


def minmax(s):
    mn, mx = s.min(), s.max()
    #falls alle werte gleich sind damit 0 rauskommt
    if mn == mx:
        return 0.0
    return (s - mn) / (mx - mn)

def diagramVisualizerGasolineVsInflationFacet(
    data,
    title,
    country=None,
    continent=None,
):
    df = data.copy()

    if continent:
        df = df[df["Continent"].isin(continent)]
    if country:
        df = df[df["Country"].isin(country)]

    df["Gasoline"]  = df.groupby("Country")["GasolinePrice"].transform(minmax)
    df["Inflation"] = df.groupby("Country")["Inflation"].transform(minmax)


    plot_df = df.melt(
    id_vars=["Year", "Country"],
    value_vars=["Gasoline", "Inflation"],
    var_name="Metric",
    value_name="Value",
    )
    
    fig = px.line(
        plot_df,
        x="Year",
        y="Value",
        color="Metric",
        facet_row="Country",
        markers=True,
        title=title,
    )

    fig.update_yaxes(range=[0, 1], title="Normalized (0–1)")
    fig.update_xaxes(title="Year")

    fig.show()
