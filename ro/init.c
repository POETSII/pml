bool is_root = deviceProperties->id == 0;

deviceState->state = is_root ? 1 : 0;
deviceState->counter = 0;

if (is_root) {

	handler_log(1, "counter = %d", ++(deviceState->counter));

	// send initial message
	toggle_msg outgoing;
	outgoing.dst = 0xFFFFFFFF; // broadcast
	send_toggle(deviceState, &outgoing);
}