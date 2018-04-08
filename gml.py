#!/usr/bin/env python

from random import sample
from docopt import docopt
from graphs import get_edge_dict
from exporter import generate_xml
from itertools import product

usage = """gml.py

Usage:
  gml.py random <nodes> <edges>
  gml.py ring <length>

"""

template = r"""<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
  <graph id="G" edgedefault="directed">
    {%- for node in nodes %}
    <node id="{{ node }}"/>
    {%- endfor %}
    {%- for src, dst in edges %}
    <edge source="{{ src }}" target="{{ dst }}"/>
    {%- endfor %}
  </graph>
</graphml>
"""


def generate(nodes, edges):
    """Create a graph with specified numbers of nodes and edges."""

    nodes = ["n%d" % i for i in range(nodes)]
    edge_list = sample(list(product(nodes, nodes)), edges)
    edges = get_edge_dict(edge_list)
    graph = {"nodes": nodes, "edges": edges}
    return graph


def generate_ring(length):
    """Create a graph consisting of a chain of length 'length'."""

    nodes = ["n%d" % i for i in range(length)]
    edge_list = zip(nodes[:-1], nodes[1:]) + [(nodes[-1], nodes[0])]
    edges = get_edge_dict(edge_list)
    graph = {"nodes": nodes, "edges": edges}
    return graph


def main():
    args = docopt(usage, version="gml.py v0.1")

    if args["random"]:
        nodes = int(args["<nodes>"])
        edges = int(args["<edges>"])
        graph = generate(nodes, edges)

    elif args["ring"]:
        length = int(args["<length>"])
        graph = generate_ring(length)

    print generate_xml(template, graph)


if __name__ == "__main__":
    main()
