import pathlib
from dash import html, dcc
from dash.dependencies import Input, Output
from src.pages import landmarkavg
from src.pages import landmark2d
from src.pages.landmark2d import visual_dash
from src.pages.landmarkavg import visualmean_dash
from src.components import navbar
import dash
import dash_bootstrap_components as dbc
import pandas as pd

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
train_data = pd.read_csv(DATA_PATH.joinpath('train.csv'))

dropdown_options = train_data.groupby('sign')['sequence_id'].apply(list).to_dict()
names = list(dropdown_options.keys())
nestedOptions = dropdown_options[names[0]]

nav = navbar.Navbar()

app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/landmark2d':
        return landmark2d.layout
    if pathname == '/landmarkavg':
        return landmarkavg.layout
    else:
        return landmark2d.layout

@app.callback(
    [Output("landmark2d", "color"),
     Output("landmarkavg", "color")],
    [Input('url', 'pathname')]
)
def update_button_color(pathname):
    if pathname == '/landmark2d':
        return "light", "outline-secondary"
    elif pathname == '/landmarkavg':
        return "outline-secondary", "light"
    else:
        return "light", "outline-secondary"

@app.callback(
    dash.dependencies.Output('sequence_dropdown', 'options'),
    [dash.dependencies.Input('sign_dropdown', 'value')]
)
def update_dropdown(name):
    return [{'label': i, 'value': i} for i in dropdown_options[name]]

@app.callback([Output(component_id="fig", component_property="figure"),
               Output(component_id="sign_cat", component_property="children")],
              [Input('sequence_dropdown', 'value')])
def callback_function(sequence_id):
    fig, sign_cat = visual_dash(sequence_id)
    return fig, sign_cat

@app.callback([Output(component_id="fig2", component_property="figure"),
               Output(component_id="sign_cat2", component_property="children")],
              [Input('sequence_dropdown', 'value')])
def callback_function(sequence_id):
    fig, sign_cat = visualmean_dash(sequence_id)
    return fig, sign_cat

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=False)
