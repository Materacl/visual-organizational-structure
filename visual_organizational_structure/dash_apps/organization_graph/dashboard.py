import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    APP_TITLE = "VOS"
    dash_app = dash.Dash(
        __name__,
        title=APP_TITLE,
        server=server,
        use_pages=True,
        routes_pathname_prefix='/dashboard/',
        external_stylesheets=[
            dbc.themes.ZEPHYR,
            dbc.icons.BOOTSTRAP
        ],
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
    )

    # Create Dash Layout
    dash_app.layout = dbc.Spinner(
        [
            dash.page_container,
            html.A(
                [
                    html.I(className='bi bi-house-door', style={'fontSize': '24px', 'color': 'black'}),
                ],
                href='/', style={
                    'position': 'absolute',
                    'top': '25px',
                    'left': '15px',
                    'transform': 'translateY(-50%)'
                }
            ),
        ],
        spinner_style={"width": "3rem", "height": "3rem"},
        id='dash-container',
        color='primary',
        fullscreen=True
    )

    return dash_app.server
