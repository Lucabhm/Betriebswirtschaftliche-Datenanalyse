import pandas as pd

EURO_LABEL = "Euro-super 95  (I)"

def gasolineEU_yearly_filtered_table(csv_path, start_year, end_year):
    
    raw = pd.read_csv(
        csv_path,
        sep=";",
        header=[0, 1, 2],
        decimal=",",
        thousands=".",
    )

    #falls kaputt geht hier Euro_label whitespaces trimmen
    
    #Datum Spalte finden und zu richtigem Datum parsen
    date_column = next(col for col in raw.columns if col[2] == "Date")
    dates = pd.to_datetime(raw[date_column], format="%d.%m.%y", errors="coerce")

    #invalid rows rausfiltern
    valid_rows = dates.notna()
    raw = raw.loc[valid_rows]
    dates = dates.loc[valid_rows]

    # EURO_LABEL spalte finden und leere/CTR spalten rausfiltern
    super95_columns = [
        col for col in raw.columns
        if col[1] == EURO_LABEL and col[0] not in {"", "CTR"}
    ]

    #Werte zu float umwandeln und auf preis pro L umrechnen
    prices = raw[super95_columns].apply(pd.to_numeric, errors="coerce") / 1000.0
    prices.index = dates
    #Zeile heist jetzt nur noch col[0]
    prices.columns = [col[0] for col in super95_columns]

    #mean berechnet mittelwert pro Jahr
    yearly_prices = prices.resample("YE").mean()
    yearly_prices.index = yearly_prices.index.year
    yearly_prices.index.name = "Year"

    return yearly_prices.loc[start_year:end_year]




