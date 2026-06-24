---
layout: default
title: 'GEMC option: gfields'
---

# `gfields`

Type: `option`

Description: define a generic plugin-backed e.m. field

Generated from:

```sh
gemc help gfields
```

```text
-gfields=<sequence> ........: define a generic plugin-backed e.m. field

   • name: Field name (unique key used by GMagneto maps)Default value: NODFLT
   • type: Field type; selects the plugin shared library gfield<type>FactoryDefault value: NODFLT
   • integration_stepper: Geant4 integration stepper name (string)Default value: G4DormandPrince745
   • minimum_step: Minimum step for the G4ChordFinder (Geant4 length units)Default value: 1.0*mm


   Adds a generic, plugin-backed electromagnetic field to the simulation.
   
   The 'type' selects the plugin shared library named gfield<type>Factory.
   Any additional scalar keys are forwarded verbatim to that plugin as string
   parameters (so the plugin alone decides which parameters it understands).
   
   Mandatory keys: name, type.
   
   Example (clas12 binary mapped field from the clas12-systems plugin):
   -gfields="[{name: clas12, type: clas12bin, solenoid: solenoid_map, torus: torus_map}]"
   
   Example (generic ASCII field map, type asciimap): the data-only map file holds the
   coordinate columns followed by the field components, while the grid is defined here.
   -gfields="[{name: solenoid, type: asciimap, symmetry: cylindrical-z, map: solenoid.txt,
   field_unit: T, coordinate1: 'transverse, 601, 0*m, 3*m',
   coordinate2: 'longitudinal, 1201, -3*m, 3*m'}]"
```
