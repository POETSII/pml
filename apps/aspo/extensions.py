
def get_root_index(tile, id, node, graph, constants):
	rootCount = constants['rootCount']
	base_id = tile * rootCount
	if (id >= base_id) and (id < base_id+rootCount):
		return (id - base_id)
	else:
		return ''
