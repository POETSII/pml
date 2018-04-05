from jinja2 import Template
from graphs import get_edge_list


def load_text(file):
    with open(file, "r") as fid:
        return fid.read()


def generate_xml(template_file, graph):

    template_str = load_text(template_file)
    template = Template(template_str)

    # Create and pass a node_info dict instead of graph['node'] (this contains
    # node indices as well as node names). Pass graph['edges'] as is.

    node_info = [
        {"name": name, "index": ind}
        for ind, name in enumerate(graph["nodes"])
    ]

    content = {
        "node_info": node_info,
        "edges": get_edge_list(graph)
    }

    print template.render(**content)
