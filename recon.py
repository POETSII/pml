#!/usr/bin/env python

from asp import calculate_dist
from files import read_csv
from graph import Graph
from random import sample
from random import uniform
from collections import defaultdict


def choose(items):
    """Take random item from a set of items."""
    return sample(items, 1)[0]


def choose_biased(items, get_weight):

    weights = map(get_weight, items)
    r = uniform(0, sum(weights))

    upto = 0

    for item, weight in zip(items, weights):
        if upto + weight >= r:
            return item
        upto += weight

    raise Exception("Failed to choose_biased")


def reconstruct(dist, verbose=False):
    """Rconstruct a graph from a degree distribution."""

    counts = sum(dist.values())
    props = [dict()] * counts  # dict

    def choose_src(items):
        get_weight = lambda item: props[item]["remaining"]
        return choose_biased(list(items), get_weight)

    reps = [[degree] * count for degree, count in dist.iteritems()]
    reps_flat = sum(reps, [])  # flatten list of lists

    for index, degree in enumerate(reps_flat):
        props[index] = {"degree": degree, "remaining": degree}

    pool = set(ind for ind in range(counts))
    acc = set([choose_src(pool)])
    edges = defaultdict(set)

    max_retries = 10
    retries = 0
    iteration = 0

    while acc and pool:

        if verbose and iteration % 100 == 0:
            print("Iteration %d, |pool| = %d" % (iteration, len(pool)))

        iteration += 1
        retries += 1

        if retries >= max_retries*len(pool):
            break

        dst = choose(pool)
        src = choose_biased(list(acc), lambda item: props[item]["remaining"])

        if props[src]["remaining"] < 2:
            if props[dst]["remaining"] < 2:
                if len(acc) < 2:
                    continue

        if dst in edges[src]:
            continue

        retries = 0

        assert src not in edges[dst], "edge consistency issue"

        edges[src].add(dst)
        edges[dst].add(src)

        props[src]["remaining"] -= 1
        props[dst]["remaining"] -= 1

        if props[src]["remaining"] == 0:
            pool = pool - {src}
            acc = acc - {src}

        if props[dst]["remaining"] == 0:
            pool = pool - {dst}
            acc = acc - {dst}

        else:
            acc.add(dst)

    nodes = range(counts)
    return Graph(nodes, edges)


def print_dist(dist):
    for degree in range(max(dist)+1):
        count = dist[degree]
        print "%d, %d" % (degree, count)


def read_dist(csv_file):
    rows = read_csv(csv_file, int)
    dist = defaultdict(int)
    for degree, count in rows:
        dist[degree] = count
    return dist


def print_dist_diff(dist1, dist2):

    max1 = max(dist1.keys())
    max2 = max(dist2.keys())
    max_degree = max([max1, max2])

    for degree in range(max_degree+1):
        c1 = dist1[degree]
        c2 = dist2[degree]
        if c1 == c2:
            continue
        print "%d -> [%d, %d]" % (degree, c1, c2)


def main():
    dist = read_dist("n4_dist.csv")
    graph = reconstruct(dist)
    dist_new = calculate_dist(graph)
    print_dist(dist_new)


if __name__ == '__main__':
    main()