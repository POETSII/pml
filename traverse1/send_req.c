message->src       = deviceProperties->id;
message->callback  = deviceState->msg_req_callback;
message->iteration = deviceState->msg_req_iteration;
message->hoplimit  = deviceState->msg_req_hoplimit;

deviceState->msg_req_rts = 0;
