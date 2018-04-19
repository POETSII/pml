#!/usr/bin/env python

from graph import Graph
from random import sample
from docopt import docopt
from exporter import generate_xml
from itertools import product

usage = """gml.py

Usage:
  gml.py random <nodes> <edges>
  gml.py ring <length>

"""

def generate(nodes, edges):
    """Create a graph with specified numbers of nodes and edges."""

    nodes = ["n%d" % i for i in range(nodes)]
    edge_list = sample(list(product(nodes, nodes)), edges)
    return Graph(nodes, edge_list)


def generate_ring(length):
    """Create a graph consisting of a chain of length 'length'."""

    nodes = ["n%d" % i for i in range(length)]
    edge_list = zip(nodes[:-1], nodes[1:]) + [(nodes[-1], nodes[0])]
    return Graph(nodes, edge_list)


def main():
    args = docopt(usage, version="gml.py v0.1")

    if args["random"]:
        nodes = int(args["<nodes>"])
        edges = int(args["<edges>"])
        graph = generate(nodes, edges)

    elif args["ring"]:
        length = int(args["<length>"])
        graph = generate_ring(length)

    print generate_xml("templates/files/ro.graphml", graph)


if __name__ == "__main__":
    main()
