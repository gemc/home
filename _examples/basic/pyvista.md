---
layout: default
title: "PyVista Geometry Visualization"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 exclude_title="Quickstart" %}


# PyVista Geometry Visualization
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

GEMC uses [PyVista](https://docs.pyvista.org/) to visualize detector geometry directly from Python.
Geometry can be viewed interactively, exported as a `.vtksz` file for web-based display, or rendered
as a screenshot. See the [PyVista API documentation](/home/documentation/api/pyvista_api)
for the full API reference.

<br/>

## Quickstart

Copy the example to your current directory:

```shell
cp -r $GEMC_HOME/examples/basic/pyvista .
cd pyvista
./gemc_pyvista.py
```

To preview the geometry interactively (opens a PyVista window):

```shell
./gemc_pyvista.py -pv
```

<br/>

## Geometry

The example defines four volumes in `pyvista_basic_shapes.py`: a transparent container box,
a solid cylinder, a sphere, and a small rotated box inside the container.

Interactive viewer:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/pyvista/pyvista.vtksz"
  title="Interactive VTK.js view of the pyvista geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

{% include figure.html
src="assets/images/examples/pyvista/geometry.png"
caption="PyVista example geometry (rendered by gemc). Box container (ghostwhite, semi-transparent), cylinder (steelblue), sphere (tomato), rotated box (gold, 35° around Z)."
%}

<br/>

## Usage

### Building the geometry

```shell
./gemc_pyvista.py
```

{% include notes/python-api-note.md %}

<br/>

### Running gemc

```shell
gemc pyvista.yaml -n=10
```

Add `-gui` to run interactively.
