---
layout: default
title: 'GEMC option: max_field_step'
---

# `max_field_step`

Type: `option`

Description: maximum accepted field step

Generated from:

```sh
gemc help max_field_step
```

```text
-max_field_step=<value> ....: maximum accepted field step


   Sets the maximum acceptable propagation step used by Geant4 magnetic-field transportation.
   
   The value is parsed as a Geant4 length expression and is passed to
   G4PropagatorInField::SetLargestAcceptableStep() when positive. The default value
   (0*mm) leaves the Geant4 default unchanged.
   
   Example: -max_field_step=5*mm
```
