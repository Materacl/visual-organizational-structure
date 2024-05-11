import dash_bootstrap_components as dbc
from dash import html

dashboard_menu_buttons = dbc.ButtonGroup(
    [
        dbc.Button([html.I(className='bi bi-file-earmark-arrow-up-fill', style={'fontSize': '14px', 'color': 'black'}),
                    " CSV"],
                   id='upload-csv-btn', n_clicks=0, outline=True, color="primary"),
    ],
    size="md",
    vertical=False,
)
