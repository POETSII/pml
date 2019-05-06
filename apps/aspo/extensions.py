
def get_root_index(tile, id, node, graph, constants):
	root_count = constants['ROOT_COUNT']
	base_id = tile * root_count
	if (id >= base_id) and (id < base_id+root_count):
		return (id - base_id)
	else:
		return ''
