---
layout: default
title: "CLAS12 DC"
---

# CLAS12 Drift Chamber Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows the CLAS12 drift chamber geometry from `clas12-systems`. It is upcoming in the next
release.

{% assign example = site.data.examples | where: "title", "DC" | first %}

<br/>

## Quickstart

From the `clas12-systems` repository, build the geometry database and run a short simulation:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/dc
./dc.py
gemc dc.yaml -n=1
```

<br/>

## Geometry

The geometry, shown below, is defined in `geometry_src/dc/dc.py` and `geometry_src/dc/geometry.py`.
The DC builder reads the local coatjava geometry factory, converts the CLAS12 drift chamber regions and
superlayers to GEMC volumes, and stores them in `gemc.db`.

The world (a box named %%root%%) contains:

- six sectors of region mother volumes named %%region1_s1%% through %%region3_s6%%
- six sectors of superlayer volumes named %%sl1_s1%% through %%sl6_s6%%

Interactive viewer:

{% assign dc_vtksz = "/home/assets/images/examples/dc/dc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ dc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 DC geometry"
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

The superlayer sensitivities use the CLAS12-specific %%dc%% digitization plugin. The identifiers record sector,
superlayer, layer, and wire numbers:

```python
gvolume.digitization = "dc"
gvolume.set_identifier("sector", sector, "superlayer", superlayer, "layer", 1, "wire", 1)
```

<br/>

## Usage

### Building the detector

Use `geometry_src/dc/dc.py` to build the detector. By default, the setup is stored in a SQLite file named
`gemc.db`.

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `dc.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc dc.yaml -gui
```

Modify `dc.yaml` as needed, in particular to add particles, control the number of threads, or change the output.

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/dc/gemc_view.png"
caption="CLAS12 DC simulation: generated electrons crossing the drift chamber geometry."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filenames and formats:

```yaml
gstreamer:
  - format: csv
    filename: dc
  - format: hipo
    filename: dc
```

See also the [Output Documentation]( /home/documentation/output ) for more information.


## Plotting with the GEMC Analyzer

Run GEMC with 2,000 events first. The default YAML file writes the analyzer CSV streams.

```shell
gemc dc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Plot the total energy deposited per hit:

```shell
gemc-analyzer dc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![DC total energy deposited per hit](/home/assets/images/examples/dc/analyzer_totEdep.png){:width="70%"}

Plot the y vs x hit positions:

```shell
gemc-analyzer dc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![DC y vs x hit positions](/home/assets/images/examples/dc/analyzer_yvsx.png){:width="70%"}

Plot the digitized TDC time:

```shell
gemc-analyzer dc_t0_digitized.csv TDC_TDC --kind csv
```

![DC digitized TDC time](/home/assets/images/examples/dc/analyzer_tdc.png){:width="70%"}
