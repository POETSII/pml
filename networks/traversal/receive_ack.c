void receive_ack_traversal(
		network_node_state_t* deviceState,
		const network_node_properties_t* deviceProperties,
		const network_ack_message_t* message
	) {

	uint32_t ind = message->callback;

	handler_log(4, "received ack from %d (callback %d)", message->src, ind);

	if (deviceState->requests_tbl_occupied[ind] == 0) {
		handler_log(1, "Error, invalid callback! Slot %d in requests table is empty", ind);
		handler_exit(1);
	}

	uint32_t replies = ++(deviceState->requests_tbl_replies_received[ind]);

	deviceState->requests_tbl_discovered_sum[ind] += message->discovered;

	uint32_t required_replies = deviceProperties->outdegree;

	handler_log(4, "%d/%d replies for this request so far", replies, required_replies);

	if (replies == required_replies) {

		uint32_t parent = deviceState->requests_tbl_requester[ind];
		int32_t callback = deviceState->requests_tbl_callback[ind];
		uint32_t discovered = deviceState->requests_tbl_discovered_sum[ind];

		if (callback == -1) {

			// this is the root request

			deviceState->discovered_counts[deviceState->iteration] = discovered;

			handler_log(2, "Iteration %d completed (total discovered = %d)", deviceState->iteration, discovered);

			bool cont = discovered > 0; // continue if non-zero nodes have been discovered

			if (cont) {

				uint32_t next_iteration = deviceState->iteration + 1;
				handler_log(1, "Start iteration %d", next_iteration);
				start_iteration(deviceState, next_iteration);

			} else {

				handler_log(2, "Traversal completed");

				uint32_t final_iteration = deviceState->iteration;

				uint32_t total_nodes = 0;

				for (uint32_t i=0; i < final_iteration; i++) {
					uint32_t discovered_i = deviceState->discovered_counts[i];
					handler_log(2, "Discovered at iteration %d = %d nodes", i, discovered_i);
					total_nodes += discovered_i;
				}

				handler_log(2, "Total discovered = %d nodes", total_nodes);
				handler_log(1, "Finished operation (%d)", deviceState->operation_counter);
				next_operation(deviceState, deviceProperties);
			}

		} else {

			handler_log(3, "Received all replies, sending ack back to parent %d (callback %d, discovered = %d) ...",
				parent, callback, discovered);

			ack_msg outgoing;

			outgoing.dst = parent;
			outgoing.callback = callback;
			outgoing.discovered = discovered;

			if (discovered)
				reverse_visitor(deviceState, deviceProperties, discovered);

			send_ack(deviceState, &outgoing);
		}

	}

}

