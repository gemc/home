---
layout: default
title: "CAD example"
---

# CAD Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example imports three STL organ meshes with the GEMC CAD factory and uses the %%dosimeter%%
digitization to record deposited energy and dose for each organ.

<br/>

## Quickstart

Copy the example to your current directory. To upload the CAD definitions, run 10 events, and
produce CSV output:

```shell
cp -r $GEMC_HOME/examples/basic/cad .
cd cad
./cad.py
gemc cad.yaml -n=10
```

<br/>

## Geometry

The geometry is defined declaratively in `stls/cad__default.yaml` and uploaded into `gemc.db` by
`cad.py`.

The CAD system named %%stls%% contains:

- %%heart_NIH3D%%, a blood-material heart mesh.
- %%respiratory_NIH3D%%, a translucent lung mesh made with %%G4_LUNG_ICRP%%.
- %%liver_NIH3D%%, a soft-tissue liver mesh.

Each entry in `stls/cad__default.yaml` sets the mesh file, material, color, scale, position, and
identifier. The %%system%% value must match both the `gsystem` name in `cad.yaml` and the directory
that contains the STL files.

See also the [CAD Imports Documentation](/home/documentation/geometry/cad_imports) for more
information.

Interactive viewer:

<iframe
  src="/home/assets/vtkjs-viewer.html?fileURL=/home/assets/images/examples/cad/cad.vtksz"
  title="Interactive VTK.js view of the CAD organ geometry"
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
  - name: gamma
    p: 1250*keV
    multiplicity: 200
    theta: 0*deg
    delta_theta: 12*deg
    phi: 0*deg
    delta_phi: 180*deg
    vz: -1000*mm
```

The source is placed 1 m upstream of the organs and emits a broad forward cone of 1.25 MeV gamma
rays.

See also the [Internal Generator Documentation](/home/documentation/generator/internal) for more
information.

<br/>

## Digitization

Each organ is configured as a %%dosimeter%% sensitive detector in `stls/cad__default.yaml`:

```yaml
defaults:
  digitization: dosimeter

volumes:
  - name: heart_NIH3D
    identifier: "organ: 1"
```

The %%dosimeter%% digitization creates and accumulates the variables %%etot%% and %%dose%% throughout
events in a run.

$$
\mathrm{dose} = \frac{\mathrm{etot}}{\mathrm{mass}}
$$

where %%etot%% is the total energy deposited in each event and %%mass%% is the organ mass computed
from the CAD mesh and assigned material.

See the [Dosimeter Documentation](/home/documentation/sensitivity/dosimeter) for more information.

<br/>

## Usage

### Building the detector

Use the Python script `cad.py` to upload the CAD definitions. The script reads
`stls/cad__default.yaml` and stores the setup in a SQLite file named `gemc.db`.

```shell
./cad.py
```

{% include notes/python-api-note.md %}

See also the [Building Geometry](/home/documentation/geometry/geometry_building) for more
information.

<br/>

### Running GEMC

The file `cad.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc cad.yaml -gui
```

Modify `cad.yaml` as needed, in particular to add particles, control the number of threads, or
change the output.

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/cad/gemc_view.png"
caption="CAD simulation: gamma rays traversing the imported heart, lung, and liver meshes."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filename and format:

```yaml
gstreamer:
  - format: csv
    filename: organs
```

{% include notes/output-note.md %}

See also the [Output Documentation](/home/documentation/output) for more information.

<br/>

## Plotting with the GEMC Analyzer

Run GEMC with 20 events first. The default YAML file writes the analyzer CSV streams.

```shell
gemc cad.yaml -n=20
```

Plot the accumulated dose:

```shell
gemc-analyzer organs_digitized.csv dose --kind csv
```

![cad accumulated dose](/home/assets/images/examples/cad/analyzer_dose.png){:width="70%"}
