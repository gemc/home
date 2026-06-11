---
layout: default
title: "Cherenkov"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 exclude_title="Quickstart" %}

[low-img]: /home/assets/images/examples/cherenkov/low_index_radiator.png
[medium-img]: /home/assets/images/examples/cherenkov/medium_index_radiator.png
[high-img]: /home/assets/images/examples/cherenkov/high_index_radiator.png
[lowy-img]: /home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png
[mediumy-img]: /home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png
[highy-img]: /home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png


# Cherenkov Example 
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows how to activate Cherenkov radiation in a GEMC detector.
The three radiator names are neutral demonstration labels. Their optical constants may be unphysical and should
not be read as definitions of real materials.

{% assign example = site.data.examples | where: "title", "Cherenkov" | first %}

You can run this example in your browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Quickstart

Copy the example to your current directory.
To create the geometry, run 1 event, and produce ROOT and CSV output files:

```shell
cp -r $GEMC_HOME/examples/optical/cherenkov .
cd cherenkov
./cherenkov.py
gemc cherenkov.yaml -n=1
```

<br/>

## Geometry

The geometry, shown below, is defined in `cherenkov.py`. It is produced in three variations:
%%default%%, %%mediumIndexRadiator%%, and %%highIndexRadiator%%.

The world (a box named %%root%%) contains a %%radiator%% box. The radiator material depends on the selected variation:

{:.zebra .compact-table}

| variation | material | color | refractive-index range |
|-----------|----------|-------|------------------------|
| %%default%% | %%lowIndexRadiator%% | red | 1.0010-1.0013 |
| %%mediumIndexRadiator%% | %%mediumIndexRadiator%% | blue | 1.0110-1.0150 |
| %%highIndexRadiator%% | %%highIndexRadiator%% | green | 1.0500-1.0530 |


- a %%gPhotonDetector%% detector composed of four boxes (%%detector_left%%, %%detector_right%%, %%detector_top%%, and %%detector_bottom%%). This leaves a small hole in the center for the beam.

Interactive viewer:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/cherenkov/cherenkov.vtksz"
  title="Interactive VTK.js view of the Cherenkov geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="assets/images/examples/cherenkov/high_index_radiator.png"
caption="Cherenkov geometry with 1 generated electron. The highIndexRadiator volume (green, style = 2 renders it as a cloud) is the medium generating Cherenkov radiation."
%}


See the [Buidling Geometry]( /home/documentation/geometry/geometry_building ) for more information.


<br/>

## Physics List

`FTFP_BERT + G4OpticalPhysics` is used by default in the YAML file. The optical physics component is required to produce optical photons.


<br/>

## Generator

The particle kinematics are defined in the YAML file:

```yaml
gparticle:
  - name: e-
    p: 1000*MeV
    vz: -50*cm
```

See also the [Internal Generator Documentation]( /home/documentation/generator/internal ) for more information.


<br/>


## Digitization

The detector volume sensitivities are specified with the %%gPhotonDetector%% digitization (one of the available GEMC prebuilt routines)
in `cherenkov.py`.

The %%identifier%% is used to distinguish the different detector boxes:

```python
backplate.digitization = "gPhotonDetector"
backplate.set_identifier("detector", panel_id)
```

See the [Flux Documentation]( /home/documentation/sensitivity/gPhotonDetector ) for more information.


<br/>

## Usage

### Building the detector

Use the Python script `cherenkov.py` to build the detector. By default, the setup is stored in a SQLite file
named `gemc.db`. Command-line options can define the database type, variations, and run number.

<br/>

### Running gemc

The file `cherenkov.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc cherenkov.yaml -gui
```

The YAML sets `g4view.cloudPoints: 60000` so cloud-style volumes are dense enough for the rendered geometry screenshots.

Modify `cherenkov.yaml` as needed, in particular to add particles, control the number of threads, or change the output.
The %%gPhotonDetector%% digitization records optical photons even when they deposit zero energy, so %%recordZeroEdep%%
is not required for this example.

<br/>

### Variations

Within the YAML file, the variation is set to %%mediumIndexRadiator%%. You can replace it with %%default%% or %%highIndexRadiator%%
to change the material. For example:

```yaml
gsystem:
  - name: cherenkov
    variation: highIndexRadiator
```

Different radiator materials produce different photon yields and angles, as shown below.
Their optical constants are demonstration values and may be unphysical.
Use the variation name in the %%gstreamer%% filename when you want separate output files for each variation.


<br/>

|:---:|:---:|:---:|
| ![low index radiator](/home/assets/images/examples/cherenkov/low_index_radiator.png) | ![medium index radiator](/home/assets/images/examples/cherenkov/medium_index_radiator.png) | ![high index radiator](/home/assets/images/examples/cherenkov/high_index_radiator.png) |
| ![low index radiator y vs x](/home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png) | ![medium index radiator y vs x](/home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png) | ![high index radiator y vs x](/home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png) |

<p class="image-caption">
  Left: <span class="gstring">lowIndexRadiator</span>, Center: <span class="gstring">mediumIndexRadiator</span>, Right: <span class="gstring">highIndexRadiator</span>.
</p>

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/cherenkov/gemc_view.png"
caption="Cherenkov simulation: electron beam entering the radiator volume."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filenames and the format:


```yaml
gstreamer:
  - format: csv
    filename: cherenkov
```

Because %%gPhotonDetector%% is a per-event digitization, GEMC will produce one output file per thread.
For ROOT files, you can use `hadd` to merge the files.

See also the [Output Documentation]( /home/documentation/output ) for more information.

<br/>

## Plotting with the GEMC Analyzer

Run GEMC with 1 events first. The default YAML file writes `cherenkov_t0_digitized.csv`.

```shell
gemc cherenkov.yaml -n=1
```

Plot the total energy deposited per hit:

```shell
gemc-analyzer cherenkov_t0_digitized.csv totEdep --kind csv
```

![Cherenkov total energy deposited per hit](/home/assets/images/examples/cherenkov/analyzer_totEdep.png){:width="70%"}

Plot the y vs x hit positions:

```shell
gemc-analyzer cherenkov_t0_true_info.csv --kind csv --data true_info --plot yvsx --xlim -20 20 --ylim -20 20
```

![Cherenkov y vs x hit positions](/home/assets/images/examples/cherenkov/analyzer_yvsx.png){:width="70%"}
