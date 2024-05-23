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
        # Optimisation
        "min-zoomed-font-size": 6,
    }
}

default_node_selected_style = dict(default_node_style)
default_node_selected_style['style'] = dict(default_node_style['style'])
default_node_selected_style['selector'] = "node:selected"
default_node_selected_style["style"]['outline-width'] = 4
default_node_selected_style["style"]['outline-offset'] = 6
default_node_selected_style["style"]['outline-color'] = "blue"
default_node_selected_style["style"]["background-opacity"] = 1
default_node_selected_style["style"]['background-color'] = "white"
default_node_selected_style["style"]['z-index'] = 9999

employee_node_style = dict(default_node_style)
employee_node_style['style'] = dict(default_node_style['style'])
employee_node_style['selector'] = "[node_label]"
employee_node_style["style"]['label'] = "data(node_label)"

employee_selected_node_style = dict(default_node_selected_style)
employee_selected_node_style['style'] = dict(default_node_selected_style['style'])
employee_selected_node_style['selector'] = "node[full_data]:selected"
employee_selected_node_style["style"]['label'] = "data(full_data)"
employee_selected_node_style["style"]['line-height'] = 1


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
    default_node_selected_style,
    employee_node_style,
    edge_style,
    employee_selected_node_style,
    # {
    #     "selector": "node:selected",
    #     "style": {
    #         "border-width": 2,
    #         "border-color": "black",
    #         "border-opacity": 1,
    #         "opacity": 1,
    #         "label": "data(label)",
    #         "color": "black",
    #         "outline-width": 4,
    #         "outline-offset": 4,
    #         "outline-color": "blue",
    #     },
    # },
]
