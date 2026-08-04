---
layout: default
title: Mirrors
order: 25
description: Create mirrors and assign optical properties
---

# Mirrors

In GEMC any optical boundary is described as a **mirror**, regardless of its use or reflective
quality: metal reflectors, painted walls, wrappings, or the interface between two transparent
media. A mirror defines a Geant4 optical surface; each volume can reference one mirror by name
through its `mirror` field.

All mirrors are created with the `GMirror` class:

```python
from pygemc import GMirror
```

<br/>

## Defining a mirror

A `GMirror` is created with its name and four mandatory fields:

| Field | Description |
|-------|-------------|
| `type` | Surface type, e.g. `dielectric_metal`, `dielectric_dielectric` |
| `finish` | Surface finish, e.g. `polished`, `ground`, `polishedfrontpainted` |
| `model` | Optical model: `glisur`, `unified`, `LUT`, `DAVIS`, `dichroic` |
| `border` | `SkinSurface`, or the name of a bordering volume (see below) |

The available types and finishes are the ones defined by Geant4 in [G4OpticalSurface][g4-optical-surface]:
unknown strings are rejected at load time.

[g4-optical-surface]: https://geant4-userdoc.web.cern.ch/

```python
mirror = GMirror("polished_metal")
mirror.description = "Polished metal mirror"
mirror.type = "dielectric_metal"
mirror.finish = "polished"
mirror.model = "unified"
mirror.border = "SkinSurface"
mirror.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV 6.0*eV"
mirror.reflectivity = "0.90 0.90 0.89 0.88 0.87"
mirror.publish(cfg)
```

<br/>

## Boundary optical properties

The optical behavior of the boundary comes from one of two sources:

### Explicit tables

Energy-dependent tables evaluated at `photonEnergy`, exactly as for
[material optical properties](/home/documentation/optical/optical_properties):

| Field | Geant4 property | Description |
|-------|------------------|-------------|
| `photonEnergy` | - | Energy axis for all other tables (required) |
| `indexOfRefraction` | RINDEX | Refractive index of the boundary |
| `reflectivity` | REFLECTIVITY | Probability that the photon is reflected |
| `efficiency` | EFFICIENCY | Absorption/detection efficiency (e.g. PMT quantum efficiency) |
| `specularlobe` | SPECULARLOBECONSTANT | Rough-surface scattering component |
| `specularspike` | SPECULARSPIKECONSTANT | Rough-surface scattering component |
| `backscatter` | BACKSCATTERCONSTANT | Rough-surface scattering component |
| `transmittance` | TRANSMITTANCE | Probability that the photon is transmitted through the surface |

Every provided table must have the same number of entries as `photonEnergy`; mismatches are
rejected when the mirror is loaded.

The scalar `sigmaAlpha` sets the surface roughness used by the `unified` model with `ground`
finishes. Note that with a `ground` finish the unified model reflects **diffusely** (Lambertian)
by default: to obtain a blurred but still specular reflection, direct the reflection into the
specular lobe with `specularlobe` and control the blur with `sigmaAlpha`:

```python
rough = GMirror("rough_metal")
rough.type = "dielectric_metal"
rough.finish = "ground"
rough.model = "unified"
rough.border = "SkinSurface"
rough.photonEnergy = "2.0*eV 4.0*eV 6.0*eV"
rough.reflectivity = "0.90 0.89 0.87"
rough.specularlobe = "1.0 1.0 1.0"
rough.sigmaAlpha = 0.03
rough.publish(cfg)
```

A `transmittance` table turns a metal mirror into a half-silvered (semi-transparent) one: at
the boundary the photon is reflected with probability R, transmitted with probability T, and
absorbed otherwise:

```python
semi = GMirror("semi_transparent")
semi.type = "dielectric_metal"
semi.finish = "polished"
semi.model = "unified"
semi.border = "beam_splitter_plate"       # border surface (see below)
semi.photonEnergy = "2.0*eV 4.0*eV 6.0*eV"
semi.reflectivity = "0.60 0.60 0.60"
semi.transmittance = "0.30 0.30 0.30"
semi.publish(cfg)
```

### From a material

Alternatively, `matOptProps` names a material whose optical properties table is used as the
boundary properties. The material does not have to be the material of either bordering volume -
think of it as a thin coating or paint:

```python
coated = GMirror("coated_metal")
coated.type = "dielectric_metal"
coated.finish = "polished"
coated.model = "unified"
coated.border = "SkinSurface"
coated.matOptProps = "mirror_coating"      # a GMaterial with optical properties
coated.publish(cfg)
```

<br/>

## Skin and border surfaces

The `border` field selects between the two Geant4 logical surface kinds:

* **`SkinSurface`**: the optical boundary covers the entire outside surface of every volume
  that references the mirror.
* **A volume name**: the optical boundary applies only to photons crossing from the referencing
  volume into the named border volume (both must belong to the same system). The direction
  matters: the surface acts on photons leaving the volume that carries the `mirror` field.

<br/>

## Assigning a mirror to a volume

Volumes reference a mirror by name through the `GVolume` `mirror` field:

```python
plate = GVolume("flat_reflector")
plate.mother = "radiator"
plate.make_box(140, 440, 5)
plate.material = "G4_Al"
plate.mirror = "polished_metal"            # skin surface on this plate
plate.publish(cfg)
```

For a border surface, the mirror is attached to the volume the photons come *from*:

```python
radiator.mirror = "black_paint"            # black_paint.border = "bottom_panel"
```

Any number of volumes can share the same mirror: GEMC creates one optical surface per mirror
definition and reuses it for every volume that references it.

<br/>

## Storage

Like geometry and materials, mirrors are written by the Python API to the factory selected at
geometry-creation time:

* **sqlite**: one row per mirror in the `mirrors` table, keyed by experiment, system, variation
  and run;
* **ascii**: one row per mirror in `<system>__mirrors_<variation>.txt`.

Both are loaded automatically by gemc together with the system geometry and materials.

<br/>

## Example

The [Mirrors example](/home/examples/optical/mirrors) shows all of the above in a working
simulation: three identical electrons aim at three reflector plates (polished, rough, and
semi-transparent), which reflect their Cherenkov photons onto three aligned photon detectors -
identical conditions, so the panel counts directly compare the reflections. A fourth panel
behind the semi-transparent plate counts the transmitted photons.

The [Parabolic Mirror example](/home/examples/optical/parabolic_mirror) shows a focusing
mirror made from two `G4Paraboloid` solids. The final mirror volume is a boolean subtraction,
%%outer_dish - inner_dish%%, and carries the `GMirror` skin surface so photons reflect from the
inner cavity toward the focus detector.

```shell
cp -r $GEMC_HOME/examples/optical/mirrors .
cd mirrors
./mirrors.py
gemc mirrors.yaml -n=10
```
