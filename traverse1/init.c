soft_clear_state(deviceState, deviceProperties);

if (is_center_node(deviceProperties))
	handler_log(1, "Start (%d operations)", {{ constants["OPERATION_COUNT"] }});

deviceState->operation_counter = 0;