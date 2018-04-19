bool is_center = deviceProperties->id == 0;

const uint32_t UNSET_DISTANCE = 0xFFFFFFFF;

deviceState->distance = is_center ? 0 : UNSET_DISTANCE;

if (is_center) {
	deviceState->discovered_counts[0] = 1; // just center node is at distance 0
    handler_log(1, "Start traversal");
    start_iteration(deviceState, 1);
}

