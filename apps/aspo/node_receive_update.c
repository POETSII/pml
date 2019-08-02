#ifdef VERBOSEDEBUG
handler_log(2,"UPD_IN");
#endif

// FIXME
//deviceState->hc = 0;
//deviceState->active = 1;

if(message->rootIdx < graphProperties->rootCount) {
	if(message->hops+1 < deviceState->buff[message->rootIdx]) {
		deviceState->buff[message->rootIdx] = message->hops+1;
		if(deviceState->updated[message->rootIdx] == 0) {
			deviceState->updatePending++;
		}
		deviceState->updated[message->rootIdx] = 1;
	}
}
