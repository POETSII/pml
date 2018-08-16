#!/usr/bin/env python

import os
import json

from graph import Graph
from docopt import docopt
from generator import generate_xml
from generator import get_path

usage = """pml v0.1

Usage:
  pml.py [options] <app.json> <file.graphml>

Options:
  -p, --param <name:value>  Specify code generation parameter(s).
  -o, --props <file.json>   Load property values from file.

"""


def read_json(file):
    """Read a JSON file."""
    with open(file, "r") as fid:
        return json.load(fid)


def get_prop_strings(props_file):
    """Parse a propery file.

    Property files are JSON files containing a mapping node -> properties.

    This function returns a corresponding mapping node -> property strings
    where a "property string" is a string serializing of the properties
    object, excluding the leading and training brackets.

    For example, if props_file contains:

    {
        "node1": {"w": 10, "h": 10},
        "node2": {"w": 20, "h": 20},
    }

    then this functions returns:

    {
        "node1": '"w": 10, "h": 10',
        "node2": '"w": 20, "h": 20',
    }

    """

    if not props_file:
        return {}

    return {node: json.dumps(props)[1:-1]
            for node, props in read_json(props_file).iteritems()}


def build(app_file, graphml_file, props_file, params=dict()):
    """Generate an XML file from app and graph files.

    Args:
        app_file (str): Path to application JSON file.
        graphml_file (str): Path to GraphML file.
        props_file (str): Path to properties file (optional).
        params (dict): Generation parameters (optional).

    Returns:
        str: XML file content.

    """

    content = read_json(app_file)

    def include_app_file(file, optional=False):
        """Return content of file in app directory.

        Args:
            file (str): Path to file.
            optional (bool): True iff loading file is optional.

        Returns:
            str: content of file.

        """
        full_file = get_path(file, app_file)
        exists = os.path.isfile(full_file)
        if exists: return generate_xml(full_file, graph, content)
        elif optional: return ''
        else: raise Exception('Required file %s not found' % file)

    def get_field_length(field):

        if "length" not in field:
            return 1  # scalar

        flen = field["length"]

        if type(flen) is int:
            return flen
        if (type(flen) is unicode) and (flen in params):
            return params[flen]
        if (type(flen) is unicode) and (flen in content["constants"]):
            return content["constants"][flen]

        raise Exception("Could not determine length of field %s" % field)

    content['params'] = params
    content['props'] = get_prop_strings(props_file)
    graph = Graph(graphml_file)
    template = 'templates/%s/template.xml' % content["model"]
    env_globals = {
        'include_app': include_app_file,
        'get_field_length': get_field_length
    }
    xml = generate_xml(template, graph, env_globals, content)
    return xml


def parse_params(param_str):
    """Convert a parameter string into a dictionary.

    The string is in the format "name1:val1,name2:val2 ...".

    Args:
      param_str (string): parameter string

    Returns:
      dict: dictionary of parameters

    """

    param_list = [item for item in param_str.split(",") if item]

    def split_param(param_str):
        parts = param_str.split(':')
        assert len(parts) == 2, 'Malformed parameter definition: %s' % param_str
        return parts

    return {name: value for name, value in map(split_param, param_list)}


def main():
    args = docopt(usage, version="pml v0.1")
    app_file = args["<app.json>"]
    props_file = args["--props"]
    graphml_file = args["<file.graphml>"]
    params = parse_params(args["--param"] or "")
    xml = build(app_file, graphml_file, props_file, params)
    print xml


if __name__ == "__main__":
    main()
