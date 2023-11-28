# 2023.11.28  19.00
import pandas as pd
from binance.client import Client
import pandas_ta as ta
import config
import time
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Binance Crypto Charts')

client = Client(config.API_KEY, config.API_SECRET)
def GetKlines(CryptoSymbol):

    klines = client.get_klines(symbol=CryptoSymbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit='90')
    klines_full_df = pd.DataFrame(klines, columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quate_asset_volume', 'no_trades', 'base_asset_volume', 'quote_asset_volume', 'ignore'])
    klines_df = klines_full_df.loc[:,['date', 'open', 'high', 'low', 'close', 'volume']]
    klines_df['date'] = pd.to_datetime(klines_df['date'], unit='ms')
    for col in ['open', 'high', 'low', 'close','volume']: 
        klines_df[col] = pd.to_numeric(klines_df[col],errors='coerce')
    return klines_df

MyCryptoNames = ['BTCUSDT','ETHUSDT','COMPUSDT','FILUSDT','MKRUSDT','BCHUSDT','SOLUSDT','AVAXUSDT','SANDUSDT','MANAUSDT']
#'ETCUSDT','DOGEUSDT','AXSUSDT','APTUSDT','MASKUSDT','MAGICUSDT','OPUSDT','XRPUSDT','BNBUSDT','LTCUSDT']


layout = dbc.Container([

 dbc.Row([
    html.Div('Streaming Crypto Charts (Updated every 30sec)', className="text-primary text-center fs-4")
     ]),
    
    dbc.Row([ 
        dbc.Card( 
            html.Div(id='crypto-table', style={  'margin':'15px',"maxHeight": "400px", "overflow": "auto"}),
            style= { 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px',"font-size": "12px"}), #overflow=Auto           
        dcc.Interval(id='refresh-interval', interval=30000, n_intervals=0),
    ]),

    ], fluid=True)


@callback(Output('crypto-table', 'children'), Input('refresh-interval', 'n_intervals'))
def update_crypto_table(n_intervals):
    crypto_info = []  

    for crypto in MyCryptoNames:   

        klines_df = GetKlines(crypto) 
        M = 25
        # ---------- Smoothed H.Ashi ----------
        klines_df['o_ema'] = ta.ema(klines_df['open'],  length=M )
        klines_df['h_ema'] = ta.ema(klines_df['high'],  length=M )
        klines_df['l_ema'] = ta.ema(klines_df['low'],  length=M )
        klines_df['c_ema'] = ta.ema(klines_df['close'],  length=M )

        klines_df['low_sha'] = klines_df[['l_ema','o_ema','c_ema']].min(axis=1) 
        klines_df['high_sha'] = klines_df[['h_ema','o_ema','c_ema']].max(axis=1) 
 
        klines_df['sha_h'] = ta.ema(klines_df['high_sha'],  length=M)
        klines_df['sha_l'] = ta.ema(klines_df['low_sha'],  length=M)
     
        sha_min  = round(klines_df['sha_l'].iloc[-2],3)
        sha_max  = round(klines_df['sha_h'].iloc[-2],3)

        # ---------- Actual Open/Close ----------
        high_0 = klines_df["high"].iloc[-1]
        high_1 = klines_df["high"].iloc[-2]
        low_0 = klines_df["low"].iloc[-1]
        low_1 = klines_df["low"].iloc[-2]
        actual_price = round(float(client.get_symbol_ticker(symbol = crypto)['price']),3)
        
        if (actual_price < sha_min and (high_0 or high_1) >= sha_min):
            text = 'SELL position!'
            #send_to_telegram(Crypto + ' sell position! Act.price: '+ str(actual_price))
            #bot.send_message(chat_id=user_id, text=Crypto + ' sell position! Act.price: '+ str(actual_price))
        elif (actual_price > sha_max and (low_0 or low_1) <= sha_max):
            text = 'BUY position!'
            #send_to_telegram(Crypto+ ' buy position! Act.price: '+ str(actual_price))
            #bot.send_message(chat_id=user_id, text=Crypto+ ' buy position! Act.price: '+ str(actual_price))
            #order_succeeded = Crypto_Order('SIDE_SELL', 0.1, 'ETHUSDT', 'order_market_buy')
        else:
            text = 'Nothing to do'

        
        crypto_info.append({'Name':crypto, 'Action:':text, 'Price':actual_price, 'SHA_High':sha_max,'SHA_Low':sha_min})
        time.sleep(0.1)
    
    crypto_df = pd.DataFrame(crypto_info)
               
    crypto_table = dbc.Table.from_dataframe(crypto_df, bordered=True, striped=True)

    return crypto_table



