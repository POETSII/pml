if (deviceState->{{ msg }}_buffer_ptr == 0) {
	// If this is executed, it is most likely due to an error in ready_to_send

	// TODO: find out why calling handler_exit here causes an error
	// handler_exit("Error, attempted to send while buffer is empty");
}

uint32_t ind = --(deviceState->{{ msg }}_buffer_ptr);

message->src = deviceProperties->id;
message->dst = deviceState->{{ msg }}_buffer_dst[ind];


// {{content}}

{% for fd_id in fields.keys() %}
message->{{ fd_id }} = deviceState->{{ msg }}_buffer_{{ fd_id }}[ind];
{% endfor %}
