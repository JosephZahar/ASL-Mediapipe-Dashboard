# import desired libraries
import plotly.io as pio
import pathlib
pio.templates.default = "simple_white"
import dash_bootstrap_components as dbc
from dash import dcc, dash
from dash import html
import warnings
from src.helper_functions import *
warnings.filterwarnings("ignore")

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
train_data = pd.read_csv(DATA_PATH.joinpath('train.csv'))

dropdown_options = train_data.groupby('sign')['sequence_id'].apply(list).to_dict()
names = list(dropdown_options.keys())
nestedOptions = dropdown_options[names[0]]

def visual_dash(sequence_id):
    data = train_data.copy()
    parquet_file = data[data.sequence_id == sequence_id]
    parquet_path = parquet_file.path.values[0]
    sign_cat = parquet_file.sign.values[0]

    parquet_df = pd.read_parquet(DATA_PATH.joinpath(parquet_path))
    fig = visualise2d_landmarks(parquet_df)

    return fig, sign_cat

fig, sign_cat = visual_dash(3127189)


sign_dropdown = dcc.Dropdown(options=[{'label':name, 'value':name} for name in names],
                                  id='sign_dropdown',
                                  clearable=False,
                                  value = 'eye', className="dbc",
                                  placeholder='Select a Sign', maxHeight=200)

sequence_dropdown = dcc.Dropdown(id='sequence_dropdown',
                               clearable=False,
                               value = 3127189,
                               className="dbc",
                               placeholder='Select a Sequence ID', maxHeight=200)

layout = dbc.Container(
    [dbc.Row([dbc.Col(sign_dropdown),
              dbc.Col(sequence_dropdown),]),
     dbc.Row([html.H1(id='sign_cat'),
         dbc.Col([
             dcc.Graph(id='fig', figure=fig,
                       style={'height': 2000}),
             html.Hr()
         ], width={'size': 12, 'offset': 0, 'order': 1})])]
)
