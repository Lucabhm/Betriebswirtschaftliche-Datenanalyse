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