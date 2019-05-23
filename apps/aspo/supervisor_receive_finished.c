
VERBOSE_PRINT("MSG:");
if((message->id >= graphProperties->nodeCount) || (message->graphInst >= graphProperties->tileCount)) {
	//Something has gone horribly wrong and we have received a message for a node that can't exist.
	DEBUG_PRINT("ERR_MSG_CELL_NE");
}
else {
	uint64_t loc = (message->graphInst * graphProperties->nodeCount) + message->id;

	if(message->fin && (message->finIdx > deviceState->finIdx[loc])) {
		//It's a finished message that is newer than what we have.
		VERBOSE_PRINT("\tFIN:" << message->id << "@" << message->graphInst << " IDX:" << message->finIdx << " VAL:"  << message->avgHops);
		if(!deviceState->fin[loc]) { //Node is not already finished.
			finCount++;
		}
		deviceState->fin[loc].fin = 1;
		deviceState->finIdx[loc] = message->finIdx;
		deviceState->avgHops[loc] = message->avgHops;
	}
	else if(!(message->fin) && message->finIdx >= deviceState->finIdx[loc]) {
		//It's a not finished message cancelling the current or future finished message
		VERBOSE_PRINT("\tNFIN:" << message->id << "@" << message->graphInst << " IDX:" << message->finIdx);
		if(deviceState->fin[loc]) { //Node is already finished.
			finCount--;
		}
		deviceState->fin[loc] = 0;
		deviceState->finIdx[loc] = message->finIdx;
		deviceState->avgHops[loc] = message->avgHops;
	}
	else {//Otherwise do nothing with the finish message as it is a duplicate.
		VERBOSE_PRINT("\tIGNORED:" << message->id << "@" << message->graphInst << " IDX:" << message->finIdx);
	}

	VERBOSE_PRINT("\tFINCOUNT:" << finCount << "/" << deviceProperties->nodeCount);

	//Periodic node count updates
	if(deviceState->loopCount == 0) {
		DEBUG_PRINT("\tNODES_DONE: " << finCount << "/" << deviceProperties->nodeCount);
		deviceState->loopCount = deviceProperties->loopMax;
	}
	deviceState->loopCount--;
	if(finCount >= deviceProperties->nodeCount) {
		//All of the nodes have finished, do something.
		DEBUG_PRINT("\tNODES_DONE: " << finCount);
		//handler_log(2, "ALL NODES_DONE");

		nodesDone = 1;
		if(!sentDone) {
			DEBUG_PRINT("\tSEND_DONE");
			//Supervisor::outputs[0]->OnSend(outMsg, msgBuf, 1);
		}
		//TODO: Send Data to MPI Land. Or write to file.
		/*
		//Wite data to CSV
		std::ofstream oFile;
		std::ostringstream ss;
		ss << "plate_" << sEdgeProperties->xSize << "x" << sEdgeProperties->ySize << "_out.csv";
		oFile.open(ss.str());
		DEBUG_PRINT("\tOFILE_OPEN: " << ss.str()) ;
		//oFile.precision(2);
		oFile << std::fixed << std::setprecision(2);
		oFile << "x, y, temp" << std::endl;

		DEBUG_PRINT("\tRESULTS_WRITE");
		for(unsigned int ix = 0; ix < sEdgeProperties->xSize; ix++) {
			loc = ix*sEdgeProperties->xSize;
			for(unsigned int iy = 0; iy < sEdgeProperties->ySize; iy++) {
				oFile << ix << ", " << iy << ", " << sEdgeState->data_t[loc].t << std::endl;
				loc++;
			}
		}
		DEBUG_PRINT("\tRESULTS_WRITTEN");

		oFile.close();
		DEBUG_PRINT("\tOFILE_CLOSE");
		*/
	}
}
