# 2023.11.07  14.00
import random 
import time

import requests 
import pandas as pd 
import pandas_ta as ta

import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
import plotly.express as px

#  py dash_plotly_sandbox.py

from mexc_crypto_api import crypto_candles_df, crypto_ema_df, mexc_allcryptos, mexc_futcryptos
M = 49

# ----- Mexc Candles graph -----
def crypto_chart(crypto_item):

    return go.Candlestick(x=crypto_candles_df(crypto_item)[M:]['opendate'], 
        open=crypto_candles_df(crypto_item)[M:]['open'], 
        high=crypto_candles_df(crypto_item)[M:]['high'],
        low=crypto_candles_df(crypto_item)[M:]['low'],
        close=crypto_candles_df(crypto_item)[M:]['close'])

def crypto_chart_ind(crypto_item): 
    return go.Scatter(x=crypto_candles_df(crypto_item)['opendate'][M:],  
                      y=crypto_ema_df(crypto_item)[M:], 
                      name="EMA_50", line=dict(color="blue"))

# ----- Mexc Spot Info graph -----
data_spot = mexc_allcryptos().query("quoteAsset == 'USDT'").nlargest(30, "priceChangePercent")
data_spot['symbol'] = data_spot['symbol'].str.replace('USDT', '')
fig_spot = px.bar(data_spot, x='symbol', y='priceChangePercent')
fig_spot.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=300, font_color="black", title_font_color="red", legend_title_font_color="green")
fig_spot.update_layout(title_text='TOP 30 SPOT Cryptos', title_x=0.5)
fig_spot.update_layout(xaxis_title=None, yaxis_title="SPOT Cryptos (%)", font=dict(size=10))

# ----- Mexc Future Info graph -----  
data_fut = mexc_futcryptos().query("quoteCoin == 'USDT'").nlargest(30, "priceChangePercent")
data_fut['symbol'] = data_fut['symbol'].str.replace('USDT', '')
fig_fut = px.bar(data_fut, x='symbol', y='priceChangePercent')
     
fig_fut.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=300, font_color="black", title_font_color="red", legend_title_font_color="green")
fig_fut.update_layout(title_text='TOP 30 FUT Cryptos', title_x=0.5)
fig_fut.update_layout(xaxis_title=None, yaxis_title="Fut. Cryptos (%)", font=dict(size=10))

# ----- Mexc 4 Crypto groups for graphs -----  
CryptoGroup1 = ["BTCUSDT","MKRUSDT","BCHUSDT","BNBUSDT","LTCUSDT","COMPUSDT","EGLDUSDT","QNTUSDT"]
CryptoGroup2 = ["ETHUSDT","ETCUSDT","FILUSDT","XMRUSDT","LINKUSDT","ICPUSDT","ATOMUSDT","APTUSDT"]
CryptoGroup3 = ["SOLUSDT","OPUSDT","FILUSDT","ETCUSDT","AVAXUSDT","XRPUSDT","MATICUSDT","MAGICUSDT"]
CryptoGroup4 = ["BLZUSDT","SHIBUSDT","ETCUSDT","AXSUSDT","DOGEUSDT","MEMEUSDT","AVAXUSDT","LUNCUSDT"]

dash.register_page(__name__, name='TOP 25 Crypto')

layout = dbc.Container([

    dbc.Row([
        html.Div('TOP 25 SPOT & Futures Crypto Info', className="text-primary text-center fs-4")
    ]),

    dbc.Row([    
        dbc.Col( 
            dbc.Card(
            [
                dcc.Dropdown(id = "dropdown_crypto1", options=[{'label': i, 'value': i} for i in CryptoGroup1], value=CryptoGroup1[0]), 
                dcc.Graph(id='graph1', config={'displayModeBar': False})
            ], className = 'card-text',  style={'padding':'15px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'15px'}), width=3), 
            #'margin':'15px','margin-left':'15px','backgroundColor':'ivory'         
        dbc.Col( 
            dbc.Card(
            [
                dcc.Dropdown(id = "dropdown_crypto2", options=[{'label': i, 'value': i} for i in CryptoGroup2], value=CryptoGroup2[0]), 
                dcc.Graph(id='graph2', config={'displayModeBar': False})
            ], className = 'card-text',  style={'padding':'15px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'15px'}), width=3),
        dbc.Col( 
            dbc.Card(
            [
                dcc.Dropdown(id = "dropdown_crypto3", options=[{'label': i, 'value': i} for i in CryptoGroup3], value=CryptoGroup3[2]), 
                dcc.Graph(id='graph3', config={'displayModeBar': False})
            ], className = 'card-text',  style={'padding':'15px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'15px'}),width=3),
        dbc.Col( 
            dbc.Card(
            [
                dcc.Dropdown(id = "dropdown_crypto4", options=[{'label': i, 'value': i} for i in CryptoGroup4], value=CryptoGroup4[3]), 
                dcc.Graph(id='graph4', config={'displayModeBar': False})
            ], className = 'card-text',  style={'padding':'15px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'15px'}),width=3)
    ], style={'margin-top':'20px'}),

    dbc.Row([   
        dbc.Col( 
            dbc.Card(  
                dcc.Graph(figure=fig_spot, config={'displayModeBar': False}),
                style={'padding':'15px','box-shadow': '5px 5px 5px gray', 'borderRadius':'15px'}), width=6),
        dbc.Col( 
            dbc.Card( 
                html.Div(dbc.Table.from_dataframe(data_spot, bordered=True, striped=True), style={  'margin':'15px',"maxHeight": "300px", "overflow": "auto"}), #scroll
                style= { 'box-shadow': '5px 5px 5px gray', 'borderRadius':'15px',"font-size": "12px"}),  width=6) #overflow=Auto, "maxHeight": "250px"            
    ], style={'margin-top':'20px'}),

    dbc.Row([   
        dbc.Col( 
            dbc.Card(  
                dcc.Graph(figure=fig_fut, config={'displayModeBar': False}),
                style={'padding':'15px','box-shadow': '5px 5px 5px gray', 'borderRadius':'15px'}), width=6),
        dbc.Col( 
            dbc.Card( 
                html.Div(dbc.Table.from_dataframe(data_fut, bordered=True, striped=True), style={  'margin':'15px',"maxHeight": "300px", "overflow": "auto"}), #scroll
                style= { 'box-shadow': '5px 5px 5px gray', 'borderRadius':'15px',"font-size": "12px"}),  width=6) #overflow=Auto, "maxHeight": "250px"            
    ], style={'margin-top':'20px'}),

], fluid=True) #className="g-0", className="pad-row"

@callback(
    Output('graph1', 'figure'), Input(component_id='dropdown_crypto1', component_property='value'))
def update_graph1(value):
    fig = go.Figure(data=[crypto_chart(value)])
    fig.add_trace(crypto_chart_ind(value))
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=300, xaxis_rangeslider_visible=False, showlegend=False)
    fig.update_xaxes(nticks=10)
    return fig

@callback(
    Output('graph2', 'figure'), Input(component_id='dropdown_crypto2', component_property='value'))
def update_graph2(value):
    fig = go.Figure(data=[crypto_chart(value)])
    fig.add_trace(crypto_chart_ind(value))
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=300, xaxis_rangeslider_visible=False, showlegend=False)
    fig.update_xaxes(nticks=10)
    return fig

@callback(
    Output('graph3', 'figure'), Input(component_id='dropdown_crypto3', component_property='value'))
def update_graph3(value):
    fig = go.Figure(data=[crypto_chart(value)])
    fig.add_trace(crypto_chart_ind(value))
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=300, xaxis_rangeslider_visible=False, showlegend=False)
    fig.update_xaxes(nticks=10)
    return fig

@callback(
    Output('graph4', 'figure'), Input(component_id='dropdown_crypto4', component_property='value'))
def update_graph4(value):
    fig = go.Figure(data=[crypto_chart(value)])
    fig.add_trace(crypto_chart_ind(value))
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=300, xaxis_rangeslider_visible=False, showlegend=False)
    fig.update_xaxes(nticks=10)
    return fig



