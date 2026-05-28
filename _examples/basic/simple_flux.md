---
layout: default
title: "Simple flux"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 exclude_title="Quickstart" %}



# Simple Flux Detector
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example uses the %%flux%% digitization to save true and digitized information in the output.

{% assign example = site.data.examples | where: "title", "Simple Flux" | first %}

You can run this example in your browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Quickstart

Copy the example to your current directory.
To create the geometry, run 10 events, and produce ROOT and CSV output files:

```shell
cp -r $GEMC_HOME/examples/basic/simple_flux .
cd simple_flux
./simple_flux.py
gemc simple_flux.yaml -n=10
```

<br/>

## Geometry

The geometry, shown below, is defined in `simple_flux.py`.

The world (a box named %%root%%) contains:

- %%target%%, a cylindrical liquid hydrogen target (%%G4_lH2%%)
- %%FluxPlane%%, a box made of air (%%G4_AIR%%) and assigned the %%flux%% digitization


{% include figure.html
src="assets/images/examples/simple_flux/geometry.png"
caption="simple_flux geometry, rendered by PyVista: the target and the sensitive flux detector FluxPlane"
%}

Interactive viewer:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/simple_flux/simple_flux.vtksz"
  title="Interactive VTK.js view of the simple_flux geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>


<br/>

## Physics List

`QBBC` is used by default, selected in the YAML file with `phys_list: QBBC`.

{% include notes/physics-list-note.md %}

<br/>

## Generator

The default kinematics is a 2 GeV proton generated along the z-axis just before the target.
A beam size of 0.1 cm is used.
This is defined in the YAML file:

```yaml
gparticle:
  - name: proton
    p: 2000
    vz: -3
    delta_vx: 0.1
    delta_vy: 0.1
    multiplicity: 10
```

{% include notes/particles-note.md %}

<br/>


## Digitization

The %%FluxPlane%% is associated with the %%flux%% digitization (one of the available GEMC prebuilt routines)
in `simple_flux.py`, with identifier %%flux_plane = 1%%.

```python
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
```



{% include notes/flux-note.md %}

In this case, the %%identifier%% contains one name: %%flux_plane%%.

In addition to the digitized variables, the true information is saved on the output stream.

{% include notes/true_info-note.md %}


<br/>

## Usage

### Building the detector

Use the Python script `simple_flux.py` to build the detector. By default, the setup is stored in a SQLite file
named `gemc.db`. Command-line options can define the database type, variations, and run number.

{% include notes/python-api-note.md %}


<br/>

### Running gemc

The file `simple_flux.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc simple_flux.yaml -gui
```

Modify `simple_flux.yaml` as needed, in particular to add particles, control the number of threads, or change the output.

<br/>

## Output

The %%gstreamer%% option selects the output name and format. Two simultaneous streams are selected:
ROOT and CSV.

```yaml
gstreamer:
  - format: csv
    filename: simple_flux
  - format: root
    filename: simple_flux
```

Because %%flux%% is a per-event digitization, GEMC will produce one output file per thread.
For ROOT files, you can use `hadd` to merge the files.


{% include notes/output-note.md %}






<br/>

## Plotting with the GEMC Analyzer

Run GEMC with 10,000 events first. The default YAML file writes `simple_flux_t0_digitized.csv` and `simple_flux_t0_true_info.csv`.

```shell
gemc simple_flux.yaml -n=10000
```

Plot the digitized total energy deposited:

```shell
python3 -m analyzer simple_flux_t0_digitized.csv totEdep --kind csv
```

![simple flux total energy deposited plot](/home/assets/images/examples/simple_flux/analyzer_totEdep.png){:width="70%"}

Plot the true particle track total energy:

```shell
python3 -m analyzer simple_flux_t0_true_info.csv E --kind csv --data true_info
```

![simple flux true track total energy plot](/home/assets/images/examples/simple_flux/analyzer_true_energy.png){:width="70%"}
