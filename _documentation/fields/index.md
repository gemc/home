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

## Attaching a field to geometry

Defining a field only registers it — it stays inert until a volume uses it. There are two ways to
apply a field to the geometry, and they can be combined:

| Scope | How | Effect |
|-------|-----|--------|
| Per volume | Set the volume's `emfield` to a field name | The field manager is installed on that volume and **propagated to all its daughters** |
| Global | `-global_field=<name>` on the command line (or `global_field: <name>` in YAML) | The field is installed on the ROOT world volume, so it applies **everywhere** |

Because Geant4 uses the field manager of the nearest enclosing volume, a per-volume `emfield`
**overrides** the global field locally. A common pattern is a global field for the whole apparatus
plus a stronger, more specific field inside one magnet:

```yaml
gmultipoles:
  - name: holding         # weak field everywhere
    pole_number: 2
    strength: 0.5
    rotaxis: z
  - name: magnet          # strong field inside one volume
    pole_number: 4
    strength: 1.2
    rotaxis: z

global_field: holding     # attach 'holding' to the ROOT world volume
```

The `magnet` field is then attached to a specific volume through that volume's `emfield` label, and
wins over `holding` wherever the two overlap. The `<name>` given to `global_field` (or to a volume's
`emfield`) must match the `name` of a field defined under `gmultipoles` or `gfields`.

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
