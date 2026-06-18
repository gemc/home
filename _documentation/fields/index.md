---
layout: default
title: Fields
order: 40
description: Configure electromagnetic fields and query them along the beamline
permalink: /documentation/fields/
---

# Fields

GEMC propagates charged tracks through one or more **electromagnetic fields**. Each field is an
independent, named object that Geant4 queries for a magnetic flux density `B` at every step point.

Fields are declared in YAML. A configuration can mix any number of them; GEMC builds the field
registry once per worker thread and hands each volume the field manager it needs.

<br/>

## Two ways to define a field

| Route | YAML key | Use when |
|-------|----------|----------|
| [Multipoles](/home/documentation/fields/multipoles) | `gmultipoles` | You want an ideal dipole, quadrupole, sextupole, … defined analytically |
| [Field plugins](/home/documentation/fields/plugins) | `gfields` | A shared-library plugin supplies the field (mapped fields, custom models) |

Both routes produce the same kind of runtime object — a `GField` — and share the same integration
controls (`integration_stepper`, `minimum_step`).

<br/>

## A minimal example

```yaml
gmultipoles:
  - name: dipole
    pole_number: 2
    strength: 2
    rotaxis: z
    rotation_angle: "30*deg"
```

```sh
gemc mydetector.yaml
```

<br/>

## Common keys

Every field entry — whichever route — accepts these integration controls:

| Key | Default | Meaning |
|-----|---------|---------|
| `name` | *(required)* | Unique key used by the field registry |
| `integration_stepper` | `G4DormandPrince745` | Geant4 stepper class name |
| `minimum_step` | `1.0*mm` | Minimum step for the `G4ChordFinder` |

<br/>

## Querying a field

You do not need a full simulation to inspect a field. Two options print `B` at chosen points and
exit — see [Field plugins → Querying](/home/documentation/fields/plugins#querying-a-field):

```sh
gemc dipole.yaml -fieldAt="10*cm 0*mm 2*m"
gemc dipole.yaml -fieldMapPoints=field_points.txt
```
