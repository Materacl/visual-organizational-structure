from flask_login import current_user
from visual_organizational_structure.models import Dashboard
import visual_organizational_structure.dash_apps.organization_graph.layouts.org_structure_graph as org_structure_graph
import visual_organizational_structure.dash_apps.organization_graph.layouts.menu_buttons as menu_buttons
import visual_organizational_structure.dash_apps.organization_graph.layouts.csv_uploader as csv_uploader
from dash import html, dcc
import dash
import json

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
            org_structure_graph.get_tree_graph([], graph_elements),
            csv_uploader.csv_uploader(state),
            menu_buttons.dashboard_menu_buttons,
            org_structure_graph.node_info_collapse
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
