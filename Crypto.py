import pandas as pd
import PySimpleGUI as sg
import plotly.graph_objects as go
import os

window1 = {'BACKGROUND': '#1c1c1c',
                'TEXT': 'white',
                'INPUT': 'lightgrey',
                'TEXT_INPUT': 'black',
                'SCROLL': 'white',
                'BUTTON': ('black', '#c0ff7d'),
                'PROGRESS': ('#000000', '#ffffff'),
                'BORDER': 0,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

sg.theme_add_new('Ardas_tema', window1)
sg.theme('Ardas_Tema')

#definerar filsökvägen för csv filen
data_dir = "C:/Users/ardas/Desktop/prog/CSV"
btc_csv = os.path.join(data_dir, "coin_Bitcoin.csv")
cdn_csv = os.path.join(data_dir, "coin_Cardano.csv")
dgc_csv = os.path.join(data_dir, "coin_Dogecoin.csv")
eth_csv = os.path.join(data_dir, "coin_Ethereum.csv")
sol_csv = os.path.join(data_dir, "coin_Solana.csv")
tet_csv = os.path.join(data_dir, "coin_Tether.csv")


#laddar csv filerna till pandas dataframe
btc = pd.read_csv(btc_csv)
cdn = pd.read_csv(cdn_csv)
dgc = pd.read_csv(dgc_csv)
eth = pd.read_csv(eth_csv)
sol = pd.read_csv(sol_csv)
tet = pd.read_csv(tet_csv)

#definerar listan av kryptovalutor och deras dataframes: https://chat.openai.com/
cryptos = {"Bitcoin" : btc, "Cardano" : cdn, "Dogecoin" : dgc, "Ethereum" : eth, "Solana" : sol, "Tether" : tet}

         
def plot_crypto(start_date, end_date, crypto_name):
    crypto_df = cryptos[crypto_name]
    # skapar en mask som filtrerar raderna som matchar med datum intervallet som användaren inmatat
    mask = (crypto_df["Date"] >= start_date) & (crypto_df["Date"] <= end_date)
    filtered_cryotp_df = crypto_df.loc[mask]

    fig = go.Figure(

        data= [
            #väljer vad x axeln ska inkludera
            go.Candlestick(
            x = filtered_cryotp_df["Date"],
            open = filtered_cryotp_df["Open"],
            high = filtered_cryotp_df["High"],
            close = filtered_cryotp_df["Close"],
            low = filtered_cryotp_df["Low"],

            ),

            go.Scatter(
            x=filtered_cryotp_df["Date"], 
            y=filtered_cryotp_df["Close"].rolling(window=10).mean(),
            mode = "lines",
            name = "medelpris",
            line= {"color": "#1900ff"}

            ),
        ]
    )
    fig.update_layout(
        title = f"Graf på {crypto_name}",
        xaxis_title = "Datum",
        yaxis_title = "Pris ($)",
        xaxis_rangeslider_visible = False
            )
    
    #visar valutan på y-axeln
    fig.update_yaxes(tickprefix = "$")

    fig.show()



#skapar en GUI med knappar och dropdown för att välja krypto och tidslinje
#fick ideen av listbox från "https://csveda.com/python-combo-and-listbox-with-pysimplegui/"
layout = [
    [sg.Text("välj en krypro valuta:"), sg.Combo(list(cryptos.keys()), key="crypto")],
    [sg.Text("Välj datum:")],
    [sg.CalendarButton("Från"), sg.Input(key="start_date", enable_events=True)],
    [sg.CalendarButton("Till"), sg.Input(key="end_date", enable_events=True)],
    [sg.Button("Visa graf"), sg.Button("Avsluta")]
]

window1 = sg.Window("Crypto marknad", layout)

while True:
    event, values = window1.Read()
    if event == sg.WIN_CLOSED:
        break
        
    elif event == "Visa graf":
        crypto_name = values["crypto"]
        start_date = values["start_date"]
        end_date = values["end_date"]

        if end_date > "2021-07-06":
            sg.popup("Du får inte välja ett datum senare än 2021-07-06 eller senare än slut datumet. Försök igen.")
        else:
            plot_crypto(start_date, end_date, crypto_name)

    if event == "Avsluta":
        break