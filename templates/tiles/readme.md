
# Tiles Template

The template is designed for applications that work over multiple copies
of the same problem within a single XML in order to increase parallelisation.

> **Tile** is a single copy of the source graph (graphml).

The number of tiles is passed as a parameter to the generator, default is 1.

Additionally, the template supports multiple device types and supervisor devices.

## Application Structure

Files:
- **app.json** contains the application definition.
- **extensions.py** (optional) contains application-specific callback functions.
	This template uses callback functions to [generate property values](#property-generation).
- **\*.c** (optional) [C++ code](#c-code).

**app.json** structure:
```json
{
	"type": "graph_type_name",
	"model": "tiles",
	"constants": {
	},
	"properties": {
	},
	"messages": {
	},
	"devices": {
	}
}
```

- **type** is the name of both the graph type and the graph instance
	as the current version supports only one graph instance per XML.
- **model** is the application model name (`"tiles"` for this template).
- **constants** (optional) is a dictionary of template constants that
	can be used in **app.json** to specify default values or array lengths
	in [field list](#field-lists) definitions.
- **properties** (optional) is the [field list](#field-lists) of graph properties.
- **messages** dictionary defines [message types](#messages).
- **devices** dictionary defines [device types](#devices).

### Devices

The `devices` dictionary defines the set of device types where the keys are device type names.
```json
"devices": {
	"device_type_name" : {
		"instance": "node",
		"doc": "device type description",
		"properties": {
		},
		"state": {
		}
	}
}
```

- **instance** specifies the device [instantiation](#device-instance-property) type.
- **doc** (optional) contains a documentation string.
- **properties** (optional) is the [field list](#field-lists) of device properties.
- **state** is the [field list](#field-lists) definition of the device state.

### Messages

The `messages` dictionary defines the set of message types where the keys are message type names.
```json
"messages": {
	"update": {
		"src": ["device_type1", "device_type2"],
		"dst": ["device_type1", "device_type2"],
		"fields": {
		}
	}
}
```

- ** src** and **dst** specify device types that can send and receive the message.
	See [Message sources and destinations](#message-sources-and-destinations).
- **fields** is the message [field list](#field-lists).

### Field lists

```json
{
	"field1": { "type": "uint32_t", "default": 0 },
	"field2": { "type": "uint8_t", "length": 100 },
	"field3": { "type": "float", "generator": "get_field3_value" }
}
```

- **type** is the C++ type of the field.
- **default** (optional) specifies the initial value.
	Can also be a string referencing a member of `constants` dictionary.
- **length** (optional) defines the array length. If length is greater than 1, an `<Array>` tag is
	generated, otherwise a `<Scalar>` tag is produced (default behaviour).
	Can also be a string referencing a member of `constants` dictionary.
- **generator** (optional) specifies the name of a callback function from **extensions.py**.
	See [Property Generators](#property_generators).

> Tuples are not supported at the moment.

The above example will produce:
```xml
<Scalar name="field1" type="uint32_t" default="0" />
<Array name="field2" type="uint8_t" length="100" />
<Scalar name="field3" type="float" />
```

Example of using `constants`:
```json
{
	"constants": {
		"FIELD1_INIT": 0,
		"FIELD2_COUNT": 100
	},
	"properties": {
		"field1": { "type": "uint32_t", "default": "FIELD1_INIT" },
		"field2": { "type": "uint8_t", "length": "FIELD2_COUNT" }
	}
}
```

### C++ code

> All C++ files are optional.

- **shared.c** contains globally shared code for the `<SharedCode>` XML section.

Device code:
- **_(device\_type)_\_shared.c** contains device shared code, `<SharedCode>`.
- **_(device\_type)_\_code.c** contains supervisor shared code, `<Code>`.
- **_(device\_type)_\_rts.c** contains device `<ReadyToSend>` handler.
- **_(device\_type)_\_idle.c** contains device `<OnCompute>` handler (idle).

_(device\_type)_ to be replaced with the respective device type name

Device pins:
- **_(device\_type)_\_receive\__(message\_type)_.c** contains `<OnReceive>`
	handler for the input pin of _(message\_type)_ message type.
- **_(device\_type)_\_send\__(message\_type)_.c** contains `<OnSend>`
	handler for the output pin of _(message\_type)_ message type.

## Instantiation and Topology

### Device _instance_ property

```json
"devices": {
	"A": { "instance": "node" },
	"B": { "instance": "node" },
	"T": { "instance": "tile" },
	"S": { "instance": "supervisor" }
}
```

The `instance` property of the device type specifies how it is instantiated
in relation to the source graph and tiles. The property can take one of the following values:

- **node** - the device is instantiated for each node in the graph in each tile.
- **tile** - the device is instantiated once per tile (tile-unique); this may be used to create local psuedo-supervisors
	that commutnicate with the nodes of one tile.
- **unique** - only one instance of the device is created (singleton).
- **supervisor** - same as `unique`, but creates `SupervisorDeviceType`
	that runs on the mothership instead of tinsel.

### Message sources and destinations

The `messages` dictionary defines the set of message types where the keys are message type names.

```json
"messages": {
	"AA": { "src": ["A"], "dst": ["A"] },
	"AB": { "src": ["A"], "dst": ["B"] },
	"AT": { "src": ["A"], "dst": ["T"] },
	"BS": { "src": ["B"], "dst": ["S"] },
	"TS": { "src": ["T"], "dst": ["S"] },
}
```

`src` is the list of device types that can send the message. Only devices in this list will have
an output port for this message type. Output port names have `_out` postfix following the
message type name.

`dst` is the list of device types that can receive the message. Only devices in this list will have
an input port for this message type. Input port names have `_in` postfix following the
message type name.

### Putting it together

Edges between device instances are generated depending on the device instantiation types
and message types.

<img src="../../svg/tiles.svg" width="50%">

- For **node-node** messages:
	- _If the source and destination device types are the same:_ create an edge for each edge in the graphml file
		(see AA messages in the example). These edges do not cross tile boundaries.
	- _If the source and destination device types differ:_ create an edge between device instances
		corresponding to the same node in the graphml (see AB messages in the example).
		These edges do not cross tile boundaries.
- For **node-tile** messages: connect each node in a graph tile to the respective tile-unique node.
- For **node-unique**, **node-supervisor**, **tile-unique**, or **tile-supervisor** messages:
	connect all instances to the unique node.

## Property Generators

Some property values are application-specific and can only be calculated for a given
graph instance. This can be done using callback functions in **extentions.py**.

This template supports generating graph instance properties and device instance properties.

### Graph instance properties

Callback function definition:
```py
def function_name(graph, constants)
```

_Arguments:_
- **graph** [Graph](../../graph.py) object created from graphml specification.
- **constants** dictionary as defined in `constants` section in **app.json**.

_Returns:_ Property value or anempty string. Empty string does not create an entry for the property.

The template also provides built-in graph property generators:
- `nodeCount` gives the number of nodes in one tile of the graph.
- `tileCount` gives the number of graph tiles in the generated XML.
- `totalNodeCount` gives the total number of nodes across all tiles.

### Device instance properties

Callback function definition:
```py
def function_name(tile, node_id, node, graph, constants)
```

_Arguments:_
- **tile** graph tile index for this device.
- **node_id** integer index for the node in a graph tile.
- **node** node name as it appears in the Graph object.
- **graph** [Graph](../../graph.py) object created from graphml specification.
- **constants** dictionary as defined in `constants` section in **app.json**.

_Returns:_ Property value or an empty string. Empty string does not create an entry for the property.

The template also provides built-in graph property generators:
- `id` gives the integer node index (`node_id` argument).
- `tile` gives the current tile index (`tile` argument).
- `outDegree` gives the number of outgoing edges for this node.

### Property generation example

**app.json**
```json
{
	"type": "example",
	"template": "tiles",
	"properties": {
		"nodes": {"type": "uint32_t", "generator": "nodeCount"},
		"leafNodes": {"type": "uint32_t", "generator": "get_leaf_nodes"}
	},
	"devices": {
		"dev": {
			"instance": "node",
			"properties": {
				"id": {"type": "uint32_t", "generator": "id"},
				"isLeaf": {"type": "uint8_t", "default": 0, "generator": "get_is_leaf"}
			}
		}
	}
}
```

**extensions.py**
```py
def get_leaf_nodes(graph, constants):
	return sum(graph.get_outdegree(node)<2 for node in graph.nodes)

def function_name(tile, node_id, node, graph, constants):
	if graph.get_outdegree(node)<2:
		return 1
	else
		return '' # do not generate property entry, use default

```

Generated graph instance:
```xml
<GraphInstance id="example" graphTypeId="example">
	<Properties>
		"nodes": 4,
		"leafNodes": 1
	</Properties>
	<DeviceInstances>
		<DevI id="dev_0_n0" type="dev"><P>"id":0</P></DevI>
		<DevI id="dev_0_n1" type="dev"><P>"id":1</P></DevI>
		<DevI id="dev_0_n2" type="dev"><P>"id":2</P></DevI>
		<DevI id="dev_0_n3" type="dev"><P>"id":3,"isLeaf":1</P></DevI>
	</DeviceInstances>
	<!-- skipping edge instances here -->
</GraphInstance>
```
