// *readyToSend =
// 	{%- for msg in messages.keys() %}
// 	(deviceState->msg_{{ msg }}_rts * RTS_FLAG_{{ msg }}_out)
// 	{{- ';' if loop.last else '+'}}
// 	{% endfor %}

bool pending_ack_messages = deviceState->ack_buffer_ptr > 0;
bool pending_req_messages = deviceState->req_buffer_ptr > 0;

*readyToSend =
	(pending_req_messages ? RTS_FLAG_req_out : 0) +
	(pending_ack_messages ? RTS_FLAG_ack_out : 0);