// (Queue) send functions

// Note: buffer pointers point to the next available slot

{%- for id, content in messages.items() %}

void send_{{ id }}(node_state_t *deviceState, {{ id }}_message_t *msg) {

	uint32_t ind = (deviceState->{{ id }}_buffer_ptr)++;

	deviceState->{{ id }}_buffer_src[ind] = msg->src;
	deviceState->{{ id }}_buffer_dst[ind] = msg->dst;

	{% for f_id, f_content in content['fields'].items() -%}
	deviceState->{{ id }}_buffer_{{ f_id }}[ind] = msg->{{ f_id }};
	{% endfor %}

}

{%- endfor %}
