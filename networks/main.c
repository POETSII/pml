void root(STATE_PROP_ARGS) {

    const uint32_t DISCOVER_VISITOR_ID = 0;
    const uint32_t nrounds = {{ params.get("nrounds", 2) }};

    handler_log(1, "This is root");

    if (deviceState->last_operation == 0) {

        deviceState->visitor_id = 0;
        handler_log(1, "Discovering parents and children ...");
        begin(deviceState, deviceProperties, DISCOVER_VISITOR_ID);

    } else if (deviceState->visitor_id < nrounds - 1) {

        uint32_t next_visitor = deviceState->visitor_id + 1;
        handler_log(1, "Running visitor %d ...", next_visitor);
        begin(deviceState, deviceProperties, next_visitor);

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