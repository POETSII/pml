// receive_req.c

deviceState->msg_req_rts = 0;

handler_log(2, "received msg from %d, iteration = %d, hoplimit = %d",
    message->requester_id,
    message->iteration,
    message->hoplimit);

uint32_t min_hoplimit = deviceState->hoplimits[message->iteration];

if (message->hoplimit > min_hoplimit) {

    // Discovered a new (shorter path from network center)

    // 1. Create a requests table entry with the details to acknowledge this
    // request in the future.

    handler_log(2, "Creating new requests entry ...");

    // 1a. Determine next available slot in requests table

    int req_ind = 0;

    while (deviceState->requests_tbl_occupied[req_ind] && (req_ind < 1000)) req_ind++;

    if (req_ind == 1000) {
        handler_log(2, "Error, requests table is full");
        handler_exit(1);
    }

    handler_log(2, "Found empty slot in requests table (index = %d)", req_ind);

    // 1b. Insert new requests entry

    deviceState->requests_tbl_occupied[req_ind]         = 1;
    deviceState->requests_tbl_requester[req_ind]        = message->requester_id;
    deviceState->requests_tbl_callback[req_ind]         = message->callback;
    deviceState->requests_tbl_replies_received[req_ind] = 0;
    deviceState->requests_tbl_discovered_sum[req_ind]   = 0;

    handler_log(2, "Inserted new entry in requests table");

    // 2. Broadcast request to neighbours

    deviceState->msg_req_rts = 1;
    deviceState->msg_req_iteration = message->iteration;
    deviceState->msg_req_callback = req_ind;
    deviceState->msg_req_hoplimit = message->hoplimit - 1;

} else {

    // Either:
    // 1. hoplimit is zero (end of traversal)
    // 2. hoplimit indicates a longer route from network center

    // Send an ack message back

    handler_log(2, "Sending ack message back ...");

    int discovered = 0; // TODO

    deviceState->msg_ack_rts = 1;
    deviceState->msg_ack_callback = message->callback;
    deviceState->msg_ack_discovered = discovered;

}
