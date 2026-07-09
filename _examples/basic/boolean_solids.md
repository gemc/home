---
layout: default
title: "Boolean Solids"
---

# Boolean Solids Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example demonstrates GEMC boolean solid operations. It builds three placed solids from
unplaced component volumes: a plate with a subtracted hole, a cross made from a union, and a lens
made from the intersection of two spheres.

<br/>

## Quickstart

Copy the example to your current directory.
To create the geometry and run 10 events:

```shell
cp -r $GEMC_HOME/examples/basic/boolean_solids .
cd boolean_solids
./boolean_solids.py
gemc boolean_solids.yaml -n=10
```

<br/>

## Geometry

The geometry is defined in `boolean_solids.py`.

The world (a box named %%root%%) contains three visible boolean volumes:

| Volume | Operation | Components |
|--------|-----------|------------|
| %%plate_with_hole%% | subtraction | %%plate_box - plate_hole%% |
| %%cross%% | union | %%bar + bar_rotated%% |
| %%lens%% | intersection | %%sphere_one * sphere_two%% |

The component volumes use the special material %%Component%%. They define the operands of the
boolean expression but are not placed as visible detector volumes. The resulting boolean volumes
are placed like any other `GVolume`, with their own material, color, position, and rotation.

Interactive viewer:

{% assign boolean_solids_vtksz = "/assets/images/examples/boolean_solids/boolean_solids.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ boolean_solids_vtksz }}"
  title="Interactive VTK.js view of the boolean solids geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Boolean Expressions

A boolean solid is selected by assigning %%solidsOpr%%:

```python
plate.solidsOpr = 'plate_box - plate_hole'
cross.solidsOpr = 'bar + bar_rotated'
lens.solidsOpr = 'sphere_one * sphere_two'
```

The first operand is evaluated at its own origin. The second operand uses its own position and
rotation relative to the first operand. For example, %%plate_hole%% is shifted by 30 mm before it is
subtracted from %%plate_box%%, so the hole is off center.

<br/>

## Generator

The particle kinematics are defined in the YAML file:

```yaml
gparticle:
  - name: e-
    p: 500*MeV
    theta: 90*deg
    vx: -40*cm
    delta_vx: 12*cm
    randomVertexModel: uniform
```

See also the [Internal Generator Documentation]( /home/documentation/generator/internal ) for more information.

<br/>

## Usage

### Building the detector

Use the Python script `boolean_solids.py` to build the detector. By default, the setup is stored in
a SQLite file named `gemc.db`.

```shell
./boolean_solids.py
```

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `boolean_solids.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc boolean_solids.yaml -gui
```

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/boolean_solids/gemc_view.png"
caption="Boolean solids simulation: electrons crossing the subtraction, union, and intersection volumes."
%}
