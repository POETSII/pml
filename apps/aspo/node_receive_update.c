#ifdef VERBOSEDEBUG
handler_log(2,"UPD_IN");
#endif

// TODO: deviceState->buff needs to be initialised to MAX_INT
// except for deviceState->buff[self] = 0

if(message->rootIdx < graphProperties->rootCount) {
	if(message->hops < deviceState->Buff[message->rootIdx]) {
		deviceState->buff[message->rootIdx] = message->hops;
		if(deviceState->updated[message->rootIdx] == 0) {
			deviceState->updatePending++;
		}
		deviceState->updated[message->rootIdx] = 1;
	}
}
