// traversal
//
// Base layer in the POETS networks application stack
//
// This layer provides a visitor-style programming model enabling top layers
// to express algorithms without getting into the details of network traversal.
//
// The following functions must be supplied by top layers:

#define STATE_PROP_ARGS network_node_state_t* deviceState, const network_node_properties_t* deviceProperties

void next_operation(STATE_PROP_ARGS);

void visit(STATE_PROP_ARGS, req_msg* outgoing);
void map(STATE_PROP_ARGS, ack_msg* outgoing);
void reduce(STATE_PROP_ARGS, const network_ack_message_t* message);

// Layer implementation:

{{ include("traversal.c") }}
{{ include("receive_ack.c") }}
{{ include("receive_req.c") }}
{{ include("init.c") }}
