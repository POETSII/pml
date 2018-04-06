from collections import defaultdict

def reduce_graph(graph, predicate):
    """Return a subset of graph with predicate(node) = True."""

    nodes = filter(predicate, graph["nodes"])
    edges = [ (node, set(dst for dst in graph["edges"][node] if dst in nodes))
        for node in nodes ]
    return {"nodes": nodes, "edges": dict(edges)}


def get_edge_list(graph):
    """Return a list of graph edges"""

    result = list()

    for src, destinations in graph["edges"].iteritems():
        for dst in destinations:
            result.append((src, dst))

    return result


def get_edge_dict(edge_list):
    """Return an edge dict given an input list of edges."""

    edge_dict = defaultdict(list)

    for src, dst in edge_list:
        edge_dict[src].append(dst)

    return edge_dict