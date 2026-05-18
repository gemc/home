---
layout: default
title: "Simple flux"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 %}



# Simple Flux Detector
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example uses the **flux digitization**
to save true and digitized information in the output. 

{% assign example = site.data.examples | where: "title", "Simple Flux" | first %}

You can run this example in your browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

The instructions below assume you have already installed GEMC.

<br/>

## Quickstart

To create the geometry and run 10 events in GEMC to produce `ROOT` and `CSV` output files:

```shell
cd $GEMC_HOME/examples/basic/simple_flux
./simple_flux.py
gemc simple_flux.yaml -n=10
```

<br/>

<br/>

## Geometry

The geometry, shown below, is defined in `simple_flux.py`.

The world (a box named %%root%%) contains: 

 - a cylindrical carbon (`G4_C`)  %%target%% 
 - a  %%FluxPlane%%, a box made of air (`G4_AIR`), of increasing transverse size. 
  %%FluxPlane%% is assigned the `flux` digitization. 


{% include figure.html
src="assets/images/examples/simple_flux/geometry.png"
caption="simple_flux geometry, rendered by PyVista: the target and the sensitive flux detector FluxPlane"
%}


<br/>

## Physics List

`FTFP_BERT` is used by default, picked in the yaml file using `phys_list: FTFP_BERT`

{% include notes/physics-list-note.md %}

<br/>

## Generator

The default kinematics is a 2 GeV proton generated along the z-axis just before the target.
A beam size of 0.1 m is used.
This is defined in the yaml file:

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

The %%FluxPlane%% is are associated to the `flux` digitization (one of the available GEMC pre-built routines) 
in `geometry.py`, with identifier %%1%%. 

```python
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
```



{% include notes/flux-note.md %}

In this case, the `identifier` contains only one name: **mychamber**

In addition to the digitized variables, the true information is saved on the output stream.

{% include notes/true_info-note.md %}


<br/>

## Usage

### Building the detector

Use the python script `simple_flux.py` to build the detector. By default, the setup is stored in a SQLite file 
name `gemc.db`. Various command line options can define the database type, variations and run number.

{% include notes/python-api-note.md %}


<br/>

### Running gemc

The file `simple_flux.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc b2.yaml -gui
```

Modify `simple_flux.yaml` as needed, in particular to add particles, control the number of threads, modify the output etc.

<br/>

## Output

The `gstreamer` option is used to select the name and format of the output. Two simultaneous streams are selected, 
`ROOT` and `CSV`:

```yaml
gstreamer:
  - format: csv
    filename: simple_flux
  - format: root
    filename: simple_flux
```

Since `flux` is a per-event digitization, GEMC will produce one output file per thread.
For `ROOT` files, you can use `hadd` to merge the files.


{% include notes/output-note.md %}






<br/>
