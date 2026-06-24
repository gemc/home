---
layout: default
title: "Constant Field"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 exclude_title="Quickstart" %}

# Constant Field Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

*Upcoming in the next release.*

This field example displays a uniform longitudinal magnetic field using `gmultipoles`. It is a
minimal scene for checking field-line visualization without running events.

{% assign example = site.data.examples | where: "title", "Constant Field" | first %}

<br/>

## Quickstart

Copy the example to your current directory, build the geometry database, and open the field display:

```shell
cp -r $GEMC_HOME/examples/fields/constant .
cd constant
./constant.py
gemc constant.yaml -gui
```

<br/>

## Geometry

The geometry is defined in `constant.py`. The world volume %%root%% contains one transparent box,
%%constant_field_box%%, with its %%mfield%% property set to %%constant%%.

<br/>

## Field Definition

The YAML file defines a longitudinal uniform field through `gmultipoles`:

```yaml
gmultipoles:
  - name: constant
    pole_number: 2
    strength: 1
    rotaxis: z
    longitudinal: true
```

The display options request 30 field lines and auxiliary geometry edges:

```yaml
show_field_lines: 30
show_auxiliary_edges: true
```

<br/>

## Field Display

{% include figure.html
src="assets/images/examples/constant/gemc_view.png"
caption="Constant field display: a transparent box with uniform field lines."
%}

<br/>

## Usage

The file `constant.yaml` sets `n: 0`, so no `/run/beamOn` is needed for this display scene. Add
`-fieldAt` to inspect the configured field at a point:

```shell
gemc constant.yaml -fieldAt="0*cm 0*cm 0*cm"
```
