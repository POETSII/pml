import xml.etree.ElementTree as ET
from collections import defaultdict


class Graph():
    def __init__(self, *args):
        # Supports two types of initialization:
        # 1. Graph(graphml_file)
        # 2. Graph(nodes, edges)

        signature = tuple(map(type, args))

        handlers = {
            (str): self._init_graphml,
            (list, list): self._init_nodes_edges,
            (list, dict): self._init_nodes_edges,
            (list, defaultdict): self._init_nodes_edges
        }

        assert signature in handlers, 'Unsupported arguments %s' % str(signature)
        handlers[signature](*args)

    def _init_graphml(self, graphml_file):
        self._load_graphml(graphml_file)

    def _init_nodes_edges(self, nodes, edges):
        self.nodes = nodes
        if type(edges) is dict: self.edges = edges
        if type(edges) is defaultdict: self.edges = edges
        else: self.set_edge_list(edges)

    def _load_graphml(self, file):

        root = ET.parse(file).getroot()[0]

        namespaces = {"graphml": "http://graphml.graphdrawing.org/xmlns"}

        edge_default = root.attrib.get("edgedefault", "directed")

        self.nodes = [
            node.attrib["id"]
            for node in root.findall("graphml:node", namespaces)
        ]

        edge_list = [(e.attrib["source"], e.attrib["target"])
                     for e in root.findall("graphml:edge", namespaces)]

        if edge_default == "directed":
            complete_list = edge_list
        else:
            flipped_list = [(dst, src) for src, dst in edge_list]
            complete_list = edge_list + flipped_list

        self.set_edge_list(complete_list)

    def set_edge_list(self, edge_list):
        self.edges = defaultdict(set)

        for src, dst in edge_list:
            self.edges[src].add(dst)

    def reduce_graph(self, predicate):
        """Return a subset of graph with predicate(node) = True."""

        nodes = filter(predicate, self.nodes)

        edge_list = [(src, dst) for src, dst in self.get_edge_list()
                     if (src in nodes and dst in nodes)]

        return Graph(nodes, edge_list)

    def get_edge_list(self):
        """Return a list of graph edges."""
        result = list()
        for src in sorted(self.edges.keys()):
            destinations = sorted(self.edges[src])
            for dst in destinations:
                result.append((src, dst))
        return result

    def get_outdegree(self, node):
        """Return outdegree of a node."""
        return len(self.edges[node])

    def map_node_names(self, name_map):

        def rename_edge(edge):
            src, dst = edge
            return (name_map[src], name_map[dst])

        new_edge_list = map(rename_edge, self.get_edge_list())

        self.nodes = sorted(name_map.values())
        self.set_edge_list(new_edge_list)


    def rename_nodes(self, name_format="n%d"):

        name_map = {
            node: name_format % ind
            for ind, node in enumerate(self.nodes)
        }

        self.map_node_names(name_map)

