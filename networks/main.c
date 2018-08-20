void finish(STATE_PROP_ARGS) {
    handler_exit(0);
}

void test2(STATE_PROP_ARGS) {
    uint16_t visitor_id = 8;
    forward_traverse(deviceState, deviceProperties, finish, visitor_id);
}

void test1(STATE_PROP_ARGS) {
    uint16_t visitor_id = 5;
    forward_traverse(deviceState, deviceProperties, test2, visitor_id);
}

void start(STATE_PROP_ARGS) {
    handler_log(1, "Discovering parents and children ...");
    uint16_t visitor_id = 0;
    forward_traverse(deviceState, deviceProperties, test1, visitor_id);
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