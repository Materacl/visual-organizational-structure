import dash
from dash import html, Input, Output, callback, dcc
import dash_cytoscape as cyto

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

elements = nodes + edges
graph_elements = nodes + edges

layout = html.Div([
    # Grid-like cell background
    html.Div(
        style={
            'position': 'fixed',
            'width': '100%',
            'height': '100%',
            'background-image': 'linear-gradient(90deg, #ccc 1px, transparent 1px), linear-gradient(180deg, #ccc 1px, transparent 1px)',
            'background-size': '20px 20px',
            'background-position': '0 0, 0 0',
            'background-attachment': 'fixed'
        }
    ),
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
        elements=graph_elements
    ),
    html.Div([
        html.Button('Button 1', id='button-1', n_clicks=0, style={'display': 'block', 'margin-bottom': '10px'}),
        html.Button('Button 2', id='button-2', n_clicks=0, style={'display': 'block'})
    ], style={'position': 'absolute', 'top': '50%', 'left': '10px', 'transform': 'translateY(-50%)'})
])


@callback(Output('cytoscape-tapNodeData-output', 'children'),
          Input('cytoscape-org-graph', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        return "You recently clicked/tapped the city: " + data['label']


@callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
          Input('cytoscape-org-graph', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        return "You recently hovered over the city: " + data['label']


@callback(Output('cytoscape-selectedNodeData-markdown', 'children'),
          Input('cytoscape-org-graph', 'selectedNodeData'))
def displaySelectedNodeData(data_list):
    if data_list is None:
        return "No city selected."

    cities_list = [data['label'] for data in data_list]
    return "You selected the following cities: " + "\n* ".join(cities_list)
