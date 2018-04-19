deviceState->state = 0;
deviceState->counter = 0;

bool is_root = deviceProperties->id == 0;

if (is_root){

	deviceState->counter = 1;

	// send message to next node:
	toggle_msg outgoing;
	outgoing.dst = 0xFFFFFFFF; // broadcast
	send_toggle(deviceState, &outgoing);

}