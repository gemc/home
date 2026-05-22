---
layout: default
title: 'GEMC option: gmultipoles'
---

# `gmultipoles`

Type: `option`

Description: define the e.m. gmultipoles

Generated from:

```sh
gemc help gmultipoles
```

```text
-gmultipoles=<sequence> ....: define the e.m. gmultipoles

   • name: Field name (unique key used by GMagneto maps)Default value: NODFLT
   • integration_stepper: Geant4 integration stepper name (string)Default value: G4DormandPrince745
   • minimum_step: Minimum step for the G4ChordFinder (Geant4 length units)Default value: 1.0*mm
   • pole_number: Pole number (even integer >= 2): 2=dipole, 4=quadrupole, ...Default value: NODFLT
   • vx: Origin X component (Geant4 length units)Default value: 0*mm
   • vy: Origin Y component (Geant4 length units)Default value: 0*mm
   • vz: Origin Z component (Geant4 length units)Default value: 0*mm
   • rotation_angle: Roll rotation angle about rotaxis (Geant4 angle units)Default value: 0*deg
   • rotaxis: Rotation/longitudinal axis: one of X, Y, ZDefault value: NODFLT
   • strength: Field strength in Tesla (defined at 1 m reference radius for multipoles)Default value: NODFLT
   • longitudinal: If true, return a uniform field aligned with rotaxis (solenoid-like)Default value: false


   Adds gmultipoles field(s) to the simulation
```
