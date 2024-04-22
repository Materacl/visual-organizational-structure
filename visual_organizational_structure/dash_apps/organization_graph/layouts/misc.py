import dash_bootstrap_components as dbc
from dash import dcc, html

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

csv_uploader = dbc.Collapse(
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    id='csv_uploader',
    is_open=True
)
