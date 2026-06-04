---
layout: default
title: "PyVista API"
---

# PyVista API
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

GEMC uses [PyVista](https://docs.pyvista.org/) to visualize detector geometry directly from Python.
Geometry can be viewed interactively, exported as a `.vtksz` file for web-based display, or rendered as a screenshot.

Import the API from `pyvista_api`:

```python
from pyvista_api import GMesh, pvmeshes_from_gmeshes, set_yz_view_x_into_screen
```

<br/>

## The `GMesh` Class

`GMesh` is the core object for building visualizable volumes. Every instance requires a unique `name`
and a PyVista `mesh`. All other parameters are optional:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | — | Unique volume identifier |
| `mesh` | `pv.PolyData` | — | PyVista mesh in local coordinates |
| `mother` | `str` | `None` | Parent volume name; `None` → placed directly in the world |
| `material` | `str` | `None` | Geant4 material name (e.g. `"G4_AIR"`) |
| `mfield` | `str` | `None` | Magnetic field name |
| `color` | `str` | `"white"` | Color name or hex string (see [Color Reference](/home/documentation/api/pyvista_colors)) |
| `opacity` | `float` | `1.0` | Opacity from `0.0` (invisible) to `1.0` (fully opaque) |
| `position` | `(x, y, z)` | `(0,0,0)` | Local translation relative to mother, in mm |
| `rotation` | `(rx, ry, rz)` | `(0,0,0)` | Intrinsic ZYX Euler angles in degrees |

Example:

```python
import pyvista as pv
from pyvista_api import GMesh

sphere_gm = GMesh(
    name="sphere",
    mesh=pv.Sphere(radius=0.7, theta_resolution=32, phi_resolution=32),
    mother="box",
    material="G4_Pb",
    color="tomato",
    opacity=0.85,
    position=(0.0, 0.0, 1.2),
    rotation=(0.0, 0.0, 0.0),
)
```

<br/>

## Supported Primitive Shapes

`GMesh` meshes are automatically converted to Geant4 solids when published via `GVolume.from_gmesh()`.
The mapping is determined by the mesh bounding geometry:

| PyVista Constructor | Detected As | Geant4 Solid | Notes |
|---------------------|-------------|--------------|-------|
| `pv.Cube(x_length, y_length, z_length)` | 8-point box | `G4Box` | Half-lengths used |
| `pv.Cylinder(radius, height, direction=(0,0,1))` | Round in XY, tall in Z | `G4Tubs` | Full 360° tube |
| `pv.Sphere(radius)` | Equal extents in all axes | `G4Sphere` | Full sphere |

Sphere detection takes priority over cylinder since both share "round in XY" bounding-box geometry.

<br/>

## Display Styles

The display appearance of a `GVolume` (created via `from_gmesh` or directly) is controlled by three attributes:

| Attribute | Value | Effect |
|-----------|-------|--------|
| `gvolume.visible` | `1` (default) | Volume is rendered normally |
| | `0` | Nearly invisible (opacity 0.05, wireframe only) — for container or world volumes |
| `gvolume.style` | `1` (default) | **Solid** surface rendering with smooth shading |
| | `0` | **Wireframe** — feature edges at 30° threshold; clean outlines on all solids including cylinders |
| | `2` | **Cloud** — semi-transparent surface with a sampled point cloud overlay |
| `gvolume.opacity` | `0.0` – `1.0` | Surface transparency; independent of `visible` |

### Style 1 — Solid (default)

```python
volume.style = 1
volume.opacity = 1.0
```

### Style 0 — Wireframe

Renders only the characteristic edges of the shape, extracted using `extract_feature_edges` at a 30°
dihedral threshold. Triangulated shapes (cylinders, spheres) show clean geometric outlines rather than
every triangle edge.

```python
volume.style = 0
```

### Style 2 — Cloud

A semi-transparent surface is shown together with an 8000-point cloud sampled from the surface.

```python
volume.style = 2
```

### `visible = 0` — Container / Envelope

Setting `visible = 0` makes the volume nearly transparent (opacity 0.05, wireframe only).
Use this for container or world volumes that should not dominate the scene:

```python
world.visible = 0   # NOT world.style = 0
```

<br/>

## Rotations

`GMesh` uses **intrinsic ZYX Euler angles**: the angles `(rx, ry, rz)` are applied sequentially
in the order X → Y → Z about the *local* frame axes, giving the rotation matrix:

```
R = Rx(rx) · Ry(ry) · Rz(rz)
```

Parent-to-world transforms are accumulated recursively through the volume hierarchy, so a child volume's
world position is `T_parent + R_parent × T_local`.

Example — 35° rotation about Z:

```python
GMesh(
    name="rotated_box",
    mesh=pv.Cube(x_length=1.2, y_length=0.4, z_length=1.2),
    mother="box",
    rotation=(0.0, 0.0, 35.0),   # (rx, ry, rz) in degrees
)
```

<br/>

## Standalone PyVista Rendering

`pvmeshes_from_gmeshes` resolves the full parent-child hierarchy (position + rotation) and returns
`(mesh, color, opacity)` tuples ready for direct PyVista rendering, without a Geant4 backend:

```python
import pyvista as pv
from pyvista_api import GMesh, pvmeshes_from_gmeshes, set_yz_view_x_into_screen

gmeshes = make_basic_shapes()
pvmeshes = pvmeshes_from_gmeshes(gmeshes)

p = pv.Plotter()
for mesh, color, opacity in pvmeshes:
    p.add_mesh(mesh, color=color, opacity=opacity, show_edges=True)

p.add_axes_at_origin(xlabel="X", ylabel="Y", zlabel="Z")
set_yz_view_x_into_screen(p, distance=10.0)
p.show()
```

`set_yz_view_x_into_screen(p, distance)` positions the camera so that +Z points right on screen
and +X points into the screen.

<br/>

## CLI Flags

These flags are accepted by any Python geometry script that uses `autogeometry`:

| Flag | Argument | Description |
|------|----------|-------------|
| `-pv` | — | Open an interactive PyVista window after building geometry |
| `-pvb` | — | Open a background (non-blocking) PyVista window |
| `-pvbg` | `<color>` | Set the PyVista background color as a name, hex color, or `r g b` triple |
| `-pvbgt` | `<color>` | Set the optional top color for a PyVista background gradient; use `none` for a flat background |
| `-pvvtk` | `<name>` | Export geometry to `<name>.vtksz` for web viewing |
| `-pvz` | `<zoom>` | Camera zoom factor for the exported VTK scene (e.g. `0.07`) |

```shell
./detector.py -pv                        # interactive window
./detector.py -pvvtk detector -pvz 0.02  # export vtksz
./detector.py -pvvtk detector -pvbg "0.92 0.92 0.98" -pvbgt none
```

To generate an offscreen screenshot via the Geant4 renderer:

```shell
./detector.py                   # build geometry (creates gemc.db)
gemc detector.yaml -n=10 \
  -g4view="[{driver: TOOLSSG_OFFSCREEN, segsPerCircle: 200}]" \
  -g4camera="[{phi: -10*deg, theta: 250*deg}]"
# output: gemc_run_0.png
```

<br/>

## Publishing to Geant4

To use a `GMesh` in a full GEMC simulation, convert it to a `GVolume` and publish it:

```python
from gconfiguration import autogeometry
from gvolume import GVolume

cfg = autogeometry("myexperiment", "mydetector")

for gm in make_shapes():
    gv = GVolume.from_gmesh(gm)
    gv.publish(cfg)
```

`GVolume.from_gmesh` automatically:
- Detects the Geant4 solid type from the mesh bounding geometry
- Sets `mother = "root"` if `gm.mother` is `None`
- Transfers `color`, `opacity`, `position`, and `rotation` from the `GMesh`
- Sets `visible = 0` if `opacity <= 0.01`

{% include notes/python-api-note.md %}
