---
layout: default
title: "CLAS12 HTCC"
---

# CLAS12 High-Threshold Cherenkov Counter Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows the CLAS12 High-Threshold Cherenkov Counter (HTCC) geometry from `clas12-systems`. It
combines native GEMC mirror optics with CAD meshes loaded through the `gcad` feature. Both systems are stored
in one SQLite database.

The HTCC geometry and digitization are available in `clas12-systems` 0.3 with GEMC 0.5 and `pygemc` 0.5.0.

{% assign example = site.data.examples | where: "title", "HTCC" | first %}

<br/>

## Quickstart

From the `clas12-systems` repository, build the geometry database and run a short simulation:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/htcc
./htcc.py
gemc htcc.yaml -n=1
```

<br/>

## Geometry

The geometry, shown below, is defined in `geometry_src/htcc/geometry.py` and orchestrated by
`geometry_src/htcc/htcc.py`. The native builders port the original clas12Tags perl scripts (gas volume,
windows, 48 elliptical mirrors, and 48 photomultiplier tubes), while the three beamline cones are imported as
CAD meshes. The native rows use the %%htcc%% SQLite system and the mesh rows use the separate %%htcc_cad%% CAD
system. Both share the same database, variation, and run, so one `gemc.db` loads the complete detector.

The world (a box named %%root%%) contains:

- the %%htcc%% gas volume built from polycone booleans, plus the %%htccEntryWindow%% and %%htccExitWindow%%
- 48 elliptical mirror segments carved from a polycone barrel and recorded with the %%htcc_AlMgF2%% optical
  surface
- photomultiplier tubes named %%pmt_<ring>_sector<sector>_<half>%%, read out in two half-sectors per sector
- Winston-cone paraboloid shells sharing the %%htcc_AlMgF2%% mirror skin
- CAD beamline cones (%%htccCone%%, %%htccMollerCone%%, %%htccMollerConeExt%%) placed under %%root%%

Interactive viewer:

{% assign htcc_vtksz = "/home/assets/images/examples/htcc/htcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ htcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 HTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Physics List

The HTCC is a Cherenkov detector, so optical photons must be produced and tracked. The YAML file selects
`FTFP_BERT + G4OpticalPhysics` with `phys_list: FTFP_BERT + G4OpticalPhysics`.

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
    phi: 60*deg
    delta_phi: 180*deg
```

See also the [Internal Generator Documentation]( /home/documentation/generator/internal ) for more information.

<br/>

## Digitization

The photomultiplier tubes use the CLAS12-specific %%htcc%% digitization plugin. The identifiers record the
sector, the mirror ring, and the half-sector the tube reads out:

```python
pmt.digitization = "htcc"
pmt.set_identifier("sector", sector, "ring", ring, "half", hindex)
```

<br/>

## Usage

### Building the detector

Use `geometry_src/htcc/htcc.py` to build the detector. The script defines the materials and mirror surfaces,
publishes the native %%htcc%% volumes, and publishes the three beamline cones as CAD meshes for the
%%htcc_cad%% system. By default, both systems are stored in a SQLite file named `gemc.db`.

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `htcc.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc htcc.yaml -gui
```

Modify `htcc.yaml` as needed, in particular to add particles, control the number of threads, or change the
output.

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/htcc/gemc_view.png"
caption="CLAS12 HTCC simulation: generated electrons crossing the high-threshold Cherenkov counter geometry."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filenames and formats:

```yaml
gstreamer:
  - format: csv
    filename: htcc
  - format: hipo
    filename: htcc
```

See also the [Output Documentation]( /home/documentation/output ) for more information.


## Plotting with the GEMC Analyzer

Run GEMC with 2,000 events first. The default YAML file writes the analyzer CSV streams.

```shell
gemc htcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Plot the total energy deposited per hit:

```shell
gemc-analyzer htcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![htcc total energy deposited per hit][htcc-analyzer_totEdep]{:width="70%"}

[htcc-analyzer_totEdep]: /home/assets/images/examples/htcc/analyzer_totEdep.png

Plot the y vs x hit positions:

```shell
gemc-analyzer htcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![htcc y vs x hit positions][htcc-analyzer_yvsx]{:width="70%"}

[htcc-analyzer_yvsx]: /home/assets/images/examples/htcc/analyzer_yvsx.png
