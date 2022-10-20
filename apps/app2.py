import assets.markdown as dm
import bisect
import dash_bootstrap_components as dbc
import datetime
import numpy as np
import pandas as pd
import pathlib
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go

from app import app
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

## Import and format data
dateparse = lambda x: datetime.datetime.strptime(x, '%d/%m/%Y')

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("my_data_4a.csv"), 
    index_col='Date', parse_dates=True, date_parser=dateparse)
df.rename(columns={'Date': 'date'}, inplace=True)
df.columns = [str(pd.to_datetime(col).date()) for col in df.columns]
cols = df.columns
df.sort_index(ascending=True, inplace=True)

## Functions 
# To built butterfly structures:
def fly_builder(df, period):
    adj = period // 3
    cols = df.columns
    flys = {}
    for i in range(0, len(cols) - 2* adj ):
        fly = df.iloc[:, i] - (2 * df.iloc[:,(i + adj)]) + df.iloc[:, i + (2 * adj)]
        flys[cols[i + adj]] = fly
    df_out = pd.DataFrame(flys)
    df_out = df_out.round(decimals=4)
    return df_out

## Create a df for Days To Expiry, DTE, for the interpolation. Using Business Days:
def business_days(df):
    dtes = {}
    for col in df.columns:
        col_date = pd.to_datetime(col).date()
        dtes[col] = [np.busday_count(date.date(), col_date) for date in df.index]
    return pd.DataFrame(dtes, index=df.index)

## Interpolating the data
def interpolation(dte_df, prices_df, days, lookback):
    """
    Takes in days-to-expiry frame and prices frame, target days, and required lookback period.
    Returns a series of interpolated prices.
    """
    dic = {}
    for ts, row in dte_df[-lookback:].iterrows():
        l = bisect.bisect_left(row.tolist(), days) - 1 # when l == 0, this wraps to -1. Catch **below**.
        r = bisect.bisect_right(row.tolist(), days)
        try: 
            l_col = dte_df.columns[l]
            r_col = dte_df.columns[r]
        except IndexError:
            if row[-1] == days:  # Catch the single edge-case where bisect_right "is" the 'days' in last col.
                dic[ts] = prices_df.loc[ts, dte_df.columns[-1]]
            break    
        if (r - l) > 1:  # When moving over columns and "days" is exactly on the column.
            dic[ts] = prices_df.loc[ts, dte_df.columns[l + 1]]
        elif (dte_df.loc[ts, l_col] > 0)  and (l >= 0):   # **Catching the wrap around**.
            l_price = prices_df.loc[ts, l_col]
            r_price = prices_df.loc[ts, r_col]
            diff = r_price - l_price
            adj = ((days - row[l]) / (row[r] - row[l])) * diff
            dic[ts] = prices_df.loc[ts, l_col] + adj     
    return pd.Series(dic, name=days, dtype='float64')
        
## Create a frame of interpolated prices based on latest DTEs of current STIR contracts
def strat_builder(*args):
    holder = {}
    for a in args:
        holder[a] = interpolation(df_days, df, a, 500)
    return pd.DataFrame(holder)

## Create the data we need
# Business days to expiry 
df_days = business_days(df)
# List of the DTE for latest prices
latest_dtes = list(df_days.iloc[-1].values)
# Interpolate
interpolated_prices = strat_builder(*latest_dtes)

## Create tabs for layout
tab1_script = dbc.Card(
    dbc.CardBody([
        html.P(dm.app2_aim, className="card-text"),
    ]))

tab2_script = dbc.Card(
    dbc.CardBody([
        html.P(dm.app2_explainer, className="card-text"),
    ]))

## Built the layout
layout = dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Constant Maturity STIR Curve Visualisation App",
                    className="text-center bg-primary text-white p-2",              
                ),
            )
        ),
        dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(tab1_script, tab_id="one", label="What are we looking at here?", 
                        style={'width': 'auto', 'height' : '425px'}),
                    dbc.Tab(tab2_script, tab_id="two", label="Parameter selection", 
                        style={'width': 'auto', 'height' : '425px'}),
                ], active_tab="one"),
                html.H5("1. Set the butterfly leg span:", style={'padding-top': '20px'}),
                dcc.Dropdown(id="Butterfly_leg_gap", options=[
                    {"label": "3-month", "value": 3},
                    {"label": "6-month", "value": 6},
                    {"label": "9-month", "value": 9},
                    {"label": "12-month", "value": 12}],
                    clearable=False, multi=False, value=3,
                    style={'height' : '40px'}),
                html.H5("2. Click on a data point to select that butterfly:",
                style={'padding-top': '20px'}),
                dcc.Graph(id='fly_chart', figure={}, config={'displayModeBar':False}),
            ], width='auto', lg=5),
            dbc.Col([
                html.H5("3. Choose how many days of data you'd like to see:",
                    style={'padding-top': '20px'}),
                dcc.Slider(id='lookback_days',
                    min=0, max=250, 
                    updatemode = 'mouseup',
                    tooltip={"placement": "top", "always_visible": True},
                    value= 100,
                    ),
                dcc.Graph(id='scatter_outright', figure={}),
                html.H5("4. Check the structure at +/- 3 months:",
                    style={'padding-top': '20px'}),
                dcc.Graph(id='rolldown'),
                html.Hr(),
                        
            ], width='auto', lg=7)
        ]),        
    ], fluid=True)

## Callbacks
@app.callback(
    Output(component_id='fly_chart', component_property='figure'),
    Input(component_id='Butterfly_leg_gap', component_property='value')
)
def update_graph(option_slctd1):
    dff = df.copy()
    dffly = fly_builder(dff, option_slctd1)
    fig = px.line(dffly.iloc[-1,:], labels={'value': "Butterfly price (bps)",
                                        'index': "Middle contract of butterfly"})
    fig.update_traces(showlegend=False)
    fig.update_layout(title_text='3M ED STIR futures butterfly curve', title_x=0.5)
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output(component_id='scatter_outright', component_property='figure'),
    Output(component_id='rolldown', component_property='figure'),
    Input(component_id='fly_chart', component_property='clickData'),
    Input(component_id='Butterfly_leg_gap', component_property='value'),
    Input(component_id='lookback_days', component_property='value')
)
def updateScatter(clickData, leg_gap, lookback):
    price_cols = df.columns.copy()
    dfs = interpolated_prices.copy()
    dft = fly_builder(dfs, leg_gap)
    dte = df_days.copy()
    if clickData == None:
        fig = px.scatter(x=None, y=None,
        labels={'y': "Interpolated butterfly price (bps)",
                'x': "Interpolated price of middle contract of butterfly"}
        )
        fig.update_layout(title_text='Selected interpolated butterfly vs mid-leg', title_x=0.5)
        fig2 = px.line(dft.iloc[:, 0], 
            labels={'value': "Fly price (bps)",
                    'index': "Time (days)",
                    'variable': "Days to expiry of structure"}
        )
        fig2.update_traces(showlegend=False)
        fig2.update_layout(title_text='3M ED interpolated butterfly history', title_x=0.5)
        return fig, fig2
    else:
        mid_date = clickData['points'][0]['x']
        mid_ix = price_cols.get_loc(mid_date)
        mid_leg_dte = dte.iloc[-1, mid_ix]
        fig = px.scatter(x=(dfs.iloc[-lookback:, mid_ix]), y=(dft.iloc[-lookback:, mid_ix -1]),
        labels={'y': "Interpolated butterfly price (bps)",
                'x': "Interpolated price of middle contract of butterfly"}
        )

        fig.add_trace(go.Scatter(x=[dfs.iloc[-1, mid_ix]], y=[dft.iloc[-1, mid_ix - 1]], mode = 'markers',
                         marker_symbol = 'circle',
                         marker_size = 15,       
                         name = 'Latest'),
                         ),
        fig.update_layout(title_text='Selected interpolated ' + str(mid_leg_dte) + ' DTE butterfly vs mid-leg', title_x=0.5,legend=dict(yanchor="top", y=-0.1, xanchor="left", x=0.00))
        
        fig2 = px.line(dft.iloc[:, mid_ix - 2: mid_ix + 1].dropna(),
            labels={'value': "Fly price (bps)",
                    'index': "Time (days)",
                    'variable': "Days to expiry of mid-leg"})
        fig2.update_layout(title_text='3M ED interpolated butterfly history', title_x=0.5, legend=dict(yanchor="top", y=-0.1, xanchor="left", x=0.00))
        fig2.update_layout(transition_duration=500)
        return fig, fig2

# ------------------------------------------------------------------------------
# if __name__ == '__main__':
#     app.run_server(debug=True)