import os
import jinja2

from random import sample
from string import lowercase
from fabric.api import run
from fabric.api import sudo
from fabric.api import cd
from fabric.api import env
from fabric.state import output
from fabric.operations import put
from fabric.operations import get
from fabric.contrib.files import exists

output["status"]   = False
output["running"]  = False
env.output_prefix  = False
env.use_ssh_config = True

def sim(template):
    """Prepare XML file."""

    temp_output = '/tmp/output.xml'
    template_path = os.path.abspath(template)
    template_dir, template_file = os.path.split(template_path)

    def include_file(file):
        """Return the text content of a 'file' inside template_dir."""

        full_file = os.path.join(template_dir, file)
        with open(full_file, "r") as fid:
            return fid.read()

    loader = jinja2.PackageLoader(__name__, '')
    env = jinja2.Environment(loader=loader)
    env.globals['include_file'] = include_file

    content = env.get_template(template).render()
    write_file(content, temp_output)

    put(temp_output, "/tmp/input.xml")
    run_script("simulate.sh")


def write_file(text, file):
    with open(file, "w") as fid:
        fid.write(text)


def run_script(script_file, quiet=False):
    local_file = "scripts/%s" % script_file
    put(local_file, "/home/vagrant", mirror_local_mode=True)
    with cd("/home/vagrant"):
        quiet_str = ">/dev/null 2>&1" if quiet else ""
        run("./%s %s" % (script_file, quiet_str))
        run("rm ./%s" % script_file)
