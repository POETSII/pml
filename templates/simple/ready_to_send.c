// *readyToSend =
// 	{%- for msg in messages.keys() %}
// 	(deviceState->msg_{{ msg }}_rts * RTS_FLAG_{{ msg }}_out)
// 	{{- ';' if loop.last else '+'}}
// 	{% endfor %}

bool pending_ack_messages = deviceState->ack_buffer_ptr > 0;

*readyToSend =
	deviceState->msg_req_rts * RTS_FLAG_req_out +
	(pending_ack_messages ? RTS_FLAG_ack_out : 0);