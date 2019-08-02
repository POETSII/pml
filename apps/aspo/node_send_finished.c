//It's a toggle.
if(!deviceState->finSent) { //Finished, but have not sent
	deviceState->finIdx++; //Increment BEFORE use!!!
	deviceState->finSent = 1;
	message->fin = 1;
	#ifdef USEDEBUG
	handler_log(2,"FIN_SENT");
	#endif
	#ifdef LESSDEBUG
	if(deviceInstance->deviceID == 0) {
		handler_log(2,"FIN_SENT");
	}
	#endif
}
else { //Sent but finished cancelled
	deviceState->finSent = 0;
	message->fin = 0;
	#ifdef USEDEBUG
	handler_log(2,"FIN_CANCEL");
	#endif
}
message->finIdx = deviceState->finIdx;

uint32_t total = 0;
for(uint32_t i = 0; i < graphProperties->rootCount; i++) {
	total += deviceState->buff[i];
}
message->avgHops = (float)total / (float)graphProperties->rootCount;

message->id = deviceProperties->id;
message->graphInst = deviceProperties->graphInst;
