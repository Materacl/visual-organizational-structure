from dash.exceptions import PreventUpdate
from visual_organizational_structure import db
from visual_organizational_structure.models import Dashboard
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling
import base64
import json
from dash import html, Input, Output, ctx, callback, callback_context
import dash_bootstrap_components as dbc


@callback(
    Output("uploader-csv", "is_open"),
    [Input("confirm-csv-uploader", "n_clicks"),
     Input("button-1", "n_clicks"),
     Input("upload-data", "filename"),
     Input("dashboard-data", 'data')],
)
def toggle_modal(confirm_clicks, open_modal_clicks, filename, data):
    if "confirm-csv-uploader" == ctx.triggered_id and filename:
        return False
    elif "button-1" == ctx.triggered_id:
        return True
    elif data["state"]:
        return True


@callback(
    Output('filename-display', 'children'),
    Input("upload-data", "filename"),
)
def update_scv_uploader(filename):
    return filename


@callback(
    [Output('cytoscape-org-graph', 'elements'),
     Output("dashboard-data", 'data')],
    [Input('upload-data', 'contents'),
     Input('cytoscape-org-graph', 'elements'),
     Input('confirm-csv-uploader', 'n_clicks'),
     Input("dashboard-data", 'data')],
)
def update_graph_from_csv(contents, current_contents, confirm_clicks, dashboard_data):
    if "confirm-csv-uploader" == ctx.triggered_id:
        if contents is None:
            raise PreventUpdate

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string).decode('utf-8')

        try:
            graph_tree = csv_handling.CSVHandler("Brusnika", decoded)
            elements = graph_tree.get_elements()
            dashboard = Dashboard.query.get(dashboard_data["dashboard_id"])
            dashboard.graph_data = json.dumps(elements)
            db.session.commit()
            return elements, {"state": False, "dashboard_id": dashboard_data["dashboard_id"]}
        except Exception as e:
            print(e)
            return dbc.Alert("There was an error processing the file.", color="danger")
    else:
        return current_contents, {"state": True, "dashboard_id": dashboard_data["dashboard_id"]}


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
