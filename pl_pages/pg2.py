# 2023.11.14  17.00
import dash
from dash import dcc, html, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate

life_expectancy = pd.read_csv('./data_files/life_expectancy.csv').query('year >= 1950')
#life_expectancy['country'] = life_expectancy['country'].str[:15]
year_min = life_expectancy['year'].min()
year_max = life_expectancy['year'].max()

dash.register_page(__name__, name='Life Exp. Analysis')

layout = dbc.Container([

    dbc.Row([ 
    #dcc.Markdown('# Life Expectancy Dashboard')
    html.Div('Life Expectancy Dashboard', className="text-primary text-center fs-4")
    ]),

    dbc.Row([
        dbc.Col(  
            dbc.Card([
                html.H6('Life expectancy by date range'),
                dcc.RangeSlider(id='year_slider', min=year_min,max=year_max,value=[year_min+30, year_max], marks={i: str(i) for i in range(year_min, year_max+1, 10)},
                step=1,tooltip={'placement': 'top', 'always_visible': True} ),
                #html.Br(),
                html.H6('Life expectancy by country'),
                dcc.Dropdown(id='country-dropdown', options=life_expectancy['country'].unique(), value=['Hungary','Austria','United States'], multi=True)
            ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}),
        width=12) 
    ], style={'margin-top':'20px'}),  #width=4) 
        
    dbc.Row([

        dbc.Col(           
            dbc.Card([
            dcc.Graph(id='life-exp-graph', config={'displayModeBar': False})
            ], style={'padding':'10px','box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}), 
        width=8),

        dbc.Col( 
            dbc.Card( 
                html.Div(id='life-exp-table', style={  'margin':'10px',"maxHeight": "300px", "overflow": "scroll"}), #scroll
                style= { 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px',"font-size": "12px"}),  width=4) #overflow=Auto           
   
    ], style={'margin-top':'20px'}),

], fluid=True)

@callback(
    Output('life-exp-graph', 'figure'), Output('life-exp-table', 'children'),
    Input('country-dropdown', 'value'),
    Input('year_slider', 'value'))

def update_output(selected_country, selected_years):
    if selected_country is None:
        raise PreventUpdate

    #msk = (life_expectancy['country'].isin(selected_country)) & (life_expectancy['year'] >= selected_years[0]) & (life_expectancy['year'] <= selected_years[1])
    #life_expectancy_filtered = life_expectancy[msk]

    life_expectancy_filtered = life_expectancy.query(f'country in {selected_country} and year >= {selected_years[0]} and year <= {selected_years[1]}')

    line_fig = px.line(life_expectancy_filtered, x='year', y='life expectancy',  color='country')
    line_fig.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), height=300, xaxis_title=None, yaxis_title='Life expectancy (years)',)

    life_exp_table = dbc.Table.from_dataframe(life_expectancy_filtered, bordered=True, striped=True)

    return line_fig, life_exp_table

