import pandas as pd

def Daten_im_Zeitraum_EU(Land):
    csv_path_Europe = '../Datenbanken/Weekly_Oil_Bulletin_Prices_History_bearbeitet.csv'
    csv_path_Inflation = '../Datenbanken/global_inflation_data.csv'

    de = pd.read_csv(csv_path_Europe, sep = ";")
    di = pd.read_csv(csv_path_Inflation, sep=",")

    Spalten = 'Consumer prices of petroleum products inclusive of duties and taxes'
    
    if Land not in de.columns:
        return False
    Reihe = de[de.index >= 2]
    Reihe = Reihe[Reihe[Spalten].apply(lambda v: isinstance(v, str) and '.' in v and len(v) == 8 and v[-2:] in ['19', '20', '21', '22', '23', '24'])]
    if Reihe.empty:
        return False

    Zeitraum = Reihe[Land]

    if (Zeitraum.notna().all().all() == False):
        # print(Land + ": Missing data between 2019-2024 in Europe Fuel Price Database")
        #print(Zeitraum[Zeitraum.isna()])
        return False

    Reihe = di[di['country_name'] == Land]
    if Reihe.empty:
        return False
    Spalten = [col for col in di.columns if any(jahr in col for jahr in ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'])]

    Zeitraum = Reihe[Spalten]

    if (Zeitraum.notna().all().all() == False):
        # print (Land + ": Missing data between 2019-2024 in Global Inflation Database")
        return False 
    return True

def Daten_im_Zeitraum(Land):
    csv_path_Fuel = '../Datenbanken/Global_Fuel_Prices_Database(Reg Gasoline (below RON 95) USD).csv'
    csv_path_Inflation = '../Datenbanken/global_inflation_data.csv'

    df = pd.read_csv(csv_path_Fuel, sep=";")
    di = pd.read_csv(csv_path_Inflation, sep=",")


    Reihe = df[df['Country'] == Land]
    if Reihe.empty:
        x = Daten_im_Zeitraum_EU(Land)
        return x
    Spalten = [col for col in df.columns if any(jahr in col for jahr in ['19', '20', '21', '22', '23', '24'])]

    Zeitraum = Reihe[Spalten]

    if (Zeitraum.notna().all().all() == False):
        # print (Land + ": Missing data between 2019-2024 in Global Fuel Price Database")
        return False

    Reihe = di[di['country_name'] == Land]
    if Reihe.empty:
        return False
    Spalten = [col for col in di.columns if any(jahr in col for jahr in ['2019', '2020', '2021', '2022', '2023', '2024'])]

    Zeitraum = Reihe[Spalten]

    if (Zeitraum.notna().all().all() == False):
        # print (Land + ": Missing data between 2019-2024 in Global Inflation Database")
        return False 
    return True
