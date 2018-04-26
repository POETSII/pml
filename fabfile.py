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

def sim():
    """Run application remotely."""
    local_file = "tmp/output.xml"
    put(local_file, "/tmp/input.xml")
    run_script_remotely("simulate.sh")


def run_script_remotely(script_file, quiet=False):
    local_file = "scripts/%s" % script_file
    put(local_file, "/tmp", mirror_local_mode=True)
    with cd("/tmp"):
        quiet_str = ">/dev/null 2>&1" if quiet else ""
        run("./%s %s" % (script_file, quiet_str))
        run("rm ./%s" % script_file)
