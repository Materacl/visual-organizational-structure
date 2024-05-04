import base64
import json

import dash_bootstrap_components as dbc
from dash import dcc
from dash import html, Input, Output, callback, ctx
from dash.exceptions import PreventUpdate
import visual_organizational_structure.dash_apps.organization_graph.layouts.graph_filter as graph_filter
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling
from visual_organizational_structure.models import Dashboard
from visual_organizational_structure import db


def csv_uploader(state: bool = False) -> dbc.Modal:
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Загрузка CSV файла"), close_button=True),
            dbc.ModalBody([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Перетащите или ',
                        html.A('Выберите Файл')
                    ]),
                    style={
                        'width': '100%',
                        'height': '100%',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'marginBottom': '15px',
                    },
                    multiple=False
                ),
                html.Div(id='filename-display', children=''),
                graph_filter.filter_chooser()
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Подтвердить",
                    id="confirm-csv-uploader",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id='uploader-csv',
        centered=True,
        is_open=state
    )


@callback(
    Output("uploader-csv", "is_open"),
    [Input("confirm-csv-uploader", "n_clicks"),
     Input("button-1", "n_clicks"),
     Input("upload-data", "filename"),
     Input("dashboard-data", 'data')],
)
def toggle_csv_uploader(confirm_clicks, open_modal_clicks, filename, data):
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
def update_scv_file_name(filename):
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
