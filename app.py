import dash
import dash_bootstrap_components as dbc
# bootstrap theme
# https://bootswatch.com/lux/
#ext_stylesheets = [dbc.themes.LUX]
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title="Tools for Traders")

server = app.server
app.config.suppress_callback_exceptions = True
