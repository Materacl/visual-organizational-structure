from flask_login import current_user
from visual_organizational_structure.models import Dashboard
from visual_organizational_structure.dash_apps.organization_graph.layouts.graphs import get_tree_graph, dashboard_menu_buttons, layout_choose
from visual_organizational_structure.dash_apps.organization_graph.layouts.misc import csv_uploader, node_info_collapse
from dash import html
import dash
import json
import visual_organizational_structure.dash_apps.organization_graph.callbacks.org_structure_callbacks

# Register the Dash app page
dash.register_page(
    __name__,
    path_template="/org-structure/<dashboard_id>",
    title='org-structure page',
    name='org-structure page'
)


def layout(dashboard_id=None):
    dashboard = Dashboard.query.get(dashboard_id)

    if not dashboard or dashboard.user_id != current_user.id:
        return unauthorized_layout()

    graph_elements = json.loads(dashboard.graph_data) if dashboard.graph_data else []

    return html.Div(
        [
            get_tree_graph([], graph_elements),
            csv_uploader,
            dashboard_menu_buttons,
            node_info_collapse,
            layout_choose
        ],
        id="page_layout",
        title=dashboard_id
    )


def unauthorized_layout():
    return html.Div(
        "This is not your board.",
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'height': '100vh',
            'font-size': '2em'
        }
    )
