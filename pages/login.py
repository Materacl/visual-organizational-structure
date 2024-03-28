import dash
from dash import html

dash.register_page(
    __name__,
    path='/login',
    title='Login page',
    name='Login page'
)

layout = html.Div([
    html.H1('This is our Login page'),
    html.Div('This is our Login page content.'),
])