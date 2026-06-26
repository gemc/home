---
layout: default
title: "CLAS12 PCAL"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 exclude_title="Quickstart" %}

# CLAS12 Preshower Calorimeter Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows the CLAS12 Preshower Calorimeter (PCAL) geometry from `clas12-systems`. It is upcoming
in the next release.

{% assign example = site.data.examples | where: "title", "PCAL" | first %}

<br/>

## Quickstart

From the `clas12-systems` repository, build the geometry database and run a short simulation:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/pcal
./pcal.py
gemc pcal.yaml -n=1
```

<br/>

## Geometry

The geometry, shown below, is defined in `geometry_src/pcal/pcal.py` and `geometry_src/pcal/geometry.py`.
The PCAL builder reads the local coatjava geometry factory, converts the CLAS12 preshower calorimeter
sectors, windows, lead layers, scintillator layers, and U, V, and W strip volumes to GEMC volumes, and
stores them in `gemc.db`.

The world (a box named %%root%%) contains, for each of the six sectors:

- sector mother volumes named %%pcal_s1%% through %%pcal_s6%%
- front and back stainless-steel windows named %%Stainless_Steel_Front_...%% and
  %%Stainless_Steel_Back_...%%
- front and back Last-a-Foam windows named %%Last-a-Foam_Front_...%% and %%Last-a-Foam_Back_...%%
- lead layers named %%PCAL_Lead_Layer_<layer>_s<sector>%%
- U, V, and W scintillator layer mothers and single/double strip volumes

The PCAL is a large geometry, so the example sets `pyvista-fast: true` in `_data/examples.yml` to use the
fast PyVista rendering path when exporting the interactive view below.

Interactive viewer:

{% assign pcal_vtksz = "/home/assets/images/examples/pcal/pcal.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ pcal_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 PCAL geometry"
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

The scintillator strips use the shared CLAS12 %%ecal%% digitization plugin. PCAL writes to the same ECAL banks
as the EC system, using hipo layers 1 through 3. The identifiers record sector, layer, and strip numbers:

```python
gvolume.digitization = "ecal"
gvolume.set_identifier("sector", sector, "layer", layer, "strip", pcal_strip_id(uvw, kind, strip))
```

<br/>

## Usage

### Building the detector

Use `geometry_src/pcal/pcal.py` to build the detector. By default, the setup is stored in a SQLite file
named `gemc.db`.

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `pcal.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc pcal.yaml -gui
```

Modify `pcal.yaml` as needed, in particular to add particles, control the number of threads, or change the
output.

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/pcal/gemc_view.png"
caption="CLAS12 PCAL simulation: generated electrons crossing the preshower calorimeter geometry."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filenames and formats:

```yaml
gstreamer:
  - format: csv
    filename: pcal
  - format: hipo
    filename: pcal
```

See also the [Output Documentation]( /home/documentation/output ) for more information.


## Plotting with the GEMC Analyzer

Run GEMC with 2,000 events first. The default YAML file writes the analyzer CSV streams.

```shell
gemc pcal.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Plot the total energy deposited per hit:

```shell
gemc-analyzer pcal_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![PCAL total energy deposited per hit](/home/assets/images/examples/pcal/analyzer_totEdep.png){:width="70%"}

Plot the y vs x hit positions:

```shell
gemc-analyzer pcal_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![PCAL y vs x hit positions](/home/assets/images/examples/pcal/analyzer_yvsx.png){:width="70%"}
