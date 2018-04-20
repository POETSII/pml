#!/usr/bin/env python

import os
import json

from graph import Graph
from docopt import docopt
from random import sample
from random import randrange
from multiprocessing import Pool


usage = """asp.py

Usage:
  asp.py [options] apl <file.graphml>
  asp.py [options] apl enable <node_list> <file.graphml>
  asp.py [options] apl disable <node_list> <file.graphml>
  asp.py [options] impact <node_count> <trials> <file.graphml>

Options:
  -i, --info         Print graph traversal information.
  -w, --workers <n>  Use n parallel workers [default: 1].
  -p, --psuedo       Use psuedo-randomization.

"""


def main():

    args = docopt(usage, version="asp.py v0.1")
    graph = Graph(args["<file.graphml>"])

    if args["apl"]:

        # list enable/disable

        if args["<node_list>"]:
            nodes = args["<node_list>"].split()
            non_existent = set(nodes) - set(graph.nodes)
            if non_existent:
                raise Exception("Non-existent node(s): %s" ", ".join(non_existent))

        if args["disable"]:
            disabled = args["<node_list>"].split()
            graph = Graph.reduce_graph(lambda node: node not in disabled)

        if args["enable"]:
            enabled = args["<node_list>"].split()
            graph = Graph.reduce_graph(lambda node: node in enabled)

        print get_apl(graph, verbose=args["--info"])

    elif args["impact"]:

        # random enable/disable

        file = args["<file.graphml>"]
        trials = int(args["<trials>"])
        nworkers = int(args["--workers"])
        node_count = int(args["<node_count>"])
        method = "psuedo" if args["--psuedo"] else "random"

        # calculate how many trials to run in each of (nworkers) tasks

        trials_batch1 = trials / nworkers
        trials_batch2 = trials - trials_batch1 * (nworkers-1)

        trials_per_task = [trials_batch1] * (nworkers-1) + [trials_batch2]

        # construct task call arguments

        task_args = [{
            "file": file,
            "trials": trials,
            "m": node_count,
            "method": method
        } for trials in trials_per_task]

        pool = Pool(nworkers)
        task_results = pool.map(get_impact_list_kwargs, task_args)
        impact_list = sum(task_results, [])  # flatten list of lists

        print json.dumps(impact_list, indent=4)

    else:

        print get_apl(graph, verbose=args["--info"])


def read_json(file):
    with open(file, "r") as fid:
        return json.load(fid)


def read_plain(file):
    with open(file, 'r') as fid:
        return fid.read()


def get_impact(graph, disabled):
    """Calculate impact of disabling a subset of graph nodes"""
    n = len(graph.nodes)
    m = len(disabled)
    graph_mod = graph.reduce_graph(lambda node: node not in disabled)
    return get_apl(graph_mod) / float((n-m)*(n-m-1))


def get_impact_list_kwargs(kwargs):
    return get_impact_list(**kwargs)


def get_impact_list(file, trials=10, m=1, method="random"):

    """Run multiple trials in which m nodes are removed from a graph, and return
    list of corresponding impact figures."""

    graph = Graph(file)
    n = len(graph.nodes)

    def get_random_nodes():
        """Generate samples of m random nodes"""
        while True:
            yield sample(graph.nodes, m)

    def get_psuedo_random_nodes():
        """Generated samples of m psuedo-random nodes"""
        inds = sample(range(n), m)
        while True:
            shift = randrange(1, n)
            inds = [(x+shift) % n for x in inds]
            yield [graph.nodes[i] for i in inds]

    gens = {
        "random": get_random_nodes,
        "psuedo": get_psuedo_random_nodes
    }

    gen = gens[method]()

    def get_impact_w():
        disabled = next(gen)
        return get_impact(graph, disabled)

    return [get_impact_w() for _ in range(trials)]


def get_apl(graph, verbose=False):
    """Calculate average path length"""

    total_pl_sum = 0

    def log(msg):
        if verbose:
            print msg

    for n in graph.nodes:
        log("Searching from node: %s" % n)
        visited = {n}
        to_visit = graph.edges[n]
        depth, node_plsum = 1, 0
        while to_visit:
            node_plsum += depth * len(to_visit)
            visited |= to_visit
            new_to_visit = set()
            for m in to_visit:
                new_to_visit |= graph.edges[m]
            to_visit = new_to_visit - visited
            log("  at depth = %d, discovered: %s" % (depth, list(to_visit)))
            depth += 1
        log("  sum of node path distances = %d" % node_plsum)
        total_pl_sum += node_plsum
    return total_pl_sum


if __name__ == "__main__":
    main()
