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

This example showcases the activation of the Cherenkov radiation in a GEMC detector.

<br/>

## Quickstart

To create the geometry and run GEMC to produce an ASCII and `ROOT` file:

```shell
cd $GEMC/examples/optical/cherenkov
./cherenkov.py
gemc cherenkov.yaml
```

<br/>

<br/>

## Geometry

The geometry, shown below, is defined in `cherenkov.py`. It is produced in three variations: `default`, `CO2` and `C4F10`.  

The world contains: 

 - a radiator, made up of different materials depending on the variation chosen:

{:.zebra .compact-table}

| variation | material                   | color | 
|-----------|----------------------------|-------|
| default   | Carbon tetrafluoride `CF4` | red   |
| CO2       | Carbon dioxide `CO2`       | blue  |
| C4F10     | Perfluorobutane `C4F10`    | green |


 - a  `flux` detector composed of 4 boxes in order to leave a small hole in the center to let
   the beam pass through.


{% include figure.html
src="assets/images/examples/cherenkov/geometry.png"
caption="Cherenkov geometry. The `CF4` default radiator (red, style = 2 renders it as cloud) is the medium generating cherenkov radiation."
%}


<br/>

## Physics List

`FTFP_BERT + G4OpticalPhysics` is used by default in the YAML file.
Notice the addition of the optical physics.


<br/>

## Generator

The default kinematics is a 1 GeV electron beam generated along the z-axis near the start of the radiator.
This is defined in the YAML file:

```yaml
gparticle:
  - name: e-
    p: 1000
    vz: -50
    delta_theta: 20
    delta_phi: 180
```


<br/>


## Digitization

The detector volumes are associated to the `flux` digitization (one of the available GEMC pre-built routines) 
in `geometry.py`. 

The identifier is used to distinguish the different detector boxes.


<br/>

## Usage

### Building the detector

Use the python script `cherenkov.py` to build the detector. By default, the setup is stored in a SQLite file 
name `gemc.db`. Various command line options can define the database type, variations and run number.

<br/>

### Running gemc

The file `cherenkov.yaml` can be used to run the setup. Add `-gui` to run in interactively:

```shell
gemc cherenkov.yaml -gui
```


Modify `cherenkov.yaml` as needed, in particular to add particles, control the number of threads, modify the output, etc.
Notice that since we are using the `flux` digitization, we need to set `recordZeroEdep` to `true` in order to 
record the optical photons, because by default the `flux` digitization does not record hits if the energy is zero.

<br/>

### Variations

Within the YAML file, the variation is set to `default`. You can replace it `CO2` or `C4F10` 
to change the material. For example:

```yaml
gsystem:
  - name: cherenkov
    variation: C4F10
```

Different radiators material will produce different photon yields, and at different angles, see the image below.
We suggest tp match the variation name to the file name in the `gstreamer` option.


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
`ROOT` and `ASCII`:


Since `flux` is a per-event digitization, GEMC will produce one output file per thread.
For `ROOT` files, you can use `hadd` to merge the files.



<br/>

<br/>
