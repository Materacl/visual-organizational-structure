import dash_bootstrap_components as dbc

dashboard_menu_buttons = dbc.ButtonGroup(
    [
        dbc.Button('Загрузить CSV', id='upload_csv_btn', n_clicks=0)
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