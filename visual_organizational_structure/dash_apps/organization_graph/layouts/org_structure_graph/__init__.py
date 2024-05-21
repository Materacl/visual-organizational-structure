import json
import pickle
import random
import base64

import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, ctx, State
from dash.exceptions import PreventUpdate
from visual_organizational_structure.models import Dashboard
import visual_organizational_structure.dash_apps.organization_graph.layouts.csv_uploader as csv_uploader
import visual_organizational_structure.dash_apps.organization_graph.layouts.org_structure_graph.style as style
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling
from visual_organizational_structure import db

# Load extra layouts
cyto.load_extra_layouts()


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
        stylesheet=style.default_stylesheet,
    )


@callback(
    Output('cytoscape-org-graph', 'elements'),
    Input('dashboard-graph-data', 'data'),
    State("dashboard-general-data", 'data')
)
def update_graph(dashboard_graph_data: dict, dashboard_general_data: dict):
    elements = dashboard_graph_data.get("graph_elements", [])
    dashboard = Dashboard.query.get(dashboard_general_data["dashboard_id"])
    dashboard.graph_data = json.dumps(elements)
    db.session.commit()
    return elements


@callback(
    [
        Output('dashboard-graph-data', 'data', allow_duplicate=True),
        Output("uploader-csv", "is_open", allow_duplicate=True)
    ],
    Input("confirm-csv-uploader", 'n_clicks'),
    [
        State('uploader-element', 'contents'),
        State("dashboard-general-data", 'data')
    ],
    prevent_initial_call=True
)
def handle_csv_uploader(upload_confirm_clicks, uploader_contents, dashboard_general_data):
    graph_elements, graph_tree = csv_uploader.get_data_from_scv(uploader_contents, dashboard_general_data)
    if graph_elements:
        dashboard_graph_data = {
            "graph_elements": graph_elements,
            "id_to_data": graph_tree.create_index_with_data(),
            "id_to_parent": graph_tree.create_index_with_parents(),
            "id_to_children": graph_tree.create_index_with_ids()
        }
        dashboard = Dashboard.query.get(dashboard_general_data["dashboard_id"])
        dashboard.id_to_data = json.dumps(dashboard_graph_data["id_to_data"])
        dashboard.id_to_parent = json.dumps(dashboard_graph_data["id_to_parent"])
        dashboard.id_to_children = json.dumps(dashboard_graph_data["id_to_children"])
        db.session.commit()
        return dashboard_graph_data, False
    else:
        raise PreventUpdate


@callback(
    Output('dashboard-graph-data', 'data', allow_duplicate=True),
    Input('search-confirm', 'n_clicks'),
    [
        State('search-input', 'value'),
        State('dashboard-graph-data', 'data')
    ],
    prevent_initial_call=True
)
def handle_search(search_confirm_clicks, search_value, dashboard_graph_data):
    if search_value:
        id_to_data = dashboard_graph_data.get("id_to_data", [])
        id_to_parent = dashboard_graph_data.get("id_to_parent", [])
        if not id_to_data:
            raise PreventUpdate
        else:
            current_id = search_value
            search_data = id_to_data.get(current_id, [])
            elements = []
            while search_data:
                elements.extend(search_data)
                current_id = id_to_parent.get(current_id, '')
                search_data = id_to_data.get(current_id, [])

            if elements:
                for element in elements:
                    if "selected" in element:
                        element["selected"].pop("selected")
                elements[0]["selected"] = True

            current_elements = dashboard_graph_data["graph_elements"]
            for current_element in current_elements:
                if "selected" in current_element:
                    current_element.pop("selected")
            dashboard_graph_data["graph_elements"] = current_elements + elements
            return dashboard_graph_data
    else:
        raise PreventUpdate


@callback(
    Output('dashboard-graph-data', 'data', allow_duplicate=True),
    Input('cytoscape-org-graph', 'tapNode'),
    State('dashboard-graph-data', 'data'),
    prevent_initial_call=True
)
def handle_tap_node(tap_node_data, dashboard_graph_data):
    id_to_data = dashboard_graph_data.get("id_to_data", [])
    id_to_children = dashboard_graph_data.get("id_to_children", [])

    tap_elements = id_to_data.get(tap_node_data['data']['id'], [])
    if tap_elements:
        current_elements = dashboard_graph_data.get("graph_elements", [])
        if all(tap_element in current_elements for tap_element in tap_elements):
            all_tap_children_ids = get_children_ids(tap_node_data['data']['id'], id_to_children)
            graph_elements = []
            for all_tap_children_id in all_tap_children_ids:
                graph_elements.extend(id_to_data[all_tap_children_id])
            graph_elements.pop(0)
            new_graph_elements = [current_element for current_element in current_elements if
                                  current_element not in graph_elements]
            dashboard_graph_data["graph_elements"] = new_graph_elements
            return dashboard_graph_data
        else:
            if 'job_title' in tap_elements[0]['data']:
                tap_elements.append(
                    {
                        'data': {'label': tap_elements[0]['data']['job_title']}
                    }
                )
            dashboard_graph_data["graph_elements"] = current_elements + tap_elements
            return dashboard_graph_data
    else:
        raise PreventUpdate


def get_children_ids(start_id: str, id_to_children: dict):
    result = []

    def dfs(current_id: str):
        result.append(current_id)
        if current_id in id_to_children:
            for child_id in id_to_children[current_id]:
                dfs(child_id)

    dfs(start_id)

    return result
