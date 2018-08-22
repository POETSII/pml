void root(STATE_PROP_ARGS) {

    const uint32_t UNINITIALIZED = 0;
    const uint32_t DISCOVER_VISITOR_ID = 0;
    const uint32_t OP1_VISITOR_ID = 5;
    const uint32_t OP2_VISITOR_ID = 8;

    if (deviceState->last_operation == 0) {

        handler_log(1, "Discovering parents and children ...");
        begin(deviceState, deviceProperties, DISCOVER_VISITOR_ID);

    } else if (deviceState->visitor_id == DISCOVER_VISITOR_ID) {

        handler_log(1, "Running visitor 5 ...");
        begin(deviceState, deviceProperties, OP1_VISITOR_ID);

    } else if (deviceState->visitor_id == OP1_VISITOR_ID) {

        handler_log(1, "Running visitor 8 ...");
        begin(deviceState, deviceProperties, OP2_VISITOR_ID);

    } else {

        handler_exit(0);

    }

}

void visit(STATE_PROP_ARGS, req_msg* outgoing) {
    handler_log(1, "Visit (visitor_id = %d)", outgoing->visitor_id);

    if (outgoing->visitor_id == 5)
        deviceState->ndescendants = 0;
}

void map(STATE_PROP_ARGS, ack_msg* outgoing){
    handler_log(1, "Map (visitor_id = %d)", outgoing->visitor_id);

    if (outgoing->visitor_id == 5)
        outgoing->payload = deviceState->ndescendants + 1;
}

void reduce(STATE_PROP_ARGS, const network_ack_message_t* message) {
    handler_log(1, "Reduce msg from %d (visitor_id = %d)", message->src, message->visitor_id);

    if (message->visitor_id == 5)
        deviceState->ndescendants += message->payload;
}