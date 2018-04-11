// initialize hoplimit

for (int i=0; i<100; i++)
    deviceState->hoplimits[i] = 0;

// initialize requests table

for (int i=0; i<1000; i++)
    deviceState->requests_tbl_occupied[i] = 0;

if (deviceProperties->id == 0) {
    handler_log(2, "Start");
    deviceState->msg_req_rts = 1;
    deviceState->msg_req_callback = -1; // special callback code for 'None'
    deviceState->msg_req_iteration = 2;
    deviceState->msg_req_hoplimit = deviceState->msg_req_iteration - 1;
}