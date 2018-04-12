from graph import Graph
from exporter import generate_xml
from fabric.api import run
from fabric.api import cd
from fabric.api import env
from fabric.state import output
from fabric.operations import put

output["status"]   = False
output["running"]  = False
env.output_prefix  = False
env.use_ssh_config = True

def sim(template, graphml):
    """Run (remote) simulation using template and graphml files."""

    # Prepare flat xml file (tmp_output)
    temp_output = 'tmp/output.xml'
    graph = Graph(graphml)
    xml = generate_xml(template, graph)
    write_file(xml, temp_output)

    # Put file on remote machine and simulate
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
