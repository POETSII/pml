if((deviceState->fin == 1) ^ (deviceState->finSent==1)) {
	*readyToSend |= RTS_FLAG_finished_out;
}
else if(deviceState->UpdatePending > 0) {  
	*readyToSend |= RTS_FLAG_update_out;
}
