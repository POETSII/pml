{%- for msg in messages.keys() %}
bool pending_{{ msg }}_messages = deviceState->{{ msg }}_buffer_ptr > 0;
{%- endfor %}

*readyToSend =
	{%- for msg in messages.keys() %}
	(pending_{{ msg }}_messages ? RTS_FLAG_{{ msg }}_out : 0)
	{{- ';' if loop.last else ' +' -}}
	{% endfor %}
