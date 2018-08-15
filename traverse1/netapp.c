void root(NODE_ARGS) {

	if (deviceState->operation_counter < 2) {
		handler_log(1, "This is root.");
		forward(root);
	} else {
		handler_exit(0);
	}
}
