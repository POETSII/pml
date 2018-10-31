import json


def read_file(file):
    """Read and return content of file as a string."""
    with open(file, "r") as fid:
        return fid.read()


def write_file(file, content):
    """Write string to file."""
    with open(file, "w") as fid:
        fid.write(content)


def write_json(obj, file):
    """Write JSON object to file."""
    with open(file, "w") as fid:
        json.dump(obj, fid, indent=4)


def read_json(file):
    """Load JSON object from file."""
    with open(file, "r") as fid:
        return json.load(fid)
