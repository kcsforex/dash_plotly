# 2023.11.07  14.00
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests 
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Streaming Crypto Charts')

def crypto_candles_df(crypto_item): 
    url_mexc_klines = f'https://api.mexc.com/api/v3/klines?symbol={crypto_item}&interval=1m&limit=100'
    resp = requests.get(url_mexc_klines)
    mexc_data = resp.json()
    mexc_klines_full_df = pd.DataFrame(mexc_data, columns = ['opendate','open','high','low','close','volume','close_time','quate_asset_volume'])
    mexc_klines_df = mexc_klines_full_df.drop(['close_time','quate_asset_volume'], axis=1) 
    mexc_klines_df['opendate'] = pd.to_datetime(mexc_klines_df['opendate'], unit='ms') + pd.Timedelta('01:00:00')
    mexc_klines_df['opendate'] = mexc_klines_df['opendate'].dt.time.astype(str).str[:-3]

    candlestick = go.Candlestick(x=mexc_klines_df['opendate'], open=mexc_klines_df['open'], 
    high=mexc_klines_df['high'],low=mexc_klines_df['low'],close=mexc_klines_df['close']) #name=crypto_item)
    return candlestick

layout = dbc.Container([

 dbc.Row([
    html.Div('Streaming Crypto Charts (Updated every 30sec)', className="text-primary text-center fs-4")
     ]),
    
    dbc.Row([ 
        dcc.Graph(id='crypto_charts', config={'displayModeBar': False}),
        dcc.Interval(id='refresh-interval', interval=30000, n_intervals=0),
    ]),

    ], fluid=True)


@callback(Output('crypto_charts', 'figure'), Input('refresh-interval', 'n_intervals'))
def update_graph17(n_intervals):

    MyCryptoNames = [["BTCUSDT","ETHUSDT","BLZUSDT"],["BCHUSDT","FILUSDT","AXSUSDT"],["XRPUSDT","ADAUSDT","SOLUSDT"],["DOGEUSDT","MATICUSDT","AVAXUSDT"]]
    fig = make_subplots(rows=4, cols=3) 

    for i in range(1,5):
        for j in range(1,4): 
                        
            fig.append_trace(crypto_candles_df(MyCryptoNames[i-1][j-1]), row=i, col=j) 
            fig.add_annotation(xref="x domain",yref="y domain", text=MyCryptoNames[i-1][j-1], x=0.5, y=1.15, showarrow=False, row=i, col=j)

            fig.update_xaxes(rangeslider= {'visible':False}, row=i, col=j)

    fig.update_layout(height=900, width=1200, showlegend=False) #title_text="Subplots"
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=70, pad=0))
    fig.update_xaxes(nticks=10)

    #fig.for_each_annotation(lambda a: a.update(text = a.text + ': ' + MyCryptoNames[a.text]))
    #fig['layout']['xaxis{}'.format(i)]['title']='Label X axis 1'

    return fig
