import dash
from dash import html

dash.register_page(
    __name__,
    path='/org-structure',
    title='org-structure page',
    name='org-structure page'
)

layout = html.Div([
    html.H1('This is our org-structure page'),
    html.Div('This is our org-structure page content.'),
])