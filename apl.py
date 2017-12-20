def get_apl(graph, verbose=False):
    """Calculate average path length"""

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
