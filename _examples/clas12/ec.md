---
layout: default
title: "CLAS12 EC"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 exclude_title="Quickstart" %}

# CLAS12 Electromagnetic Calorimeter Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows the CLAS12 electromagnetic calorimeter (EC) geometry from `clas12-systems`. It is upcoming
in the next release.

{% assign example = site.data.examples | where: "title", "EC" | first %}

<br/>

## Quickstart

From the `clas12-systems` repository, build the geometry database and run a short simulation:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ec
./ec.py
gemc ec.yaml -n=1
```

<br/>

## Geometry

The geometry, shown below, is defined in `geometry_src/ec/ec.py` and `geometry_src/ec/geometry.py`.
The EC builder reads the local coatjava geometry factory, converts the CLAS12 calorimeter sectors, lids, lead
absorbers, and scintillator strips to GEMC volumes, and stores them in `gemc.db`.

The world (a box named %%root%%) contains:

- six sector mother volumes named %%ec_s1%% through %%ec_s6%%
- three lid layers per sector (%%eclid1%% to %%eclid3%%): two stainless-steel skins and a Last-a-Foam core
- lead absorber layers named %%lead_<layer>_s<sector>_view_<view>_stack_<stack>%%
- U, V, and W scintillator strips named %%U_strip_...%%, %%V_strip_...%%, and %%W_strip_...%%

The EC is a large geometry, so the example sets `pyvista-fast: true` in `_data/examples.yml` to use the fast
PyVista rendering path when exporting the interactive view below.

Interactive viewer:

{% assign ec_vtksz = "/home/assets/images/examples/ec/ec.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ec_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 EC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Physics List

`FTFP_BERT` is used by default, selected in the YAML file with `phys_list: FTFP_BERT`.

{% include notes/physics-list-note.md %}

<br/>

## Generator

The particle kinematics are defined in the YAML file:

```yaml
gparticle:
  - name: e-
    p: 5000*MeV
    delta_p: 1*GeV
    theta: 25*deg
    delta_theta: 15*deg
    randomThetaModel: cosine
    delta_phi: 180*deg
```

See also the [Internal Generator Documentation]( /home/documentation/generator/internal ) for more information.

<br/>

## Digitization

The scintillator strips use the CLAS12-specific %%ec%% digitization plugin. The identifiers record sector,
layer, and strip numbers:

```python
gvolume.digitization = "ec"
gvolume.set_identifier("sector", sector, "layer", hipo_layer, "strip", strip)
```

<br/>

## Usage

### Building the detector

Use `geometry_src/ec/ec.py` to build the detector. By default, the setup is stored in a SQLite file named
`gemc.db`.

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `ec.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc ec.yaml -gui
```

Modify `ec.yaml` as needed, in particular to add particles, control the number of threads, or change the output.

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/ec/gemc_view.png"
caption="CLAS12 EC simulation: generated electrons showering in the electromagnetic calorimeter geometry."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filenames and formats:

```yaml
gstreamer:
  - format: csv
    filename: ec
  - format: hipo
    filename: ec
```

See also the [Output Documentation]( /home/documentation/output ) for more information.
