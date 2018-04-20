#!/usr/bin/env python

from graph import Graph
from random import sample
from docopt import docopt
from operator import mul
from exporter import generate_xml
from itertools import product
from collections import defaultdict

usage = """gml.py

Usage:
  gml.py [options] full <nodes>
  gml.py [options] random <nodes> <edges>
  gml.py [options] line [--fold] <length>
  gml.py [options] grid [--fold] <length> <width>
  gml.py [options] cube [--fold] <length> <width> <height>
  gml.py [options] hypercube [--fold] <side>...

Options:
  -d, --directed  Produce directed graph.
  -i, --id=<id>   Specify instance name [default: graph].
  -c, --indices   Name nodes based on indices.

"""

def normalize_node_names(graph):
    """Return isomorphic graph instance with node names
    in the form n1, n2 ..."""

    nodes = graph.nodes
    edge_list = graph.get_edge_list()

    node_d = {
        node: "n%d" % ind
        for ind, node in enumerate(nodes)
    }

    ren_e = lambda (src, dst): (node_d[src], node_d[dst])

    new_edge_list = map(ren_e, edge_list)
    new_nodes = sorted(node_d.values())

    result = Graph(new_nodes, new_edge_list)
    return result

def generate_full(n):
    """Create a fully connected topology."""
    get_name = lambda ind: "n%d" % ind
    get_edges = lambda ind: range(ind+1, n)
    nodes = map(get_name, range(n))
    edges = {get_name(ind): map(get_name, get_edges(ind)) for ind in range(n)}
    return Graph(nodes, edges)


def generate_random(nodes, edges):
    """Create a graph with specified numbers of nodes and edges."""

    nodes = ["n%d" % i for i in range(nodes)]
    edge_list = sample(list(product(nodes, nodes)), edges)
    return Graph(nodes, edge_list)


def generate_hypercube(sides, fold=False):
    """Return a hypercube topology with given side length and dimensionality.

    Dimensions are folded iff fold is True.
    """

    dimensions = len(sides)

    n = reduce(mul, sides, 1)  # n = product(sides)

    def get_weight(d):
        """Get weight of dimension."""
        return reduce(mul, sides[:d], 1)

    def ind2sub(ind):
        if not (0 <= ind < n):
            raise Exception("incorrect index %d (only %d nodes)" % (ind, n))

        subs = [None for _ in sides]
        remainder = ind

        for d in reversed(range(dimensions)):
            weight = get_weight(d)
            subs[d] = remainder / weight
            remainder -= subs[d] * weight

        return subs

    def sub2ind(subs):
        in_range = [0 <= sub < side for sub, side in zip(subs, sides)]

        if not all(in_range):
            raise Exception("incorrect subindex list")

        return sum([subs[i] * get_weight(i) for i in range(dimensions)])


    def move(index, dimension, distance):
        subs = ind2sub(index)
        subs[dimension] += distance
        return sub2ind(subs)

    def move_till_side(index, dimension, direction):
        subs = ind2sub(index)
        subs[dimension] = (sides[dimension] - 1) if (direction == 1) else 0
        return sub2ind(subs)

    def get_node_name(index):
        subs = ind2sub(index)
        parts = map(str, subs)
        name = "n" + "-".join(parts)
        return name

    nodes = map(get_node_name, range(n))
    edges = defaultdict(list)

    for i in range(n):
        node = get_node_name(i)
        subs = ind2sub(i)

        def add_neighbour(ind):
            name = get_node_name(ind)
            edges[node].append(name)

        for d in range(dimensions):

            if subs[d] < sides[d] - 1:
                add_neighbour(move(i, d, 1))  # positive neighbour
            elif fold:
                add_neighbour(move_till_side(i, d, -1))

    # remove duplicates
    edges = {src: list(set(dsts)) for src, dsts in edges.iteritems()}
    graph = Graph(nodes, edges)

    return graph


def main():
    args = docopt(usage, version="gml.py v0.1")

    if args["random"]:
        nodes = int(args["<nodes>"])
        edges = int(args["<edges>"])
        graph = generate_random(nodes, edges)

    if args["full"]:
        nodes = int(args["<nodes>"])
        graph = generate_full(nodes)

    elif args["line"]:
        length = int(args["<length>"])
        fold = args["--fold"]
        graph = generate_hypercube([length], fold)

    elif args["grid"]:
        length = int(args["<length>"])
        width = int(args["<width>"])
        fold = args["--fold"]
        graph = generate_hypercube([length, width], fold)

    elif args["cube"]:
        length = int(args["<length>"])
        width = int(args["<width>"])
        height = int(args["<height>"])
        fold = args["--fold"]
        graph = generate_hypercube([length, width, height], fold)

    elif args["hypercube"]:
        sides = map(int, args["<side>"])
        fold = args["--fold"]
        graph = generate_hypercube(sides, fold)

    content = {
        "directed": args["--directed"],
        "instance": args["--id"]
    }

    if args["--indices"]:
        graph = normalize_node_names(graph)

    print generate_xml("templates/files/base.graphml", graph, content=content)


if __name__ == "__main__":
    main()
