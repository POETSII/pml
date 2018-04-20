#!/usr/bin/env python

import os
import json

from graph import Graph
from docopt import docopt
from generator import generate_xml
from generator import get_path

usage = """pml.py

Usage:
  pml.py <app.json> <file.graphml>

"""


def main():

    args = docopt(usage, version="pml.py ver 1.0")
    xml = build(args["<app.json>"], args["<file.graphml>"])
    print xml


def build(app_file, graphml_file):
    def include_app_file(file, optional=False):
        full_file = get_path(file, app_file)
        if os.path.isfile(full_file):
            return generate_xml(full_file, graph, content)
        elif optional:
            return ''
        else:
            raise Exception('Required file %s not found' % file)

    def read_json(file):
        with open(file, "r") as fid:
            return json.load(fid)

    content = read_json(app_file)
    graph = Graph(graphml_file)
    template = 'templates/%s/template.xml' % content["template"]
    env_globals = {'include_app': include_app_file}
    xml = generate_xml(template, graph, env_globals, content)
    return xml


if __name__ == "__main__":
    main()
