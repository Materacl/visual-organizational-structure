import json

import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, ctx
from dash.exceptions import PreventUpdate
from visual_organizational_structure.models import Dashboard

stylesheet = [
    {
        'selector': 'node',  # Style for nodes
        'style': {
            'label': 'data(label)',  # Updated to use 'label' from node data
            'text-valign': 'center',  # Center the text vertically
            'text-halign': 'center',  # Align the text to the center
            'text-margin-y': '0px',  # Adjust vertical text margin
            'text-margin-x': '0px',  # Adjust horizontal text margin
            'background-color': '#1f77b4',  # Change node color to a blue shade
            'color': 'white',  # Change text color to white
            'shape': 'roundrectangle',  # Use roundrectangle shape for nodes
            'width': 'label',  # Set node width based on label size
            'height': 'label',  # Set node height based on label size
            'font-size': '16px',  # Adjust font size
            'padding': '10px',  # Add padding to node
            'text-wrap': 'wrap'  # Allow text to wrap within node
        }
    },
    {
        'selector': '.nonterminal',
        'style': {
            'label': 'data(confidence)',
            'background-opacity': 0,
            "text-halign": "left",
            "text-valign": "top",
        }
    },
    {
        'selector': '.support',
        'style': {'background-opacity': 0}
    },
    {
        'selector': 'edge',
        'style': {
            "source-endpoint": "inside-to-node",
            "target-endpoint": "inside-to-node",
        }
    },
    {
        'selector': '.terminal',
        'style': {
            'label': 'data(name)',
            'width': 10,
            'height': 10,
            "text-valign": "center",
            "text-halign": "right",
            'background-color': '#222222'
        }
    }
]


def get_tree_graph(graph_roots=None, graph_elements=None):
    """
    Create and return a Cytoscape tree graph with specified layout and style.

    Parameters:
    - graph_elements (list, optional): List of node and edge elements for the graph.

    Returns:
    - dash_cytoscape.Cytoscape: Cytoscape tree graph object.
    """
    # Define the Cytoscape graph
    return cyto.Cytoscape(
        id='cytoscape-org-graph',
        # Layout configuration
        layout={
            'name': 'breadthfirst',  # Use 'breadthfirst' layout algorithm
            'roots': '[id = "MAIN"]',  # Root node
        },
        # Zoom configuration
        minZoom=0.1,
        maxZoom=5,
        # Enable box selection
        boxSelectionEnabled=True,
        # Make the graph responsive
        responsive=True,
        # Style configuration
        style={
            'width': '100%',  # Set width to 100%
            'height': '100vh',  # Set height to 100% of viewport height
            'position': 'fixed',  # Fixed position
            'top': 0,  # Top position
            'left': 0  # Left position
        },
        # Graph elements
        elements=graph_elements,
        # Stylesheet configuration
        stylesheet=stylesheet
    )


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


@callback(
    Output('cytoscape-org-graph', 'elements'),
    [Input("dashboard-data", 'data'),
     Input('confirm-csv-uploader', 'n_clicks')]
)
def update_graph(dashboard_data, confirm_clicks):
    if "confirm-csv-uploader" == ctx.triggered_id:
        dashboard = Dashboard.query.get(dashboard_data['dashboard_id'])
        graph_elements = json.loads(dashboard.graph_data)
        if graph_elements is None:
            raise PreventUpdate
        elif len(graph_elements) > 100:
            return []
        else:
            return graph_elements


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
