from flask_login import current_user
from visual_organizational_structure.models import Dashboard
import visual_organizational_structure.dash_apps.organization_graph.layouts.org_structure_graph as org_structure_graph
import visual_organizational_structure.dash_apps.organization_graph.layouts.menu as menu
import visual_organizational_structure.dash_apps.organization_graph.layouts.csv_uploader as csv_uploader
import visual_organizational_structure.dash_apps.organization_graph.layouts.graph_search as graph_search
from dash import html, dcc
import dash
import json
import dash_bootstrap_components as dbc

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
            dcc.Store(id="dashboard-data",
                      data={"state": state, "dashboard_id": dashboard_id}),
            org_structure_graph.get_tree_graph(graph_elements, roots='[id = "MAIN"]'),
            csv_uploader.csv_uploader(state),
            dbc.Navbar(
                dbc.Container(
                    [
                        dbc.Col(
                            graph_search.search_bar,
                        ),
                        dbc.Col(
                            menu.dashboard_menu_buttons,
                        ),
                    ],
                    style={'justify-content': 'space_between', 'gap': '15px'}
                ),
                color='transparent'
            ),
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
