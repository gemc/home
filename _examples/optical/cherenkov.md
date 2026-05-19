---
layout: default
title: "Cherenkov"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 %}

[default-img]: /home/assets/images/examples/cherenkov/default.png
[CO2-img]: /home/assets/images/examples/cherenkov/co2.png
[C4F10-img]: /home/assets/images/examples/cherenkov/c4f10.png
[defaulty-img]: /home/assets/images/examples/cherenkov/default_yield.png
[CO2y-img]: /home/assets/images/examples/cherenkov/co2_yield.png
[C4F10y-img]: /home/assets/images/examples/cherenkov/c4f10_yield.png


# Cherenkov Example 
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows how to activate Cherenkov radiation in a GEMC detector.

{% assign example = site.data.examples | where: "title", "Cherenkov" | first %}

You can run this example in your browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Quickstart

Copy the example to your current directory.
To create the geometry, run 10 events, and produce `ROOT` and `CSV` output files:

```shell
cp -r $GEMC_HOME/examples/optical/cherenkov .
cd cherenkov
./cherenkov.py
gemc cherenkov.yaml -n=10
```

<br/>

## Geometry

The geometry, shown below, is defined in `cherenkov.py`. It is produced in three variations: `default`, `CO2`, and `C4F10`.

The world (a box named %%root%%) contains a %%radiator%% box. The radiator material depends on the selected variation:

{:.zebra .compact-table}

| variation | material                   | color | 
|-----------|----------------------------|-------|
| default   | Carbon tetrafluoride `CF4` | red   |
| CO2       | Carbon dioxide `CO2`       | blue  |
| C4F10     | Perfluorobutane `C4F10`    | green |


- a `flux` detector composed of four boxes (%%detector_left%%, %%detector_right%%, %%detector_top%%, and %%detector_bottom%%). This leaves a small hole in the center for the beam.


{% include figure.html
src="assets/images/examples/cherenkov/geometry.png"
caption="Cherenkov geometry. The CF4 default radiator (red, style = 2 renders it as a cloud) is the medium generating Cherenkov radiation."
%}

Interactive viewer:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/cherenkov/cherenkov.vtksz"
  title="Interactive VTK.js view of the Cherenkov geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>


<br/>

## Physics List

`FTFP_BERT + G4OpticalPhysics` is used by default in the YAML file. The optical physics component is required to produce optical photons.


<br/>

## Generator

The default kinematics is a 1 GeV electron beam generated along the z-axis near the start of the radiator.
This is defined in the YAML file:

```yaml
gparticle:
  - name: e-
    p: 1000
    vz: -50
```


<br/>


## Digitization

The detector volumes are associated with the `flux` digitization (one of the available GEMC pre-built routines)
in `cherenkov.py`.

The identifier is used to distinguish the different detector boxes:

```python
backplate.digitization = "flux"
backplate.set_identifier("detector", panel_id)
```


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


Modify `cherenkov.yaml` as needed, in particular to add particles, control the number of threads, or change the output.
Because this example uses `flux` digitization for optical photons, `recordZeroEdep` must be set to `true`.
Optical photons deposit zero energy, and the `flux` digitization does not record zero-energy hits by default.

<br/>

### Variations

Within the YAML file, the variation is set to `CO2`. You can replace it with `default` or `C4F10`
to change the material. For example:

```yaml
gsystem:
  - name: cherenkov
    variation: C4F10
```

Different radiator materials produce different photon yields and angles, as shown below.
Use the variation name in the `gstreamer` filename when you want separate output files for each variation.


<br/>

|:---------------:|:-----------:|:-----------:|
| ![default-img]  | ![CO2-img]  | ![C4F10-img] |
| ![defaulty-img] | ![CO2y-img] | ![C4F10y-img] |

<p class="image-caption">
  Left: default (<code>CF4</code>) radiator, Center: <code>CO2</code>, Right: <code>C4F10</code>.
</p>

<br/>

## Output

The `gstreamer` option is used to select the name and format of the output. Two simultaneous streams are selected, 
`CSV` and `ROOT`:

```yaml
gstreamer:
  - format: csv
    filename: cherenkov
  - format: root
    filename: cherenkov
```

Because `flux` is a per-event digitization, GEMC will produce one output file per thread.
For `ROOT` files, you can use `hadd` to merge the files.

{% include notes/output-note.md %}

<br/>

## Plotting with the GEMC Analyzer

Run GEMC with 1,000 events first. The default YAML file writes `cherenkov_t0_digitized.csv` and `cherenkov_t0_true_info.csv`.

```shell
gemc cherenkov.yaml -n=1000
```

Plot the digitized photon energy:

```shell
python3 -m analyzer cherenkov_t0_digitized.csv E --kind csv
```

![Cherenkov digitized energy plot](/home/assets/images/examples/cherenkov/analyzer_digitized_energy.png){:width="70%"}

Plot the true particle track total energy:

```shell
python3 -m analyzer cherenkov_t0_true_info.csv E --kind csv --data true_info
```

![Cherenkov true track total energy plot](/home/assets/images/examples/cherenkov/analyzer_true_energy.png){:width="70%"}

<br/>

<br/>
