# REQUIRED INSTALLS bisect, dash, datetime, numpy, pandas, plotly

from cmath import nan
#from datetime import date
import assets.markdown as dm
import datetime

#from turtle import width
import dash_bootstrap_components as dbc

#import numpy as np
import os
import pandas as pd
#import plotly.express as px  # (version 4.7.0 or higher)
#import plotly.graph_objects as go
#import pytz
import pathlib
from collections import OrderedDict
from dash import ctx, Dash, dash_table, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from dash.dependencies import Input, Output, State

from app import app
#app = Dash(__name__, external_stylesheets=external_stylesheets)



## Import and clean data.
#source_1 = 'C:/Users/CM/Documents/Projects/my_site2
source_1 = './datasets/zn_sample.csv' # <--- file path
dt_format = '%d/%m/%Y %H:%M' #<-- change if needed
dateparse = lambda x: datetime.datetime.strptime(x, dt_format)

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("zn_sample.csv"), 
                    parse_dates=['Date and Time'], date_parser=dateparse)
df.set_index('Date and Time', inplace=True)  

## Initialize the parameter input data table
input_params = ['Start time', ' End time', 'Interval', 'Timezone']
input_df = pd.DataFrame(OrderedDict([
    ('Slice', [1, 2, 3, 4, 5]),
    ('Start_time', ['15:45', '21:00', None,None,None]),
    ('End_time', ['16:00', '21:30', None,None,None]),
    ('Interval', [1, 5, None, None, None]),
    ('Timezone', ['UTC', 'UTC', None, None, None])
]))
tz_options =  ['UTC', 'Europe/London', 'America/Chicago', 'Australia/Sydney', 'Asia/Shanghai','Europe/Berlin']


# Unused code from previous iteration as desktop app. Not incorporated in web version.
# if entire_folder:
#     for filename in os.listdir(folder):
#         if filename.endswith('.csv'):
#             source = folder + '/' + filename
#             time_slicer(source, slices, start_date, end_date)
# else:
#     source = source_1
#     time_slicer(source, slices, start_date, end_date)

## Markdown for placement in tabs.

## Tab layout
tab1_script = dbc.Card(
    dbc.CardBody(
        [
            html.P(dm.app3_aim, className="card-text"),
        ]
    ),
)
tab2_script = dbc.Card(
    dbc.CardBody(
        [
            html.P(dm.app3_explainer, className="card-text"),
        ]
    ),
)

## App page layout
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Time slicing",
                    className="text-center bg-primary text-white p-2",              
                ),
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(tab1_script, tab_id="one", label="What are we looking at here?", style={'width': 'auto', 'height' : '425px'}),
                                dbc.Tab(tab2_script, tab_id="two", label="Parameter explainer", style={'width': 'auto', 'height' : '425px'}),
                            ], active_tab="one"
                        ),
                        dbc.Row([
                            dbc.Col([
                                html.H5("Execute on single file or multiple files?",
                                    style={'padding-top': '20px'}),
                                dcc.RadioItems([
                                        {'label' : 'Single', 'value': True},
                                        {'label': 'Multiple', 'value': False}], 
                                    id= 'whole_folder',
                                    inline=True,
                                    value=True,
                                    style={'height' : '40px'}
                        ),
                            ]),
                            dbc.Col([
                                html.H5("Enter Location:",
                                style={'padding-top': '20px', 'padding-bottom': '10px'}),
                                dcc.Input(id="file_folder_input", type="text", placeholder="", readOnly=True),
                            ]),
                        ]),
                        
                    ], width='auto', lg=5,
                ),
                dbc.Col(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.H5("Do you require running High / Low?",
                                    style={'padding-top': '20px'}),
                                dcc.RadioItems([
                                        {'label': 'No', 'value': False },
                                        {'label' : 'Yes', 'value': True }
                                        ], 
                                    id= 'hilo_bool',
                                    value=False,
                                    inline=True,
                                    style={'height' : '40px'}
                                ),
                            ]),
                                dbc.Col([
                                html.H5("Enter running High / Low reset time:",
                                style={'padding-top': '20px'}),
                                dcc.Input(id="hilo_time", type="text", placeholder="13:20"),
                            ]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.H5("Would you like to specify timezones for the slices?",
                                    style={'padding-top': '20px'}),
                                dcc.RadioItems([
                                        {'label': 'No', 'value': False },
                                        {'label' : 'Yes', 'value': True }
                                        ],
                                    id='tz_bool',
                                    value=False,
                                    inline=True,
                                    style={'height' : '40px'}
                                ),
                            ]),
                            dbc.Col([
                                html.H5("Base data timezone:",
                                    style={'padding-top': '20px'}),
                                dcc.Dropdown(id="base_tz",
                                    options= [
                                                {'label': i, 'value': i}
                                                for i in tz_options
                                            ],
                                    clearable=False, multi=False, value=None, placeholder='', disabled=True,
                                    style={'height' : '40px', 'padding-top': '15px'},
                                ),
                            ]),
                        ]),
                        html.H5("Select a date range:",
                            style={'padding-top': '20px'}
                            ),
                        dcc.DatePickerRange(
                            id='slice_range',
                            min_date_allowed=df.index[0].date().strftime("%Y-%m-%d"),
                            max_date_allowed=df.index[-1].date().strftime("%Y-%m-%d"),
                            start_date=df.index[0].date(),
                            end_date=df.index[-1].date(),
                            updatemode='singledate',
                        ),
                        html.H5("Input required time slices:",
                            style={'padding-top': '20px'}
                            ),
                        dash_table.DataTable(
                            id='time_slices',
                            data = input_df.to_dict('records'),
                            columns=[
                                {'id': 'Slice', 'name': 'Slice', 'editable': False}, 
                                {'id': 'Start_time', 'name': 'Start_time(HH:MM)'},
                                {'id': 'End_time', 'name': 'End_time (HH:MM)'},
                                {'id': 'Interval', 'name': 'Interval (minutes)'},
                                {'id': 'Timezone', 'name': 'Timezone', 'presentation': 'dropdown'},
                            ],
                            editable = True, 
                            dropdown ={
                                'Timezone': {
                                    'options': [
                                        {'label': i, 'value': i}
                                        for i in tz_options
                                    ]
                                }
                            }
                        ),
                        html.Div(id='table-dropdown-container'),
                        html.Div([
                        html.Button(id='submit_button',                
                            children='Submit'
                        )
                        ]),
                        dash_table.DataTable(
                        id='output',
                        ),
                        html.Button("Download CSV", id="btn_csv", disabled=True),
                        dcc.Download(id="download_csv"),
                        
                        #html.Iframe(srcDoc="C:/Users/CM/Downloads/BOB_vs_ZN.html",
                        # html.Iframe(src= 'C:/Users/CM/Documents/Projects/my_site2/assets/BOB_vs_ZN.html',
                        # html.Iframe(src="test1.pdf",
                        # #Content-Security-Policy: frame-ancestors 'self',
                        # style={"height": "1067px", "width": "100%"})

                        # html.Div(
                        # # html.Iframe(id="embedded-pdf", src="assets/test1.pdf")
                        # # html.Iframe( src=os.path.join("assets", "test1.pdf"))
                        # html.Iframe(id="serviceFrameSend", src="../assets/BOB_vs_ZN.html",width="1000", height="1000")
                        # #src=os.path.join("assets", "test1.pdf")

                        # )
                    ], width='auto', lg=7,
                )
            ]
        ),
        dbc.Row(
            dbc.Col(   
                 dash_table.DataTable(id='output'),
            ),
        ),    
    ], fluid=True,
)
## Callbacks

@app.callback(
    Output("btn_csv", 'disabled'),
    Input('output', 'data'),
    State('output', 'data'),
)
def activate_download_button(data, state):
    return True if data == None else False


@app.callback(
    Output("download_csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('output', 'data'),
    prevent_initial_call=True,
    )
def func(n_clicks, frame):
    if frame != None:
        df_out = pd.DataFrame(frame)
        return dcc.send_data_frame(df_out.to_csv, "time_sliced_data.csv")

@app.callback(
    Output('file_folder_input','placeholder'),
    Input('whole_folder','value'),
    State('file_folder_input','placeholder'),
    )
def update_file(w_f, placeholder):
    new_placeholder = "C:/Users/datasets.sample.csv" if w_f == True else "C:/Users/datasets"
    return new_placeholder

@app.callback(
    Output('base_tz','placeholder'),
    Output('base_tz','value'),
    Output('base_tz', 'disabled'),
    Input('tz_bool','value'),
    State('base_tz','placeholder'),
    )
def update_file(use_tz, placeholder):
    if use_tz == True:
        new_placeholder ="Select base timezone"
        new_disabled = False
        new_value = 'value'
    else:
        new_placeholder = "n/a"
        new_disabled = True
        new_value = None
    return new_placeholder, new_value, new_disabled

@app.callback(
    Output('output', 'data'),
    State('base_tz', 'value'),
    State('tz_bool', 'value'),
    State('slice_range', 'start_date'),
    State('slice_range', 'end_date'),
    State('hilo_time', 'value'),
    State('hilo_bool', 'value'),
    State('whole_folder', 'value'),
    State('time_slices', 'data'),
    Input('submit_button', 'n_clicks'),
    State('submit_button', 'n_clicks')
    )
def time_slicer(base_tz, use_tz, start_date, end_date, hilo_time, hilo_bool, w_f, time_slices, n_clicks, state):
    """
    This is the main function of the app. Comments throughout.
    """
    if 'submit_button' == ctx.triggered_id: 
        df_temp = df.copy()
        start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        end_date =  pd.to_datetime(end_date, format='%Y-%m-%d')
        if use_tz == True:
            df_temp = df_temp.tz_localize(base_tz, ambiguous=True)
            start_date = start_date.tz_localize(base_tz, ambiguous=True)
            end_date = end_date.tz_localize(base_tz, ambiguous=True)
        ## Process the user slices
        slices = []
        for row in time_slices:
            if use_tz == False:
                if row['Start_time'] and row['End_time'] and row['Interval']:
                    slices.append(((row['Start_time'], row['End_time']), row['Interval'], row['Timezone']))
            else:
                if all([cell != None for cell in row.values()]):
                    slices.append(((row['Start_time'], row['End_time']), row['Interval'], row['Timezone']))
        
        ## Add running high / low
        if hilo_bool == True:
            df_temp['RunningHigh'] = df_temp['High'].groupby(pd.Grouper(freq='24h', origin=hilo_time)).cummax()
            df_temp['RunningLow'] = df_temp['Low'].groupby(pd.Grouper(freq='24h', origin=hilo_time)).cummin()
        
        ## Process each time slice
        for i in range(len(slices)):
            resamp = df_temp.resample((str(slices[i][1]) + 'T'), label='right', closed='right').last()
            resamp['Interval_Open'] = df_temp['Open'].resample((str(slices[i][1]) + 'T'), label='right', closed='right').first()
            resamp['Interval_Hi'] = df_temp['High'].resample((str(slices[i][1]) + 'T'), label='right', closed='right').max()
            resamp['Interval_Lo'] = df_temp['Low'].resample((str(slices[i][1]) + 'T'), label='right', closed='right').min()
            df_1 = resamp.dropna()
            
            if use_tz == True:
                if slices[i][2] != base_tz:
                    df_1 = df_1.tz_convert(slices[i][2])

            temp_slice = df_1.between_time(slices[i][0][0], slices[i][0][1])
            df_sliced = pd.DataFrame()
            df_sliced = pd.concat([df_sliced, temp_slice], axis=0)
        
        df_sliced.sort_index(inplace=True)
        df_sliced = df_sliced.loc[start_date : end_date + pd.offsets.BDay(1)]

        df_sliced.reset_index(inplace=True)
        data = df_sliced.to_dict('records')

        return data
    
# ------------------------------------------------------------------------------
# if __name__ == '__main__':
#     app.run_server(debug=True)