import base64

import dash_bootstrap_components as dbc
from dash import dcc, html, State, Input, Output, callback
from dash.exceptions import PreventUpdate
from visual_organizational_structure.dash_apps.organization_graph.data import csv_handling

csv_uploader = dbc.Modal(
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
    is_open=False
)


@callback(
    [Output('filename-display-text', 'children'),
     Output('filename-display', 'is_open')],
    Input('uploader-element', 'contents'),
    State("uploader-element", "filename"),
)
def update_scv_file_name(contents, filename):
    if filename:
        return filename, True
    else:
        return filename, False


@callback(
    Output("uploader-csv", "is_open", allow_duplicate=True),
    Input("upload-csv-btn", "n_clicks"),
    prevent_initial_call=True
)
def toggle_csv_uploader(open_uploader_clicks):
    return True


def get_data_from_scv(contents: str):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string).decode('utf-8')

    graph_tree = csv_handling.CSVHandler(decoded)
    return graph_tree
