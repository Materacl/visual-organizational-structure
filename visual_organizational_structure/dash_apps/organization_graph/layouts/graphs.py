import dash_cytoscape as cyto


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
            'roots': '[id = "LE0"]',  # Root node
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
    )
