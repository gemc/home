---
layout: default
title: "CLAS12 FTOF"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 exclude_title="Quickstart" %}

# CLAS12 Forward Time-of-Flight Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows the CLAS12 Forward Time-of-Flight (FTOF) geometry from `clas12-systems`. It is upcoming
in the next release.

{% assign example = site.data.examples | where: "title", "FTOF" | first %}

<br/>

## Quickstart

From the `clas12-systems` repository, build the geometry database and run a short simulation:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ftof
./ftof.py
gemc ftof.yaml -n=1
```

<br/>

## Geometry

The geometry, shown below, is defined in `geometry_src/ftof/ftof.py` and `geometry_src/ftof/geometry.py`.
The FTOF builder reads the local coatjava geometry factory, converts the CLAS12 forward TOF panels and
scintillator paddles to GEMC volumes, and stores them in `gemc.db`.

The world (a box named %%root%%) contains, for each of the six sectors:

- three panel mother volumes named %%ftof_p1a_s<sector>%%, %%ftof_p1b_s<sector>%%, and %%ftof_p2_s<sector>%%
- scintillator paddles named %%panel1a_sector<sector>_paddle_<n>%% (23 paddles), %%panel1b_...%% (62), and
  %%panel2_...%% (5)
- a lead shield behind panels 1a and 2 named %%ftof_shield_p1a_sector<sector>%% and
  %%ftof_shield_p2_sector<sector>%%

Interactive viewer:

{% assign ftof_vtksz = "/home/assets/images/examples/ftof/ftof.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ftof_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FTOF geometry"
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
    delta_theta: 12*deg
    randomThetaModel: cosine
    delta_phi: 180*deg
```

See also the [Internal Generator Documentation]( /home/documentation/generator/internal ) for more information.

<br/>

## Digitization

The scintillator paddles use the CLAS12-specific %%ftof%% digitization plugin. Each paddle is read out at
both ends, so the plugin splits every hit into a Left and a Right PMT channel. The identifiers record
sector, panel, paddle, and PMT side:

```python
gvolume.digitization = "ftof"
gvolume.set_identifier("sector", sector, "panel", layer, "paddle", paddle, "side", 0)
```

<br/>

## Usage

### Building the detector

Use `geometry_src/ftof/ftof.py` to build the detector. By default, the setup is stored in a SQLite file
named `gemc.db`.

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `ftof.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc ftof.yaml -gui
```

Modify `ftof.yaml` as needed, in particular to add particles, control the number of threads, or change the
output.

<br/>

## Output

The %%gstreamer%% option selects the output filenames and formats:

```yaml
gstreamer:
  - format: csv
    filename: ftof
  - format: hipo
    filename: ftof
```

See also the [Output Documentation]( /home/documentation/output ) for more information.
