# 2023.11.19  10.00
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import requests 
import dash
import os
import time
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from mexc_crypto_api import crypto_candles_df

dash.register_page(__name__, name='Crypto Heatmap')

MyCryptos = ["BTCUSDT","ETHUSDT","BLZUSDT","BCHUSDT","FILUSDT","AXSUSDT","XRPUSDT","ADAUSDT","SOLUSDT",
"DOGEUSDT","EGLDUSDT","SHIBUSDT","ATOMUSDT","COMPUSDT","APTUSDT","FLOKIUSDT","MAGICUSDT","MANAUSDT",
"SANDUSDT","MATICUSDT","AVAXUSDT","LUNAUSDT","ETCUSDT","MKRUSDT","LUNCUSDT","OPUSDT","LINKUSDT"]

if (os.path.isfile('./data_files/crypto_heatmap.csv') == False or ((time.time() - os.path.getmtime('./data_files/crypto_heatmap.csv')) > 50000)):
    full_crypto_df = pd.DataFrame()
    for item in MyCryptos:
        mexc_klines_df = crypto_candles_df(item,60,972)[['opendate','close']]  #.iloc[:,[1,7,8,5]]
        mexc_klines_df['close'] = mexc_klines_df['close'].apply(pd.to_numeric, errors='coerce')
        mexc_klines_df['symbol'] = item
        mexc_klines_df['indexcol'] = mexc_klines_df.index
        full_crypto_df = pd.concat([full_crypto_df, mexc_klines_df], axis=0)
        full_crypto_df['date'] = pd.to_datetime(full_crypto_df['opendate']).dt.day_of_year
    full_crypto_df.to_csv('./data_files/crypto_heatmap.csv')
    #print('created again')
else:
    full_crypto_df = pd.read_csv('./data_files/crypto_heatmap.csv')
    #print('only loaded')

date_min = pd.to_datetime(full_crypto_df['opendate']).dt.day_of_year.min()
date_max = pd.to_datetime(full_crypto_df['opendate']).dt.day_of_year.max()

layout = dbc.Container([

 dbc.Row([
    html.Div('Crypto Heatmap (Correlations)', className="text-primary text-center fs-4")
     ]),

      dbc.Row([
        dbc.Col(  
            dbc.Card([
                html.H6('Crypto correlations by last 40 days'),
                dcc.RangeSlider(id='day_slider', min=0, max=date_max-date_min, value=[20, date_max-date_min],
                step=1,tooltip={'placement': 'top', 'always_visible': True} ),
            ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}),
        width=12) 
    ], style={'margin-top':'20px'}),  #width=4) 
    
    dbc.Row([ 
           dbc.Col(  
            dbc.Card([
                html.H6('Crypto heatmap for 20 cryptos'),
                dcc.Graph(id='crypto_heatmaps', config={'displayModeBar': False})
               ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}),
        width=12) 
    ], style={'margin-top':'20px'}),  #width=4) 


    ], fluid=True) # Fluid=True -> fit screen layout!


@callback(
    Output('crypto_heatmaps', 'figure'), Input('day_slider','value'))
def update_heatmap(sel_day):

    filtered_crypto_df = full_crypto_df.query(f'date >= {sel_day[0]+date_min} and date <= {sel_day[1]+date_min}')

    pivot_df = pd.pivot_table(filtered_crypto_df, index='indexcol', values='close',  columns='symbol').reset_index() #.unstack() #, 
    crypto_heatmap_df = pivot_df.drop('indexcol', axis=1).rename_axis(None, axis=1).corr().round(2)

    fig = px.imshow(crypto_heatmap_df, text_auto=True)

    fig.update_layout(height=900) #title_text="Subplots", width=1200 showlegend=False
    fig.update_layout(margin=dict(l=10, r=10, t=0, b=0, pad=0))

    return fig
