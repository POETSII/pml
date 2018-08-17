// traversal
//
// Base layer in the POETS networks application stack
//
// This layer provides a visitor-style programming model enabling top layers
// to express algorithms without getting into the details of network traversal.
//
// The following functions must be supplied by top layers:

void next_operation(network_node_state_t*, const network_node_properties_t*);
void reverse_visitor(network_node_state_t*, const network_node_properties_t*, int);
void forward_visitor(network_node_state_t*, const network_node_properties_t*, int);

// Layer implementation:

{{ include("traversal.c") }}
{{ include("receive_ack.c") }}
{{ include("receive_req.c") }}
{{ include("init.c") }}
