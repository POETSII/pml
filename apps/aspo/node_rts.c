if((deviceState->fin == 1) ^ (deviceState->finSent==1)) {
	*readyToSend |= RTS_FLAG_finished_out;
}
else if(deviceState->updatePending > 0 || (deviceState->active==0 && deviceProperties->rootIdx>=0)) {
	*readyToSend |= RTS_FLAG_update_out;
}
