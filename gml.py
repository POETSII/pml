#!/usr/bin/env python

from graph import Graph
from random import sample
from docopt import docopt
from operator import mul
from generator import generate_xml
from itertools import product
from collections import defaultdict

usage = """gml.py

Usage:
  gml.py [options] full <nodes>
  gml.py [options] tree <depth> <bfactor>
  gml.py [options] random <nodes> <edges>
  gml.py [options] line [--fold] <length>
  gml.py [options] grid [--fold] <length> <width>
  gml.py [options] cube [--fold] <length> <width> <height>
  gml.py [options] hypercube [--fold] <side>...

Options:
  -d, --directed  Produce directed graph.
  -i, --id=<id>   Specify instance name [default: graph].
  -c, --coords    Name nodes based on coordinates.

"""


def generate_tree(depth, bfactor):
    """Create a tree graph.

    Args:
        depth (int): tree depth.
        bfactor (int): branching factor.

    Returns:
        Graph: graph object.
    """

    edges = defaultdict(list)
    nodes, frontier = ["n"], ["n"]

    for _ in range(depth-1):
        new_frontier = []
        for node in frontier:
            children = ["%s-%d" % (node, ind) for ind in range(bfactor)]
            nodes += children
            edges[node] += children
            new_frontier += children
        frontier = new_frontier

    graph = Graph(nodes, edges)
    return graph


def generate_full(n):
    """Create a fully-connected graph.

    Args:
        n (int): number of nodes.

    Returns:
        Graph: graph object.

    """
    get_name = lambda ind: "n%d" % ind
    get_edges = lambda ind: range(ind + 1, n)
    nodes = map(get_name, range(n))
    edges = {get_name(ind): map(get_name, get_edges(ind)) for ind in range(n)}
    return Graph(nodes, edges)


def generate_random(nodes, edges):
    """Create a graph with random edges.

    Args:
        nodes (int): number of nodes.
        edges (int): number of edges.

    Returns:
        Graph: graph object.

    """
    nodes = ["n%d" % i for i in range(nodes)]
    edge_list = sample(list(product(nodes, nodes)), edges)
    return Graph(nodes, edge_list)


def generate_hypercube(sides, fold=False):
    """Create a hypercube graph.

    Args:
       sides ([int]): list of dimension lengths.
       fold (bool): fold all dimensions.

    Returns:
        Graph: graph object.

    """
    dimensions = len(sides)
    n = reduce(mul, sides, 1)  # n = product(sides)

    def get_weight(d):
        """Get weight of dimension.

        The weight of a dimension is the product of previous dimensions'
        lengths. For example, assume we have a hypercube with sides = [60, 60,
        24] (representing the seconds, minutes and hours of time). In this
        case, the weight of a second is 1, the weight of a minute is 1x60 = 60
        and the weight of an hour is 60x60 = 3600. Intuitively, the weight
        here is how many units of the smallest dimension does a unit of each
        dimension weigh (for the smallest dimension, it's 1 by definition).

        This function is used for calculating indices from hypercube
        coordinates.

        Args:
            d (int): index of dimension.

        Returns:
            int: weight of dimension `d`.

        """
        return reduce(mul, sides[:d], 1)

    def ind2sub(ind):
        """Convert a hypercube node index to a coordinate list.

        Args:
            ind (int): index.

        Returns:
            [int]: coordinates.

        """
        assert (0 <= ind < n), 'incorrect index %d (only %d nodes)' % (ind, n)

        subs = [None for _ in sides]
        remainder = ind

        for d in reversed(range(dimensions)):
            weight = get_weight(d)
            subs[d] = remainder / weight
            remainder -= subs[d] * weight

        return subs

    def sub2ind(subs):
        """Convert a list of hypercube coordinates to an index.

        Args:
            subs ([int]): coordinates.

        Returns:
            int: index.

        """
        in_range = [0 <= sub < side for sub, side in zip(subs, sides)]
        assert all(in_range), 'incorrect subindex list'
        return sum([subs[i] * get_weight(i) for i in range(dimensions)])

    # Create graph

    edges = defaultdict(list)
    nodes = range(n)

    for ind in nodes:
        subs = ind2sub(ind)
        for d in range(dimensions):
            last_along_dimension = subs[d] == sides[d] - 1
            if last_along_dimension and not fold: continue
            adjacent_subs = list(subs)
            adjacent_subs[d] = (adjacent_subs[d] + 1) % sides[d]
            adjacent_ind = sub2ind(adjacent_subs)
            edges[ind].append(adjacent_ind)

    graph = Graph(nodes, edges)

    # Rename nodes

    def get_node_name(ind):
        """Get coordinate-based node name.

        For example, 'n-1-2-3' where 1, 2 and 3 are node coordinates.

        Args:
            ind (int): node index.

        Returns:
            str: node name.

        """
        subs = ind2sub(ind)
        parts = map(str, subs)
        name = "n" + "_".join(parts)
        return name

    node_map = {ind: get_node_name(ind) for ind in range(n)}
    graph.map_node_names(node_map)
    return graph


def main():
    args = docopt(usage, version="gml.py v0.1")

    if args["random"]:
        nodes = int(args["<nodes>"])
        edges = int(args["<edges>"])
        graph = generate_random(nodes, edges)

    elif args["tree"]:
        depth = int(args["<depth>"])
        bfactor = int(args["<bfactor>"])
        graph = generate_tree(depth, bfactor)

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

    content = {"directed": args["--directed"], "instance": args["--id"]}

    if not args["--coords"]:
        graph.rename_nodes("n%d")

    print generate_xml("templates/files/base.graphml", graph, content=content)


if __name__ == "__main__":
    main()
