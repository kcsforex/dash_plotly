# 2023.11.07  16.00
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, pages_folder="pl_pages", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

sidebar = dbc.Nav(
            [
                dbc.NavLink([
                    html.Div(page["name"] + '_', className="ms-2"),
    
                    ],  href=page["path"], active="exact"
            ) 
            for page in dash.page_registry.values()

            ],  vertical=True, pills=True, className="bg-light"
)


app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.Div("Python Multipage App with Dash", style={'fontSize':20, 'textAlign':'center'}))          
    ]),

    html.Hr(),

    dbc.Row([
            dbc.Col([
                sidebar, html.Img(src=app.get_asset_url('smoking2.jpg'))], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col([
                dash.page_container], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ])

], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=False)
   
