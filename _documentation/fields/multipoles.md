---
layout: default
title: Multipoles
order: 41
description: Define an ideal multipole magnetic field analytically with the gmultipoles key
permalink: /documentation/fields/multipoles/
---

# Multipole Fields

The `gmultipoles` key defines an **ideal multipole** magnetic field analytically — no map file is
needed. It covers the standard accelerator elements: dipole, quadrupole, sextupole, and higher
orders.

```yaml
gmultipoles:
  - name: q1
    pole_number: 4
    strength: 1.2
    rotaxis: z
    vz: "30*cm"
```

Each list entry becomes one independently named field.

<br/>

## How the field is built

The transverse field follows the common accelerator convention. With `n = pole_number / 2`:

- the magnitude scales like `r^(n-1)`, with the reference radius fixed at `r0 = 1 m`;
- the azimuthal dependence is `cos((n-1)·φ)` / `sin((n-1)·φ)` in the plane perpendicular to
  `rotaxis`.

So `pole_number: 2` (n = 1) is a uniform transverse dipole, `pole_number: 4` (n = 2) is a
quadrupole whose field grows linearly with radius, and so on. The field is evaluated in a
magnet-centered frame (translated by `vx/vy/vz`, unrolled by `-rotation_angle` about `rotaxis`),
then rotated back into the lab frame.

<br/>

## Parameters

| Key | Default | Meaning |
|-----|---------|---------|
| `name` | *(required)* | Unique field name |
| `pole_number` | *(required)* | Even integer ≥ 2: 2 = dipole, 4 = quadrupole, 6 = sextupole, … |
| `strength` | *(required)* | Field strength in Tesla, defined at the 1 m reference radius |
| `rotaxis` | *(required)* | Longitudinal / rotation axis: `X`, `Y`, or `Z` |
| `rotation_angle` | `0*deg` | Roll rotation about `rotaxis` (Geant4 angle units) |
| `vx`, `vy`, `vz` | `0*mm` | Magnet origin in the lab frame (Geant4 length units) |
| `longitudinal` | `false` | If `true`, return a uniform axial field aligned with `rotaxis` |
| `integration_stepper` | `G4DormandPrince745` | Geant4 stepper class name |
| `minimum_step` | `1.0*mm` | Minimum step for the `G4ChordFinder` |

Strengths and lengths preserve unit expressions, so `strength: 1.2`, `vz: "30*cm"`, and
`rotation_angle: "30*deg"` are all parsed with their units.

<br/>

## Longitudinal (solenoid-like) mode

Setting `longitudinal: true` returns a uniform field aligned with `rotaxis` instead of a multipole
expansion. This is a convenience for configuration symmetry, not a true multipole:

```yaml
gmultipoles:
  - name: solenoid_like
    pole_number: 2        # still required, but ignored in longitudinal mode
    strength: 5           # uniform 5 T along the axis
    rotaxis: z
    longitudinal: true
```

<br/>

## Quick check

Print the field at a point without running a simulation:

```sh
gemc dipole.yaml -fieldAt="0*cm 0*cm 0*cm"
```

```
field=dipole source=fieldAt x=0 fm y=0 fm z=0 fm Bx=... By=... Bz=... |B|=2 tesla
```

See [Field plugins → Querying](/home/documentation/fields/plugins#querying-a-field) for the full
query syntax, including reading many points from a file.
