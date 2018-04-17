message->src = deviceProperties->id;
message->dst = deviceState->msg_ack_dst;
message->callback = deviceState->msg_ack_callback;
message->discovered = deviceState->msg_ack_discovered;

deviceState->msg_ack_rts = 0;
