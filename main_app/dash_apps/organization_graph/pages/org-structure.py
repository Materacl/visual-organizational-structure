import dash
from dash import html, Input, Output, callback, State
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

# Register the Dash app page
dash.register_page(
    __name__,
    path='/',
    title='org-structure page',
    name='org-structure page'
)

# Nodes and edges definitions
nodes = [
    {
        'data': {'id': short, 'label': label}
    }
    for short, label in (
        ('la', 'Los Angeles'),
        ('nyc', 'New York'),
        ('to', 'Toronto'),
        ('mtl', 'Montreal'),
        ('van', 'Vancouver'),
        ('chi', 'Chicago'),
        ('bos', 'Boston'),
        ('hou', 'Houston')
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

graph_elements = nodes + edges

# Define the collapse component for node information
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

# Define the Dash app layout
layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-org-graph',
        layout={
            'name': 'breadthfirst',
            'roots': '[id = "nyc"]',
            'idealEdgeLength': 100,
            'nodeOverlap': 20,
            'refresh': 20,
            'fit': True,
            'padding': 30,
            'randomize': False,
            'componentSpacing': 100,
            'nodeRepulsion': 400000,
            'edgeElasticity': 100,
            'nestingFactor': 5,
            'gravity': 80,
            'numIter': 1000,
            'initialTemp': 200,
            'coolingFactor': 0.95,
            'minTemp': 1.0
        },
        minZoom=0.5,
        maxZoom=5,
        boxSelectionEnabled=True,
        responsive=True,
        style={'width': '100%', 'height': '100vh', 'position': 'fixed', 'top': 0, 'left': 0},
        elements=graph_elements,
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'background-color': 'rgba(0, 128, 0, 0.5)',  # Green with opacity
                    'shape': 'ellipse',  # Use ellipse shape for nodes
                    'width': 50,  # Set node width
                    'height': 50  # Set node height
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle'
                }
            }
        ]
    ),
    html.Div([
        dbc.Button('Button 1', id='button-1', n_clicks=0, style={'display': 'block', 'margin-bottom': '10px'}),
        dbc.Button('Button 2', id='button-2', n_clicks=0, style={'display': 'block'})
    ], style={'position': 'absolute', 'top': '50%', 'left': '10px', 'transform': 'translateY(-50%)'}),
    node_info_collapse
])


# Define Dash callbacks
@callback(Output('node-info-content', 'children'),
          Input('cytoscape-org-graph', 'tapNodeData'))
def update_node_info(data):
    if data:
        return html.P(f"You clicked on {data['label']}. Additional info can be shown here.")
    return None


@callback(
    Output('node-info-collapse', 'is_open'),
    Input('cytoscape-org-graph', 'tapNodeData'),
    Input('node-info-collapse', 'is_open'),
    State('node-info-collapse', 'children')
)
def toggle_collapse(data, is_open, current_node_data):
    if data:
        if data == current_node_data:
            return not is_open
        return True
    return False


@callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
          Input('cytoscape-org-graph', 'mouseoverNodeData'))
def displayMouseoverNodeData(data):
    if data:
        return "You recently hovered over the city: " + data['label']


@callback(Output('cytoscape-tapNodeData-output', 'children'),
          Input('cytoscape-org-graph', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        return "You recently clicked/tapped the city: " + data['label']


@callback(Output('cytoscape-selectedNodeData-markdown', 'children'),
          Input('cytoscape-org-graph', 'selectedNodeData'))
def displaySelectedNodeData(data_list):
    if data_list is None:
        return "No city selected."

    cities_list = [data['label'] for data in data_list]
    return "You selected the following cities: " + "\n* ".join(cities_list)