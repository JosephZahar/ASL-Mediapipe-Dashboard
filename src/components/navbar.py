from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.Button("2D Visuals", href="/landmark2d", id="landmark2d", color="outline-secondary", className="mr-6")),
                dbc.NavItem(dbc.Button("Mean Visual", href="/landmarkavg", id="landmarkavg", color="outline-secondary", className="mr-6")),
            ],
            brand="ASL Visualization Dashboard",
            brand_href="/landmark2d",
            id="navbar",
            color="dark",
            brand_style={'fontSize': '30px', 'textAlign': 'center', 'width': '100%'},
        dark=True,
        ),
    ])

    return layout