from pml import build
from graph import Graph
from fabric.api import run
from fabric.api import cd
from fabric.api import env
from fabric.state import output
from fabric.operations import put

output["status"]   = False
output["running"]  = False
env.output_prefix  = False
env.use_ssh_config = True

def sim(app, graphml):
    """Run (remote) simulation using app and graphml files."""

    # Prepare flat xml file (tmp_output)
    temp_output = 'tmp/output.xml'
    xml = build(app, graphml)
    write_file(xml, temp_output)

    # Put file on remote machine and simulate
    put(temp_output, "/tmp/input.xml")
    run_script("simulate.sh")


def write_file(text, file):
    with open(file, "w") as fid:
        fid.write(text)


def run_script(script_file, quiet=False):
    local_file = "scripts/%s" % script_file
    put(local_file, "/tmp", mirror_local_mode=True)
    with cd("/tmp"):
        quiet_str = ">/dev/null 2>&1" if quiet else ""
        run("./%s %s" % (script_file, quiet_str))
        run("rm ./%s" % script_file)
