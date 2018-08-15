soft_clear_state(deviceState, deviceProperties);

deviceState->operation_counter = 0;

if (is_center_node(deviceProperties))
	root(deviceState, deviceProperties);
