import json

def write_json(obj, file):
    """Write JSON object to file."""
    with open(file, "w") as fid:
        json.dump(obj, fid, indent=4)


def write_file(file, content):
    """Write string to file."""
    with open(file, "w") as fid:
        fid.write(content)


def read_json(file):
    """Load JSON object from file."""
    try:
        with open(file, "r") as fid:
            return json.load(fid)
    except IOError:
        return None
