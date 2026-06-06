---
layout: default
title: GVolume Properties
order: 10
description: Complete reference for the GVolume class — properties, rotations, and placement conventions
---

`GVolume` is the Python class that defines a Geant4 physical volume in GEMC. Every volume in a detector
system is an instance of `GVolume`, published to the active database factory via `gvolume.publish(cfg)`.

```python
from gvolume import GVolume

gvolume = GVolume("my_box")
gvolume.make_box(30, 20, 10)           # 30 × 20 × 10 mm half-lengths
gvolume.material = "G4_Al"
gvolume.mother   = "world"
gvolume.publish(cfg)
```

<br/>

---

## Mandatory properties

These three must be set before calling `publish()`, or GEMC will exit with an error.

| Property | Type | Description |
|----------|------|-------------|
| `solid` | str | Geant4 solid name, e.g. `"G4Box"`, `"G4Tubs"`, `"G4Trap"` |
| `parameters` | str | Comma-separated dimensions with units, matching the solid's constructor order |
| `material` | str | Geant4 NIST name (`"G4_Al"`) or a custom `GMaterial` name |

Solids and their parameter strings are described in the [solid types reference](solidTypes).

<br/>

---

## Placement

### `mother`

Name of the parent volume. Defaults to `"root"` (the world volume).

```python
gvolume.mother = "sector_envelope"
```

### `position`

Location of this volume's centre relative to its mother, in mm. Use `set_position()` to set it
with explicit units:

```python
gvolume.set_position(0, 0, 150)              # mm (default)
gvolume.set_position(0, 0, 15, lunit='cm')   # explicit unit
```

The default is `"0*mm, 0*mm, 0*mm"`.

### `rotations` / `set_rotation()` / `add_rotation()`

The orientation of the volume relative to its mother frame. Three methods are available:

**`set_rotation(x, y, z, lunit='deg', order='')`** — defines a single rotation applied to the
x, y, z axes in that order (or in the order given by `order`):

```python
gvolume.set_rotation(10, 45, 30)             # 10° around x, then 45° y, then 30° z
gvolume.set_rotation(30, 45, 10, order='zyx')  # 30° around z first, then y, then x
```

**`add_rotation(x, y, z, lunit='deg')`** — appends a further xyz rotation on top of whatever
has already been set. Cumulative calls stack left-to-right:

```python
gvolume.add_rotation(0, 0, 40)   # first: 40° around z
gvolume.add_rotation(10, 0, 0)   # then:  10° around x
```

Ordered rotations are stored as `"ordered: zxy, 90*deg, 25*deg, 0*deg"` in the database, so the
axis order is preserved for Geant4 and for pyvista rendering.

<br/>

---

## Placement type and rotation convention

`g4placement_type` controls which Geant4 constructor places the volume, and therefore how the
rotation matrix **R** relates local-frame points to world-frame points.

```python
gvolume.g4placement_type = "active"    # default
gvolume.g4placement_type = "passive"   # GEMC2 / clas12Tags compatibility
```

### Active — `G4Transform3D(R, T)`

Geant4 stores `frot = R⁻¹ = Rᵀ` internally. Navigation inverts the stored matrix, so the
forward transformation from local to world coordinates is:

```
p_world = R_raw × p_local + T
```

This is the default and matches the behaviour of new GEMC3 geometries written in Python.

### Passive — `G4PVPlacement(&rot, T)`

Geant4 stores `frot = R` directly (no inversion). Navigation applies `frot` to map from world
to local, so the forward transformation is:

```
p_world = R_rawᵀ × p_local + T
```

Use `"passive"` when porting geometries from GEMC2 or clas12Tags, where the
`G4PVPlacement(rotation, translation, ...)` constructor was used. The rotation matrix **R** in
those systems is the *frame* rotation (a passive rotation of the coordinate axes), so transposing
it gives the correct active transformation needed to move points into the world frame.

**Example — DC region 1, sector 1:**

```python
gvolume.set_rotation(90, 25, 0, order='zxy')  # ordered: zxy, 90*deg, 25*deg, 0*deg
gvolume.g4placement_type = "passive"
```

`R_raw = Rx(25°) @ Rz(90°)`.  
With passive placement: `R_rawᵀ @ (0, 0, 1) ≈ (0.42, 0, 0.91)` — the local z-axis points
radially outward at 25° polar tilt, which is the correct orientation for the drift chamber wedge.

<br/>

---

## Display properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `visible` | int | `1` | `1` = visible, `0` = invisible (rendered as faint wireframe in pyvista) |
| `style` | int | `1` | `1` = solid surface, `0` = wireframe, `2` = point cloud |
| `color` | str | `"778899"` | Six-digit hex RGB string, e.g. `"ff0000"` for red. An optional 7th digit (0–5) sets transparency: `0` = opaque, `5` = fully transparent |
| `opacity` | float | `1` | Opacity override for pyvista rendering (0.0–1.0) |

```python
gvolume.color   = "0000ff4"   # mostly transparent blue
gvolume.visible = 1
gvolume.style   = 0           # wireframe
```

<br/>

---

## Sensitivity

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `digitization` | str | `None` | Name of the digitization plugin. Built-in choices: `"flux"`, `"particle_counter"`, `"integral_counter"`, `"dosimeter"`. Custom plugins use a `.gplugin` filename |
| `identifier` | str | `None` | Set with `set_identifier(*pairs)` — unique key/value pairs that tag every hit in this volume |

```python
gvolume.digitization = "flux"
gvolume.set_identifier("sector", 1, "layer", 3, "wire", 42)
```

<br/>

---

## Fields and existence

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `mfield` | str | `None` | Name of a magnetic field file attached to this volume |
| `exist` | int | `1` | `1` = volume is built, `0` = volume is skipped (can be toggled via jcard modifiers) |
| `description` | str | `None` | Free-text description stored in the database |

<br/>

---

## Not yet implemented

| Property | Description |
|----------|-------------|
| `copyOf` | Intended to copy an existing volume |
| `solidsOpr` | Intended for boolean solid operations |
| `mirror` | Intended to define a G4OpticalSurface |
