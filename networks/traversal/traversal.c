// traversal
//
// POETS middleware to perform MapReduce-style computations on networks

bool is_center_node(const network_node_properties_t* deviceProperties) {

    return deviceProperties->id == 0;
}

int create_request(network_node_state_t *deviceState, uint32_t requester, uint32_t callback) {

    // Determine next available slot in requests table

    int req_ind = 0;

    while (deviceState->requests_tbl_occupied[req_ind] && (req_ind < {{ constants["TABLE_SIZE"] }})) req_ind++;

    if (req_ind >= {{ constants["TABLE_SIZE"] }}) {
        handler_log(1, "Request table full, could not create new request.");
        handler_exit(1);
    }

    // insert request into available slot (req_ind)

    deviceState->requests_tbl_occupied[req_ind]         = 1;
    deviceState->requests_tbl_requester[req_ind]        = requester;
    deviceState->requests_tbl_callback[req_ind]         = callback;
    deviceState->requests_tbl_replies_received[req_ind] = 0;
    deviceState->requests_tbl_discovered_sum[req_ind]   = 0;

    return req_ind; // return request index (non-negative return value indicates success)
}

void start_iteration(STATE_PROP_ARGS, uint32_t iteration) {

    // clear hoplimit

    for (int i=0; i<100; i++)
        deviceState->hoplimits[i] = 0;

    // clear requests table

    for (int i=0; i<{{ constants["TABLE_SIZE"] }}; i++)
        deviceState->requests_tbl_occupied[i] = 0;

    // Insert a dummy request entry in the requests table to kick-start the
    // traversal process. The entry is marked as root by setting callback = -1
    // and it is inserted at index 0 in the table.

    int req_ind = create_request(deviceState, 0, -1);

    // Now broadcast a request to neighbours

    uint32_t is_last_iteration = deviceState->iteration == deviceState->diameter;
    uint32_t passed_visitor_id = is_last_iteration ? deviceState->visitor_id : 0;

    req_msg outgoing;

    outgoing.dst = 0xFFFFFFFF; // broadcast
    outgoing.iteration = iteration;
    outgoing.callback = 0; // index of root request object in requests table
    outgoing.hoplimit = iteration - 1;
    outgoing.op_id = deviceState->operation_counter;
    outgoing.visitor_id = passed_visitor_id;

    if (passed_visitor_id)
        visit(deviceState, deviceProperties, &outgoing);

    send_req(deviceState, &outgoing);

    // Set hoplimit of this iteration manually

    deviceState->hoplimits[iteration] = iteration;
    deviceState->iteration = iteration;
}

void finished_iteration_cb(STATE_PROP_ARGS, int32_t discovered) {

    deviceState->discovered_counts[deviceState->iteration] = discovered;

    handler_log(2, "Iteration %d completed (total discovered = %d)", deviceState->iteration, discovered);

    bool cont = discovered > 0; // continue if non-zero nodes have been discovered

    if (cont) {

        uint32_t next_iteration = deviceState->iteration + 1;
        handler_log(1, "Start iteration %d (visitor_id = %d)", next_iteration, deviceState->visitor_id);
        start_iteration(deviceState, deviceProperties, next_iteration);

    } else {

        handler_log(2, "Traversal completed");

        deviceState->diameter = deviceState->iteration - 1;

        uint32_t final_iteration = deviceState->iteration;
        uint32_t total_nodes = 0;

        for (uint32_t i=0; i < final_iteration; i++) {
            uint32_t discovered_i = deviceState->discovered_counts[i];
            handler_log(2, "Discovered at iteration %d = %d nodes", i, discovered_i);
            total_nodes += discovered_i;
        }

        handler_log(2, "Total discovered = %d nodes", total_nodes);
        handler_log(1, "Finished operation (%d)", deviceState->operation_counter);
        root(deviceState, deviceProperties);
    }

}

void soft_clear_state(STATE_PROP_ARGS) {

    deviceState->req_counter = 0;

    for (int i=0; i<{{ constants["TABLE_SIZE"] }}; i++) {
        deviceState->requests_tbl_occupied[i] = 0;
        deviceState->requests_tbl_discovered_sum[i] = 0;
        deviceState->requests_tbl_replies_received[i] = 0;
        deviceState->requests_tbl_requester[i] = 0;
        deviceState->requests_tbl_callback[i] = 0;
    }

    for (int i=0; i<100; i++) {
        deviceState->hoplimits[i] = 0;
        deviceState->discovered_counts[i] = 0;
    }

    const uint32_t UNSET_DISTANCE = 0xFFFFFFFF;

    deviceState->distance = is_center_node(deviceProperties) ? 0 : UNSET_DISTANCE;

}

void begin(STATE_PROP_ARGS, uint32_t visitor_id) {
    (deviceState->operation_counter)++;
    deviceState->visitor_id = visitor_id;
    soft_clear_state(deviceState, deviceProperties);

    deviceState->discovered_counts[0] = 1; // just center node is at distance 0
    deviceState->visitor_id = visitor_id;
    handler_log(1, "Start traversal (visitor = %d)", deviceState->visitor_id);
    start_iteration(deviceState, deviceProperties, 1);
}
