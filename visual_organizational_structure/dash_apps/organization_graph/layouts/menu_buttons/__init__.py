import dash_bootstrap_components as dbc

dashboard_menu_buttons = dbc.ButtonGroup(
    [
        dbc.Button('Загрузить файл', id='button-1', n_clicks=0),
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