void start(STATE_PROP_ARGS) {

    if (deviceState->operation_counter < 1) {
        handler_log(1, "This is root.");
        forward_traverse(deviceState, deviceProperties, start);
        return;
    }

	handler_exit(0);
}

void forward_visitor(STATE_PROP_ARGS, int distance) {
    handler_log(1, "distance = %d", distance);
}

void reverse_visitor(STATE_PROP_ARGS, int discovered) {
    handler_log(1, "discovered = %d", discovered);
}
