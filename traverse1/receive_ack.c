bool is_broadcast = message->dst == 0xFFFFFFFF;
bool is_intended_recipient = message->dst == deviceProperties->id;

if (!is_broadcast && !is_intended_recipient) return;

uint32_t ind = message->callback;

handler_log(2, "received ack from %d (callback %d)", message->src, ind);

if (deviceState->requests_tbl_occupied[ind] == 0) {
	handler_log(2, "Error, invalid callback! Slot %d in requests table is empty", ind);
	handler_exit(1);
}

uint32_t replies = ++(deviceState->requests_tbl_replies_received[ind]);

deviceState->requests_tbl_discovered_sum[ind] += message->discovered;

uint32_t required_replies = deviceProperties->outdegree;

handler_log(2, "%d/%d replies for this request so far", replies, required_replies);

if (replies == required_replies) {

	uint32_t parent = deviceState->requests_tbl_requester[ind];
	int32_t callback = deviceState->requests_tbl_callback[ind];
	uint32_t discovered = deviceState->requests_tbl_discovered_sum[ind];

	if (callback == -1) {

		// this is the root request

		deviceState->discovered_counts[deviceState->iteration] = discovered;

		handler_log(1, "Iteration %d completed (total discovered = %d)", deviceState->iteration, discovered);

		bool cont = discovered > 0; // continue if non-zero nodes have been discovered

		if (cont) {

			uint32_t next_iteration = deviceState->iteration + 1;
			handler_log(2, "Start iteration %d", next_iteration);
			start_iteration(deviceState, next_iteration);

		} else {

			handler_log(1, "Traversal completed");

			uint32_t final_iteration = deviceState->iteration;

			uint32_t total_nodes = 0;

			for (uint32_t i=0; i < final_iteration; i++) {
				uint32_t discovered_i = deviceState->discovered_counts[i];
				handler_log(1, "Discovered at iteration %d = %d nodes", i, discovered_i);
				total_nodes += discovered_i;
			}

			handler_log(1, "Total discovered = %d nodes", total_nodes);

			int OP_COUNT = 1000;

			if (deviceState->operation_counter >= OP_COUNT-1) {
				handler_log(3, "End of operations.");
				handler_exit(0);
			} else {
				(deviceState->operation_counter)++; // increment traversal counter
				soft_clear_state(deviceState, deviceProperties);
			}


		}

	} else {

		handler_log(2, "Received all replies, sending ack back to parent %d (callback %d, discovered = %d) ...",
			parent, callback, discovered);

		ack_msg outgoing;

		outgoing.dst = parent;
		outgoing.callback = callback;
		outgoing.discovered = discovered;

		send_ack(deviceState, &outgoing);

	}

}
