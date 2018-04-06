from os import path
from jinja2 import Template
from graphs import get_edge_list


def load_text(file):
    with open(file, "r") as fid:
        return fid.read()


def generate_xml(template, graph):
    """Return an XML file (string) generated from 'graph' based on an XML
    template 'template'.

    'template' can either be a filename or a template string."""

    if path.isfile(template):
        template_str = load_text(template)
    else:
        template_str = template

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

    return Template(template_str).render(**content)
