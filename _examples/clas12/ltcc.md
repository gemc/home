---
layout: default
title: "CLAS12 LTCC"
---

# CLAS12 Low-Threshold Cherenkov Counter Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows the CLAS12 Low-Threshold Cherenkov Counter (LTCC) geometry from `clas12-systems`. It
combines native GEMC mirror optics with CAD meshes loaded through the `gcad` feature. Both systems are stored
in one SQLite database.

**Upcoming in the next release:** the LTCC geometry and digitization are currently available from the
`clas12-systems` development branch.

{% assign example = site.data.examples | where: "title", "LTCC" | first %}

<br/>

## Quickstart

From the `clas12-systems` repository, build the geometry database and run a short simulation:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ltcc
./ltcc.py
gemc ltcc.yaml -n=1
```

<br/>

## Geometry

The geometry, shown below, is defined in `geometry_src/ltcc/geometry.py` and orchestrated by
`geometry_src/ltcc/ltcc.py`. The native builders port the original clas12Tags perl scripts (mirror shapes,
PMTs, and iron shields), while the reflective Winston cones and the mechanical frame are imported as CAD
meshes. The native rows use the %%ltcc%% SQLite system and the mesh rows use the separate %%ltcc_cad%% CAD
system. Both share the same database, variation, and run, so one `gemc.db` loads the complete detector.

The world (a box named %%root%%) contains, for each of the six sectors:

- a gas mother wedge named %%ltccS<sector>%% holding that sector's optics
- cylindrical, hyperbolic, and elliptical mirror segments recorded with the %%ltcc_AlMgF2%% optical surface
- photomultiplier tubes named %%pmt_s<sector><side>_<n>%%, read out on the left and right of each segment
- 5 mm iron shields covering the outer face of the Winston cones
- CAD Winston cones (%%WC_S%%, %%WC_M%%, %%WC_L%%) and frame meshes reused as %%copyOf%% placements

Interactive viewer:

{% assign ltcc_vtksz = "/home/assets/images/examples/ltcc/ltcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ltcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 LTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Physics List

The LTCC is a Cherenkov detector, so optical photons must be produced and tracked. The YAML file selects
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

The photomultiplier tubes use the CLAS12-specific %%ltcc%% digitization plugin. The identifiers record the
sector, the PMT side, and the mirror segment the tube reads out:

```python
pmt.digitization = "ltcc"
pmt.set_identifier("sector", sector, "side", side_id, "segment", n)
```

<br/>

## Usage

### Building the detector

Use `geometry_src/ltcc/ltcc.py` to build the detector. The script defines the materials and mirror surfaces,
publishes the native %%ltcc%% volumes, uploads the CAD definitions for the %%ltcc_cad%% system from
`stls/cad__default.yaml`, and adds the CAD `copyOf` placements. By default, both systems are stored in a
SQLite file named `gemc.db`.

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `ltcc.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc ltcc.yaml -gui
```

Modify `ltcc.yaml` as needed, in particular to add particles, control the number of threads, or change the
output.

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/ltcc/gemc_view.png"
caption="CLAS12 LTCC simulation: generated electrons crossing the low-threshold Cherenkov counter geometry."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filenames and formats:

```yaml
gstreamer:
  - format: csv
    filename: ltcc
  - format: hipo
    filename: ltcc
```

See also the [Output Documentation]( /home/documentation/output ) for more information.


## Plotting with the GEMC Analyzer

Run GEMC with 2,000 events first. The default YAML file writes the analyzer CSV streams.

```shell
gemc ltcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Plot the total energy deposited per hit:

```shell
gemc-analyzer ltcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![ltcc total energy deposited per hit][ltcc-analyzer_totEdep]{:width="70%"}

[ltcc-analyzer_totEdep]: /home/assets/images/examples/ltcc/analyzer_totEdep.png

Plot the y vs x hit positions:

```shell
gemc-analyzer ltcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![ltcc y vs x hit positions][ltcc-analyzer_yvsx]{:width="70%"}

[ltcc-analyzer_yvsx]: /home/assets/images/examples/ltcc/analyzer_yvsx.png
