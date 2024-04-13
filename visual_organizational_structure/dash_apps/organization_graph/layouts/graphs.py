import dash_cytoscape as cyto


def get_tree_graph(graph_elements=None):
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
            'roots': '[id = "nyc"]',  # Root node
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
        # Zoom configuration
        minZoom=0.5,
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
        stylesheet=[
            {
                'selector': 'node',  # Style for nodes
                'style': {
                    'background-color': 'rgba(0, 128, 0, 0.5)',  # Green with opacity
                    'shape': 'ellipse',  # Use ellipse shape for nodes
                    'width': 50,  # Set node width
                    'height': 50  # Set node height
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
    )
