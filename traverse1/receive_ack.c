if (message->dst != deviceProperties->id)
	return; // node is not the intended recipient of this message

uint32_t ind = message->callback;

handler_log(2, "received ack from %d (callback %d)", message->src, ind);

if (deviceState->requests_tbl_occupied[ind] == 0) {
	handler_log(2, "Error, invalid callback! Slot %d in requests table is empty", ind);
	handler_exit(1);
}

uint32_t replies = ++(deviceState->requests_tbl_replies_received[ind]);

uint32_t required_replies = deviceProperties->outdegree;

handler_log(2, "%d/%d replies for this request so far", replies, required_replies);

if (replies == required_replies) {

	uint32_t parent = deviceState->requests_tbl_requester[ind];
	int32_t callback = deviceState->requests_tbl_callback[ind];
	uint32_t discovered = 0; // for now

	if (callback == -1) {

		// this is the root request

		handler_log(2, "Traversal completed");

		handler_exit(0);

	} else {

		handler_log(2, "Received all replies, sending ack back to parent %d (callback %d) ...", parent, callback);

		deviceState->msg_ack_rts = 1;
		deviceState->msg_ack_callback = callback;
		deviceState->msg_ack_discovered = discovered;
		deviceState->msg_ack_dst = parent;

	}

}
