import jinja2
import os

def load_text(file):
    with open(file, "r") as fid:
        return fid.read()


def generate_xml(template, graph):
    """Generate xml string from xml template and graph object.

    'template' can either be a filename or a template string."""

    is_file = os.path.isfile(template)

    template_str = load_text(template) if is_file else template
    template_dir = os.path.split(template)[0] if is_file else '.'

    # Create jinja template content

    node_info = [
        {"name": name, "index": ind}
        for ind, name in enumerate(graph.nodes)
    ]

    content = {
        "node_info": node_info,
        "edges": graph.get_edge_list(),
        "graph": graph
    }

    # Prepare jinja environment (with include_file function)

    def include_file(file):
        full_file = os.path.join(template_dir, file)
        return generate_xml(full_file, graph)

    loader = jinja2.PackageLoader(__name__, '')
    env = jinja2.Environment(loader=loader)
    env.globals['include_file'] = include_file

    # Return rendered template

    return env.get_template(template).render(**content)
