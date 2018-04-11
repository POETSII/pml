#!/bin/bash

set -e

SCHEMA_DIR='/home/shared/graph_schema'
GRAPH_TYPE="graph-type-1"
INPUT_XML='/tmp/input.xml'

CPP_FILE=$SCHEMA_DIR/providers/$GRAPH_TYPE.graph.cpp
HPP_FILE=$SCHEMA_DIR/providers/$GRAPH_TYPE.graph.hpp
SO_FILE=$SCHEMA_DIR/providers/$GRAPH_TYPE.graph.so

mkdir -p $SCHEMA_DIR/providers

echo "Validating graph type xml ..."

java \
  -jar $SCHEMA_DIR/external/jing-20081028/bin/jing.jar \
  -c $SCHEMA_DIR/master/virtual-graph-schema-v2.rnc \
  $INPUT_XML

echo "Generating cpp file ..."

python3 \
  $SCHEMA_DIR/tools/render_graph_as_cpp.py \
  $INPUT_XML \
  $CPP_FILE \
  # 2> /dev/null

echo "Generating hpp file ..."

python3 \
  $SCHEMA_DIR/tools/render_graph_as_cpp.py \
  --header \
  < $INPUT_XML \
  > $HPP_FILE \
  2> /dev/null

echo "Compiling provider ..."

g++ \
  -fPIC \
  -g \
  -I $SCHEMA_DIR/include \
  -I $SCHEMA_DIR/providers \
  -I/usr/include/glib-2.0  \
  -I/usr/include/glibmm-2.4  \
  -I/usr/include/libxml++-2.6  \
  -I/usr/include/libxml2  \
  -I/usr/include/sigc++-2.0  \
  -I/usr/lib/x86_64-linux-gnu/glib-2.0/include  \
  -I/usr/lib/x86_64-linux-gnu/glibmm-2.4/include  \
  -I/usr/lib/x86_64-linux-gnu/libxml++-2.6/include  \
  -I/usr/lib/x86_64-linux-gnu/sigc++-2.0/include \
  -ldl \
  -lglib-2.0 \
  -lglibmm-2.4 \
  -lgobject-2.0 \
  -lsigc-2.0 \
  -lxml++-2.6 \
  -lxml2 \
  -pthread \
  -shared \
  -std=c++11  \
  -W \
  -Wall \
  -Wno-unused-but-set-variable \
  -Wno-unused-local-typedefs \
  -Wno-unused-parameter \
  -Wno-unused-variable \
  -o $SO_FILE \
  $CPP_FILE

# run simulation

echo "Simulating ..."

(cd $SCHEMA_DIR && bin/epoch_sim $INPUT_XML)
