import base64
import datetime
import io

import pandas as pd

import dash
from dash import html, dcc, Input, Output, callback, State, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from flask_login import current_user
from visual_organizational_structure.models import Dashboard

from visual_organizational_structure.dash_apps.organization_graph.layouts.graphs import get_tree_graph
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling

from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import dash

import base64
import datetime
import io

import pandas as pd

# Register the Dash app page
dash.register_page(
    __name__,
    path_template="/org-structure/<dashboard_id>",
    title='org-structure page',
    name='org-structure page'
)

# Define the collapse component for node information
node_info_collapse = dbc.Collapse(
    dbc.Card(
        [
            dbc.CardHeader("Node Information"),
            dbc.CardBody(html.Div(id='node-info-content'))
        ]
    ),
    id='node-info-collapse',
    is_open=False,
    style={'position': 'fixed', 'top': '10px', 'right': '10px', 'z-index': 1000}
)


# Define the Dash app layout
def layout(dashboard_id=None):
    dashboard = Dashboard.query.get(dashboard_id)

    if not dashboard or dashboard.user_id != current_user.id:
        return html.Div(
            "This is not your board.",
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
                'height': '100vh',
                'font-size': '2em'
            }
        )

    return html.Div([
        get_tree_graph([], []),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        dbc.ButtonGroup([
            dbc.Button('Button 1', id='button-1', n_clicks=0),
            dbc.Button('Button 2', id='button-2', n_clicks=0)
        ],
            style={'position': 'absolute', 'top': '50%', 'left': '10px', 'transform': 'translateY(-50%)'},
            size="md",
            vertical=True,
        ),

        node_info_collapse
    ])


@callback(
    Output('cytoscape-org-graph', 'elements'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    Input('button-1', 'n_clicks')
)
def update_graph(contents, filename, last_modified, button_1_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'upload-data':
        if contents is None:
            raise PreventUpdate

        content_type, content_string = contents[0].split(',')

        decoded = base64.b64decode(content_string).decode('utf-8')

        try:
            # Generate graph data from the uploaded CSV content
            elements = csv_handling.generate_graph_data_from_csv2(decoded)
            return elements
        except Exception as e:
            print(e)
            return dbc.Alert("There was an error processing the file.", color="danger")

    elif trigger_id == 'button-1':
        return csv_handling.test_graph_data2

    raise PreventUpdate


# Define Dash callbacks
@callback(Output('node-info-content', 'children'),
          Input('cytoscape-org-graph', 'tapNodeData'))
def update_node_info(data):
    if data:
        return html.P(f"You clicked on {data['label']}. Additional info can be shown here.")
    return None


@callback(
    Output('node-info-collapse', 'is_open'),
    Input('cytoscape-org-graph', 'tapNodeData'),
    Input('node-info-collapse', 'is_open'),
    State('node-info-collapse', 'children')
)
def toggle_collapse(data, is_open, current_node_data):
    if data:
        if data == current_node_data:
            return not is_open
        return True
    return False


@callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
          Input('cytoscape-org-graph', 'mouseoverNodeData'))
def displayMouseoverNodeData(data):
    if data:
        return "You recently hovered over the city: " + data['label']


@callback(Output('cytoscape-tapNodeData-output', 'children'),
          Input('cytoscape-org-graph', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        return "You recently clicked/tapped the city: " + data['label']


@callback(Output('cytoscape-selectedNodeData-markdown', 'children'),
          Input('cytoscape-org-graph', 'selectedNodeData'))
def displaySelectedNodeData(data_list):
    if data_list is None:
        return "No city selected."

    cities_list = [data['label'] for data in data_list]
    return "You selected the following cities: " + "\n* ".join(cities_list)

# Handle file upload and load it into a graph
# @callback(
#     Output('cytoscape-org-graph', 'elements'),
#     Input('upload-data', 'contents'),
#     State('upload-data', 'filename'),
#     State('upload-data', 'last_modified')
# )
# def update_graph(contents, filename, last_modified):
#     if contents is None:
#         raise PreventUpdate
#
#     content_type, content_string = contents.split(',')
#
#     decoded = base64.b64decode(content_string).decode('utf-8')
#
#     try:
#         if 'csv' in filename:
#             # Generate graph data from the uploaded CSV content
#             elements = csv_handling.generate_graph_data_from_csv(decoded)
#             return elements
#     except Exception as e:
#         print(e)
#         return dbc.Alert("There was an error processing the file.", color="danger")
#
#     raise PreventUpdate
