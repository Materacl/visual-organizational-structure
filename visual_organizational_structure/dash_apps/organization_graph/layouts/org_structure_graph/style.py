default_node_style = {
    "selector": "node",
    "style": {
        'label': "data(label)",
        # Text
        'text-valign': 'center',
        'text-halign': 'center',
        'text-margin-y': '0px',
        'text-margin-x': '0px',
        'color': 'black',
        'font-size': '46px',
        'padding': '10px',
        'text-wrap': 'wrap',
        # Shape
        'shape': 'roundrectangle',
        'compound-sizing-wrt-labels': 'include',
        'width': 'label',
        'height': 'label',
        "opacity": 1,
        # Background
        'background-color': '#1f77b4',
        "background-opacity": 0,
        # Border
        "border-width": "3px",
        # Outline
        # "outline-width": "10px",
    }
}

employee_node_style = dict(default_node_style)
employee_node_style['style'] = dict(default_node_style['style'])
employee_node_style['selector'] = "[job_title]"
employee_node_style["style"]['label'] = "data(job_title)"

director_node_style = dict(employee_node_style)
director_node_style['style'] = dict(employee_node_style['style'])
director_node_style['selector'] = "[job_title = 'Директор']"
director_node_style["style"]['color'] = "red"

employee_info_node_style = {
    "selector": "[node_info]",
    "style": {
        'label': "data(node_info)",
        # Text
        'text-valign': 'center',
        'text-halign': 'center',
        'text-margin-y': '0px',
        'text-margin-x': '0px',
        'color': 'black',
        'font-size': '46px',
        'padding': '10px',
        'text-wrap': 'wrap',
        # Background
        'background-color': '#1f77b4',
        "background-opacity": 0,
    }
}

edge_style = {
        "selector": "edge",
        "style": {
            "width": 6,
            "line-style": "solid",
            "line-cap": "round",
            "line-fill": "linear-gradient",
            # Color
            "line-color": "black",
            "opacity": 1,
            "line-gradient-stop-colors": "black gray",
            "line-gradient-stop-positions": "50%",
            # Curve Style
            "curve-style": "taxi",
            'edge-distances': "node-position",
            "taxi-direction": "vertical",
            "taxi-turn": "150px",
            "taxi-turn-min-distance": "50px",
            # Arrows
            "target-arrow-shape": "triangle",
            "target-arrow-color": "black",
        },
    }

default_stylesheet = [
    default_node_style,
    employee_node_style,
    director_node_style,
    employee_info_node_style,
    edge_style,
    {
        "selector": ":selected",
        "style": {
            "border-width": 2,
            "border-color": "black",
            "border-opacity": 1,
            "opacity": 1,
            "label": "data(label)",
            "color": "green",
        },
    },
]
