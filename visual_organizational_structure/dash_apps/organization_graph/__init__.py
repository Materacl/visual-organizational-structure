import dash
from dash import html
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
    dash_app.layout = html.Div(
        [
            dash.page_container,
            html.A(
                [
                    html.I(className='bi bi-house-door', style={'fontSize': '24px', 'color': 'black'}),
                ],
                href='/', style={
                    'position': 'absolute',
                    'top': '30px',
                    'left': '15px',
                    'transform': 'translateY(-50%)'
                }
            ),
        ],
        id='dash-container',
    )

    return dash_app.server
