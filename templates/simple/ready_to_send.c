*readyToSend =
	{%- for msg in messages.keys() %}
	(deviceState->msg_{{ msg }}_rts * RTS_FLAG_{{ msg }}_out)
	{{- ';' if loop.last else '+'}}
	{% endfor %}
