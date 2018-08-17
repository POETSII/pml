void receive_ack_traversal(network_node_state_t* deviceState, const network_node_properties_t* deviceProperties, const network_ack_message_t* message) {

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
		uint16_t discovered = deviceState->requests_tbl_discovered_sum[ind];

		if (callback == -1) {

			// this is the root request

			finished_iteration_cb(deviceState, deviceProperties, discovered);

		} else {

			handler_log(3, "Received all replies, sending ack back to parent %d (callback %d, discovered = %d) ...",
				parent, callback, discovered);

			ack_msg outgoing;

			outgoing.dst = parent;
			outgoing.callback = callback;
			outgoing.discovered = discovered;
			outgoing.visitor_id = message->visitor_id;

			if ((message->visitor_id == 1) && (parent == deviceState->parent)) {
				// handler_log(1, "Sending ack to %d (deviceState->parent = %d)", parent, deviceState->parent);
				reverse_visitor(deviceState, deviceProperties, discovered);
			}

			if (message->visitor_id == 0 && (discovered >= deviceState->nchildren))
				deviceState->nchildren = discovered;

			send_ack(deviceState, &outgoing);
		}

	}

}
