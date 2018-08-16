// Middleware to perform MapReduce-style computations on networks

#define STATE_PROP_ARGS network_node_state_t* deviceState, const network_node_properties_t* deviceProperties

typedef void (*callback_t)(STATE_PROP_ARGS);

callback_t current_cb = 0; // not initializing this causes memory errors

void start_traversal(STATE_PROP_ARGS) {
	deviceState->discovered_counts[0] = 1; // just center node is at distance 0
	handler_log(2, "Start traversal");
	start_iteration(deviceState, 1);
}

void forward_traverse(STATE_PROP_ARGS, callback_t cb) {
	(deviceState->operation_counter)++;
	current_cb = cb;
	soft_clear_state(deviceState, deviceProperties);
	start_traversal(deviceState, deviceProperties);
}

void next_operation(STATE_PROP_ARGS) {
	callback_t cb = current_cb;
	current_cb = 0;
	if (cb) cb(deviceState, deviceProperties);
}
