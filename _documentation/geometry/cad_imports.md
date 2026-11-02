---
layout: default
title: CAD Import
description: Convert engineering CAD to meshes, optimize and validate them, and publish GEMC volumes
---

# Import CAD geometry

GEMC builds CAD volumes as Geant4 tessellated solids from STL or PLY meshes. A mesh supplies the surface;
a placement record supplies its material, mother volume, position, rotation, and optional sensitivity.
A STEP assembly must first be tessellated into meshes. GEMC does not import STEP directly.

**Upcoming with the next release:** `pygemc.build_cad` publishes GXML, YAML, JSON, or calculated
placement records through an existing geometry configuration. The examples below identify where this
new helper is used. The `gemc-sqlite -cad` uploader remains available for YAML and JSON definitions.

[build_cad API](#build-cad) · [STEP conversion](#convert-step-to-stl) ·
[Mesh optimization](#prepare-and-optimize-the-stl) ·
[First import](#create-your-first-cad-system)

## build_cad API {#build-cad}

**Upcoming with the next release.** Import the shared publisher from `pygemc`:

```python
from pygemc import build_cad

volumes = build_cad(
    configuration,
    source,
    cad_dir=None,
    defaults=None,
    material_aliases=None,
    passive=False,
    warn_missing_meshes=False,
)
```

%%configuration%% is the existing `GConfiguration` to publish into. %%source%% accepts a GXML, YAML,
or JSON path, a document dictionary containing %%volumes%%, or an iterable of placement dictionaries.
Use file paths for authored placements and dictionaries for positions calculated by detector code.

| Argument | Default | Purpose |
| --- | --- | --- |
| %%cad_dir%% | %%None%% | Override the document's runtime mesh directory; otherwise use %%cad%%. |
| %%defaults%% | %%None%% | Supply shared volume properties, such as material and rotation. |
| %%material_aliases%% | %%None%% | Map source material names to runtime material names. |
| %%passive%% | %%False%% | Force GEMC2 frame rotations for every source and copy when true. |
| %%warn_missing_meshes%% | %%False%% | Warn when a mesh is absent beside the placement file. |

The function returns a list of published `GVolume` objects. It uses the configuration's current
experiment, system, variation, run, and output factory. It does not clear banks or choose variations.
Document defaults are applied first, then %%defaults%%, then each placement's own properties.

The default mesh extension is %%stl%%; a document's %%extension%% can select %%ply%%. A source volume
uses %%<cad_dir>/<name>.<extension>%%, with optional %%file%% and %%scale%% overrides. A %%copyOf%%
placement reuses its source solid without loading another mesh. Missing files do not prevent database
generation; the runtime must have the referenced meshes.

For CLAS12, call with %%passive=True%%. With %%passive=False%%, each record's %%g4placement_type%%
is honored and otherwise defaults to active placement.

The [complete first-import example](#create-your-first-cad-system) builds a placement file and Python
runner from scratch. [GXML and calculated-placement examples](#reuse-existing-gxml-and-calculated-placements)
show how detector builders use the same function.

## Workflow

1. Select the physical parts and materials, and record their units and coordinate frames.
2. Export one STL per distinct solid from the STEP model, retaining the engineering source.
3. Repair and simplify candidate meshes, preserving the features needed by the simulation.
4. Describe the placements in YAML, JSON, GXML, or Python.
5. Publish the records, load the geometry in GEMC, and check construction and overlaps.
6. Compare dimensions, material volume, and transport before accepting an optimized mesh.

Use [native Geant4 solids](solidTypes) for simple boxes, tubes, or cones when they describe the part
adequately. Reserve meshes for shapes whose engineering detail matters. A CAD material region needs a
closed surface, including its inner walls and rim faces; an uncapped sheet is not a solid.

## Convert STEP to STL

STEP preserves engineering surfaces and assembly structure. STL stores triangles without units,
materials, or placement metadata. Keep the STEP file and a record of its CAD application, export
settings, part names, material assignments, and coordinate convention.

Export different material regions separately. An assembly containing steel, copper, and vacuum cannot
be represented by one tessellated volume with three materials. Repeated identical parts can share one
mesh and use separate placements.

### Export with FreeCAD

Open the STEP file in `FreeCAD`, inspect the imported bodies, and select the required solid rather
than exporting the entire assembly indiscriminately. Create a mesh from the selected shape with
controlled linear and angular deflection, then export that mesh as STL. Menu names vary by version;
the Python console provides a repeatable alternative.

The following example tessellates a STEP file containing one solid. Run it in FreeCAD's Python console
or as a macro; ordinary Python environments do not normally include the `Part` and `MeshPart` modules.

```python
import math
import Part
import MeshPart

shape = Part.read("/absolute/path/bracket.step")
if len(shape.Solids) != 1:
    raise ValueError("Export each physical solid separately")

mesh = MeshPart.meshFromShape(
    Shape=shape,
    LinearDeflection=0.1,
    AngularDeflection=math.radians(10),
    Relative=False,
)
mesh.write("/absolute/path/bracket_raw.stl")
print("Triangles:", mesh.CountFacets)
```

%%LinearDeflection%% is an absolute surface approximation tolerance in FreeCAD's internal millimetres
when %%Relative%% is false. %%AngularDeflection%% is in radians. The example values are starting points,
not acceptance limits: choose tolerances against the smallest required wall, opening, curvature, and
clearance. A coarser export reduces triangle count but can turn a circular bore into a visibly polygonal
one or distort a mating surface. Record the settings so the STL can be regenerated.

For an assembly, export each selected solid with an explicit frame convention. Choose either assembly
coordinates in the vertices or local part coordinates plus a GEMC placement. Applying the assembly
transform during both export and placement moves the part twice. Check a known dimension, the axis
directions, the origin, and at least one mating face after export.

### Units and scale

GEMC interprets mesh coordinates as **millimetres multiplied by a uniform scale**. Use %%scale: 1%%
for millimetre exports, %%scale: 10%% for centimetres, or %%scale: 25.4%% for inches. Placement strings
carry their own units independently of the mesh scale.

Keep the exported dimensions and the placement convention together. Correct a unit mismatch once,
either in the mesh coordinates or in %%scale%%. Do not apply both corrections. Avoid silently recentering
an STL: GEMC rotates and translates the vertices about the origin stored in that file.

## Prepare and optimize the STL

Keep immutable raw exports and generate candidates into a separate directory. Start by measuring
triangle count, connected components, bounds, minimum wall thickness, open boundary edges, winding,
non-manifold edges, self-intersections, and signed material volume. A surface with zero boundary edges
can still self-intersect or contain invalid internal walls.

Use the `pygemc` environment that includes `pymeshlab`, for example an activated installed GEMC
%%python_env%%. The geometry-only build environment may not contain mesh-processing dependencies.

### Repair surface defects and reduce triangles

The [Cure Mesh utility](/home/documentation/api/cure_mesh) welds vertices, removes duplicate and
degenerate facets, decimates, repairs, closes boundary loops, and reorients faces.

```shell
gemc-cure-mesh bracket_raw.stl -o bracket_repaired.stl -f 0 --min-component-faces 0
gemc-cure-mesh bracket_repaired.stl -o bracket_candidate.stl -f 5000 --min-component-faces 0
```

The first command skips decimation and retains disconnected components; it still performs welding and
surface repair. The second requests 5,000 facets. Repair can add facets, and a requested target is not a
promise of final count or geometric accuracy. Run one mesh per process.

The default weld tolerance is a percentage of the bounding-box diagonal. On a long part, that can
exceed a thin wall or a narrow gap. Set %%--merge-percent%% from the part's dimensions and verify that
nearby surfaces remain separate. Likewise, component removal must not discard a small physical part.

Closing an accidental crack is different from capping a designed aperture. A valid hollow tube has
closed inner and outer surfaces joined at its ends, while its bore stays empty. Review every repair
that changes boundaries. Screened Poisson reconstruction can inflate thin shells, round interfaces,
or close passages; do not use it as a general repair for engineering tubes and cones.

### Remove selected engineering holes

A drilled through-hole in a watertight part is a tunnel with its own wall. It has no open boundary
edges, so ordinary surface-hole closing does not remove it.

When the simulation permits filling small fastener holes, `gemc-remove-holes` can identify small
wall groups and cap the resulting loops:

```shell
gemc-remove-holes bracket_repaired.stl -o bracket_no_bolts.stl --max-hole-diameter 4
```

%%--max-hole-diameter%% uses mesh-coordinate units, usually millimetres. Keep it below any functional
opening that must remain. The utility uses geometric heuristics; inspect the result, especially on
curved, slanted, or irregular parts. It does not understand which opening carries a beam or a cable.

Filling bolt holes adds material. Removing blind recesses, threads, or chamfers also changes the model.
Record each intended feature removal and its material-volume change. Protect beam apertures, cooling
channels, optical paths, grooves needed by neighboring parts, and all required mechanical clearances.
A targeted edit to the STEP solid followed by tessellation can preserve interfaces more reliably than
a broad mesh operation.

### Smooth surfaces and simplify further

Smoothing moves vertices. It can shrink a shell, round a sealing face, reduce a bore, and change material
thickness. Apply it selectively to noisy surfaces, with boundaries and sharp features constrained.
Use a measured displacement limit and retain an unsmoothed candidate for comparison. Smooth shading in a
viewer changes appearance only; it does not improve the tessellated surface used for tracking.

Other useful operations include merging coplanar triangles, retriangulating flat annuli, removing
duplicate internal faces, uniting overlapping pieces of the same physical material, replacing tiny
threads with smooth shafts, and sharing identical meshes through copies. Reconstruct a simple analytic
surface when its dimensions are known instead of smoothing it blindly. Keep different material regions
and intentional gaps separate.

Choose the triangle budget per part. A small flat plate may need only tens of triangles; a curved optical
surface may need many more. Reduce in stages and compare surface distances, cross-sections, apertures,
and wall thickness at every stage.

### Ask an agent to optimize a mesh

Give the agent the original STEP/STL, the part's role in the detector, its coordinate frame, neighboring
parts, protected features, and explicit error limits. State whether material may be added or removed,
which holes may be filled, and whether placements may change. Specify the available mesh tools and
require the agent to save a reproducible script.

A useful starting prompt is:

> Inspect this STL and its engineering STEP source before editing. Preserve the original files and
> generate candidates with a reproducible script. Report triangles, bounds, connected components,
> boundary edges, non-manifold edges, self-intersections, winding, signed volume, and minimum wall
> thickness before and after. Protect the beam bore, mounting planes, optical faces, and mating
> clearances. Repair cracks and duplicate/internal facets, then try conservative decimation.
> Smooth only selected noisy surfaces while protecting edges. Fill only the identified bolt holes;
> retain all functional passages. Report intentional material additions separately from simplification
> error. Propose dimensional and volume tolerances for review before changing the geometry. Compare
> cross-sections and surface distances, construct the candidate in GEMC, and test neighboring placements
> for overlaps. Benchmark loading and tracking with identical events and repeated runs. Deliver the
> script, candidate, validation report, and remaining warnings.

Replace the protected-feature list with the actual part's constraints. Add numerical limits before
optimization starts: maximum surface displacement, bore radius error, wall-thickness error, and material
volume change. An agent's visual judgment or a lower triangle count alone does not establish correctness.

## Create your first CAD system

The following example places one aluminum bracket twice. Prepare a millimetre STL named
%%bracket.stl%% and create this working directory:

```text
my_cad/
  build_geometry.py
  cad.yaml
  geometry.yaml
  stls/
    bracket.stl
```

Keep raw engineering exports elsewhere in the source tree; %%stls%% contains the accepted runtime mesh.

### Write the placement definition

Save this as %%cad.yaml%%:

```yaml
system: mechanics
experiment: demo
variation: default
run: 1
cad_dir: stls
extension: stl

defaults:
  material: G4_Al
  color: "aabbcc"
  g4placement_type: passive
  position: 0*mm, 0*mm, 0*mm
  rotation: 0*deg, 0*deg, 0*deg

volumes:
  - name: bracket
    description: Aluminum bracket
    scale: 1
  - name: bracket_copy
    copyOf: bracket
    position: 200*mm, 0*mm, 0*mm
```

The source defaults to %%stls/bracket.stl%% because its name matches the mesh stem. A %%copyOf%% record
reuses the source solid and needs no %%bracket_copy.stl%%. Its position and rotation are independent;
the same source and scale are reused within the system. Choose a copy position that clears your actual
part; 200 mm is only an example. For a different source filename, set %%file: other_name.stl%%.

Only listed volumes are published. Extra STL files in the directory are ignored. Defaults apply first,
and individual records override them. Quote hexadecimal colors so YAML treats them as strings.

### Publish with build_cad

**Upcoming with the next release:** save this as %%build_geometry.py%%:

```python
from pathlib import Path

from pygemc import autogeometry, build_cad

directory = Path(__file__).resolve().parent
cfg = autogeometry("demo", "mechanics")
build_cad(cfg, directory / "cad.yaml", passive=True)
```

Run it from %%my_cad%% using the `pygemc` Python environment:

```shell
python build_geometry.py -f sqlite -sql gemc.db
gemc-sqlite -sql gemc.db -sv
```

The helper publishes through %%cfg%%, so the configuration owns the experiment, system, variation,
run number, and output format. Top-level metadata in %%cad.yaml%% does not override an existing
configuration. The helper does not clear existing banks or initialize variations; leave that lifecycle
to the detector runner. It also supports ASCII output and the configuration's PyVista preview.

%%passive=True%% forces the GEMC2 frame-rotation convention for sources and copies. Otherwise the helper
honors each record's %%g4placement_type%%, defaulting to the active `GVolume` convention.
CLAS12 geometry uses passive placement throughout.

### Upload without writing Python

For a standalone YAML or JSON definition, the existing uploader creates the geometry records directly:

```shell
gemc-sqlite -sql gemc.db -cad cad.yaml
```

This route takes the experiment, system, variation, and run from the document, with optional command-line
overrides. It replaces geometry in the selected bank. Use a separate output database while developing
placements. Custom materials and optical surfaces must also be published; their definitions are not
embedded in this CAD placement document.

### Load the system in GEMC

Save this as %%geometry.yaml%%:

```yaml
experiment: demo
runno: 1
nthreads: 1
gsystem:
  - name: mechanics
    factory: sqlite
check_overlaps: 2
```

Run from the directory containing %%gemc.db%% and %%stls%%:

```shell
gemc geometry.yaml -n=0
```

This uses SQLite geometry rows with %%solid = CAD%% and parameters such as
%%stls/bracket.stl, 1%%. The SQLite loader resolves the mesh path and the CAD solid builder constructs
the tessellated volume. Native and CAD rows may share a SQLite system. Separate companion systems,
such as %%detector_cad%%, remain useful for organizing references and run-dependent placements.

The older %%factory: CAD%% route discovers meshes in a directory named after the system and matches
their stems to placement names. Its directory and scale conventions differ from the explicit path
example above. Keep the steering factory and the authored records consistent.

## Reuse existing GXML and calculated placements

**Upcoming with the next release:** the shared helper accepts existing GEMC2 GXML files:

```python
build_cad(
    cfg,
    directory / "cad" / f"cad_{cfg.variation}.gxml",
    cad_dir="stls",
    passive=True,
    material_aliases={"Air_Opt": "G4_AIR_Optical"},
)
```

Whitespace-separated GXML positions and rotations become GEMC field strings. %%copyOf%% reuses a
mesh; %%sensitivity="mirror: surface_name"%% becomes an optical skin, rather than readout sensitivity.
GEMC2 optical labels are not interpreted as readout identifiers. %%material_aliases%% supplies any
source-to-runtime material-name translation.

Calculated placements can pass an iterable of dictionaries instead of a file:

```python
placements = [
    {"name": "cone", "position": f"0*mm, 0*mm, {zshift}*mm"},
    {"name": "extension", "position": f"0*mm, 0*mm, {zshift + 1}*mm"},
]
build_cad(
    cfg, placements, cad_dir="stls", passive=True,
    defaults={"material": "G4_Al", "rotation": "0*deg, 180*deg, 0*deg"},
)
```

Keep survey shifts, sector calculations, and variation selection in the detector script. The helper
handles publication, mesh paths and scales, copies, materials, optical skins, and supported volume fields.
Document dictionaries may also contain %%cad_dir%%, %%extension%%, %%defaults%%, and %%volumes%%.
Returned `GVolume` objects describe the published records.

## Materials, optical surfaces, and sensitive volumes

Each CAD volume has one material. Use a Geant4 material such as %%G4_Al%% or publish a custom
`GMaterial` before loading the system. A CAD record's %%mirror%% names a `GMirror` optical surface;
publish the surface under the same system as its CAD placements, including a separate companion system
when one is used.

A sensitive placement can add these fields:

```yaml
digitization: flux
identifier: "id: 1"
```

%%sensitivity%% is accepted as an alias for %%digitization%%, and %%identifiers%% as an alias for
%%identifier%% in YAML/JSON/Python records. Sensitivity collects hits using the configured readout.

A tessellated solid has no native Geant4 constructor dimensions. For CAD hits,
%%GHit::getDetectorDimensions()%% returns an empty vector. A digitization plugin must obtain the
dimensions it needs from detector constants or the identity, rather than indexing that vector.

## Validate and measure the result

Compare candidates against both the engineering input and a repaired, unsimplified reference. Report
intentional hole filling separately so added material is not mistaken for a decimation error.

| Check | Evidence to retain |
| --- | --- |
| Shape and frame | Bounds, reference points, axis directions, cross-sections, bidirectional surface distances |
| Functional detail | Aperture sizes, minimum walls, mating planes, neighboring clearances |
| Topology | Boundary edges, connected shells, winding, non-manifold edges, self-intersections |
| Material | Signed volume for valid closed meshes, relative volume change, density and mass |
| Database | Names, mothers, materials, mesh paths, scale, rotations, copies, surfaces, run and variation |
| Runtime | Expected volume count, construction warnings, overlap diagnostics, short tracking run |
| Performance | Triangle counts, loading time, peak memory, and repeated tracking measurements |

Use %%check_overlaps: 2%% for a quick Geant4 overlap pass; increase sampling with
%%check_overlaps: 10000%% for a denser check. Sampling can miss thin overlaps, so also inspect critical
interfaces geometrically. Successful construction does not prove correct material distribution or
clearance.

For performance comparisons, use the same primaries, random seeds, physics list, Geant4 build,
thread count, and event count. Separate geometry loading from event tracking and repeat runs.
A smaller STL does not guarantee faster tracking. Preserve the measurements and unresolved warnings
beside the regeneration script.

If a mesh loads with orientation warnings, investigate internal seams, duplicate surfaces, and winding
before further simplification. Do not trade a dimensionally correct bore for a warning-free reconstruction.
Correctness and reproducibility determine whether an optimization is ready to use.
