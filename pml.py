#!/usr/bin/env python

import os
import json

from graph import Graph
from docopt import docopt
from generator import generate_xml
from generator import get_path

usage = """pml v0.1

Usage:
  pml.py [-p <name:value>...] <app.json> <file.graphml>

Options:
  -p, --param <name:value>  Specify a code generation parameter.

"""


def build(app_file, graphml_file, params=dict()):
    """Generate an XML file from app and graph files.

    Args:
        app_file (str): Path to application JSON file.
        graphml_file (str): Path to GraphML file.

    Returns:
        str: xml file content.

    """

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

    def read_json(file):
        """Read a JSON file."""
        with open(file, "r") as fid:
            return json.load(fid)

    content = read_json(app_file)
    content['params'] = params
    graph = Graph(graphml_file)
    template = 'templates/%s/template.xml' % content["model"]
    env_globals = {'include_app': include_app_file}
    xml = generate_xml(template, graph, env_globals, content)
    return xml

def parse_params(param_list):
    """Convert a parameter list into a dictionary.

    Each item in the list is a string in the form 'name:value'.

    Inputs:
      param_list (list): list of parameter strings

    Returns:
      dict: dictionary of parameters

    """

    def split_param(param_str):
        parts = param_str.split(':')
        assert len(parts) == 2, 'Malformed parameter definition: %s' % param_str
        return parts

    return {name: value for name, value in map(split_param, param_list)}


def main():
    args = docopt(usage, version="pml v0.1")
    xml = build(args["<app.json>"], args["<file.graphml>"],
                parse_params(args["--param"]))
    print xml


if __name__ == "__main__":
    main()
