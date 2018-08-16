void init_traversal(
		network_node_state_t* deviceState,
		const network_node_properties_t* deviceProperties
	) {

	soft_clear_state(deviceState, deviceProperties);
	deviceState->operation_counter = 0;

}
