/*message->src       = deviceProperties->id;
message->callback  = deviceState->msg_req_callback;
message->iteration = deviceState->msg_req_iteration;
message->hoplimit  = deviceState->msg_req_hoplimit;

deviceState->msg_req_rts = 0;
*/

if (deviceState->req_buffer_ptr == 0) {
	// If this is executed, it is most likely due to an error in ready_to_send

	// TODO: find out why calling handler_exit here causes an error
	// handler_exit("Error, attempted to send while buffer is empty");
}

uint32_t ind = --(deviceState->req_buffer_ptr);

message->src = deviceProperties->id;
message->dst = deviceState->req_buffer_dst[ind];
message->callback = deviceState->req_buffer_callback[ind];
message->iteration = deviceState->req_buffer_iteration[ind];
message->hoplimit = deviceState->req_buffer_hoplimit[ind];
