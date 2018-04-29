#!/usr/bin/env python

from random import randint
from itertools import product


def read_csv(filename):
    """Read content of a CSV file.

    Removes carriage returns and trailing whitespace.

    """
    with open(filename, 'r') as fid:
        return fid.read().replace('\r', '').strip()


def parse_csv_content(content):
    """Convert CSV file content to a matrix.

    Inputs:
      content (string): csv file content.

    Returns:
      matrix as list of lists.

    """
    lines = content.split('\n')
    matrix = [map(int, line.split(',')) for line in lines]
    return matrix


def verify_matrix(matrix):
    """Checks if matrix rows have same size."""

    n = len(matrix[0])
    for row in matrix[1:]:
        assert len(row) == n, 'Mismatch in row sizes'


def print_matrix(matrix):
    """Print matrix."""
    for row in matrix:
        print ', '.join(map(str, row))


def main():
    content = read_csv('a.txt')
    matrix = parse_csv_content(content)
    verify_matrix(matrix)
    print_matrix(matrix)


if __name__ == '__main__':
    main()
