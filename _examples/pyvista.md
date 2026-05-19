---
layout: default
title: "PyVista"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 %}

# PyVista Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example shows how to create PyVista meshes and publish them as GEMC volumes.
The current source example is `gemc/src/examples/basic/pyvista`.

<br/>

## Quickstart

Copy the example to your current directory.
To open the PyVista visualization:

```shell
cp -r $GEMC_HOME/examples/basic/pyvista .
cd pyvista
./pyvista_basic_shapes.py
```

To publish the PyVista meshes as GEMC volumes:

```shell
./gemc_pyvista.py
```

<br/>

## Geometry

The geometry is defined in `pyvista_basic_shapes.py`.

The example creates:

- %%cube%%, a light-blue PyVista cube published as a GEMC volume with material `G4_AIR`
- %%cylinder%%, a light-green PyVista cylinder placed inside %%cube%% with material `G4_WATER`

`gemc_pyvista.py` converts the `GMesh` objects into `GVolume` objects and publishes them through the GEMC Python API.

<br/>

## Physics List

This example focuses on PyVista geometry conversion and does not define a GEMC physics list.

<br/>

## Generator

This example focuses on geometry visualization and conversion. It does not define generated particles.

<br/>

## Digitization

The current PyVista example does not assign a sensitive digitization to any volume.
It does not produce detector hit quantities by default.

<br/>

## Usage

### Building the detector

Run `gemc_pyvista.py` to publish the PyVista meshes as GEMC volumes.
The script enables PyVista support directly through `autogeometry`.

<br/>

### Running GEMC

The current source example does not include a YAML steering file.
To run it through GEMC, add a steering file that selects the published system, a physics list, generated particles, and output streams.

<br/>

## Output

The current source example is a geometry-conversion demonstration and does not configure GEMC output.

<br/>

## Plotting with the GEMC Analyzer

Because the current PyVista example has no steering file, generated particles, or sensitive digitization, it does not produce detector quantities for the analyzer to plot by default.
After adding those pieces, run GEMC with 1,000 events first:

```shell
gemc pyvista.yaml -n=1000
```

Plot the digitized total energy deposited:

```shell
python3 -m analyzer pyvista_t0_digitized.csv totEdep --kind csv
```

![PyVista total energy deposited plot](/home/assets/images/examples/pyvista/analyzer_totEdep.png){:width="70%"}

Plot the true particle energy:

```shell
python3 -m analyzer pyvista_t0_true_info.csv E --kind csv --data true_info
```

![PyVista true energy plot](/home/assets/images/examples/pyvista/analyzer_true_energy.png){:width="70%"}
