#!/usr/bin/env python

import os
import json

from graph import Graph
from docopt import docopt
from generator import generate_xml
from generator import get_path

usage = """PML v0.1

Usage:
  pml.py <app.json> <file.graphml>

"""


def build(app_file, graphml_file):
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
    graph = Graph(graphml_file)
    template = 'templates/%s/template.xml' % content["model"]
    env_globals = {'include_app': include_app_file}
    xml = generate_xml(template, graph, env_globals, content)
    return xml


def main():
    args = docopt(usage, version="PML v0.1")
    xml = build(args["<app.json>"], args["<file.graphml>"])
    print xml


if __name__ == "__main__":
    main()
