def reduce_graph(graph, predicate):
    """Return a subset of graph with predicate(node) = True."""

    nodes = filter(predicate, graph["nodes"])
    edges = [ (node, set(dst for dst in graph["edges"][node] if dst in nodes))
        for node in nodes ]
    return {"nodes": nodes, "edges": dict(edges)}


def get_edge_list(graph):
    """Return a list of graph edges"""

    def get_sublist(source, destinations):
        return [(source, dest) for dest in destinations]

    sublists = [get_sublist(source, destinations)
        for source, destinations in graph["edges"].iteritems()]

    return sum(sublists, [])  # return flattened list
