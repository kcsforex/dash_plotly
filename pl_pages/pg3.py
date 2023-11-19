# 2023.11.14  11.00
import pandas as pd 
import pandas_ta as ta
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
import plotly.express as px
import os
from datetime import datetime

from youtube_api import get_channel_stats, get_video_ids, get_video_details

youtube_channel_stat_df = get_channel_stats()[['channelName','subscribers','views','totalVideos']]
#youtube_channel_stat_df = youtube_channel_stat_df.sort_values(by=['subscribers'], ascending=False)

youtube_datafile = './data_files/all_youtube_videos.csv'
videos_full_df = pd.read_csv(youtube_datafile)
file_unixmoddate = os.path.getmtime(youtube_datafile) #getctime
file_moddate = datetime.fromtimestamp(file_unixmoddate)
  
dash.register_page(__name__, name='Youtube Data')

layout = dbc.Container([

    dbc.Row([
        html.Div('TOP 20 HUN YouTube Influencers Stats/Info', className="text-primary text-center fs-4")
    ]),

# --------------- 2. row, 1. col ---------------
    dbc.Row([ 

        dbc.Col([ 
        # ----- 2/1. container -----
            dbc.Card([
                html.H6('Select GroupBy'),
                dcc.RadioItems( options=[
                    {"label":" Subscribers", "value":'subscribers'},
                    {"label":" Total views", "value":'views'},
                    {"label":" Total videos", "value":'totalVideos'},
                ], id='youtube-radio1', value='subscribers')],
            style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', "height": "120px"}),
        
        # ----- 2/2. container -----
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H6('Data Source'),
                        dbc.Label("Youtube data source last updated: " f'{file_moddate}', style = {"color": "green","font-weight":"light",'display':'flex','justifyContent':'center'}),
                        ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', "height": "190px"})
                ])
            ],style={'margin-top':'10px'})

        ], width=2),

# --------------- 2. row, 2. col ---------------
        dbc.Col( 
            dbc.Card(  
                dcc.Graph(id='youtube-fig', figure=px.bar(youtube_channel_stat_df, x='channelName', y='subscribers'), config={'displayModeBar': False}),
                style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}), width=5),

# --------------- 2. row, 3. col ---------------
        dbc.Col( 
            dbc.Card( 
                html.Div( #dbc.Table.from_dataframe(youtube_channel_stat_df, bordered=True, striped=True)
                id='container-table1', style={  'margin':'10px',"maxHeight": "300px", "overflow": "auto"}), #scroll
                style= { 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px',"font-size": "12px"}),  width=5) #overflow=Auto, "maxHeight": "250px"            
   
    ], style={'margin-top':'20px'}),

# --------------- 3. row, 1. col ---------------
    dbc.Row([ 

        dbc.Col([ 
        # ----- 3/1. container -----    
            dbc.Card([
                html.H6('Select Param GroupBy'), 
                dcc.RadioItems( options=[
                    {"label":" View Count", "value":'viewCount'},
                    {"label":" Like Count", "value":'likeCount'},
                    {"label":" Comment Count", "value":'commentCount'},
                    {"label":" Video Duration", "value":'durationSecs'}
                ], id='youtube-radio2', value='viewCount')],
            style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', "height": "140px"}),
        
        # ----- 3/2. container -----
            dbc.Row([
                dbc.Col([             
                    dbc.Card([
                        html.H6('Select Youtube Channels'),
                        dcc.Dropdown(options=videos_full_df['channelTitle'].unique(),  id='youtube-dropdown2', value='UborCraft',  maxHeight=135)],
                        style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', "height": "220px"})
                ])
            ],style={'margin-top':'10px'})

        ], width=3),

# --------------- 3. row, 2. col ---------------

        dbc.Col( 
            dbc.Card( 
                html.Div(id='container-table2', style={  'margin':'10px',"maxHeight": "350px", "overflow": "scroll"}), #scroll
                style= { 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', "font-size": "12px"}),  width=9) #overflow=Auto, "maxHeight": "250px"            
   
    ], style={'margin-top':'20px'}),


], fluid=True)


@callback(
    Output('youtube-fig', 'figure'), Output('container-table1', 'children'), 
    Input('youtube-radio1', 'value'))
def update_graph(value):

    youtube_stat_df = youtube_channel_stat_df.sort_values(by=[value], ascending=False)
    youtube_stat_df['channelName'] = youtube_stat_df['channelName'].str[:15]

    youtube_stat_table = dbc.Table.from_dataframe(youtube_stat_df, bordered=True, striped=True)

    fig_channel_stat = px.bar(youtube_stat_df, x='channelName', y=value)
    fig_channel_stat.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=300, font_color="black", title_font_color="blue")
    fig_channel_stat.update_layout(title_text=f'Youtube Channel order by {value}', title_x=0.5, xaxis_title=None, font=dict(size=10))
    return fig_channel_stat, youtube_stat_table


@callback(
    Output('container-table2', 'children'), 
    Input('youtube-radio2', 'value'), Input('youtube-dropdown2', 'value'))
def update_graph2(value2r,value2d):

    videos_filter_df = videos_full_df.query(f'channelTitle == "{value2d}"').nlargest(50, value2r)
    #videos_filter_df = videos_full_df[videos_full_df.channelTitle == value2d].nlargest(50, value2r)
    return dbc.Table.from_dataframe(videos_filter_df, bordered=True, striped=True)



