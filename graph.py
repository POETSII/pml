from xml.etree import ElementTree as ET
from collections import defaultdict


class Graph():
    def __init__(self, *args):
        """Initialize graph.

        Supports the following types of initializations:
            g = Graph(graphml_file)
            g = Graph(nodes, edges)

        where:
            graphml_file (str): path to source GraphML file.
            nodes (list): list of node objects.
            edges (list): list of edges, each as (node, node).

        `edges` can alternatively be provided as a dict(node -> node).

        """

        signature = tuple(map(type, args))

        handlers = {
            (str,): self._load_graphml,
            (list, list): self._init_nodes_edges,
            (list, dict): self._init_nodes_edges,
            (list, defaultdict): self._init_nodes_edges
        }

        assert signature in handlers, 'Unsupported arguments %s' % str(
            signature)
        handlers[signature](*args)

    def _init_nodes_edges(self, nodes, edges):
        self.nodes = nodes
        if type(edges) is list: self.set_edge_list(edges)
        else: self.edges = edges

    def _load_graphml(self, graphml_file):
        """Load nodes and edges from a GraphML file.

        Args:
            graphml_file (str): Path to file.

        """

        root = ET.parse(graphml_file).getroot()[0]
        namespaces = {"graphml": "http://graphml.graphdrawing.org/xmlns"}
        edge_default = root.attrib.get("edgedefault", "directed")

        self.nodes = [
            node.attrib["id"]
            for node in root.findall("graphml:node", namespaces)
        ]

        edge_list = [(e.attrib["source"], e.attrib["target"])
                     for e in root.findall("graphml:edge", namespaces)]

        if edge_default == "undirected":
            reversed_edges = [(dst, src) for src, dst in edge_list]
            edge_list += reversed_edges

        self.set_edge_list(edge_list)

    def set_edge_list(self, edge_list):
        """Load edges from an edge list.

        Args:
            edge_list ([(node, node)]): edge list.

        """
        self.edges = defaultdict(set)

        for src, dst in edge_list:
            self.edges[src].add(dst)

    def reduce_graph(self, predicate):
        """Return a copy graph with a subset of nodes.

        Each node is part of the returned graph iff predicate(node) is True.

        Args:
            predicate (callable :: node -> bool)

        Returns:
            Graph: graph object.

        """

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
        """Return outdegree of `node`."""
        return len(self.edges[node])

    def map_node_names(self, name_map):
        """Rename graph nodes based on a name map.

        Args:
            name_map (dict (node -> node)): name mapping dictionary.

        """
        def rename_edge(edge):
            src, dst = edge
            return (name_map[src], name_map[dst])

        new_edge_list = map(rename_edge, self.get_edge_list())

        self.nodes = sorted(name_map.values())
        self.set_edge_list(new_edge_list)

    def rename_nodes(self, name_format="n%d"):
        """Rename graph nodes using indices.

        Args:
            name_format (str): node renaming format (must contain '%d').

        """
        name_map = {
            node: name_format % ind
            for ind, node in enumerate(self.nodes)
        }

        self.map_node_names(name_map)
