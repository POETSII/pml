#!/bin/env python

from gml import generate_ring
from exporter import generate_xml
from itertools import product


def get_lengths(digits=[1, 2, 5], exponents=range(7)):
    """Return list of numbers in the form:

    1, 2, 5, 10, 20, 50, 100, 200, 500 ...

    or similar, depending on 'digits' and 'exponents'."""

    lengths = [dig * (10**expo) for dig, expo in product(digits, exponents)]

    return sorted(lengths)


def write_file(text, file):
    """Write a string 'text' to given 'file'."""

    with open(file, "w") as fid:
        fid.write(text)


def main():

    template_file = "templates/ro.xml"

    for length in get_lengths():

        xml_file = "xml/ro-%d.xml" % length
        print "Generating %s ..." % xml_file
        graph = generate_ring(length)
        xml = generate_xml(template_file, graph)
        write_file(xml, xml_file)


if __name__ == '__main__':
    main()
