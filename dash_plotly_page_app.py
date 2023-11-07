# 2023.11.07  16.00
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = px.data.gapminder()

app.layout = html.Div([

        dbc.Row([
                dbc.Col([
                    dcc.Dropdown(options=df.continent.unique(),  id='cont-choice')], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4)
            ]),

        dbc.Row([
                dbc.Col([
                    dcc.Graph(id='line-fig',
                    figure=px.histogram(df, x='continent',   y='lifeExp', histfunc='avg'))], width=12)
            ])
    ])

@callback(
    Output('line-fig', 'figure'),Input('cont-choice', 'value')
)
def update_graph(value):
    if value is None:
        fig = px.histogram(df, x='continent', y='lifeExp', histfunc='avg')
    else:
        dff = df[df.continent==value]
        fig = px.histogram(dff, x='country', y='lifeExp', histfunc='avg')
    return fig

if __name__ == "__main__":
    app.run_server(debug=False)
    #app.run(debug=True, use_reloader=True)
