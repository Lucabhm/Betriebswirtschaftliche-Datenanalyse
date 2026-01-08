import pandas as pd

def vergleich_laender():
    csv_path_Fuel = '../Datenbanken/Global_Fuel_Prices_Database(Reg Gasoline (below RON 95) USD).csv'
    csv_path_Europe = '../Datenbanken/Weekly_Oil_Bulletin_Prices_History_bearbeitet.csv'
    csv_path_Inflation = '../Datenbanken/global_inflation_data.csv'

    df = pd.read_csv(csv_path_Fuel, sep=";")
    de = pd.read_csv(csv_path_Europe, sep = ";")
    de = de.T
    di = pd.read_csv(csv_path_Inflation, sep=",")

    Länder = set(df['Country']).intersection(set(di['country_name'])).union(set(di['country_name']).intersection(set(de.index[1:])))
    Länder = sorted(Länder)
    return (Länder)
