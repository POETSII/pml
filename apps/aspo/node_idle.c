if(deviceState->active==0 && deviceProperties->rootIdx >= 0) {
	return(1);
}
if(deviceState->active==1 && deviceInstance->deviceID == 0) {
	if(heartbeatIndex > 9) { // Execute on every tenth OnIdle.
		heartbeatIndex = 0;
		P_Msg_t hbMsg;

		hbMsg.header.messageLenBytes = sizeof(P_Msg_Hdr_t); // HB is only a header.
		hbMsg.header.destEdgeIndex = 0;
		
		// Important! needs to be manually edited after in the PML-generated XML
		hbMsg.header.destPin = (deviceInstance->numInputs - 1); //HB is last pin
		
		hbMsg.header.messageTag = 0; //HB is first declared message

		//Loop through the devices on this softswitch
		for(unsigned int i = 0; i < deviceInstance->thread->numDevInsts; i++) {
			hbMsg.header.destDeviceAddr = i;
			softswitch_onReceive(deviceInstance->thread, &hbMsg);
		}
	}
	else {
		heartbeatIndex++;
	}
	return(1);
}
return(0); //GOTCHA: Surely this should be defualt behaviour?
