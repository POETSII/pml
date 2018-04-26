## User's Manual

### Content

- [Application Structure](#application-structure)
- [Configuration File Format](#configuration-file-format)
- [Parameters](#parameters)
- [The `simple` Model](#the-simple-model)
- [Generating Graphs using `gml`](#generating-graphs-using-gml)
- [Ring Oscillator Example](#ring-oscillator-example)

### Application Structure

Each `pml` application consists of a single application configuration file
(called `app.json` by convention) and a number of `.c` files in the same
directory (the _application directory_).

### Configuration File Format

`pml` supports different programming models through the use of application
models. Interpreting the configuration file is done entirely by the model's
template -- the tool does not do anything beyond loading the configuration
file, examining its `model` field, loading the respective template then
passing configuration values (and the graph instance) through Jinja's context
to the template. This is intentional as it means the tool can be extended to
support a rich variety of programming models by adding model template files
instead of modifying tool source code. Different models may require slightly
different configuration files but the general structure will always be
similar.

At the moment, a single model `simple` is supported, which requires the
following minimum application configuration:

```json
{
    "type": "network",
    "model": "simple",
    "messages": {
        "req": {}
    },
    "device": {
        "name": "node",
        "state": {
            "visited": {}
         }
    }
}
```

The top-level fields `type`, `model`, `messages` and `device` are all
required. `type` is the application name (corresponding to graph type in XML),
`messages` is a dictionary of message types and `device` contains device type
information (recall that `simple` applications have a single device type).

#### Messages

Message objects have optional `doc` and `fields` fields, for example:

```json
"messages": {
    "req": {
        "doc": "Request message",
        "fields": {
            "id": {
                "doc": "Unique identifier"
            },
            "operation": {
                "type": "uint16_t",
                "doc": "Number of operation to initiate"
            }
        }
    }
}
```

where `doc` is message documentation and `fields` is a dictionary of message
field objects. The above is translated to the following XML:

```xml
<MessageType id="req">
    <Documentation>Request message</Documentation>
    <Message>
        <Scalar type="uint32_t" name="src">
            <Documentation>
                Source node id
            </Documentation>
        </Scalar>
        <Scalar type="uint32_t" name="dst">
            <Documentation>
                Destination node id
            </Documentation>
        </Scalar>
        <Scalar type="uint16_t" name="operation">
            <Documentation>
                Number of operation to initiate
            </Documentation>
        </Scalar>
        <Scalar type="uint32_t" name="id">
            <Documentation>
                Unique identifier
            </Documentation>
        </Scalar>
    </Message>
</MessageType>
```

Two things are worth noting here:

First, there are two undeclared fields (`src` and `dst`) under `<Message>`.
These are hidden fields inserted by the `simple` model, in this case to
support tracking message sources and destinations. In general, it is not so
uncommon for `pml` model templates to insert additional content in the output
XML (e.g. message/state fields or C code) to support more features or
capabilities.

Second, while `id` has no `type` field in the configuration, its type has been
specified as `uint32_t` in the generated XML file. This is because the
`simple` model assumes undeclared types are `uint32_t` (future models will
adopt the same convention). Given that `uint32_t` is the default type (and in
line with the format's minimalist philosophy) specifying `uint32_t` types is
discouraged.

#### Device

The device object must contain `name` and `state` fields. For example,

```json
"device": {
    "name": "node",
    "state": {
        "visited": {},
        "results": {
            "length": 100
        }
    }
}
```

(adding `length` to a state element turns it into an array)

which is translated to

```xml
<DeviceType id="node">
    <Properties>
        <Scalar name="id" type="uint32_t"></Scalar>
        <Scalar name="outdegree" type="uint32_t"></Scalar>
    </Properties>
    <State>
        <!-- Device state fields: -->
        <Scalar name="visited" type="uint32_t"></Scalar>
        <Array name="results" type="uint32_t" length="100"></Array>
        <!-- Software buffer for (outgoing) req messages: -->
        <Array name="req_buffer_dst" type="uint32_t" length="1000"></Array>
        <Scalar name="req_buffer_ptr" type="uint32_t"></Scalar>
        <Array name="req_buffer_operation" type="uint16_t" length="1000"></Array>
        <Array name="req_buffer_id" type="uint16_t" length="1000"></Array>
    </State>
    <!-- InputPin and OutputPin sections removed for brevity -->
</DeviceType>
```

As with message objects, the generated `<DeviceType>` contains some additional
elements that are not present in the JSON description:

- Two device properties: `id` and `outdegree`
- Several state elements named `req_buffer_*`

Again, these are used to support some model features. Apart from these, the
state elements `visited` and `results` have been specified as expected.

### Parameters

`pml` accepts an arbitrary number of code generation parameters using the
`--param` switch. For example:

```
./pml --param sbufsize:500 --param target:simulation app.json file.graphml
```

Parameters are used as a mechanism to override model/application constants and
behavior per generated application instance. They are passed to
model/application templates as a dictionary with the name `params` (within
Jinja's context). Each model has its own parameters so consult individual
model sections for details.

### The `simple` Model

At the moment, `pml` supports a single programming model, called `simple`. The
rationale and mechanics of this model are described here.

#### Programming Model

In the POETS XML schema, incoming messages trigger receive handlers that
update the device's state. The latter is then used to trigger and construct
outgoing messages. This is an intuitive way to model state-focused
computations such as finite element analysis, but may be less convenient for
other types of applications. For example, consider a network traversal
algorithm in which incoming messages are simply forwarded to neighboring
devices (assuming slightly different content per outgoing message). Expressing
this algorithm in a single code block is more convenient than splitting it
into two (receive and send) parts that communicate through device state.

The `simple` model provides a simpler programming interface to accommodate
applications where messages do not signify state updates (e.g. network
traversal, stream processing, combinatorial solvers). It uses state-based
software buffers to enable message receive handlers to queue outgoing messages
for delivery, removing the need to communicate with send handlers via state.
Since send handlers are no longer needed, the model does away with them
completely and lets users code the application as a set of receive handlers.
This model is not necessarily the most suitable for _all_ applications, but it
is particularly convenient for _some_.

#### Code Files

An accompanying file `receive_MSGTYPE.c` must be present in the application
directory for each message of the type `MSGTYPE`. The content of these files
are inserted into the `<DeviceType>` section of the generated XML file.

If a file `shared.c` is present in the application directory, its contents are
inserted into the `<SharedCode>` section.

Also, if a file `init.c` is present, its contents are inserted into the
initialization section of the device.

#### Sending Messages

Outgoing messages can be queued in receive handlers as follows:

```c
// File: receive_req.c

req_msg outgoing;

outgoing.dst = 1;
outgoing.id = 10;
outgoing.operation = 3;

send_toggle(deviceState, &outgoing);
```

In this example, an outgoing message of type `req` is constructed and queued
for delivery (note that its destination is specified in the `dst` field).

#### Parameters

`simple` has the following parameters:

| Name       | Type    | Description                                    | Default Value |
|:-----------|:--------|:-----------------------------------------------|:--------------|
| `sbufsize` | Integer | Size of outgoing message buffers               | 1000          |
| `target`   | String  | Generation target (`simulation` or `hardware`) | `simulation`  |

`target` makes slight adjustments to make the generated code compatible with
either `epochsim` or POETS hardware.

### Generating Graphs using `gml`

Aside from application files, `pml` requires input graphs to create
application instances. The repository contains a dedicated tool (`gml`) to
generate graphs of various topologies in GraphML format, ready to be used with
`pml`.

#### Usage:

```
Usage:
  gml.py [options] full <nodes>
  gml.py [options] tree <depth> <bfactor>
  gml.py [options] random <nodes> <edges>
  gml.py [options] line [--fold] <length>
  gml.py [options] grid [--fold] <length> <width>
  gml.py [options] cube [--fold] <length> <width> <height>
  gml.py [options] hypercube [--fold] <side>...

Options:
  -d, --directed  Produce directed graph.
  -i, --id=<id>   Specify instance name [default: graph].
  -c, --coords    Name nodes based on coordinates.
```

### Ring Oscillator Example

The directory [`ro`](../ro) contains an example ring oscillator `pml`
application that can be used to demo the tool. The example consists of only
three files:

File                                         | Description
-------------------------------------------- | -----------
[`app.json`](../ro/app.json)                 | Configuration file
[`init.c`](../ro/init.c)                     | State initialization handler
[`receive_toggle.c`](../ro/receive_toggle.c) | Message receive handler

This example is based on the `simple` model and contains a single device type
(`node`) and message type (`toggle`). During initialization, the root node (id
= 0) broadcasts a `toggle` message. Any node that receives a `toggle` will
increment a local counter then either broadcast another `toggle` (if counter
<= 10) or terminate the application (if counter = 10).

The following commands generate an instance of this application

```bash
# File: generate_ro_instance.sh

# Generate graph
./gml.py line --fold 10 > /tmp/chain.graphml

# Combine app config with graph to generate app instance
./pml.py ro/app.json /tmp/chain.graphml > /tmp/ro_inst.xml
```

Here, `gml` is used to create a line graph with 10 nodes. The `--fold` switch
connects the first and last nodes to create a chain.

When this example is ran, the `toggle` message generated by the root node will
circle the chain 10 times then the application will terminate.
