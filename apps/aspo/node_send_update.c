#ifdef VERBOSEDEBUG
handler_log(2,"UPD_OUT");
#endif

if(deviceState->active==0 && deviceProperties->rootIdx>=0) {
	deviceState->buff[deviceProperties->rootIdx] = 0;
	message->rootIdx = deviceProperties->rootIdx;
	message->hops = 0;
}
else {
	for(uint32_t i = 0; i < graphProperties->rootCount; i++) {
		if(deviceState->updated[i]) {
			message->rootIdx = i;
			message->hops = deviceState->buff[i];

			deviceState->updated[i] = 0;
			deviceState->updatePending--;
			break;
		}
	}
}

deviceState->hc = 0;
deviceState->active = 1;
