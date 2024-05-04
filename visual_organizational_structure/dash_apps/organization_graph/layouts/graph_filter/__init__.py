import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback
from dash_cytoscape.utils import Tree


def filter_chooser(graph_tree: Tree = None):
    return html.Div(
        [
            dbc.Button(
                "Open collapse",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
                id="collapse",
                is_open=False,
            ),
        ]
    )


@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
