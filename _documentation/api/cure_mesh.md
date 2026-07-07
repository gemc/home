---
layout: default
title: Cure Mesh
category: api
---

# Cure Mesh

<span style="color:orange">Upcoming in the next release.</span>

`cure_mesh` is a pygemc utility that **simplifies and repairs CAD meshes** (STL, PLY, OBJ, ...) so that
Geant4's `G4TessellatedSolid` loads them quickly and without complaints.

Raw scanned or printed meshes are often heavy (hundreds of thousands of triangles) and are stored as an
unwelded triangle soup with inconsistent facet winding and small holes. When such a mesh is imported as a
CAD volume, Geant4 prints warnings while closing the solid:

```
Defects in solid:  - there are holes in the surface!
Defects in solid:  - some facets have wrong orientation!
Defects in solid:  - negative cubic volume, please check orientation of facets!
```

`cure_mesh` produces a lighter, watertight, coherently-oriented mesh that loads much faster and silences
those warnings.

## Dependencies

`cure_mesh` uses [pymeshlab](https://pymeshlab.readthedocs.io) (MeshLab's engine), which is a pygemc
dependency and is pre-installed in the GEMC Python environment (`python_env/`) created during
`meson install`. No separate installation is needed when using the `gemc-cure-mesh` command or the
`python3` interpreter from that environment.

## What it does

Each mesh is processed with a single pymeshlab pipeline:

1. **Weld** coincident vertices and drop duplicate / null faces — turns the STL soup into a connected mesh.
2. **Remove noise** — discard tiny disconnected components.
3. **Decimate** — quadric edge collapse down to a target facet count (this is what makes loading fast).
4. **Repair** — fix non-manifold edges and close holes so the surface is watertight.
5. **Re-orient** — make the facet winding coherent and flip the whole mesh outward when its signed volume
   is negative.

Decimation and repair do not change the bounding box appreciably, so any `scale` / `position` authored for
the mesh in a [CAD definition](/home/documentation/geometry/cad_imports) stays valid.

## Command line

```sh
gemc-cure-mesh input.stl -o output.stl -f 15000
```

| Option | Default | Meaning |
| --- | --- | --- |
| `input` (positional) | — | mesh to read (stl / ply / obj / ...) |
| `-o`, `--output` | overwrite input | output mesh (the format follows the extension) |
| `-f`, `--target-faces` | `20000` | target facet count for decimation (`0` skips decimation) |
| `--min-component-faces` | `100` | remove connected components smaller than this |
| `--merge-percent` | `0.1` | vertex-weld threshold, as a percent of the bounding-box diagonal |
| `--hole-iterations` | `4` | repair / close-holes passes |
| `--remove-self-intersections` | off | also delete self-intersecting facets (see Notes) |
| `--reconstruct poisson` | off | rebuild one watertight manifold before decimation (fragmented scans) |
| `--poisson-depth` | `9` | octree depth for `--reconstruct poisson` |

Process one mesh per invocation: pymeshlab's native engine is not reliable when several meshes are handled
back-to-back in the same interpreter.

## Python

```python
from pygemc.utilities import cure_mesh

stats = cure_mesh("heart.stl", "heart.stl", target_faces=15000)
# {'faces_in': 149992, 'faces_out': 14986, 'volume': 0.09,
#  'boundary_edges': 0, 'watertight': True}
```

`cure_mesh(input_path, output_path=None, target_faces=20000, merge_percent=0.1,
min_component_faces=100, hole_iterations=4, verbose=True)` returns a dictionary with the input and output
facet counts, the mesh volume, the number of remaining boundary edges, and whether the result is
watertight. `output_path=None` overwrites the input in place.

## Before and after: the heart

Curing the heart mesh from the [`cad` example](https://github.com/gemc/src/tree/main/examples/basic/cad)
with

```sh
gemc-cure-mesh heart_NIH3D.stl -o heart_NIH3D.stl -f 15000
```

| Property                  | Before             | After            |
| ------------------------- | ------------------ | ---------------- |
| Facets                    | 149,992            | 14,990           |
| File size                 | 7.5 MB             | 0.75 MB          |
| Boundary edges (holes)    | 12                 | 0                |
| Self-intersecting facets  | 5                  | 0                |
| Non-manifold vertices     | 5                  | 2                |
| Signed volume             | negative (open)    | positive         |

The cured mesh is about **10× lighter** (7.5 MB → 0.75 MB, 150k → 15k facets) and **20 of its 22
topological defects are repaired** (22 → 2): it is now watertight with no self-intersections and a positive
volume. Geant4 no longer reports holes, wrong-orientation, or negative-volume warnings for it, and it loads
roughly an order of magnitude faster.

## Notes

- The pipeline is opinionated: it always welds, repairs, and re-orients, not just decimates. Use
  `target_faces=0` for a repair-only pass and `min_component_faces=0` to keep every component.
- Adding `--remove-self-intersections` deletes self-intersecting facets and re-closes the openings; it
  clears the last defects on meshes that cure cleanly, but can fragment or crash pymeshlab on heavily
  broken scans, so it is off by default.
- Hole closing deliberately avoids the self-intersection mode that can crash the engine, so a genuinely
  open surface may keep a few small openings and still print a harmless "holes in the surface" warning.
  For a badly fragmented scan (many shells, large holes) use `--reconstruct poisson`, which rebuilds a
  single watertight manifold from the point-cloud normals before decimation.
