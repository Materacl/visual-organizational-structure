from dash.exceptions import PreventUpdate
from visual_organizational_structure import db
from visual_organizational_structure.models import Dashboard
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling
import base64
import json
from dash import Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash import html


@callback(
    [Output('cytoscape-org-graph', 'elements'),
     Output('csv_uploader', 'is_open')],
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename'),
     Input('upload-data', 'last_modified'),
     Input('page_layout', 'title')]
)
def update_graph(contents, filename, last_modified, title):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string).decode('utf-8')

    try:
        elements = csv_handling.generate_graph_data_from_csv2(decoded)
        dashboard = Dashboard.query.get(title)
        dashboard.graph_data = json.dumps(elements)
        db.session.commit()
        return elements, False
    except Exception as e:
        print(e)
        return dbc.Alert("There was an error processing the file.", color="danger")


@callback(
    Output('cytoscape-org-graph', 'layout'),
    Input('dropdown-update-layout', 'value')
)
def update_layout(layout):
    return {
        'name': layout,
        'animate': True,
        'roots': '[id = "LE0"]'
    }


@callback(
    Output('node-info-content', 'children'),
    Input('cytoscape-org-graph', 'tapNodeData'),
)
def display_node_info(node_data):
    if node_data is None:
        raise PreventUpdate

    # Create a table to display the node's attributes
    node_info_table = html.Table(
        [
            html.Tr([html.Td("Node ID"), html.Td(node_data['id'])]),
            # Add more rows as needed for other node attributes
        ]
    )

    return node_info_table
