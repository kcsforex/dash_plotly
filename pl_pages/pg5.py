# 2023.11.05  15.00
import pandas as pd 
import pandas_ta as ta
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
import plotly.express as px

from mexc_crypto_api import mexc_allcryptos, mexc_futcryptos
  
dash.register_page(__name__, name='KCS Data Crypto')

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 5 and much more!'),
        #dcc.Graph(figure=html_bokeh)
    ]
)



