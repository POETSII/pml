// (Queue) send functions

// Note: buffer pointers point to the next available slot

{%- for id, content in messages.items() %}
{%- set msg_struct = id + '_msg' %}
{%- set field_items = content.get('fields', {}).items() %}

struct {{ msg_struct }} {
	uint32_t src;
	uint32_t dst;
	{%- for f_id, f_content in field_items -%}
	{%- set f_type = f_content.get('type', 'uint32_t') %}
	{{ f_type }}  {{ f_id }};
	{%- endfor %}
};

void send_{{ id }}(node_state_t *deviceState, {{ msg_struct }} *msg) {

	uint32_t ind = (deviceState->{{ id }}_buffer_ptr)++;

	deviceState->{{ id }}_buffer_dst[ind] = msg->dst;

	{%- for f_id, f_content in field_items %}
	deviceState->{{ id }}_buffer_{{ f_id }}[ind] = msg->{{ f_id }};
	{% endfor %}

}

{%- endfor %}
