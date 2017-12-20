from jinja2 import Template


def load_text(file):
    with open(file, "r") as fid:
        return fid.read()


def generate_xml(template_file, graph):
    template_str = load_text(template_file)
    template = Template(template_str)
    content = {
        "nodes": graph["nodes"],
        "edges": get_edge_list(graph)
    }
    print template.render(**content)
