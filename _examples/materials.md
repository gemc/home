---
layout: default
title: "Materials"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 %}

# Materials Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows how to define custom materials in Python and assign them to GEMC geometry volumes.
The current source example is `gemc/src/examples/basic/b3`.

<br/>

## Quickstart

Copy the example to your current directory.
To create the geometry and run one event:

```shell
cp -r $GEMC_HOME/examples/basic/b3 .
cd b3
./b3.py
gemc b3.yaml -n=1
```

<br/>

## Geometry

The geometry is defined in `geometry.py` and built by `b3.py`.

The world (a box named %%root%%) contains:

- %%Detector%%, an air-filled cylindrical mother volume
- %%Ring1%%, an air-filled cylindrical ring used as a detector-building example

The geometry file also contains commented code showing how additional ring copies can be generated.

<br/>

## Materials

The custom materials are defined in `materials.py`:

- `bepoxy`, an epoxy material defined by the number of atoms of H, N, O, and C
- `bcarbonFiber`, a carbon-fiber material defined by fractional masses of `G4_C` and `bepoxy`

These examples show the two common material-definition patterns: composition by atom count and composition by fractional mass.

<br/>

## Physics List

`QBBC` is used by default, selected in the YAML file with `phys_list: QBBC`.

{% include notes/physics-list-note.md %}

<br/>

## Generator

The default kinematics is a 1.5 GeV electron generated with an angular spread:

```yaml
gparticle:
  - name: e-
    p: 1500
    theta: 23.0
    delta_theta: 4.0
    delta_phi: 18.0
    multiplicity: 1
```

{% include notes/particles-note.md %}

<br/>

## Digitization

The current `b3` source example does not assign a sensitive digitization to any volume.
It is primarily a geometry and material-definition example, so it does not produce detector hit quantities by default.

<br/>

## Usage

### Building the detector

Use the Python script `b3.py` to build the detector. By default, the setup is stored in a SQLite file named `gemc.db`.
Command-line options can define the database type, variations, and run number.

{% include notes/python-api-note.md %}

<br/>

### Running GEMC

The file `b3.yaml` can be used to run the setup.
Add `-gui` to run GEMC interactively:

```shell
gemc b3.yaml -gui
```

Modify `b3.yaml` as needed, in particular to add particles, control the number of threads, or change the output.

<br/>

## Output

The source YAML file does not define a `gstreamer` output block.
Add one if you want GEMC to write output files:

```yaml
gstreamer:
  - format: csv
    filename: b3
  - format: root
    filename: b3
```

{% include notes/output-note.md %}

<br/>

## Plotting with the GEMC Analyzer

Because the current `b3` example has no sensitive digitization, it does not produce detector quantities for the analyzer to plot by default.
After adding a sensitive volume and a `gstreamer` output block, run GEMC with 1,000 events first:

```shell
gemc b3.yaml -n=1000
```

Plot the digitized total energy deposited:

```shell
python3 -m analyzer b3_t0_digitized.csv totEdep --kind csv
```

![materials total energy deposited plot](/home/assets/images/examples/materials/analyzer_totEdep.png){:width="70%"}

Plot the true particle energy:

```shell
python3 -m analyzer b3_t0_true_info.csv E --kind csv --data true_info
```

![materials true energy plot](/home/assets/images/examples/materials/analyzer_true_energy.png){:width="70%"}
