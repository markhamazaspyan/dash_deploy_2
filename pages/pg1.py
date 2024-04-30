import dash
from dash import dcc, html, callback
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime
import plotly.graph_objects as go
import plotly.express as px


dash.register_page(__name__,
                   path="/candlestick",
                   name="Candlestick_chart",
                   title="Candlestick"
                   )



start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 3)
df = web.DataReader(['AMZN','GOOGL','META','MSFT','NVDA'],
                    'stooq', start=start, end=end,)

# make multicolumn df to one column
df.columns=["_".join(x) for x in df.columns.values]

df.reset_index(inplace=True)
df.rename(columns={'index': 'Date'}, inplace=True)


stocks = ['AMZN','GOOGL','META','MSFT','NVDA']


layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id="stock_selector", options=[{"label":x,"value":x} for x in stocks], multi=False, value=stocks[0]),
                dcc.Graph(id="stock_selector_graph", figure={})])
        ])

])


@callback(
    Output('stock_selector_graph', 'figure'),
    Input('stock_selector', 'value')
)
def update_graph1(stock):

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df[f'Open_{stock}'], high=df[f'High_{stock}'],
                    low=df[f'Low_{stock}'], close=df[f'Close_{stock}'])
                    ])
    fig.update_layout(xaxis_rangeslider_visible=False)

    return fig