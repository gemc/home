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
```
