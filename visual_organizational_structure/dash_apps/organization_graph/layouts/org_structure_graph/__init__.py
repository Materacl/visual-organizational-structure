import json
import time

import dash_cytoscape as cyto
from dash import callback, Input, Output, State, clientside_callback
from dash.exceptions import PreventUpdate
from visual_organizational_structure.models import Dashboard
import visual_organizational_structure.dash_apps.organization_graph.layouts.csv_uploader as csv_uploader
import visual_organizational_structure.dash_apps.organization_graph.layouts.org_structure_graph.style as style
from visual_organizational_structure import db
from visual_organizational_structure.utils import cache

TIMEOUT = 60

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
        boxSelectionEnabled=True,
        responsive=True,
        panningEnabled=True,
        autoRefreshLayout=True,
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
    Input('dashboard-graph-elements', 'data'),
    State("dashboard-general-data", 'data'),
    prevent_initial_call=True
)
@cache.memoize(timeout=TIMEOUT)
def update_graph(dashboard_graph_elements: list, dashboard_general_data: dict):
    dashboard = Dashboard.query.get(dashboard_general_data["dashboard_id"])
    if dashboard.graph_data != json.dumps(dashboard_graph_elements):
        dashboard.graph_data = json.dumps(dashboard_graph_elements)
        db.session.commit()
    return dashboard_graph_elements


@callback(
    [
        Output('dashboard-graph-elements', 'data', allow_duplicate=True),
        Output('dashboard-graph-data', 'data'),
        Output("uploader-csv", "is_open", allow_duplicate=True)
    ],
    Input("confirm-csv-uploader", 'n_clicks'),
    [
        State('uploader-element', 'contents'),
        State("dashboard-general-data", 'data')
    ],
    prevent_initial_call=True,
    running=[(Output("confirm-csv-uploader", "disabled"), True, False)]
)
@cache.memoize(timeout=TIMEOUT)
def handle_csv_uploader(upload_confirm_clicks, uploader_contents, dashboard_general_data):
    graph_tree = csv_uploader.get_data_from_scv(uploader_contents)
    graph_elements = graph_tree.find_by_id('MAIN', method='bfs').get_elements(recursion=False)
    if graph_elements:
        dashboard_graph_data = {
            "id_to_data": graph_tree.create_index_with_data(),
            "id_to_parent": graph_tree.create_index_with_parents(),
            "id_to_children": graph_tree.create_index_with_ids()
        }
        dashboard = Dashboard.query.get(dashboard_general_data["dashboard_id"])
        converted_paths = {str(key): value for key, value in graph_tree.paths.items()}
        dashboard.graph_paths = json.dumps(converted_paths)
        dashboard.graph_roots = '[id = "MAIN"]'
        dashboard.id_to_data = json.dumps(dashboard_graph_data["id_to_data"])
        dashboard.id_to_parent = json.dumps(dashboard_graph_data["id_to_parent"])
        dashboard.id_to_children = json.dumps(dashboard_graph_data["id_to_children"])
        db.session.commit()
        return graph_elements, dashboard_graph_data, False
    else:
        raise PreventUpdate


@callback(
    Output('dashboard-graph-elements', 'data', allow_duplicate=True),
    Input('search-confirm', 'n_clicks'),
    [
        State('search-input', 'value'),
        State('dashboard-graph-elements', 'data'),
        State('dashboard-graph-data', 'data')
    ],
    prevent_initial_call=True,
    running=[(Output("search-confirm", "disabled"), True, False)]
)
@cache.memoize(timeout=TIMEOUT)
def handle_search(search_confirm_clicks, search_value, current_elements, dashboard_graph_data):
    if not search_value:
        raise PreventUpdate

    id_to_data = dashboard_graph_data.get("id_to_data", {})
    id_to_parent = dashboard_graph_data.get("id_to_parent", {})

    if not id_to_data:
        raise PreventUpdate

    elements = []
    current_id = search_value
    while current_id:
        search_data = id_to_data.get(current_id, [])
        elements.extend(search_data)
        current_id = id_to_parent.get(current_id, '')

    return current_elements + elements


@callback(
    Output('dashboard-graph-elements', 'data', allow_duplicate=True),
    Input('cytoscape-org-graph', 'tapNodeData'),
    [
        State('dashboard-graph-elements', 'data'),
        State('dashboard-graph-data', 'data'),
    ],
    prevent_initial_call=True,
    running=[(Output("cytoscape-org-graph", "disabled"), True, False)]
)
@cache.memoize(timeout=TIMEOUT)
def handle_tap_node(tap_node_data, current_elements, dashboard_graph_data):
    if not tap_node_data:
        raise PreventUpdate

    node_id = tap_node_data['id']
    id_to_data = dashboard_graph_data.get("id_to_data", {})
    id_to_children = dashboard_graph_data.get("id_to_children", {})

    tap_elements = id_to_data.get(node_id, [])
    if len(tap_elements) <= 1:
        raise PreventUpdate

    if any(elem in current_elements for elem in tap_elements[1:]):
        children_ids = get_children_ids(node_id, id_to_children)
        elements_to_remove = [elem for cid in children_ids for elem in id_to_data.get(cid, [])]
        elements_to_remove.pop(0)
        new_graph_elements = [elem for elem in current_elements if elem not in elements_to_remove]
        return new_graph_elements
    else:
        if 'job_title' in tap_elements[0]['data']:
            tap_elements.append({'data': {'label': tap_elements[0]['data']['job_title']}})
    return current_elements + tap_elements


@cache.memoize(timeout=TIMEOUT)
def get_children_ids(start_id: str, id_to_children: dict) -> list:
    result = []

    def dfs(current_id: str):
        result.append(current_id)
        for child_id in id_to_children.get(current_id, []):
            dfs(child_id)

    dfs(start_id)
    return result
