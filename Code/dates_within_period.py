import pandas as pd

def Daten_im_Zeitraum_EU(Land):
    data_Fuel_Europe = '../Datenbanken/Weekly_Oil_Bulletin_Prices_History_bearbeitet.csv'
    data_Inflation = '../Datenbanken/global_inflation_data.csv'

    de = pd.read_csv(data_Fuel_Europe, sep = ";")
    di = pd.read_csv(data_Inflation, sep=",")

    Spalten = 'Consumer prices of petroleum products inclusive of duties and taxes'

    #Überprüfung nach fehlenden Daten in der Fuel_EU Datenbank
    if Land not in de.columns:
        return False
    Reihe = de[de.index >= 2] #Die Daten beginnen ab der 3. Zeile
    Reihe = Reihe[Reihe[Spalten].apply(lambda v: isinstance(v, str) and '.' in v and len(v) == 8 and v[-2:] in ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24'])] 
    #In dieser Datenbank ist das dAtum nicht als date, sondern als String eingetragen. Daher wird hier nach Zeilen, deren Wert ein String ist, einen Punkt enthält, Länge 8 hat und auf 19–
    #"v" =  der Inhalt in den Datumszeilen
    #"lamdbda" =  gibt nur True/False von v wieder
    #"v: isinstance(v, str)" = überrpüft ob v ein String ist
    #"and in '.' in v and len(v) == 8": überprüft ob der String eine Punkt hat und exakt 8 Zeichen lang ist
    if Reihe.empty:
        return False

    Zeitraum = Reihe[Land]

    if (Zeitraum.notna().all().all() == False):
        #print(Land + ": Missing data between 2019-2024 in Europe Fuel Price Database")
        #print(Zeitraum[Zeitraum.isna()])
        return False
    #Überprüfung Ende
    
    #Überprüfung nach fehlenden Daten in der Inflation Datenbank
    Reihe = di[di['country_name'] == Land]
    if Reihe.empty:
        return False
    Spalten = [col for col in di.columns if any(jahr in col for jahr in ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'])]

    Zeitraum = Reihe[Spalten]

    if (Zeitraum.notna().all().all() == False):
        # print (Land + ": Missing data between 2019-2024 in Global Inflation Database")
        return False
    #Überprüfung Ende
    return True

def Daten_im_Zeitraum(Land):
    data_Fuel_World = '../Datenbanken/Global_Fuel_Prices_Database(Reg Gasoline (below RON 95) USD).csv'
    data_Inflation = '../Datenbanken/global_inflation_data.csv'

    df = pd.read_csv(data_Fuel_World, sep=";")
    di = pd.read_csv(data_Inflation, sep=",")


    #Überprüfung nach fehlenden Daten in der Fuel_World Datenbank
    Reihe = df[df['Country'] == Land]
    if Reihe.empty:
        #Falls keine Daten des Landes in der Datenbank Fuel_World ist, dann überprüft ob die Daten in Fuel_EU liegen
        x = Daten_im_Zeitraum_EU(Land)
        return x
    Spalten = [col for col in df.columns if any(jahr in col for jahr in ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'])]

    Zeitraum = Reihe[Spalten] #Reihe = das Land, Spalte = die Jahre 2019-2024

    if (Zeitraum.notna().all().all() == False): #Falls eine Zeile in dem Zeitraum für das Land leer ist, gibt er falsch zurück
        # print (Land + ": Missing data between 2019-2024 in Global Fuel Price Database")
        return False
    #Überprüfung Ende

    #Überprüfung nach fehlenden Daten in der Inflation Datenbank
    Reihe = di[di['country_name'] == Land]
    if Reihe.empty:
        return False
    Spalten = [col for col in di.columns if any(jahr in col for jahr in ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'])]

    Zeitraum = Reihe[Spalten]

    if (Zeitraum.notna().all().all() == False):
        # print (Land + ": Missing data between 2019-2024 in Global Inflation Database")
        return False
    #Überprüfung Ende
    
    return True
