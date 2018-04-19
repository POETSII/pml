int create_request(node_state_t *deviceState, uint32_t requester, uint32_t callback) {

	// 1a. Determine next available slot in requests table

	int req_ind = 0;

	while (deviceState->requests_tbl_occupied[req_ind] && (req_ind < 1000)) req_ind++;

	if (req_ind == 1000) return -1; // fail if table is full

	deviceState->requests_tbl_occupied[req_ind]         = 1;
	deviceState->requests_tbl_requester[req_ind]        = requester;
	deviceState->requests_tbl_callback[req_ind]         = callback;
	deviceState->requests_tbl_replies_received[req_ind] = 0;
	deviceState->requests_tbl_discovered_sum[req_ind]   = 0;

	return req_ind; // a non-negative result indicates success
}

bool start_iteration(node_state_t *deviceState, uint32_t iteration) {

	// clear hoplimit

	for (int i=0; i<100; i++)
	    deviceState->hoplimits[i] = 0;

	// clear requests table

	for (int i=0; i<1000; i++)
	    deviceState->requests_tbl_occupied[i] = 0;

	// Insert a dummy request entry in the requests table to kick-start the
	// traversal process. The entry is marked as root by setting callback = -1
	// and it is inserted at index 0 in the table.

	int req_ind = create_request(deviceState, 0, -1);

	if (req_ind == 1000) return false; // fail if table is full

	// Now broadcast a request to neighbours

	req_msg outgoing;

	outgoing.dst = 0xFFFFFFFF; // broadcast
	outgoing.iteration = iteration;
	outgoing.callback = 0; // index of root request object in requests table
	outgoing.hoplimit = iteration - 1;

	send_req(deviceState, &outgoing);

	// Set hoplimit of this iteration manually

	deviceState->hoplimits[iteration] = iteration;

	deviceState->iteration = iteration;

	return true; // success
}