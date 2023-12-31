# 2023.11.29  10.00
import requests
import pandas as pd
import pandas_ta as ta

def act_price(crypto_item):
    url_act_price = f'https://api.mexc.com//api/v3/ticker/price?symbol={crypto_item}'
    resp = requests.get(url_act_price)
    mexc_act_price_data = resp.json()
    mexc_act_price = pd.to_numeric(mexc_act_price_data['price'], errors='coerce')
    return mexc_act_price

# ---------- Mexc Candles data ----------
def crypto_candles_df(crypto_item, int_minute, limit): 
    url_mexc_klines = f'https://api.mexc.com/api/v3/klines?symbol={crypto_item}&interval={int_minute}m&limit={limit}'
    resp = requests.get(url_mexc_klines)
    mexc_data = resp.json()
    mexc_klines_full_df = pd.DataFrame(mexc_data, columns = ['opendate','open','high','low','close','volume','close_time','quate_asset_volume'])
    mexc_klines_df = mexc_klines_full_df.drop(['close_time','quate_asset_volume'], axis=1) 

    mexc_cols = ['open','high','low','close','volume']
    mexc_klines_df[mexc_cols] = mexc_klines_df[mexc_cols].apply(pd.to_numeric, errors='coerce')

    mexc_klines_df['opendate'] = pd.to_datetime(mexc_klines_df['opendate'], unit='ms') + pd.Timedelta('01:00:00')

    return mexc_klines_df

# ---------- Mexc EMA Candles data ----------
def crypto_ema_df(crypto_item):   
    return ta.ema(crypto_candles_df(crypto_item,1,150)['close'],  length=50)

# ---------- Mexc Spot Info data ----------
def mexc_allcryptos():

    url_mexc_info = "https://api.mexc.com/api/v3/exchangeInfo"
    resp = requests.get(url_mexc_info) #verify=False
    data = resp.json()
    mexc_allinfo_df = pd.DataFrame(data['symbols'], columns= ['symbol','status','baseAsset','baseAssetPrecision','quoteAsset','quoteAssetPrecision','maxQuoteAmount','fullName'])
    
    url_mexc_24h = 'https://api.mexc.com/api/v3/ticker/24hr'
    resp = requests.get(url_mexc_24h)
    mexc_data = resp.json()
    mexc_all24h_df = pd.DataFrame(mexc_data, columns = ['symbol','priceChange','priceChangePercent','prevClosePrice','lastPrice','highPrice','lowPrice','volume','quoteVolume'])    
    
    mexc_all_df  = mexc_all24h_df.merge(mexc_allinfo_df, how="left", on=["symbol"])
    mexc_all_df = mexc_all_df[['symbol','quoteAsset','priceChangePercent','prevClosePrice','lastPrice','highPrice','lowPrice','volume','quoteVolume','fullName']]
    
    mexc_all_cols = ['prevClosePrice','lastPrice','highPrice','lowPrice']
    mexc_all_df[mexc_all_cols] = mexc_all_df[mexc_all_cols].apply(pd.to_numeric, errors='coerce').round(5)
    mexc_all_cols = ['priceChangePercent','volume','quoteVolume']
    mexc_all_df[mexc_all_cols] = mexc_all_df[mexc_all_cols].apply(pd.to_numeric, errors='coerce').round(2)
 
    return  mexc_all_df


# ---------- Mexc Futures info data  ----------
def mexc_futcryptos():

    url_mexc_fut = 'https://contract.mexc.com/api/v1/contract/detail'
    resp = requests.get(url_mexc_fut)
    mexc_data = resp.json()
    mexc_fut_full_df = pd.DataFrame(mexc_data['data'],columns = ['symbol','baseCoin','quoteCoin','contractSize','minLeverage', 'maxLeverage','priceUnit','minVol', 'maxVol'])
    mexc_fut_full_df['symbol'] = [item.replace('_USDT','USDT') for item in mexc_fut_full_df['symbol']]
    mexc_fut_full_df = mexc_fut_full_df.query('maxLeverage >= 125')

    url_mexc_24h = 'https://api.mexc.com/api/v3/ticker/24hr'
    resp = requests.get(url_mexc_24h)
    mexc_data = resp.json()
    mexc_all24_df = pd.DataFrame(mexc_data, columns = ['symbol','priceChange','priceChangePercent','prevClosePrice','lastPrice','highPrice','lowPrice','volume','quoteVolume'])
    
    mexc_fut_df = mexc_fut_full_df.merge(mexc_all24_df, how="left", on=["symbol"])
    mexc_fut_df = mexc_fut_df[['symbol','quoteCoin','priceChange','priceChangePercent','prevClosePrice','lastPrice','highPrice','lowPrice','volume','quoteVolume']]
    
    mexc_fut_cols = ['priceChange','priceChangePercent','prevClosePrice','lastPrice','highPrice','lowPrice','volume','quoteVolume']
    mexc_fut_df[mexc_fut_cols] = mexc_fut_df[mexc_fut_cols].apply(pd.to_numeric, errors='coerce', axis=1).round(3)
    
    return mexc_fut_df
