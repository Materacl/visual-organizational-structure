import json
import random

import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, ctx, State
from dash.exceptions import PreventUpdate
from visual_organizational_structure.models import Dashboard
import visual_organizational_structure.dash_apps.organization_graph.layouts.csv_uploader as csv_uploader
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling
from visual_organizational_structure import db

# Load extra layouts
cyto.load_extra_layouts()

default_stylesheet = [
    {
        "selector": "node",
        "style": {
            'label': 'data(label)',
            # Text
            'text-valign': 'center',
            'text-halign': 'center',
            'text-margin-y': '0px',
            'text-margin-x': '0px',
            'color': 'black',
            'font-size': '46px',
            'padding': '10px',
            'text-wrap': 'wrap',
            # Shape
            'shape': 'roundrectangle',
            'width': 'label',
            'height': 'label',
            "opacity": 1,
            # Background
            'background-color': '#1f77b4',
            "background-opacity": 0,
            # Border
            "border-width": "3px",
            # Outline
            # "outline-width": "10px",
        }
    },
    {
        "selector": "edge",
        "style": {
            "width": 6,
            "line-style": "solid",
            "line-cap": "round",
            "line-fill": "linear-gradient",
            # Color
            "line-color": "black",
            "opacity": 1,
            "line-gradient-stop-colors": "black gray",
            "line-gradient-stop-positions": "50%",
            # Curve Style
            "curve-style": "taxi",
            'edge-distances': "node-position",
            "taxi-direction": "vertical",
            "taxi-turn": "150px",
            "taxi-turn-min-distance": "50px",
            # Arrows
            "target-arrow-shape": "triangle",
            "target-arrow-color": "black",
        },
    },
    {
        "selector": ":selected",
        "style": {
            "border-width": 2,
            "border-color": "black",
            "border-opacity": 1,
            "opacity": 1,
            "label": "data(label)",
            "color": "black",
            "z-index": 9999,
        },
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
            'name': 'dagre',
            'roots': roots,
            'animate': True,
            'animationDuration': 100,
            'responsive': True,
            'wheelSensitivity': 1,
            # Dagre
            'nodeSep': 50,
            'edgeSep': 10,
            'rankSep': 200,
            'rankDir': 'TB',
            'align': 'DR',
            'acyclicer': 'greedy',
            'ranker': 'tight-tree',
            'spacingFactor': 1,
            'nodeDimensionsIncludeLabels': True,
        },
        minZoom=0.1,
        maxZoom=5,
        boxSelectionEnabled=True,
        clearOnUnhover=True,
        responsive=True,
        style={
            'width': '100%',
            'height': '100vh',
            'position': 'fixed',
            'top': 0,
            'left': 0
        },
        elements=graph_elements,
        stylesheet=default_stylesheet,
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
        return handle_tap_node(tap_node_data, dashboard_data)

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
            for element in elements:
                element["classes"] = ""
            elements[0]["selected"] = True
        return elements
    else:
        raise PreventUpdate


def handle_tap_node(tap_node_data, dashboard_data):
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
        return new_graph_elements
    else:
        dashboard.graph_data = json.dumps(current_elements + graph_elements)
        db.session.commit()
        return current_elements + graph_elements
