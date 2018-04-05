import xml.etree.ElementTree as ET

def load_graphml(file):

    # load file
    try:
        root = ET.parse(file).getroot()[0]
    except IOError:
        raise Exception("File not found: %s" % file)

    namespaces = {"graphml": "http://graphml.graphdrawing.org/xmlns"}
    get_node_name = lambda e_node : e_node.attrib["id"]
    nodes = map(get_node_name, root.findall("graphml:node", namespaces))

    # create, populate and return graph
    edges = {n:set() for n in nodes}

    for e in root.findall("graphml:edge", namespaces):
        src = e.attrib["source"]
        dst = e.attrib["target"]
        edges[src].add(dst)

    graph = {
        "nodes": nodes,
        "edges": edges
    }

    return graph
