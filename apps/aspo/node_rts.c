if((deviceState->fin == 1) ^ (deviceState->finSent==1)) {
	*readyToSend |= RTS_FLAG_finished_out;
}
else if(deviceState->active==0 || deviceState->updatePending > 0) {
	deviceState->hc = 0;
	deviceState->active = 1;
	*readyToSend |= RTS_FLAG_update_out;
}
