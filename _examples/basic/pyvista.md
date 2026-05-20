---
layout: default
title: "PyVista Geometry Visualization"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 %}


# PyVista Geometry Visualization
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

GEMC uses [PyVista](https://docs.pyvista.org/) to visualize detector geometry directly from Python.
Geometry can be viewed interactively, exported as a `.vtksz` file for web-based display, or rendered as a screenshot.

This example demonstrates the `GMesh` API for constructing visualization meshes: supported primitive shapes,
display styles, colors, opacity, and rotations.

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

{% assign example = site.data.examples | where: "title", "PyVista" | first %}

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

## The `GMesh` class

`GMesh` is the core object for building visualizable volumes. Import it from `pyvista_api`:

```python
from pyvista_api import GMesh, pvmeshes_from_gmeshes, set_yz_view_x_into_screen
```

Every `GMesh` requires a unique `name` and a PyVista `mesh`. All other parameters are optional:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | — | Unique volume identifier |
| `mesh` | `pv.PolyData` | — | PyVista mesh in local coordinates |
| `mother` | `str` | `None` | Parent volume name; `None` → placed directly in the world |
| `material` | `str` | `None` | Geant4 material name (e.g. `"G4_AIR"`) |
| `mfield` | `str` | `None` | Magnetic field name |
| `color` | `str` | `"white"` | Color name or hex string (see [Color Reference](#color-reference)) |
| `opacity` | `float` | `1.0` | Opacity from `0.0` (invisible) to `1.0` (fully opaque) |
| `position` | `(x, y, z)` | `(0,0,0)` | Local translation relative to mother, in mm |
| `rotation` | `(rx, ry, rz)` | `(0,0,0)` | Intrinsic ZYX Euler angles in degrees (see [Rotations](#rotations)) |

Example:

```python
import pyvista as pv
from pyvista_api import GMesh

sphere_mesh = pv.Sphere(radius=0.7, theta_resolution=32, phi_resolution=32)
sphere_gm = GMesh(
    name="sphere",
    mesh=sphere_mesh,
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
The mapping is determined by the mesh's geometry:

| PyVista Constructor | Detected As | Geant4 Solid | Notes |
|---------------------|-------------|--------------|-------|
| `pv.Cube(x_length, y_length, z_length)` | 8-point box | `G4Box` | Half-lengths used |
| `pv.Cylinder(radius, height, direction=(0,0,1))` | Round in XY, tall in Z | `G4Tubs` | Full 360° tube |
| `pv.Sphere(radius)` | Equal extents in all axes | `G4Sphere` | Full sphere |

Detection uses bounding-box heuristics; sphere detection takes priority over cylinder detection
since spheres also satisfy the "round in XY" cylinder criterion.

<br/>

## Display Styles

When using `GVolume` objects (via `from_gmesh` or directly), the display appearance is controlled
by three attributes:

| Attribute | Values | Effect |
|-----------|--------|--------|
| `gvolume.visible` | `1` (default) | Volume is rendered normally |
| | `0` | Volume is nearly invisible (opacity reduced to 0.05, wireframe outline only) — useful for container/world volumes |
| `gvolume.style` | `1` (default) | **Solid** surface rendering |
| | `0` | **Wireframe** — feature edges extracted at 30° threshold, clean outlines on all solids |
| | `2` | **Cloud** — semi-transparent surface with a scattered point cloud overlay |
| `gvolume.opacity` | `0.0` – `1.0` | Surface transparency; independent of `visible` |

### Style 1 — Solid (default)

All surfaces fully rendered, smooth shading on curved shapes.

```python
tube.style = 1   # default
tube.opacity = 1.0
```

### Style 0 — Wireframe

Renders only the characteristic edges of the shape, extracted using PyVista's `extract_feature_edges`
at a 30° dihedral threshold. Triangulated solids (cylinders, spheres) show clean outlines rather than
every triangle edge.

```python
tube.style = 0
```

### Style 2 — Cloud

A semi-transparent surface is shown with an additional point cloud sampled from the surface.
Useful for visualizing volumes where you want to see both the outline and the interior.

```python
tube.style = 2
```

### `visible = 0` — Container / Envelope

Setting `visible = 0` makes the volume nearly transparent (opacity 0.05, wireframe only),
which is the correct way to define container or world volumes that should not dominate the scene:

```python
world.visible = 0   # NOT world.style = 0
```

<br/>

## Rotations

`GMesh` uses **intrinsic ZYX Euler angles**: the three rotation angles `(rx, ry, rz)` apply
sequentially in the order X → Y → Z about the *local* frame axes.

The final rotation matrix is:

```
R = Rx(rx) · Ry(ry) · Rz(rz)
```

Parent-to-world transforms are accumulated recursively through the volume hierarchy.

Example — rotate 35° about Z:

```python
rotbox_gm = GMesh(
    name="rotated_box",
    mesh=pv.Cube(x_length=1.2, y_length=0.4, z_length=1.2),
    mother="box",
    rotation=(0.0, 0.0, 35.0),   # (rx, ry, rz) in degrees
    ...
)
```

<br/>

## Standalone PyVista Rendering

`pvmeshes_from_gmeshes` applies the full hierarchy transform (position + rotation relative to parent)
and returns `(mesh, color, opacity)` tuples ready for direct PyVista rendering, without needing a
Geant4 backend:

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
| `-pvvtk` | `<name>` | Export geometry to `<name>.vtksz` for web viewing (no window opened) |
| `-pvz` | `<zoom>` | Camera zoom factor for the exported VTK scene (e.g. `0.07`) |

Examples:

```shell
./gemc_pyvista.py -pv                     # interactive window
./gemc_pyvista.py -pvvtk pyvista -pvz 0.07  # export vtksz with zoom 0.07
```

To generate an offscreen screenshot using the Geant4 renderer:

```shell
./gemc_pyvista.py                        # build geometry (creates gemc.db)
gemc pyvista.yaml -n=10 \
  -g4view="[{driver: TOOLSSG_OFFSCREEN, segsPerCircle: 200}]" \
  -g4camera="[{phi: -10*deg, theta: 250*deg}]"
# output: gemc_run_0.png
```

<br/>

## Color Reference

Colors can be specified as CSS/HTML color names or as 6-digit hex strings (e.g. `"FF6347"` for tomato).
A metallic sheen can be added with the prefix `"metallic, <color>"`.

### Basics

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `black` | `000000` | <span style="display:inline-block;width:20px;height:14px;background:#000000;border:1px solid #ccc"></span> | `white` | `FFFFFF` | <span style="display:inline-block;width:20px;height:14px;background:#FFFFFF;border:1px solid #ccc"></span> | `red` | `FF0000` | <span style="display:inline-block;width:20px;height:14px;background:#FF0000;border:1px solid #ccc"></span> |
| `green` | `008000` | <span style="display:inline-block;width:20px;height:14px;background:#008000;border:1px solid #ccc"></span> | `blue` | `0000FF` | <span style="display:inline-block;width:20px;height:14px;background:#0000FF;border:1px solid #ccc"></span> | `yellow` | `FFFF00` | <span style="display:inline-block;width:20px;height:14px;background:#FFFF00;border:1px solid #ccc"></span> |
| `cyan` | `00FFFF` | <span style="display:inline-block;width:20px;height:14px;background:#00FFFF;border:1px solid #ccc"></span> | `magenta` | `FF00FF` | <span style="display:inline-block;width:20px;height:14px;background:#FF00FF;border:1px solid #ccc"></span> | `gray` | `808080` | <span style="display:inline-block;width:20px;height:14px;background:#808080;border:1px solid #ccc"></span> |
| `silver` | `C0C0C0` | <span style="display:inline-block;width:20px;height:14px;background:#C0C0C0;border:1px solid #ccc"></span> | `maroon` | `800000` | <span style="display:inline-block;width:20px;height:14px;background:#800000;border:1px solid #ccc"></span> | `olive` | `808000` | <span style="display:inline-block;width:20px;height:14px;background:#808000;border:1px solid #ccc"></span> |
| `navy` | `000080` | <span style="display:inline-block;width:20px;height:14px;background:#000080;border:1px solid #ccc"></span> | `teal` | `008080` | <span style="display:inline-block;width:20px;height:14px;background:#008080;border:1px solid #ccc"></span> | `purple` | `800080` | <span style="display:inline-block;width:20px;height:14px;background:#800080;border:1px solid #ccc"></span> |

### Grays

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `whitesmoke` | `F5F5F5` | <span style="display:inline-block;width:20px;height:14px;background:#F5F5F5;border:1px solid #ccc"></span> | `gainsboro` | `DCDCDC` | <span style="display:inline-block;width:20px;height:14px;background:#DCDCDC;border:1px solid #ccc"></span> | `lightgray` | `D3D3D3` | <span style="display:inline-block;width:20px;height:14px;background:#D3D3D3;border:1px solid #ccc"></span> |
| `darkgray` | `A9A9A9` | <span style="display:inline-block;width:20px;height:14px;background:#A9A9A9;border:1px solid #ccc"></span> | `slategray` | `708090` | <span style="display:inline-block;width:20px;height:14px;background:#708090;border:1px solid #ccc"></span> | `dimgray` | `696969` | <span style="display:inline-block;width:20px;height:14px;background:#696969;border:1px solid #ccc"></span> |
| `lightslategray` | `778899` | <span style="display:inline-block;width:20px;height:14px;background:#778899;border:1px solid #ccc"></span> | `darkslategray` | `2F4F4F` | <span style="display:inline-block;width:20px;height:14px;background:#2F4F4F;border:1px solid #ccc"></span> | | | |

### Blues

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `aliceblue` | `F0F8FF` | <span style="display:inline-block;width:20px;height:14px;background:#F0F8FF;border:1px solid #ccc"></span> | `ghostwhite` | `F8F8FF` | <span style="display:inline-block;width:20px;height:14px;background:#F8F8FF;border:1px solid #ccc"></span> | `lavender` | `E6E6FA` | <span style="display:inline-block;width:20px;height:14px;background:#E6E6FA;border:1px solid #ccc"></span> |
| `powderblue` | `B0E0E6` | <span style="display:inline-block;width:20px;height:14px;background:#B0E0E6;border:1px solid #ccc"></span> | `lightblue` | `ADD8E6` | <span style="display:inline-block;width:20px;height:14px;background:#ADD8E6;border:1px solid #ccc"></span> | `lightskyblue` | `87CEFA` | <span style="display:inline-block;width:20px;height:14px;background:#87CEFA;border:1px solid #ccc"></span> |
| `skyblue` | `87CEEB` | <span style="display:inline-block;width:20px;height:14px;background:#87CEEB;border:1px solid #ccc"></span> | `deepskyblue` | `00BFFF` | <span style="display:inline-block;width:20px;height:14px;background:#00BFFF;border:1px solid #ccc"></span> | `dodgerblue` | `1E90FF` | <span style="display:inline-block;width:20px;height:14px;background:#1E90FF;border:1px solid #ccc"></span> |
| `cornflowerblue` | `6495ED` | <span style="display:inline-block;width:20px;height:14px;background:#6495ED;border:1px solid #ccc"></span> | `steelblue` | `4682B4` | <span style="display:inline-block;width:20px;height:14px;background:#4682B4;border:1px solid #ccc"></span> | `lightsteelblue` | `B0C4DE` | <span style="display:inline-block;width:20px;height:14px;background:#B0C4DE;border:1px solid #ccc"></span> |
| `royalblue` | `4169E1` | <span style="display:inline-block;width:20px;height:14px;background:#4169E1;border:1px solid #ccc"></span> | `mediumblue` | `0000CD` | <span style="display:inline-block;width:20px;height:14px;background:#0000CD;border:1px solid #ccc"></span> | `darkblue` | `00008B` | <span style="display:inline-block;width:20px;height:14px;background:#00008B;border:1px solid #ccc"></span> |
| `midnightblue` | `191970` | <span style="display:inline-block;width:20px;height:14px;background:#191970;border:1px solid #ccc"></span> | `slateblue` | `6A5ACD` | <span style="display:inline-block;width:20px;height:14px;background:#6A5ACD;border:1px solid #ccc"></span> | `blueviolet` | `8A2BE2` | <span style="display:inline-block;width:20px;height:14px;background:#8A2BE2;border:1px solid #ccc"></span> |
| `indigo` | `4B0082` | <span style="display:inline-block;width:20px;height:14px;background:#4B0082;border:1px solid #ccc"></span> | | | | | | |

### Cyans & Teals

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `cadetblue` | `5F9EA0` | <span style="display:inline-block;width:20px;height:14px;background:#5F9EA0;border:1px solid #ccc"></span> | `lightseagreen` | `20B2AA` | <span style="display:inline-block;width:20px;height:14px;background:#20B2AA;border:1px solid #ccc"></span> | `turquoise` | `40E0D0` | <span style="display:inline-block;width:20px;height:14px;background:#40E0D0;border:1px solid #ccc"></span> |
| `mediumturquoise` | `48D1CC` | <span style="display:inline-block;width:20px;height:14px;background:#48D1CC;border:1px solid #ccc"></span> | `darkturquoise` | `00CED1` | <span style="display:inline-block;width:20px;height:14px;background:#00CED1;border:1px solid #ccc"></span> | `paleturquoise` | `AFEEEE` | <span style="display:inline-block;width:20px;height:14px;background:#AFEEEE;border:1px solid #ccc"></span> |
| `aquamarine` | `7FFFD4` | <span style="display:inline-block;width:20px;height:14px;background:#7FFFD4;border:1px solid #ccc"></span> | `mediumaquamarine` | `66CDAA` | <span style="display:inline-block;width:20px;height:14px;background:#66CDAA;border:1px solid #ccc"></span> | `darkcyan` | `008B8B` | <span style="display:inline-block;width:20px;height:14px;background:#008B8B;border:1px solid #ccc"></span> |

### Greens

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `honeydew` | `F0FFF0` | <span style="display:inline-block;width:20px;height:14px;background:#F0FFF0;border:1px solid #ccc"></span> | `palegreen` | `98FB98` | <span style="display:inline-block;width:20px;height:14px;background:#98FB98;border:1px solid #ccc"></span> | `lightgreen` | `90EE90` | <span style="display:inline-block;width:20px;height:14px;background:#90EE90;border:1px solid #ccc"></span> |
| `springgreen` | `00FF7F` | <span style="display:inline-block;width:20px;height:14px;background:#00FF7F;border:1px solid #ccc"></span> | `lime` | `00FF00` | <span style="display:inline-block;width:20px;height:14px;background:#00FF00;border:1px solid #ccc"></span> | `limegreen` | `32CD32` | <span style="display:inline-block;width:20px;height:14px;background:#32CD32;border:1px solid #ccc"></span> |
| `lawngreen` | `7CFC00` | <span style="display:inline-block;width:20px;height:14px;background:#7CFC00;border:1px solid #ccc"></span> | `chartreuse` | `7FFF00` | <span style="display:inline-block;width:20px;height:14px;background:#7FFF00;border:1px solid #ccc"></span> | `greenyellow` | `ADFF2F` | <span style="display:inline-block;width:20px;height:14px;background:#ADFF2F;border:1px solid #ccc"></span> |
| `yellowgreen` | `9ACD32` | <span style="display:inline-block;width:20px;height:14px;background:#9ACD32;border:1px solid #ccc"></span> | `darkseagreen` | `8FBC8F` | <span style="display:inline-block;width:20px;height:14px;background:#8FBC8F;border:1px solid #ccc"></span> | `seagreen` | `2E8B57` | <span style="display:inline-block;width:20px;height:14px;background:#2E8B57;border:1px solid #ccc"></span> |
| `forestgreen` | `228B22` | <span style="display:inline-block;width:20px;height:14px;background:#228B22;border:1px solid #ccc"></span> | `mediumseagreen` | `3CB371` | <span style="display:inline-block;width:20px;height:14px;background:#3CB371;border:1px solid #ccc"></span> | `darkgreen` | `006400` | <span style="display:inline-block;width:20px;height:14px;background:#006400;border:1px solid #ccc"></span> |
| `olivedrab` | `6B8E23` | <span style="display:inline-block;width:20px;height:14px;background:#6B8E23;border:1px solid #ccc"></span> | `darkolivegreen` | `556B2F` | <span style="display:inline-block;width:20px;height:14px;background:#556B2F;border:1px solid #ccc"></span> | | | |

### Yellows & Oranges

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `lightyellow` | `FFFFE0` | <span style="display:inline-block;width:20px;height:14px;background:#FFFFE0;border:1px solid #ccc"></span> | `lemonchiffon` | `FFFACD` | <span style="display:inline-block;width:20px;height:14px;background:#FFFACD;border:1px solid #ccc"></span> | `ivory` | `FFFFF0` | <span style="display:inline-block;width:20px;height:14px;background:#FFFFF0;border:1px solid #ccc"></span> |
| `beige` | `F5F5DC` | <span style="display:inline-block;width:20px;height:14px;background:#F5F5DC;border:1px solid #ccc"></span> | `wheat` | `F5DEB3` | <span style="display:inline-block;width:20px;height:14px;background:#F5DEB3;border:1px solid #ccc"></span> | `tan` | `D2B48C` | <span style="display:inline-block;width:20px;height:14px;background:#D2B48C;border:1px solid #ccc"></span> |
| `khaki` | `F0E68C` | <span style="display:inline-block;width:20px;height:14px;background:#F0E68C;border:1px solid #ccc"></span> | `gold` | `FFD700` | <span style="display:inline-block;width:20px;height:14px;background:#FFD700;border:1px solid #ccc"></span> | `goldenrod` | `DAA520` | <span style="display:inline-block;width:20px;height:14px;background:#DAA520;border:1px solid #ccc"></span> |
| `darkgoldenrod` | `B8860B` | <span style="display:inline-block;width:20px;height:14px;background:#B8860B;border:1px solid #ccc"></span> | `orange` | `FFA500` | <span style="display:inline-block;width:20px;height:14px;background:#FFA500;border:1px solid #ccc"></span> | `darkorange` | `FF8C00` | <span style="display:inline-block;width:20px;height:14px;background:#FF8C00;border:1px solid #ccc"></span> |

### Browns

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `burlywood` | `DEB887` | <span style="display:inline-block;width:20px;height:14px;background:#DEB887;border:1px solid #ccc"></span> | `peru` | `CD853F` | <span style="display:inline-block;width:20px;height:14px;background:#CD853F;border:1px solid #ccc"></span> | `chocolate` | `D2691E` | <span style="display:inline-block;width:20px;height:14px;background:#D2691E;border:1px solid #ccc"></span> |
| `sienna` | `A0522D` | <span style="display:inline-block;width:20px;height:14px;background:#A0522D;border:1px solid #ccc"></span> | `saddlebrown` | `8B4513` | <span style="display:inline-block;width:20px;height:14px;background:#8B4513;border:1px solid #ccc"></span> | `rosybrown` | `BC8F8F` | <span style="display:inline-block;width:20px;height:14px;background:#BC8F8F;border:1px solid #ccc"></span> |
| `brown` | `A52A2A` | <span style="display:inline-block;width:20px;height:14px;background:#A52A2A;border:1px solid #ccc"></span> | | | | | | |

### Reds & Corals

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `mistyrose` | `FFE4E1` | <span style="display:inline-block;width:20px;height:14px;background:#FFE4E1;border:1px solid #ccc"></span> | `peachpuff` | `FFDAB9` | <span style="display:inline-block;width:20px;height:14px;background:#FFDAB9;border:1px solid #ccc"></span> | `lightcoral` | `F08080` | <span style="display:inline-block;width:20px;height:14px;background:#F08080;border:1px solid #ccc"></span> |
| `salmon` | `FA8072` | <span style="display:inline-block;width:20px;height:14px;background:#FA8072;border:1px solid #ccc"></span> | `darksalmon` | `E9967A` | <span style="display:inline-block;width:20px;height:14px;background:#E9967A;border:1px solid #ccc"></span> | `lightsalmon` | `FFA07A` | <span style="display:inline-block;width:20px;height:14px;background:#FFA07A;border:1px solid #ccc"></span> |
| `coral` | `FF7F50` | <span style="display:inline-block;width:20px;height:14px;background:#FF7F50;border:1px solid #ccc"></span> | `tomato` | `FF6347` | <span style="display:inline-block;width:20px;height:14px;background:#FF6347;border:1px solid #ccc"></span> | `orangered` | `FF4500` | <span style="display:inline-block;width:20px;height:14px;background:#FF4500;border:1px solid #ccc"></span> |
| `firebrick` | `B22222` | <span style="display:inline-block;width:20px;height:14px;background:#B22222;border:1px solid #ccc"></span> | `darkred` | `8B0000` | <span style="display:inline-block;width:20px;height:14px;background:#8B0000;border:1px solid #ccc"></span> | `crimson` | `DC143C` | <span style="display:inline-block;width:20px;height:14px;background:#DC143C;border:1px solid #ccc"></span> |

### Pinks & Purples

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `pink` | `FFC0CB` | <span style="display:inline-block;width:20px;height:14px;background:#FFC0CB;border:1px solid #ccc"></span> | `lightpink` | `FFB6C1` | <span style="display:inline-block;width:20px;height:14px;background:#FFB6C1;border:1px solid #ccc"></span> | `hotpink` | `FF69B4` | <span style="display:inline-block;width:20px;height:14px;background:#FF69B4;border:1px solid #ccc"></span> |
| `deeppink` | `FF1493` | <span style="display:inline-block;width:20px;height:14px;background:#FF1493;border:1px solid #ccc"></span> | `palevioletred` | `DB7093` | <span style="display:inline-block;width:20px;height:14px;background:#DB7093;border:1px solid #ccc"></span> | `orchid` | `DA70D6` | <span style="display:inline-block;width:20px;height:14px;background:#DA70D6;border:1px solid #ccc"></span> |
| `mediumorchid` | `BA55D3` | <span style="display:inline-block;width:20px;height:14px;background:#BA55D3;border:1px solid #ccc"></span> | `darkorchid` | `9932CC` | <span style="display:inline-block;width:20px;height:14px;background:#9932CC;border:1px solid #ccc"></span> | `thistle` | `D8BFD8` | <span style="display:inline-block;width:20px;height:14px;background:#D8BFD8;border:1px solid #ccc"></span> |
| `plum` | `DDA0DD` | <span style="display:inline-block;width:20px;height:14px;background:#DDA0DD;border:1px solid #ccc"></span> | `violet` | `EE82EE` | <span style="display:inline-block;width:20px;height:14px;background:#EE82EE;border:1px solid #ccc"></span> | `mediumpurple` | `9370DB` | <span style="display:inline-block;width:20px;height:14px;background:#9370DB;border:1px solid #ccc"></span> |
| `rebeccapurple` | `663399` | <span style="display:inline-block;width:20px;height:14px;background:#663399;border:1px solid #ccc"></span> | `darkviolet` | `9400D3` | <span style="display:inline-block;width:20px;height:14px;background:#9400D3;border:1px solid #ccc"></span> | `mediumvioletred` | `C71585` | <span style="display:inline-block;width:20px;height:14px;background:#C71585;border:1px solid #ccc"></span> |

### Hex Color Format

Six-digit hex strings are also accepted directly (without the `#` prefix):

```python
gvolume.color = "4682B4"   # same as "steelblue"
gvolume.color = "FF6347"   # same as "tomato"
```

<br/>

## Publishing to Geant4

To use a `GMesh` in a full GEMC simulation, convert it to a `GVolume` and publish it:

```python
from gconfiguration import autogeometry
from gvolume import GVolume
from pyvista_basic_shapes import make_basic_shapes

cfg = autogeometry("examples", "pyvista")

for gm in make_basic_shapes():
    gv = GVolume.from_gmesh(gm)
    gv.publish(cfg)
```

`GVolume.from_gmesh` automatically:
- Detects the Geant4 solid type from the mesh bounding geometry
- Sets `mother = "root"` if `gm.mother` is `None`
- Transfers `color`, `opacity`, `position`, and `rotation` from the `GMesh`
- Sets `visible = 0` if `opacity <= 0.01`

{% include notes/python-api-note.md %}
