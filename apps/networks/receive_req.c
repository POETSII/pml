if (message->dst != 0xFFFFFFFF) // if not a broadcast
    if (message->dst != deviceProperties->id) // ... and not directed at this node
        return; // don't process incoming message

receive_req_traversal(deviceState, deviceProperties, message);
