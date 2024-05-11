import json
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, ctx, State
from dash.exceptions import PreventUpdate
from visual_organizational_structure.models import Dashboard
import visual_organizational_structure.dash_apps.organization_graph.layouts.csv_uploader as csv_uploader
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling
from visual_organizational_structure import db

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
]


def get_tree_graph(graph_elements=None, roots=None):
    """
    Create and return a Cytoscape tree graph with specified layout and style.

    Parameters:
    - graph_elements (list, optional): List of node and edge elements for the graph.

    Returns:
    - dash_cytoscape.Cytoscape: Cytoscape tree graph object.
    """
    return cyto.Cytoscape(
        id='cytoscape-org-graph',
        layout={
            'name': 'breadthfirst',
            'roots': roots,
        },
        minZoom=0.1,
        maxZoom=5,
        boxSelectionEnabled=True,
        responsive=True,
        style={
            'width': '100%',
            'height': '100vh',
            'position': 'fixed',
            'top': 0,
            'left': 0
        },
        elements=graph_elements,
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

last_node_timestamp = ''
graph_tree_index = None
graph_tree_index_labels = None


@callback(
    Output('cytoscape-org-graph', 'elements'),
    [Input('uploader-element', 'contents'),
     Input("confirm-csv-uploader", 'n_clicks'),
     Input("dashboard-data", 'data'),
     Input('search-input', 'value'),
     Input('search-confirm', 'n_clicks'),
     Input('cytoscape-org-graph', 'tapNodeData')],
    State('cytoscape-org-graph', 'elements')
)
def update_graph(uploader_contents, upload_confirm, dashboard_data, search_value, search_clicks, tap_node_data,
                 current_elements):
    global last_node_timestamp
    global graph_tree_index
    if "confirm-csv-uploader" == ctx.triggered_id:
        return handle_csv_uploader(uploader_contents, dashboard_data)

    elif 'search-confirm' == ctx.triggered_id:
        return handle_search(search_value, dashboard_data, current_elements)

    elif tap_node_data and last_node_timestamp != tap_node_data.get('timeStamp', None):
        return handle_tap_node(tap_node_data, dashboard_data, current_elements)

    else:
        raise PreventUpdate


def handle_csv_uploader(uploader_contents, dashboard_data):
    global graph_tree_index
    global graph_tree_index_labels
    graph_elements, graph_tree = csv_uploader.get_data_from_scv(uploader_contents, dashboard_data)
    if graph_elements:
        graph_tree_index = graph_tree.create_index()
        graph_tree_index_labels = graph_tree.create_index_with_labels()
        return graph_elements
    else:
        raise PreventUpdate


def handle_search(search_value, dashboard_data, current_elements):
    global graph_tree_index
    global graph_tree_index_labels
    if search_value:
        dashboard = Dashboard.query.get(dashboard_data["dashboard_id"])
        if graph_tree_index or graph_tree_index_labels is None:
            decoded = dashboard.raw_data
            graph_tree = csv_handling.CSVHandler("Brusnika", decoded)
            graph_tree_index = graph_tree.create_index()
            graph_tree_index_labels = graph_tree.create_index_with_labels()

        search_tree = graph_tree_index.get(search_value, None)
        elements = []
        while search_tree is not None:
            elements.extend(search_tree.get_elements(recursion=False))
            search_tree = search_tree.parent

        if elements:
            dashboard.graph_data = json.dumps(elements)
            db.session.commit()
        return elements
    else:
        raise PreventUpdate


def handle_tap_node(tap_node_data, dashboard_data, current_elements):
    global last_node_timestamp
    global graph_tree_index
    last_node_timestamp = tap_node_data.get('timeStamp', None)
    dashboard = Dashboard.query.get(dashboard_data["dashboard_id"])

    if graph_tree_index is None:
        decoded = dashboard.raw_data
        graph_tree_index = csv_handling.CSVHandler("Brusnika", decoded).create_index()

    print(tap_node_data)
    tap_tree = graph_tree_index[tap_node_data['id']]
    graph_elements = tap_tree.get_elements(recursion=False)
    current_elements = json.loads(dashboard.graph_data)
    if tap_tree.is_leaf():
        raise PreventUpdate
    elif all(graph_element in current_elements for graph_element in graph_elements):
        graph_elements = tap_tree.get_elements()
        graph_elements.pop(0)
        new_graph_elements = [current_element for current_element in current_elements if
                              current_element not in graph_elements]
        dashboard.graph_data = json.dumps(new_graph_elements)
        db.session.commit()
        return new_graph_elements
    else:
        dashboard.graph_data = json.dumps(current_elements + graph_elements)
        db.session.commit()
        return current_elements + graph_elements
