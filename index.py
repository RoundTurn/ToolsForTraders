from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from app import server
# import all pages in the app
from apps import app2, app3, app4
# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Constant Maturity STIR Curve", href="/visualizing"),
        dbc.DropdownMenuItem("Time Slicing", href="/slicing"),
        dbc.DropdownMenuItem("Relative Value Curves", href="/backtest"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [                 
                        dbc.Col(dbc.NavbarBrand("Tools For Traders", className="ml-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/backtest':
        return app4.layout
    elif pathname == '/slicing':
        return app3.layout
    # elif pathname == '/singapore':
    #     return singapore.layout
    else:
        return app2.layout
if __name__ == '__main__':
    # app.run_server(host='127.0.0.1', debug=True)
    app.run_server(debug=False)
