---
layout: default
title: 'GEMC option: global_field'
---

# `global_field`

Type: `option`

Description: associate a field with the ROOT world volume

Generated from:

```sh
gemc help global_field
```

```text
-global_field=<value> ......: associate a field with the ROOT world volume


   Associates a configured electromagnetic field with the ROOT (top-level) world volume.
   
   The value must be the name of a field defined with -gmultipoles or -gfields. The field's
   G4FieldManager is installed on the ROOT world volume and propagated to all daughters, so it
   applies everywhere a more specific per-volume field has not been set.
   
   Example: -global_field=dipole1
```
