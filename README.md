## POETS Application-level Drug Discovery Tool (PML)

This is a software tool that generates POETS markup (POETS XML) from drug
discovery graph instances (GraphML), and can perform average shortest path
analysis on input problems, serving as a reference implementation for POETS
and other software tools.

The general usage pattern for the tool is `pml.py [options] <sucbommand> <files..>`.

### Usage

```
Usage:
  pml.py [options] apl <file.graphml>
  pml.py [options] apl enable <node_list> <file.graphml>
  pml.py [options] apl disable <node_list> <file.graphml>
  pml.py [options] impact <node_count> <trials> <file.graphml>
  pml.py [options] genxml <template.xml> <file.graphml>

Options:
  -i, --info         Print graph traversal information.
  -w, --workers <n>  Use n parallel workers [default: 1].
  -p, --psuedo       Use psuedo-randomization.
```

### Requirements

PML requires Python 2 and `pip`.

### Installation

Using `virtualenv`:

```bash
git clone https://github.com/tuura/pml.git
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Generating POETS XML

To generate a POETS XML file, you'll need

1. a `jinja2` template xml file (the tool ships with ready-made drug discovery
template `templates/fantasi.xml`)

2. an input problem graph

#### Example

```bash
# Download a test problem graph from POETS website

wget -q https://poets-project.org/download/n3.graphml

# Run the tool

./pml.py genxml templates/fantasi.xml n3.graphml > poets.xml
```

This will generate a POETS application for calculating average shortest path
in the supplied `n3.graphml` problem instance.
