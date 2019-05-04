if(deviceState->active && (deviceState->finSent==0)) {
	deviceState->hc++;

	#ifdef VERBOSEDEBUG
	handler_log(2,"HB_REC");
	#endif

	if(deviceState->hc >= deviceProperties->hcMax) {
		deviceState->fin = 1;
	}
}
else {
	#ifdef VERBOSEDEBUG
	//handler_log(2,"HB_IGN");
	#endif        
}
