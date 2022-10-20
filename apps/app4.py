import dash_bootstrap_components as dbc

from app import app
from dash import html


## App page layout
layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H2(
                "Relative Value Curves - A Backtest",
                className="text-center bg-primary text-white p-2",              
            ),
        )
    ),
    
    html.Div(
        html.Iframe(id="serviceFrameSend", 
                    src="../assets/CC_showcase.html",width="1000", height="1000",
                    ),style={"text-align":"center"}
    )
    ], fluid=True)
