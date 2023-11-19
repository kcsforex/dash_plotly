# 2023.11.14  16.00
import dash
from dash import dcc, html, callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, name='Fast Food Map USA') # '/' is home page

fastfood_df = pd.read_csv("./data_files/fastfood_restaurants_us.csv", index_col=0).drop('websites', axis=1)
#ddf = fastfood_df.query('province == "CA"')

layout = dbc.Container([

        dbc.Row([ 
            html.Div('Fast Food restaurant in USA Dashboard', className="text-primary text-center fs-4")
        ]),

        dbc.Row([
             
            dbc.Col([
                dbc.Card([
                    html.H6('Fast Food restaurant by province'),
                    dcc.Dropdown(options=fastfood_df['province'].unique(), id='prov-choice', value=['NY','TX', 'FL','CA'], multi=True)
                ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'})
            ], width=5),

            dbc.Col([
                dbc.Card([
                    html.H6('Fast Food restaurant by types'),
                    dcc.Dropdown(options=fastfood_df['name'].unique(),  id='cat-choice',  value=["Burger King","McDonald's","Wendy's"], multi=True)
                ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'})
            ], width=7)

        ], style={'margin-top':'20px'}),

        dbc.Row([

            dbc.Col([
                dbc.Card([  
                    dcc.Graph(id='fastfood_map', config={'displayModeBar': False})
                ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'})
            ], width=7),

            dbc.Col([
                dbc.Card([  
                    html.Div(id='fastfood-table', style={  'margin':'10px',"maxHeight": "400px", "overflow": "scroll"}), #scroll
                ], style={'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', "font-size": "12px"})
            ], width=5)

        ], style={'margin-top':'20px'})

    ])

@callback(
    Output('fastfood_map', 'figure'), Output('fastfood-table', 'children'),
    Input('prov-choice', 'value'),
    Input('cat-choice', 'value')
)
def update_graph(prov_value, cat_value):
    if prov_value is None or cat_value is None:
        raise PreventUpdate

    #ddf = fastfood_df.query('province == "CA"')
    fastfood_filtered_df = fastfood_df.query(f'province== {prov_value} and name == {cat_value}') # "" if single value with space
   
    fastfood_fig = go.Figure(go.Scattermapbox(
        lat=fastfood_filtered_df["latitude"], lon=fastfood_filtered_df["longitude"],
        mode='markers', marker=go.scattermapbox.Marker(size=5),
        text=fastfood_filtered_df['name'],
    ))

    fastfood_fig.update_layout(
        autosize=True, hovermode='closest',
        mapbox=dict(accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
        bearing=0,center=dict(lat=37.7,lon=-96.0), pitch=0,zoom=3))

    fastfood_fig.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=400, font_color="black", title_font_color="gray")
    fastfood_fig.update_layout(title_text=f'Fas Food Restaurant in USA', title_x=0.5, xaxis_title=None, font=dict(size=12))

    fastfood_table = dbc.Table.from_dataframe(fastfood_filtered_df.iloc[:, [1, 6, 8, 2, 0, 4, 5]], bordered=True, striped=True)
    
    return fastfood_fig, fastfood_table
