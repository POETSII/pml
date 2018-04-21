## User's Manual

### Application Structure

Each `pml` application consists of a single application configuration file
(called `app.json` by convention) and a number of `.c` files, all stored in
the same directory.

### Configuration File Format

`pml` supports different programming models through the use of application
templates. The interpretation of the configuration file is done entirely by
the template -- the tool does not do anything with the configuration file
beyond loading it, examining the `template` field, loading the respective
template then passing it configuration values (and the graph instance) through
Jinja's context. This is intentional as it means the tool can be extended to
support a rich variety of programming models by the addition of template files
(as opposed to modifying tool source code). The upshot however is that the
configuration file format is not fixed and will vary depending on choice of
template. In general, templates will maintain as much similarity between
configuration file structure as possible.

At the moment, a single template `simple` is supported, which requires the
following minimum application configuration:

```json
{
    "type": "ro",
    "template": "simple",
    "messages": {
        "toggle": {}
    },
    "device": {
        "name": "node",
        "state": {
            "counter": {}
         }
    }
}
```

The top-level fields `type`, `template`, `messages` and `device` are all
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

Two things are worth noting here.

First, you may notice the existence of two undeclared fields `src` and `dst`
under `<Message>`. These are hidden fields inserted by the `simple` template,
in this case to support tracking message sources and destinations. In general,
it is not so uncommon for `pml` templates to insert additional content in the
output XML (e.g. message/state fields or C code) to support more features or
capabilities.

Second, while `id` has no `type` field, its type has been specified as
`uint32_t`. This is because the `simple` template assumes undeclared types are
`uint32_t` (future templates will adopt the same convention). Given that
`uint32_t` is the default type (and in line with the format's minimalist
philosophy) specifying `uint32_t` types is discouraged.

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

(the include of `length` field under a state field turns it into an array)

which is translated into

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

As with message objects, the device contains some additional elements that are
not present in the JSON description:

- Two device properties `id` and `outdegree`
- Several state elements named `req_buffer_*` (used as a software buffer for outgoing `req` messages)

Apart from these, the state fields `visited` and `results` have been specified
as expected (again, the type `uint32_t` is assumed by default).
