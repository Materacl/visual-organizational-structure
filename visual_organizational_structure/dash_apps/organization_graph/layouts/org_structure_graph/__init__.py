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

@callback(
    [Output('cytoscape-org-graph', 'elements'),
     Output('cytoscape-org-graph', 'layout'),
     Output('filter-info-text', 'children')],
    [Input('uploader-element', 'contents'),
     Input("dashboard-data", 'data'),
     Input('confirm-csv-uploader', 'n_clicks'),
     Input('confirm-filter', 'n_clicks'),
     Input('filter-dropdown', 'value'),
     Input('cytoscape-org-graph', 'tapNodeData')],
    [State('cytoscape-org-graph', 'elements'),
     State('cytoscape-org-graph', 'layout')]
)
def update_graph(uploader_contents, dashboard_data, confirm_clicks, filter_clicks, filter_value, tap_node_data,
                 current_elements,
                 current_layout):
    global last_node_timestamp
    global graph_tree_index

    if "confirm-csv-uploader" == ctx.triggered_id:
        return handle_csv_uploader(uploader_contents, dashboard_data, current_layout)

    elif 'confirm-filter' == ctx.triggered_id:
        return handle_filter_confirmation(dashboard_data, filter_value, current_layout, current_elements)

    elif tap_node_data and last_node_timestamp != tap_node_data.get('timeStamp', None):
        return handle_tap_node(tap_node_data, dashboard_data, current_elements, current_layout)

    else:
        raise PreventUpdate


def handle_csv_uploader(uploader_contents, dashboard_data, current_layout):
    global graph_tree_index
    graph_elements, graph_tree = csv_uploader.get_data_from_scv(uploader_contents, dashboard_data)
    if graph_elements:
        graph_tree_index = graph_tree.create_index()
        return graph_elements, current_layout, ''
    else:
        raise PreventUpdate


def handle_filter_confirmation(dashboard_data, filter_value, current_layout, current_elements):
    dashboard = Dashboard.query.get(dashboard_data["dashboard_id"])
    decoded = dashboard.raw_data
    graph_tree = csv_handling.CSVHandler("Brusnika", decoded)
    graph_elements = graph_tree.find_by_id(filter_value, method='bfs').get_elements()
    if len(graph_elements) > 200:
        return current_elements, current_layout, 'Слишком большой граф, выберите другой элемент!'
    else:
        dashboard.graph_data = json.dumps(graph_elements)
        roots = f'[id = "{filter_value}"]'
        dashboard.graph_roots = roots
        db.session.commit()
        current_layout['roots'] = roots
        return graph_elements, current_layout, ''


def handle_tap_node(tap_node_data, dashboard_data, current_elements, current_layout):
    global last_node_timestamp
    global graph_tree_index
    last_node_timestamp = tap_node_data.get('timeStamp', None)
    dashboard = Dashboard.query.get(dashboard_data["dashboard_id"])

    if graph_tree_index is None:
        decoded = dashboard.raw_data
        graph_tree_index = csv_handling.CSVHandler("Brusnika", decoded).create_index()

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
        return new_graph_elements, current_layout, ''
    else:
        dashboard.graph_data = json.dumps(current_elements + graph_elements)
        db.session.commit()
        return current_elements + graph_elements, current_layout, ''

