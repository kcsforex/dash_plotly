# 2023.11.18  19.00
from dash import Dash, dcc, html, callback, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score

dash.register_page(__name__, name='Random Forest')

# ---------------------
wine_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/winequality-red.csv')
quality_label = LabelEncoder()
wine_df['quality'] = quality_label.fit_transform(wine_df['quality'])
X1 = wine_df.drop('quality', axis = 1)
y1 = wine_df['quality']
#print(wine_df.columns)

# ---------------------
housing_df = pd.read_csv('../KCS_Flask/data_files/housing.csv', nrows=1000)
#read_csv(..., skiprows=1000000, nrows=999999)
from sklearn.impute import KNNImputer
housing_df_temp = housing_df.copy()
columns_list = [col for col in housing_df_temp.columns if housing_df_temp[col].dtype != 'object']
new_column_list = [col for col in housing_df_temp.loc[:, housing_df_temp.isnull().any()]]
housing_df_temp = housing_df_temp[new_column_list]

knn = KNNImputer(n_neighbors = 3)
knn.fit(housing_df_temp)
array_values = knn.transform(housing_df_temp)
housing_df_temp = pd.DataFrame(array_values, columns = new_column_list)
for column_name in new_column_list:
    housing_df[column_name] = housing_df_temp.replace(housing_df[column_name],housing_df[column_name])

housing_df['rooms_per_household'] = housing_df['total_rooms']/housing_df['households']
housing_df['bedrooms_per_room'] = housing_df['total_bedrooms']/housing_df['total_rooms']
housing_df['population_per_household']= housing_df['population']/housing_df['households']
housing_df['coords'] = housing_df['longitude']/housing_df['latitude']

housing_df = housing_df.drop('total_rooms', axis=1)
housing_df = housing_df.drop('households', axis=1)
housing_df = housing_df.drop('total_bedrooms', axis=1)
housing_df = housing_df.drop('population', axis=1)
housing_df = housing_df.drop('longitude', axis=1)
housing_df = housing_df.drop('latitude', axis=1)

#housing_df["ocean_proximity"].value_counts()
#housing_df_encoded = pd.get_dummies(data=housing_df, columns=['ocean_proximity'])
#housing_df_encoded.columns = [c.lower().replace(' ', '_').replace('<', '_') for c in housing_df_encoded.columns]

X2 = housing_df[['housing_median_age', 'median_income','bedrooms_per_room','population_per_household','coords']]
y2 = housing_df['median_house_value']

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = dbc.Container([

    dbc.Row([
        #html.H1('Scikit-Learn with Dash', style={'textAlign': 'center'}),
        html.Div('Scikit-Learn with RandomForest', className="text-primary text-center fs-4")
    ]),
		
    dbc.Row([
         
        dbc.Col([       
		dbc.Card([ 
            html.Div([
                html.H6('Select Test Size:'), dcc.Input(value=0.3, type='number', debounce=True, id='test-size1', min=0.1, max=0.9, step=0.1),
            	html.H6("R.Forest n_est:"), dcc.Input(value=150, type='number', debounce=True, id='nestimator-size1', min=10, max=200, step=10),
                html.H6("Acc. Score:"), html.Div(id='placeholder1', style={'color':'red'}, children="")
            ])       
		], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', 'height': '200px'}),
        ], width=2),

        dbc.Col([       
		dbc.Card([ 
            html.Div([
                html.H6('R.ForestClassifier Actual/Predicted diff.'),
                dcc.Graph(id="wine-graph-class", config={'displayModeBar': False}),
            ])       
		], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', 'height': '200px'}),
        ], width=4),

        dbc.Col([       
		dbc.Card([
            html.Div([
                html.H6('Select Test Size:'), dcc.Input(value=0.2, type='number', debounce=True, id='test-size2', min=0.2, max=0.9, step=0.1),    
                html.H6("R.Forest n_est:"), dcc.Input(value=150, type='number', debounce=True, id='nestimator-size2', min=10, max=200, step=10),    
                html.H6("R2 Score:"), html.Div(id='placeholder2', style={'color':'red'}, children="")
            ])               
		], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', 'height': '200px'}),      
        ], width=2),

        dbc.Col([       
		dbc.Card([ 
            html.Div([
                html.H6('R.ForestRegressor Actual/Predicted diff.'),
                dcc.Graph(id="house-graph-regress", config={'displayModeBar': False}),
            ])       
		], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px', 'height': '200px'}),
        ], width=4),	
			
    ], style={'margin-top':'20px'}),     

    dbc.Row([	
         
        dbc.Col([
            dbc.Card([
                dcc.Dropdown(id='wine-dropdown', options=wine_df.columns, value='fixed acidity'),
            	dcc.Graph(id="wine-graph-hist", config={'displayModeBar': False}),
            ], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}), 
        ], width=6),
              		
        dbc.Col([
            dbc.Card([
                dcc.Dropdown(id='house-dropdown', options=housing_df.columns, value='median_income'),
            	dcc.Graph(id="house-graph-hist", config={'displayModeBar': False}),
            ], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}), 
        ], width=6)	

    ], style={'margin-top':'20px'}),
		
    dbc.Row([
         
        dbc.Col([
            dbc.Card([
                html.Div(dbc.Table.from_dataframe(wine_df, bordered=True, striped=True), style= {"font-size": "12px", "maxHeight":"350px", "overflow": "scroll"})
            ], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}) 
   	    ], width=6), 

        dbc.Col([
            dbc.Card([
                html.Div(dbc.Table.from_dataframe(housing_df[:100], bordered=True, striped=True), style={"font-size":"12px", "maxHeight":"350px", "overflow": "scroll"})
            ], style={'padding':'10px', 'box-shadow': '5px 5px 5px gray', 'borderRadius':'10px'}) 
   	    ], width=6),    

    ], style={'margin-top':'20px'})


], fluid=True)


# ---------- Wine df hist ----------
@callback(
    Output("wine-graph-hist", "figure"),
    Input("wine-dropdown", "value"))
def wine_hist(wine_val):
    fig=px.histogram(wine_df, wine_val, histfunc='avg')
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), yaxis_title=f'Avg. of {wine_val}', height=350)
    return fig

# ---------- House df hist ----------
@callback(
    Output("house-graph-hist", "figure"),
    Input("house-dropdown", "value"))
def house_hist(house_val):
    fig=px.histogram(housing_df, house_val, histfunc='avg')
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10, pad=10), yaxis_title=f'Avg. of {house_val}',height=350)
    return fig

# ---------- RandomForestClassifier ----------
@callback(
    Output("wine-graph-class", "figure"),
	Output('placeholder1', 'children'),
	Input('test-size1', 'value'),
	Input('nestimator-size1', 'value'))
def update_randomforest_class(test_size_value, nestimator_value):
    X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size=test_size_value, random_state=2)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)
     
    rfc = RandomForestClassifier(n_estimators=nestimator_value)
    rfc.fit(X_train, y_train)
    pred_rfc = rfc.predict(X_test)
    score_rfc = accuracy_score(y_test, pred_rfc)

    rfc_pred_test_df = pd.DataFrame({'Actual': y_test, 'Predicted': pred_rfc})
    rfc_pred_test_df['diff'] = (rfc_pred_test_df['Predicted'] / rfc_pred_test_df['Actual'] -1) * 100
    fig=px.histogram(rfc_pred_test_df, x='diff', range_x=[-100, 100], nbins=200, color_discrete_sequence=['indianred'])
    fig.update_layout(margin=dict(l=10, r=10, t=0, b=0, pad=0), height=150)

    return fig, score_rfc.round(3) 

# ---------- RandomForestRegressor ----------
@callback(
    Output("house-graph-regress", "figure"),
	Output('placeholder2', 'children'),
	Input('test-size2', 'value'),
	Input('nestimator-size2', 'value'))
def update_randomforest_regressor(test_size_value, nestimator_value):
    X_train, X_test, y_train, y_test = train_test_split(X2, y2, test_size=test_size_value, random_state=42, shuffle=True)
    
    rf_model = RandomForestRegressor(n_estimators=nestimator_value,random_state=10)
    rf_model.fit(X_train, y_train)
    pred_rfr = rf_model.predict(X_test)
    score_rfr = r2_score(y_test, pred_rfr)

    rfr_pred_test_df = pd.DataFrame({'Actual': y_test, 'Predicted': pred_rfr})
    rfr_pred_test_df['diff'] = (rfr_pred_test_df['Predicted'] / rfr_pred_test_df['Actual'] -1) * 100
    fig=px.histogram(rfr_pred_test_df, x='diff', range_x=[-100, 100], nbins=200, color_discrete_sequence=['indianred'])
    fig.update_layout(margin=dict(l=10, r=10, t=0, b=0, pad=0), height=150)

    return fig, score_rfr.round(3) 
