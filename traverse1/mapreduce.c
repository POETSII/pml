// Middleware to perform MapReduce-style computations on networks

#define NODE_ARGS network_node_state_t* deviceState, const network_node_properties_t* deviceProperties
#define forward(CALLBACK) _forward_traverse(CALLBACK, deviceState, deviceProperties)
typedef void (*traverse_handler)(NODE_ARGS);
traverse_handler current_cb;

void start_traversal(NODE_ARGS) {
	deviceState->discovered_counts[0] = 1; // just center node is at distance 0
	handler_log(2, "Start traversal");
	start_iteration(deviceState, 1);
}

void _forward_traverse(traverse_handler handler, NODE_ARGS) {
	(deviceState->operation_counter)++;
	current_cb = handler;
	soft_clear_state(deviceState, deviceProperties);
	start_traversal(deviceState, deviceProperties);
}

void next_operation(NODE_ARGS) {
	traverse_handler cb = current_cb;
	current_cb = 0;
	if (cb)
		cb(deviceState, deviceProperties);
}

// (user supplied logic):

{{ include('netapp.c') }}