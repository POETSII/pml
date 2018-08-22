from fabric.api import cd
from fabric.api import env
from fabric.state import output
from fabric.operations import run
from fabric.operations import put
from fabric.operations import local


output["status"]   = False
output["running"]  = False
env.output_prefix  = False
env.use_ssh_config = True


def sim():
    """Run application remotely."""
    local_file = "tmp/output.xml"
    put(local_file, "/tmp/input.xml")
    run_script_remotely("simulate.sh")


def gen():
    """Generate application (locally)."""
    local("./gen.sh")


def hardware():
    """Run application on remote POETS machine."""
    local_file = "tmp/output.xml"
    put(local_file, "~/network/output.xml")
    run_script_remotely("run_on_hardware.sh", workdir="~/network")


def run_script_remotely(script_file, workdir="/tmp", quiet=False):
    local_file = "scripts/%s" % script_file
    put(local_file, workdir, mirror_local_mode=True)
    with cd(workdir):
        quiet_str = ">/dev/null 2>&1" if quiet else ""
        run("./%s %s" % (script_file, quiet_str))
        run("rm ./%s" % script_file)
