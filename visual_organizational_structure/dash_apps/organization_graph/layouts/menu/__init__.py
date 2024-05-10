import dash_bootstrap_components as dbc
from dash import html

dashboard_menu_buttons = dbc.ButtonGroup(
    [
        dbc.Button([html.I(className='bi bi-file-earmark-arrow-up-fill', style={'fontSize': '14px', 'color': 'black'}),
                    " CSV"],
                   id='upload-csv-btn', n_clicks=0, outline=True, color="primary"),
        dbc.Button('Фильтр', id='filter-csv-btn', n_clicks=0),
        html.P(id="output")
    ],
    style={
        'position': 'absolute',
        'top': '30px',
        'left': '375px',
        'transform': 'translateY(-50%)'
    },
    size="md",
    vertical=False,
)

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search", id='search-input', debounce=True)),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0, id='search-confirm'
            ),
            width="auto",
        ),
    ],
    id='search-bar',
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
    style={
        'position': 'absolute',
        'top': '30px',
        'left': '50px',
        'transform': 'translateY(-50%)'
    },
)
