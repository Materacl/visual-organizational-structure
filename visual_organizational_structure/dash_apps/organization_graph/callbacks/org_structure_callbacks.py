from dash.exceptions import PreventUpdate
from visual_organizational_structure import db
from visual_organizational_structure.models import Dashboard
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling
import base64
import json
from dash import html, Input, Output, ctx, callback, callback_context
import dash_bootstrap_components as dbc


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
