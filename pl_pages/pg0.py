# 2023.11.14  11.00
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path='/', name='Home') # '/' is home page


layout = dbc.Container([

            dbc.Row([ 
        #dcc.Markdown('# Life Expectancy Dashboard')
        html.Div('My experience & portfolios', className="text-primary text-center fs-4")
        ]),

        dbc.Row([
                dbc.Col([
                    dcc.Markdown('### KCS Bios')], width=12)
            ])
    ])


