import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# 1. Initialize the Dash app
app = dash.Dash(__name__)

# 2. Expose the Flask server for Gunicorn (CRITICAL FOR PRODUCTION)
server = app.server

# 3. Create sample data (You'll replace this with your Trading Bot data)
df = pd.DataFrame({
    "Asset": ["BTC", "ETH", "SOL", "DOT"],
    "Price": [45000, 2500, 100, 7],
    "Signal": ["BUY", "HOLD", "BUY", "SELL"]
})

fig = px.bar(df, x="Asset", y="Price", color="Signal", title="Bot Status")

# 4. Define the Layout
app.layout = html.Div([
    html.H1("AI Trading Bot Dashboard"),
    html.Div("Real-time performance from KVM 2 Server"),
    dcc.Graph(figure=fig),
    
    # Auto-refresh component (updates every 30 seconds)
    dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0)
])

if __name__ == '__main__':
    # This part only runs during local development
    app.run_server(debug=True, port=8050)