from flask_login import current_user
from visual_organizational_structure.models import Dashboard
from visual_organizational_structure.dash_apps.organization_graph.layouts.graphs import get_tree_graph, node_info_collapse, layout_choose
from visual_organizational_structure.dash_apps.organization_graph.layouts.misc import show_csv_uploader, dashboard_menu_buttons
from dash import html, dcc
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

    if dashboard.graph_data:
        graph_elements = json.loads(dashboard.graph_data)
        state = False
    else:
        graph_elements = []
        state = True

    return html.Div(
        [
            dcc.Store(id="dashboard-data", data={"state": state, "dashboard_id": dashboard_id}),
            get_tree_graph([], graph_elements),
            show_csv_uploader(state),
            dashboard_menu_buttons,
            node_info_collapse
        ]
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
