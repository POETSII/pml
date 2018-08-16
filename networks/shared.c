// POETS Network Application Stack

// Layer 1 (traversal)
{{ include("traversal/include.h") }}

// Layer 2 (mapreduce)
{{ include("mapreduce.c") }}

// Layer 3 (application)
{{ include('main.c') }}
