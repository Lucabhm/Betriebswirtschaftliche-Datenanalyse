import pandas as pd

#Berechnung für ein Land: 
def _pearson_group (g: pd.DataFrame, min_n: int = 3) -> pd.Series:
    n = len(g)
    if n < min_n:
        return pd.Series({"n": n, "pearson": float("nan")})

    return pd.Series({
        "n": n,
        "pearson": g["GasolinePriceDiff"].corr(g["Inflation"])
    })

#Korrelation: 
def pearson_for_all_countries(res: pd.DataFrame, min_n: int = 3) -> pd.DataFrame:
    tmp = res[["Country", "GasolinePriceDiff", "Inflation"]].copy()
    tmp["GasolinePriceDiff"] = pd.to_numeric(tmp["GasolinePriceDiff"], errors="coerce")
    tmp["Inflation"] = pd.to_numeric(tmp["Inflation"], errors="coerce")
    tmp = tmp.dropna()

    out = (
        tmp.groupby("Country")
           .apply(_pearson_group, min_n=min_n)
           .reset_index()
    )
    return out