bool is_root = deviceProperties->id == 0;

deviceState->state = 0;
deviceState->counter = is_root ? 1 : 0;

if (is_root) {
	// send initial message
	toggle_msg outgoing;
	outgoing.dst = 0xFFFFFFFF; // broadcast
	send_toggle(deviceState, &outgoing);
}