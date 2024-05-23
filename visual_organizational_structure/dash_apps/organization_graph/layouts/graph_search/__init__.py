import ast
import json
import time

import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback, dcc, ctx
from dash.exceptions import PreventUpdate
from visual_organizational_structure.models import Dashboard

search_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Form(
                dcc.Dropdown(
                    placeholder="Search", id='search-input', style={'width': '1000px'}
                ),
            ),
            width="auto",
        ),
        dbc.Col(
            dbc.Button(
                html.I(className='bi bi-search', style={'fontSize': '14px'}),
                color="primary", className="ms-2", n_clicks=0, id='search-confirm'
            ),
            width="auto",
        ),
        dcc.Store(id="search_options", storage_type='session'),
    ],
    id='search-bar',
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)


@callback(
    Output('search-input', 'options'),
    Input("search_options", 'data'),
    prevent_initial_call=True
)
def set_search_options(search_options_data):
    return search_options_data["options"]


@callback(
    Output("search_options", 'data'),
    Input("confirm-csv-uploader", 'n_clicks'),
    State("dashboard-general-data", 'data'),
)
def get_search_options(upload_clicks, dashboard_data):
    time.sleep(3)  # Временно
    return {"options": get_options(dashboard_data)}


def get_options(dashboard_data):
    dashboard = Dashboard.query.get(dashboard_data["dashboard_id"])
    if dashboard.graph_paths:
        paths = json.loads(dashboard.graph_paths)
        options = []
        if paths:
            for path, path_id in paths.items():
                path = ast.literal_eval(path)
                if path:
                    options.append({'label': ' -> '.join(path), 'value': path_id})
        return options
    else:
        return []
