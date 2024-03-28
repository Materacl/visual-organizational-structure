import dash
from dash import html

dash.register_page(
    __name__,
    path='/support',
    title='support page',
    name='support page'
)

layout = html.Div([
    html.H1('This is our support page'),
    html.Div('This is our support page content.'),
])