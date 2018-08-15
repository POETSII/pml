void root(NODE_ARGS) {

    if (deviceState->operation_counter < 1) {
        handler_log(1, "This is root.");
        forward(root);
    } else {
        handler_exit(0);
    }
}

void forward_visitor(NODE_ARGS, int distance) {
    handler_log(1, "distance = %d", distance);
}

void reverse_visitor(NODE_ARGS, int discovered) {
    handler_log(1, "discovered = %d", discovered);
}