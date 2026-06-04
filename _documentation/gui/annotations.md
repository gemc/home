---
layout: default
title: "Annotations"
category: "Gui"
permalink: /documentation/gui/annotations/
---

# Annotations

Annotations add labels and scene decorations to GEMC visualizations without changing the detector geometry.
They are useful for screenshots, tutorials, and presentations where volumes need visible names, scale bars, axes,
or frame decorations.

Annotations are regular YAML options. Keep them in a separate file, usually `annotations.yaml`, when you want the
same example to run either with a clean scene or with labels:

```shell
gemc detector.yaml
gemc detector.yaml annotations.yaml
```

GEMC reads YAML files in command-line order. Later files override options with the same name, so the main YAML should
not also define `g4text` or `g4decoration` when those options live in `annotations.yaml`.

<br/>

## Text Labels

Use `g4text` for 2D screen text or 3D text placed in the scene.

```yaml
g4text:
  - kind: 2D
    text: exampleB1
    color: green
    layout: right
    x: 0.9
    y: -0.9
    size: 24
  - kind: 3D
    text: Shape1
    color: red
    x: 0
    y: 6
    z: -4
    unit: cm
    size: 30
    dx: 4
    dy: 4
```

For 3D labels, `x`, `y`, `z`, and `unit` place the label in geometry coordinates. The `dx` and `dy` values control
the text offset used by Geant4's 3D text command. Offscreen screenshots can render text smaller than the interactive
viewer, so use a larger `size` when preparing documentation images.

<br/>

## Scene Decorations

Use `g4decoration` for scale bars, axes, frame outlines, date stamps, and Geant4 logos.

```yaml
g4decoration:
  scale: true
  scaleLength: 10
  scaleUnit: mm
  scaleDirection: z
  scaleColor: "0.9 0.9 0.9"
  axes: true
  frame: true
  frameColor: red
  frameLineWidth: 2
```

Only enable the decorations that help the image. For dense geometry figures, labels and a scale bar are often clearer
than axes, logos, or frames.

<br/>

## Examples

The `b1` and `materials` examples keep labels and decorations in separate annotation files:

```shell
gemc b1.yaml annotations.yaml
gemc materials.yaml annotations.yaml
```

Run the main YAML by itself to render the same geometry without annotations.

See also:

- [`g4text`](/home/documentation/api/options/g4text)
- [`g4decoration`](/home/documentation/api/options/g4decoration)
