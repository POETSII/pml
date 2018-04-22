## Developer's Guide

### Content

- [General Organization](#general-organization)
- [Developing New Models](#developing-new-models)

### General Organization

The main parts of this repository are listed below.

Item                               | Type                 | Description
---------------------------------- | -------------------- | -----------
[`pml.py`](pml.py)                 | File (Python module) | Top level module (`pml` tool)
[`gml.py`](gml.py)                 | File (Python module) | Top level module (`gml` tool)
[`graph.py`](graph.py)             | File (Python module) | Graph class
[`generator.py`](generator.py)     | File (Python module) | XML generation functions
[`doc`](doc)                       | Directory            | Documentation
[`templates`](templates)           | Directory            | Model template files
[`ro`](ro)                         | Directory            | Ring oscillator application
[`traverse1`](traverse1)           | Directory            | Asynchronous network traversal application

### Developing New Models

Models can be added by creating new Jinja template files and saving them as
`templates/MODEL_NAME/template.xml`. Templates should create a compliant POETS
XML file using the configuration and graph objects passed by `pml` through
Jinja's context.

For example, to create the `<MessageTypes>` section, the template can include

```xml
<MessageTypes>
{% for id, content in messages.items() %}
<MessageType id="{{ id }}">
    <Documentation>{{ content['doc'] }}</Documentation>
</MessageType>
{% endfor %}
</MessageTypes>
```

In the above, `messages` is the value of the `messages` field in the
application's configuration file. Other configuration file fields are made
available in Jinja's context in a similar manner.

Templates are free in how they use configuration fields. For example,
replacing `messages` above with `msgs` in both the template and configuration
files will result in the same output. However, it is strongly recommended that
you have a look at existing templates and adopt the same structure and
terminology whenever possible. Minimizing differences in model configuration
file structures will reduce the amount of effort required to (1) learn newer
models (2) understand model differences and (3) migrate applications to
different models.

Other than configuration fields, `pml` adds the following to Jinja's context:

- a `graph` object to access graph-related information
- an `include` function to include files from template directory
- an `include_app` function to include functions from app directory

A good starting point to learn about generating code using `pml`'s context
objects is to have a look at existing model templates inside the `templates`
directory, particularly the file
[`templates/simple/template.xml`](templates/simple/template.xml).
