import xml.etree.ElementTree as ET
from collections import defaultdict

class Graph():

    def __init__(self, *args):
        # Supports two types of initialization:
        # 1. Graph(graphml_file)
        # 2. Graph(nodes, edges)

        handlers = {
            1: self.__init_graphml__,
            2: self.__init_nodes_edges__
        }

        def raise_invalid(*_):
            raise Exception("Invalid constructor arguments")

        handler = handlers.get(len(args), raise_invalid)
        handler(*args)

    def __init_graphml__(self, graphml_file):
        self.load_graphml(graphml_file)

    def __init_nodes_edges__(self, nodes, edges):
        self.nodes = nodes

        if type(edges) is dict:
            self.edges = edges
        else:
            self.set_edge_list(edges)

    def load_graphml(self, file):

        root = ET.parse(file).getroot()[0]

        namespaces = {"graphml": "http://graphml.graphdrawing.org/xmlns"}

        edge_default = root.attrib.get("edgedefault", "directed")

        is_directed = edge_default == "directed"

        self.nodes = {
            node.attrib["id"]
            for node in root.findall("graphml:node", namespaces)
        }

        edge_list = [
            (e.attrib["source"], e.attrib["target"])
            for e in root.findall("graphml:edge", namespaces)
        ]

        if is_directed:
            complete_list = edge_list
        else:
            flipped_list = [(dst, src) for src, dst in edge_list]
            complete_list = edge_list + flipped_list

        self.set_edge_list(complete_list)

    def set_edge_list(self, edge_list):
        self.edges =defaultdict(set)

        for src, dst in edge_list:
            self.edges[src].add(dst)

    def reduce_graph(self, predicate):
        """Return a subset of graph with predicate(node) = True."""

        nodes = filter(predicate, self.nodes)

        edge_list = [
            (src, dst) for src, dst in self.get_edge_list()
            if (src in nodes and dst in nodes)
            ]

        return Graph(nodes, edge_list)

    def get_edge_list(self):
        """Return a list of graph edges."""
        result = list()
        for src, destinations in self.edges.iteritems():
            for dst in destinations:
                result.append((src, dst))
        return result

    def get_node_list(self):
        return enumerate(self.nodes)

    def get_outdegree(self, node):
        """Return outdegree of a node."""
        return len(self.edges[node])
