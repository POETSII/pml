### Generating POETS XML

To generate a POETS XML file, you'll need

1. a `jinja2` template xml file (the tool ships with a ready-made drug
discovery template `templates/fantasi.xml`)

2. an input problem graph

#### Example

```bash
# Download a test problem graph from POETS website

wget -q https://poets-project.org/download/n3.graphml

# Run the tool

./pml.py gen templates/fantasi.xml n3.graphml > poets.xml
```

This will generate a POETS application for calculating average shortest path
in the supplied `n3.graphml` problem instance.

### Reference Algorithms

#### Average Path Length (APL)

The tool can calculate the APL of an input graph as follows:

```
./pml.py apl n3.graphml
```

Refer to the following paper for a definition of APL:

[1] Andrey Mokhov, Alessandro de Gennaro, Ghaith Tarawneh, Jonny Wray, Georgy Lukyanov, Sergey Mileiko, Joe Scott, Alex Yakovlev, Andrew Brown. _Language and Hardware Acceleration Backend for Graph Processing_. Forum on specification & Design Languages (FDL 2017). In Press.
[[paper](https://github.com/tuura/papers/blob/master/fdl-2017/graphs-on-fpga.pdf),
[slides](https://github.com/tuura/papers/blob/master/fdl-2017/graphs-on-fpga-slides.pdf)]

Certain nodes can be excluded from the graph using `apl disable <node_list>` where `<node_list>` is a *double-quoted* list of node names, as they are defined in the input GraphML file, for example:

```
./pml.py apl disable "000001 000002 000003" n3.graphml
```

Note that node names are *strings* and so attempting to run the above with say `./pml.py apl disable "1 2 3" n3.graphml` will result in an error.

In case the disabled nodes form the majority of all nodes, it may be easier to
specify which nodes are _enabled_ instead:

```
./pml.py apl enable "000001 000002 000003" n3.graphml
```

#### Impact Analysis

Impact is a measure of the network perturbance caused by node removal, as a
function of removed node count. Again, refer to [1] for a concrete definition
of _impact_. PML can calculate impact as follows:

```
./pml.py impact 20 10 n3.graphml

[
    2.4294239750908146,
    2.4255504485136035,
    2.443787530580473,
    2.442008303061754,
    2.410037808584773,
    2.4274779449922157,
    2.3967492030543407,
    2.466380013344206,
    2.439228260063756,
    2.4178219289791683
]
```

Here running 10 trials in which 20 random nodes where removed from the graph,
and calculating impact in each case. The output produced by the tool is a JSON list.

Impact analysis can be parallelized using the `--workers` switch.

### Benchmark Problems

These are sample graphs of increasing complexity (n5 is the largest, with 3487
nodes) that PML can convert into POETS XML:

* https://poets-project.org/download/n1.graphml
* https://poets-project.org/download/n2.graphml
* https://poets-project.org/download/n3.graphml
* https://poets-project.org/download/n4.graphml
* https://poets-project.org/download/n5.graphml

The following archive contains 10 more graphs ranging from 1k to 10k nodes
which can be used for stress testing:

* https://poets-project.org/download/big_network_problems.tar.gz

### Sample Generated POETS Markup

These files are generated using the `fantasi.xml` template and the graphs n1
through n5 above:

* https://poets-project.org/download/fantasi-n1.xml
* https://poets-project.org/download/fantasi-n2.xml
* https://poets-project.org/download/fantasi-n3.xml
* https://poets-project.org/download/fantasi-n4.xml
* https://poets-project.org/download/fantasi-n5.xml

### Other Tools

The repo contains a simple support tool `gml.py` that can be used to generate
random graphs in GraphML format (usage is `gml.py <nodes> <edges>`).
