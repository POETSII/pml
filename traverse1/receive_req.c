handler_log(2, "received req with target %d", message->dst);

if (message->dst != 0xFFFFFFFF) // if not a broadcast
    if (message->dst != deviceProperties->id) // ... and not directed at this node
        return; // don't process incoming message

handler_log(2, "received msg from %d, iteration = %d, hoplimit = %d",
    message->src,
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
    deviceState->requests_tbl_requester[req_ind]        = message->src;
    deviceState->requests_tbl_callback[req_ind]         = message->callback;
    deviceState->requests_tbl_replies_received[req_ind] = 0;
    deviceState->requests_tbl_discovered_sum[req_ind]   = 0;

    handler_log(2, "Inserted new entry in requests table");

    // 2. Broadcast request to neighbours

    req_message_t outgoing;

    outgoing.src = deviceProperties->id;
    outgoing.dst = 0xFFFFFFFF; // broadcast
    outgoing.iteration = message->iteration;
    outgoing.callback = req_ind;
    outgoing.hoplimit = message->hoplimit - 1;

    send_req(deviceState, &outgoing);

    // Finally, update hoplimits table

    deviceState->hoplimits[message->iteration] = message->hoplimit;

} else {

    // Either:
    // 1. hoplimit is zero (end of traversal)
    // 2. hoplimit indicates a longer route from network center

    // Send an ack message back

    handler_log(2, "Sending ack message back to %d ...", message->src);

    uint32_t discovered = 0; // TODO

    ack_message_t outgoing;

    outgoing.src = deviceProperties->id;
    outgoing.dst = message->src;
    outgoing.callback = message->callback;
    outgoing.discovered = discovered;

    send_ack(deviceState, &outgoing);

}
