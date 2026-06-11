---
layout: default
title: Geometry Structure Helpers
order: 35
description: Helper methods for building structured detector geometries — arrays, rings, and repetitive layouts
---

This page documents `GVolume` helper methods that place multiple copies of a volume in
structured patterns. These methods handle position, rotation, and naming automatically,
so that building arrays and rings requires only a few lines of Python.

<br/>

---

## `distribute_on_circle`

```python
copies = gvolume.distribute_on_circle(
    n, radius,
    phistart=0, phispan=360,
    align=False, axis='z',
    lunit='mm', aunit='deg'
)
```

Replicates `gvolume` at `n` equal angular steps along a circle of the given `radius`.
Returns a `list[GVolume]`, one copy per step, each named `<name>_i`.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n` | int | — | Number of copies |
| `radius` | float | — | Circle radius in `lunit` |
| `phistart` | float | `0` | Starting angle in `aunit` |
| `phispan` | float | `360` | Angular span in `aunit` (step = `phispan / n`) |
| `align` | bool | `False` | If `True`, rotate each copy around `axis` by its φᵢ angle so the volume stays radially aligned |
| `axis` | str | `'z'` | Symmetry axis: `'x'`, `'y'`, or `'z'` |
| `lunit` | str | `'mm'` | Length unit for `radius` |
| `aunit` | str | `'deg'` | Angle unit for `phistart`, `phispan`, and alignment rotations |

### Positions

Each copy `i` is placed at φᵢ = `phistart + i × phispan / n`:

| `axis` | position |
|--------|----------|
| `'z'`  | `(radius·cos φᵢ,  radius·sin φᵢ,  0)` |
| `'x'`  | `(0,  radius·cos φᵢ,  radius·sin φᵢ)` |
| `'y'`  | `(radius·cos φᵢ,  0,  radius·sin φᵢ)` |

### Alignment rotation

With `align=True` the template's existing rotation is preserved as the first half of a
`doubleRotation:` entry, and the angular step φᵢ is appended as the second half.
This is stored in GEMC's `doubleRotation: rx1, ry1, rz1, rx2, ry2, rz2` format so that
Geant4 and PyVista both apply the rotations in the correct order.

For `axis='z'` and a template rotation of `(0, 0, -90)°`:

```
doubleRotation: 0*deg, 0*deg, -90*deg, 0*deg, 0*deg, φᵢ*deg
```

Geant4 applies this as Rz(−90°) then Rz(φᵢ), giving a combined rotation of Rz(φᵢ − 90°),
which maps the template's wide face radially outward at angle φᵢ.

### Example — scintillator barrel

The [scintillator barrel example](/home/examples/basic/scintillator_barrel) uses
`distribute_on_circle` to tile 48 trapezoidal paddles into a closed barrel ring:

```python
import math
from pygemc import autogeometry, GVolume

cfg = autogeometry("examples", "scintillator_barrel")

n      = 48
radius = 400.0   # mm
pZ     = 500.0   # mm — half-length along beam axis
pY     =  20.0   # mm — radial half-thickness

# Chord formula: adjacent outer faces meet exactly
half_step = math.radians(180.0 / n)
pX    = (radius + pY) * math.sin(half_step)   # outer half-width
pLTX  = (radius - pY) * math.sin(half_step)   # inner half-width

paddle = GVolume("paddle")
paddle.mother = "root"
paddle.make_general_trapezoid(pZ, 0, 0, pY, pLTX, pX, 0, pY, pLTX, pX, 0)
paddle.material = "G4_PLASTIC_SC_VINYLTOLUENE"
paddle.color = "cornflowerblue"
paddle.set_rotation(0, 0, -90)   # wide face (local +Y) → radially outward
paddle.digitization = "flux"

for i, v in enumerate(paddle.distribute_on_circle(n, radius, align=True, axis='z')):
    v.set_identifier("paddle", i)
    v.publish(cfg)
```

The chord formula ensures that, for any `n`, the outer faces of adjacent paddles are
contiguous: `pX = (radius + pY) · sin(π/n)` and `pLTX = (radius − pY) · sin(π/n)`.

{% include figure.html
src="assets/images/examples/scintillator_barrel/geometry.png"
caption="Scintillator barrel geometry with n=10 paddles (rendered by PyVista):
cornflowerblue G4Trap paddles tiling the barrel ring, wider face outward."
%}

Interactive viewer (full 48-paddle barrel):

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/scintillator_barrel/scintillator_barrel.vtksz"
  title="Interactive VTK.js view of the scintillator_barrel geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

---

## More structure helpers

Additional placement helpers will be documented here as they are added to `GVolume`.
