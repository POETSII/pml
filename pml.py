#!/usr/bin/env python

import os
import sys
import json

from importlib import import_module
from files import read_file
from files import read_json
from graph import Graph
from docopt import docopt
from pretty import prettify_xml
from generator import generate_xml
from generator import get_path


usage = """pml v0.1

Usage:
  pml.py [options] <app.json> <file.graphml>

Options:
  --param <name:value>  Specify code generation parameter(s).
  --props <file.json>   Load property values from file.
  --pretty              Pretty-print XML using xmllint.

"""

def is_str(s):
    try:
        return type(s) is unicode
    except NameError:
        return type(s) is str

def pml(app_file, graphml, props=dict(), params=dict(), prettify=False):
    """Generate a POETS XML file.

    Args:
        app_file (str): Path to application JSON file.
        graphml (str): Content of a GraphML file.
        props (dict): Application properties (optional).
        params (dict): Generation parameters (optional).

    Returns:
        str: XML file content.
    """

    content = read_json(app_file)
    if not 'constants' in content:
        content['constants'] = {}
    content['constants'].update(params)

    ext_file = get_path('extensions.py', app_file)
    ext_exists = os.path.isfile(ext_file)
    if ext_exists:
        sys.path.append(os.path.split(app_file)[0])
        ext = import_module('extensions')

    def call_extension(func_name, params):
        if ext_exists and hasattr(ext, func_name):
            func = getattr(ext, func_name)
            return func(**params)
        else: raise Exception('Required extension function %s not found' % func_name)
        
    def include_app_file(file, optional=False):
        """Return content of file in app directory.

        Args:
            file (str): Path to file.
            optional (bool): True iff loading file is optional.

        Returns:
            str: content of file.
        """
        full_file = get_path(file, app_file).replace('\\','/')
        exists = os.path.isfile(full_file)
        if exists: return generate_xml(full_file, graph, content)
        elif optional: return ''
        else: raise Exception('Required file %s not found' % file)

    def get_field_default(field):
        if 'default' not in field:
            return ''
        
        fdef = field['default']
        
        if (type(fdef) is int) or (type(fdef) is float):
            return fdef
        if (is_str(fdef)) and (fdef in content['constants']):
            return content['constants'][fdef]
        
        return fdef
    
    def get_field_length(field):
        if "length" not in field:
            return 1  # scalar

        flen = field['length']

        if type(flen) is int:
            return flen
        if (is_str(flen)) and (flen in content['constants']):
            return content['constants'][flen]

        raise Exception('Could not determine length of field %s' % field)

    def get_props_string(json):
        """Return a bracketless string representation of a JSON object."""
        return json.dumps(json)[1:-1]

    content['params'] = params
    content['props'] = props
    graph = Graph(graphml)
    template = 'templates/%s/template.xml' % content["model"]
    env_globals = {
        'call_extension': call_extension,
        'include_app': include_app_file,
        'get_field_length': get_field_length,
        'get_field_default': get_field_default,
        'get_props_string': get_props_string
    }

    xml = generate_xml(template, graph, env_globals, content)
    return prettify_xml(xml) if prettify else xml


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
    args = docopt(usage, version='pml v0.1')
    xml = pml(
        app_file=args['<app.json>'],
        graphml=read_file(args['<file.graphml>']),
        props=read_json(args['--props']) if args['--props'] else {},
        params=parse_params(args['--param'] or ''),
        prettify=args['--pretty']
    )
    print(xml)


if __name__ == "__main__":
    main()
