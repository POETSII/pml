handler_log(2, "msg_req_rts = %d", deviceState->msg_req_rts);
handler_log(2, "msg_ack_rts = %d", deviceState->msg_ack_rts);
*readyToSend = deviceState->msg_req_rts || deviceState->msg_ack_rts;