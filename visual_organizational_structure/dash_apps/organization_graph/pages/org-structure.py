import base64

import dash
from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from flask_login import current_user
from visual_organizational_structure.models import Dashboard

from visual_organizational_structure.dash_apps.organization_graph.layouts.graphs import get_tree_graph
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling


# Register the Dash app page
dash.register_page(
    __name__,
    path_template="/org-structure/<dashboard_id>",
    title='org-structure page',
    name='org-structure page'
)

# Nodes and edges definitions
nodes = [
    {
        'data': {'id': short, 'label': label}
    }
    for short, label in (
        ('la', 'Los Angeles'),
        ('nyc', 'New York'),
        ('to', 'Toronto'),
        ('mtl', 'Montreal'),
        ('van', 'Vancouver'),
        ('chi', 'Chicago'),
        ('bos', 'Boston'),
        ('hou', 'Houston')
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

graph_elements = nodes + edges

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
        get_tree_graph(csv_handling.test_graph_data),
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
            multiple=False
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


# Add callback to handle file upload
@callback(
    Output('cytoscape-org-graph', 'elements'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def update_graph(contents, filename):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    # Call method from csv_handling.py to generate nodes
    nodes = csv_handling.generate_graph_data_from_csv(decoded.decode('utf-8'))

    return nodes
