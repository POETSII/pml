import os

from fabric.api import cd
from fabric.api import env
from fabric.context_managers import shell_env
from fabric.state import output
from fabric.operations import run
from fabric.operations import put
from fabric.operations import local
from fabric.contrib.files import exists


output["status"]        = False
output["running"]       = False
env.output_prefix       = False
env.use_ssh_config      = True
env.connection_attempts = 10


def rbuild(local_file, remote_dir):
    """Build application ELF on remote POETS machine."""
    run("mkdir -p %s" % remote_dir)
    remote_file = os.path.join(remote_dir, "output.xml")
    put(local_file, remote_file)
    return run_script_remotely("pts-xmlc.sh", remote_dir)


def rrun(remote_dir="~/network"):
    """Run application EOF on remote POETS machine."""
    return run_script_remotely("pts-serve.sh", workdir=remote_dir)


def run_script_remotely(script_file, workdir="/tmp", quiet=False):
    local_file = os.path.join("scripts", script_file)
    put(local_file, workdir, mirror_local_mode=True)
    with cd(workdir):
        quiet_str = ">/dev/null 2>&1" if quiet else ""
        output = run("./%s %s" % (script_file, quiet_str))
        run("rm ./%s" % script_file)
        return output
