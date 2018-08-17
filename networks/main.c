void finish(STATE_PROP_ARGS) {
	handler_exit(0);
}

void test(STATE_PROP_ARGS) {
	handler_log(1, "Running visitors ...");
	uint16_t op_type = 1;
	forward_traverse(deviceState, deviceProperties, finish, op_type);
}

void start(STATE_PROP_ARGS) {

    handler_log(1, "Discovering parents and children ...");
    uint16_t op_type = 0;
    forward_traverse(deviceState, deviceProperties, test, op_type);
}

void forward_visitor(STATE_PROP_ARGS, int distance) {
    handler_log(1, "Forward visitor");
}

void reverse_visitor(STATE_PROP_ARGS, int discovered) {
    handler_log(1, "Reverse visitor");
}
