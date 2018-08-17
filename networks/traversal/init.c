void init_traversal(network_node_state_t* deviceState, const network_node_properties_t* deviceProperties) {

	soft_clear_state(deviceState, deviceProperties);
	deviceState->last_operation = 0;
	deviceState->parent = -1;
	deviceState->nchildren = 0;
	deviceState->diameter = -1;
}
