bool finished = deviceState->counter >= 10;

if (finished) {

	handler_exit(0);

} else {

	handler_log(1, "counter = %d", ++(deviceState->counter));

	// toggle state:
	deviceState->state = 1 - deviceState->state;

	// send message to next node:
	toggle_msg outgoing;
	outgoing.dst = 0xFFFFFFFF; // broadcast
	send_toggle(deviceState, &outgoing);

}
