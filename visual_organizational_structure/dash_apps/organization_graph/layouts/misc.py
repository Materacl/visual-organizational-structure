import dash_bootstrap_components as dbc
from dash import dcc, html

dashboard_menu_buttons = dbc.ButtonGroup(
    [
        dbc.Button('Button 1', id='button-1', n_clicks=0),
        dbc.Button('Button 2', id='button-2', n_clicks=0)
    ],
    style={
        'position': 'absolute',
        'top': '50%',
        'left': '10px',
        'transform': 'translateY(-50%)'
    },
    size="md",
    vertical=True,
)


def show_csv_uploader(state=False):
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
                    },
                    multiple=False
                ),
                html.Div(id='filename-display', children='')
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
