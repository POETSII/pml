if (deviceState->ack_buffer_ptr == 0) {
	// If this is executed, it is most likely due to an error in ready_to_send

	// TODO: find out why calling handler_exit here causes an error
	// handler_exit("Error, attempted to send while buffer is empty");
}

uint32_t ind = (deviceState->ack_buffer_ptr)--;

message->src = deviceProperties->id;
message->dst = deviceState->ack_buffer_dst[ind];
message->callback = deviceState->ack_buffer_callback[ind];
message->discovered = deviceState->ack_buffer_discovered[ind];
