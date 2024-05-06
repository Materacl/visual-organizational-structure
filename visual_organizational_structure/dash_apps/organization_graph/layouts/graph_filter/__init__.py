import json

import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback, dcc, ctx
from dash.exceptions import PreventUpdate
from dash_cytoscape.utils import Tree
from visual_organizational_structure.models import Dashboard


def filter_chooser(state: bool = False) -> dbc.Modal:
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Фильтрация графа"), close_button=True),
            dbc.ModalBody(
                [
                    dbc.Label("Dropdown", html_for="dropdown"),
                    dbc.Form(
                        dcc.Dropdown(
                            id="filter-dropdown",
                        ),
                    ),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Подтвердить",
                    id="confirm-filter",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id='graph-filter-window',
        centered=True,
        is_open=state
    )


@callback(
    Output('filter-dropdown', 'options'),
    [Input('filter-csv-btn', 'n_clicks'),
     Input('filter-dropdown', 'options'),
     Input('graph-filter-window', 'is_open')],
    State('dashboard-data', 'data')
)
def get_filter_options(filter_clicks, current_options, filter_window_is_open, dashboard_data):
    if 'filter-csv-btn' == ctx.triggered_id or filter_window_is_open:
        dashboard = Dashboard.query.get(dashboard_data['dashboard_id'])
        graph_elements = json.loads(dashboard.graph_no_filter_data)
        options = []
        for v, element in enumerate(graph_elements):
            if 'label' in element['data']:
                options.append({'label': element['data']['label'], 'value': element['data']['id']})
        print(options)
        return options
    else:
        raise PreventUpdate
