import pandas as pd

def vergleich_laender():
    data_Fuel_World = '../Datenbanken/Global_Fuel_Prices_Database(Reg Gasoline (below RON 95) USD).csv'
    data_Fuel_Europe = '../Datenbanken/Weekly_Oil_Bulletin_Prices_History_bearbeitet.csv'
    data_Inflation = '../Datenbanken/global_inflation_data.csv'

    dw = pd.read_csv(data_Fuel_World, sep=";")
    de = pd.read_csv(data_Fuel_Europe, sep = ";")
    de = de.T
    di = pd.read_csv(data_Inflation, sep=",")
    
    #set:Erzeugt eine Menge aus den gesuchten Spalten der Datenbanken, in dem Fall der Name der Länder
    #intersection: Wählt nur Länder aus, die in beiden Datenbanken sich überschneiden und erstelt somit eine Schnittmenge
    #union: Vereint die Schnittmengen aus Inflation-Fuel_World und Inflation-Fuel_EU
    #index[1:]: Beim Datensatz EU-Weekly-Oil-Prices, fangen die Daten erst in der 2. Spalte an, die erste Zeile wird so übersprungen
    Länder = set(dw['Country']).intersection(set(di['country_name'])).union(set(di['country_name']).intersection(set(de.index[1:])))
    Länder = sorted(Länder)
    return (Länder)
