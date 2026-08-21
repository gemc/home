---
layout: default
title: "CLAS12 FT"
---

# CLAS12 Forward Tagger Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows the CLAS12 Forward Tagger (FT) geometry from `clas12-systems`. The FT sits at small
polar angles and is built from three subsystems: an electromagnetic calorimeter, a scintillator hodoscope,
and a Micromegas tracker.

**Upcoming in the next release:** the FT geometry and digitization are currently available from the
`clas12-systems` development branch.

{% assign example = site.data.examples | where: "title", "FT" | first %}

<br/>

## Quickstart

From the `clas12-systems` repository, build the geometry database and run a short simulation:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ft
./ft.py
gemc ft.yaml -n=1
```

<br/>

## Geometry

The geometry, shown below, is defined in `geometry_src/ft/geometry.py` and built by
`geometry_src/ft/ft.py`. The FT builder assembles the three subsystems into a single `gemc.db`:

- the **calorimeter**, a matrix of PbWO4 crystals, each wrapped and coupled to an APD, named
  %%ft_cal_cr_h<ih>_v<iv>%%, plus copper housing, motherboard, and shielding volumes
- the **hodoscope**, scintillator tiles named per sector, layer, and component
- the **tracker**, Micromegas disks with kapton, photoresist, and ring volumes on each layer and side

The world (a box named %%root%%) contains all three subsystems. Flux detectors are added at the calorimeter
and tracker to record the incident particle flux.

Interactive viewer:

{% assign ft_vtksz = "/home/assets/images/examples/ft/ft.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ft_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FT geometry"
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
    p: 2000*MeV
    theta: 3*deg
    phi: 10*deg
    delta_phi: 180*deg
```

See also the [Internal Generator Documentation]( /home/documentation/generator/internal ) for more information.

<br/>

## Digitization

Each FT subsystem uses its own CLAS12-specific digitization plugin. The calorimeter crystals use %%ft_cal%%,
the hodoscope tiles use %%ft_hodo%%, and the tracker disks use %%ft_trk%%. The identifiers record the
component read out, for example the calorimeter crystal row and column:

```python
digitization="ft_cal",
identifiers=("ih", ix, "iv", iy),
```

<br/>

## Usage

### Building the detector

Use `geometry_src/ft/ft.py` to build the detector. By default, the setup is stored in a SQLite file named
`gemc.db`.

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `ft.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc ft.yaml -gui
```

Modify `ft.yaml` as needed, in particular to add particles, control the number of threads, or change the
output.

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/ft/gemc_view.png"
caption="CLAS12 FT simulation: generated electrons crossing the forward tagger geometry."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filenames and formats:

```yaml
gstreamer:
  - format: csv
    filename: ft
  - format: hipo
    filename: ft
```

See also the [Output Documentation]( /home/documentation/output ) for more information.

The forward tagger reads out three detectors (%%ft_cal%%, %%ft_hodo%%, and %%ft_trk%%) with different
identifier structures. The analyzer example below disables true-information and digitized output for the
flux, hodoscope, and tracker detectors so the CSV contains the consistent %%ft_cal%% schema.


## Plotting with the GEMC Analyzer

Run GEMC with 2,000 events first. The default YAML file writes the analyzer CSV streams.

```shell
gemc ft.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build \
  -no_true_info="flux ft_hodo ft_trk" -no_digitized="flux ft_hodo ft_trk"
```

Plot the total energy deposited per hit:

```shell
gemc-analyzer ft_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ft total energy deposited per hit][ft-analyzer_totEdep]{:width="70%"}

[ft-analyzer_totEdep]: /home/assets/images/examples/ft/analyzer_totEdep.png

Plot the y vs x hit positions:

```shell
gemc-analyzer ft_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ft y vs x hit positions][ft-analyzer_yvsx]{:width="70%"}

[ft-analyzer_yvsx]: /home/assets/images/examples/ft/analyzer_yvsx.png
