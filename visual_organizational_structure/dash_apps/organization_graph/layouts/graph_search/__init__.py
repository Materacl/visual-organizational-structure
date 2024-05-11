import ast
import json

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
    ],
    id='search-bar',
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)


@callback(
    Output("output", "children"),
    [Input('search-input', 'value'),
     Input('search-confirm', 'n_clicks')],
)
def listen_search(input, search_clicks):
    if search_clicks:
        return input
    else:
        raise PreventUpdate


@callback(
    Output('search-input', 'options'),
    Input("confirm-csv-uploader", 'n_clicks'),
    [State('search-input', 'options'),
     State("dashboard-data", 'data')],
)
def set_search_options(upload_clicks, current_options, dashboard_data):
    if "confirm-csv-uploader" == ctx.triggered_id or not current_options:
        return get_options(dashboard_data)
    else:
        raise PreventUpdate


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