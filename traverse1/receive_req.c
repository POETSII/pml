if (message->dst != 0xFFFFFFFF) // if not a broadcast
    if (message->dst != deviceProperties->id) // ... and not directed at this node
        return; // don't process incoming message

handler_log(3, "received msg from %d, iteration = %d, hoplimit = %d",
    message->src,
    message->iteration,
    message->hoplimit);

if (message->operation != deviceState->last_operation) {

    // This message marks the beginning of a new operation. Perform a (soft)
    // clear of device state.

    handler_log(2, "New operation");

    if (deviceProperties->id != 0)
        soft_clear_state(deviceState, deviceProperties);

    deviceState->last_operation = message->operation;

}

uint32_t min_hoplimit = deviceState->hoplimits[message->iteration];

if (message->hoplimit > min_hoplimit) {

    // Discovered a new (shorter path from network center)

    // 1. Create a requests table entry with the details to acknowledge this
    // request in the future.

    handler_log(3, "Creating new requests entry ...");

    int req_ind = create_request(deviceState, message->src, message->callback);

    if (req_ind >= 0) {
        handler_log(3, "Inserted new entry in requests table (slot %d)", req_ind);
    } else {
        handler_log(1, "Error, requests table is full");
        handler_exit(1);
    }

    // 2. Broadcast request to neighbours

    req_msg outgoing;

    outgoing.dst = 0xFFFFFFFF; // broadcast
    outgoing.iteration = message->iteration;
    outgoing.callback = req_ind;
    outgoing.hoplimit = message->hoplimit - 1;
    outgoing.operation = message->operation;

    send_req(deviceState, &outgoing);

    // Finally, update hoplimits table

    deviceState->hoplimits[message->iteration] = message->hoplimit;

} else {

    // Either:
    // 1. hoplimit is zero (end of traversal)
    // 2. hoplimit indicates a longer route from network center

    // Send an ack message back

    handler_log(3, "Sending ack message back to %d ...", message->src);

    bool distance_unset = deviceState->distance == 0xFFFFFFFF;

    if (distance_unset) {
        deviceState->distance = message->iteration;
        handler_log(3, "I am at distance %d from center", deviceState->distance);
    }

    ack_msg outgoing;

    outgoing.dst = message->src;
    outgoing.callback = message->callback;
    outgoing.discovered = distance_unset ? 1 : 0;

    send_ack(deviceState, &outgoing);

}
