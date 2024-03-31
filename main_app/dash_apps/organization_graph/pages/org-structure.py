import dash
from dash import html, Input, Output, callback, dcc
import dash_cytoscape as cyto

dash.register_page(
    __name__,
    path='/',
    title='org-structure page',
    name='org-structure page'
)
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
    html.H1('This is our org-structure page'),
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
        minZoom = 0.5,
        maxZoom = 5,
        boxSelectionEnabled = True,
        responsive=True,
        style={'width': '100%', 'height': '400px'},
        elements=graph_elements
    ),
    html.P(id='cytoscape-tapNodeData-output'),
    html.P(id='cytoscape-tapEdgeData-output'),
    html.P(id='cytoscape-mouseoverNodeData-output'),
    html.P(id='cytoscape-mouseoverEdgeData-output'),
    dcc.Markdown(id='cytoscape-selectedNodeData-markdown')
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

