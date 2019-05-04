#ifdef VERBOSEDEBUG
handler_log(2,"UPD_OUT");
#endif

for(int i = 0; i < graphProperties->rootCount; i++) {
	if(deviceState->updated[i]) {
		message->rootIdx = i;
		message->hops = deviceState->buff[i];

		deviceState->updated[i] = 0;
		deviceState->updatePending--;
		break;
	}
}
