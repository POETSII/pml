#!/usr/bin/env python

import sys
from docopt import docopt
import xml.etree.ElementTree as ET

usage = """pml.py

Usage:
  pml.py [--verbose] <file.graphml>
  pml.py enable <nodes> [--verbose] <file.graphml>
  pml.py disable <nodes> [--verbose] <file.graphml>
  pml.py --version
  pml.py --help

Options:
  --verbose  Print graph traversal information.
"""

def load_graphml(file):
	# load file
	try:
		root = ET.parse(file).getroot()[0]
	except IOError:
		print "File not found: %s" % file
		sys.exit(1)
	# parse nodes
	namespaces = {"graphml": "http://graphml.graphdrawing.org/xmlns"}
	get_node_name = lambda e_node : e_node.attrib["id"]
	nodes = map(get_node_name, root.findall("graphml:node", namespaces))
	# create, populate and return graph
	edges = {n:set() for n in nodes}
	for e in root.findall("graphml:edge", namespaces):
		n1 = e.attrib["source"]
		n2 = e.attrib["target"]
		edges[n1].add(n2)
		edges[n2].add(n1)
	graph = {
		"nodes": nodes,
		"edges": edges
	}
	return graph

def calculate_avg_path_length(graph, verbose=False):
	total_pl_sum = 0
	def log(msg):
		if verbose:
			print msg
	for n in graph["nodes"]:
		log("Searching from node: %s" % n)
		visited = set([n])
		to_visit = graph["edges"][n]
		depth = 1
		node_plsum = 0
		while to_visit:
			node_plsum += depth * len(to_visit)
			visited |= to_visit
			new_to_visit = set()
			for m in to_visit:
				new_to_visit |= graph["edges"][m]
			to_visit = new_to_visit - visited
			log("  at depth = %d, discovered: %s" % (depth, list(to_visit)))
			depth += 1
		log("  sum of node path distances = %d" % node_plsum)
		total_pl_sum += node_plsum
	return total_pl_sum

def disable_nodes(graph, disabled_node_str):
	disabled = disabled_node_str.split(" ")
	# filter out disabled nodes from node list
	graph["nodes"] = [n for n in graph["nodes"] if n not in disabled]
	# filter out disabled nodes from node edges
	is_enabled = lambda n : n not in disabled
	new_edges = {}
	for n in graph["nodes"]:
		new_edges[n] = set(filter(is_enabled, graph["edges"][n]))
	graph["edges"] = new_edges

def enable_nodes(graph, enabled_node_str):
	enabled = enabled_node_str.split(" ")
	disabled = [n for n in graph["nodes"] if n not in enabled]
	disable_nodes(graph, " ".join(disabled))

def main():
	args = docopt(usage, version="pml.py ver 1.0")
	file = args["<file.graphml>"]
	graph = load_graphml(file)
	if args["disable"]:
		disable_nodes(graph, args["<nodes>"])
	if args["enable"]:
		enable_nodes(graph, args["<nodes>"])
	verbose = args["--verbose"]
	print calculate_avg_path_length(graph, verbose)

if __name__ == "__main__":
	main()
