import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash import dcc, html

stylesheet1 = [
    {
        'selector': 'node',  # Style for nodes
        'style': {
            'label': 'data(label)',  # Updated to use 'label' from node data
            'text-valign': 'center',  # Center the text vertically
            'text-halign': 'center',  # Align the text to the center
            'text-margin-y': '0px',  # Adjust vertical text margin
            'text-margin-x': '0px',  # Adjust horizontal text margin
            'background-color': '#1f77b4',  # Change node color to a blue shade
            'color': 'white',  # Change text color to white
            'shape': 'roundrectangle',  # Use roundrectangle shape for nodes
            'width': 'label',  # Set node width based on label size
            'height': 'label',  # Set node height based on label size
            'font-size': '16px',  # Adjust font size
            'padding': '10px',  # Add padding to node
            'text-wrap': 'wrap'  # Allow text to wrap within node
        }
    },
    {
        'selector': 'edge',  # Style for edges
        'style': {
            'width': 3,
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle'
        }
    }
]

stylesheet2 = [
    {
        'selector': 'node',  # Style for nodes
        'style': {
            'label': 'data(label)',  # Updated to use 'label' from node data
            'text-valign': 'center',  # Center the text vertically
            'text-halign': 'center',  # Align the text to the center
            'text-margin-y': '0px',  # Adjust vertical text margin
            'text-margin-x': '0px',  # Adjust horizontal text margin
            'background-color': '#1f77b4',  # Change node color to a blue shade
            'color': 'white',  # Change text color to white
            'shape': 'roundrectangle',  # Use roundrectangle shape for nodes
            'width': 'label',  # Set node width based on label size
            'height': 'label',  # Set node height based on label size
            'font-size': '16px',  # Adjust font size
            'padding': '10px',  # Add padding to node
            'text-wrap': 'wrap'  # Allow text to wrap within node
        }
    },
    {
        'selector': '.nonterminal',
        'style': {
            'label': 'data(confidence)',
            'background-opacity': 0,
            "text-halign": "left",
            "text-valign": "top",
        }
    },
    {
        'selector': '.support',
        'style': {'background-opacity': 0}
    },
    {
        'selector': 'edge',
        'style': {
            "source-endpoint": "inside-to-node",
            "target-endpoint": "inside-to-node",
        }
    },
    {
        'selector': '.terminal',
        'style': {
            'label': 'data(name)',
            'width': 10,
            'height': 10,
            "text-valign": "center",
            "text-halign": "right",
            'background-color': '#222222'
        }
    }
]


def get_tree_graph(graph_roots=None, graph_elements=None):
    """
    Create and return a Cytoscape tree graph with specified layout and style.

    Parameters:
    - graph_elements (list, optional): List of node and edge elements for the graph.

    Returns:
    - dash_cytoscape.Cytoscape: Cytoscape tree graph object.
    """
    # Define the Cytoscape graph
    return cyto.Cytoscape(
        id='cytoscape-org-graph',
        # Layout configuration
        layout={
            'name': 'breadthfirst',  # Use 'breadthfirst' layout algorithm
            'roots': '[id = "MAIN"]',  # Root node
        },
        # Zoom configuration
        minZoom=0.1,
        maxZoom=5,
        # Enable box selection
        boxSelectionEnabled=True,
        # Make the graph responsive
        responsive=True,
        # Style configuration
        style={
            'width': '100%',  # Set width to 100%
            'height': '100vh',  # Set height to 100% of viewport height
            'position': 'fixed',  # Fixed position
            'top': 0,  # Top position
            'left': 0  # Left position
        },
        # Graph elements
        elements=graph_elements,
        # Stylesheet configuration
        stylesheet=stylesheet2
    )


node_info_collapse = dbc.Collapse(
    dbc.Card(
        [
            dbc.CardHeader("Node Information"),
            dbc.CardBody(html.Div(id='node-info-content'))
        ]
    ),
    id='node-info-collapse',
    is_open=False,
    style={'position': 'fixed', 'top': '10px', 'right': '10px', 'z-index': 1000}
)

layout_choose = dcc.Dropdown(
    id='dropdown-update-layout',
    value='breadthfirst',
    clearable=False,
    options=[
        {'label': name.capitalize(), 'value': name}
        for name in ['breadthfirst', 'random']
    ]
)
