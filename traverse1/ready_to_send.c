*readyToSend =
	(deviceState->msg_req_rts * RTS_FLAG_req_out) +
	(deviceState->msg_ack_rts * RTS_FLAG_ack_out);