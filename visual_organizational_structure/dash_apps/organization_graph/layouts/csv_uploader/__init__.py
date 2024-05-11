import base64
import json

import dash_bootstrap_components as dbc
from dash import dcc
from dash import html, Input, Output, callback, ctx
from dash.exceptions import PreventUpdate
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling
from visual_organizational_structure.models import Dashboard
from visual_organizational_structure import db


def csv_uploader(state: bool = False) -> dbc.Modal:
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Загрузка CSV файла"), close_button=True),
            dbc.ModalBody([
                dcc.Upload(
                    id='uploader-element',
                    children=html.Div([
                        'Перетащите или Выберите Файл'
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
                    multiple=False,
                    accept='.csv'
                ),
                dbc.Collapse(
                    [
                        dbc.Card(
                            [
                                html.I(id='filename-display-icon', className='bi bi-filetype-csv',
                                       style={'fontSize': '60px'}),
                                html.Div(id='filename-display-text', children='')
                            ],
                            style={'width': '25%', 'text-align': 'center', 'margin-bottom': '15px'}
                        ),
                    ],
                    id="filename-display",
                    is_open=False,
                ),
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
    [Output('filename-display-text', 'children'),
     Output('filename-display', 'is_open')],
    Input("uploader-element", "filename"),
)
def update_scv_file_name(filename):
    if filename:
        return filename, True
    else:
        return filename, False


@callback(
    [Output("uploader-csv", "is_open"),
     Output("dashboard-data", 'data')],
    [Input("confirm-csv-uploader", "n_clicks"),
     Input("upload-csv-btn", "n_clicks"),
     Input("uploader-element", "filename"),
     Input("dashboard-data", 'data')],
)
def toggle_csv_uploader(confirm_clicks, open_modal_clicks, filename: str, dashboard_data: dict):
    if "confirm-csv-uploader" == ctx.triggered_id and filename:
        dashboard_data['state'] = False
        return False, dashboard_data
    elif "upload-csv-btn" == ctx.triggered_id or dashboard_data["state"]:
        dashboard_data['state'] = True
        return True, dashboard_data
    else:
        return dashboard_data['state'], dashboard_data


def get_data_from_scv(contents, dashboard_data):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string).decode('utf-8')

    try:
        graph_tree = csv_handling.CSVHandler("Brusnika", decoded)
        elements = graph_tree.find_by_id('MAIN', method='bfs').get_elements(recursion=False)
        dashboard = Dashboard.query.get(dashboard_data["dashboard_id"])
        dashboard.graph_data = json.dumps(elements)
        converted_paths = {str(key): value for key, value in graph_tree.paths.items()}
        dashboard.graph_paths = json.dumps(converted_paths)
        dashboard.raw_data = decoded
        dashboard.graph_roots = '[id = "MAIN"]'
        db.session.commit()
        return elements, graph_tree
    except Exception as e:
        print(e)
        return dbc.Alert("There was an error processing the file.", color="danger")
