import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback
from dash_cytoscape.utils import Tree


def filter_chooser(graph_tree: Tree = None, state: bool = False) -> dbc.Modal:
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Фильтр графа"), close_button=True),
            dbc.ModalBody(),
            dbc.ModalFooter(),
        ],
        id='graph-filter-window',
        centered=True,
        is_open=state
    )
