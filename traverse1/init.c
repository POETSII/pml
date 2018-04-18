// initialize hoplimit

for (int i=0; i<100; i++)
    deviceState->hoplimits[i] = 0;

// initialize requests table

for (int i=0; i<1000; i++)
    deviceState->requests_tbl_occupied[i] = 0;

if (deviceProperties->id == 0) {

    handler_log(2, "Start");

    handler_log(2, "sum(3+5) = %d", sum(3, 5));

    // Insert a dummy request entry in the requests table to kick-start the
    // traversal process. The entry is marked as root by setting callback = -1
    // and it is inserted at index 0 in the table.

    deviceState->requests_tbl_occupied[0] = 1;
    deviceState->requests_tbl_requester[0] = 0;
    deviceState->requests_tbl_callback[0] = -1; // special code for root request
    deviceState->requests_tbl_replies_received[0] = 0;
    deviceState->requests_tbl_discovered_sum[0]  = 0;

    // Now broadcast a request to neighbours

    uint32_t iteration = 3;

    deviceState->msg_req_rts = 1;
    deviceState->msg_req_callback = 0; // index of root request object in requests table
    deviceState->msg_req_iteration = iteration;
    deviceState->msg_req_hoplimit = iteration - 1;

    // Set hoplimit of this iteration manually

    deviceState->hoplimits[iteration] = iteration;

}

