---
layout: default
title: 'GEMC option: no_field'
---

# `no_field`

Type: `option`

Description: reset the field of one or more volumes

Generated from:

```sh
gemc help no_field
```

```text
-no_field=<value> ..........: reset the field of one or more volumes


   Removes the electromagnetic field association from one or more volumes.
   
   The value is either the name of a gvolume, a whitespace- or comma-separated list of gvolume
   names, or the special value 'all'. A listed volume that was associated with a field (per-volume
   or inherited) has that association removed, so it is left with no field. The special value 'all'
   resets every per-volume field and also clears the 'global_field' option.
   
   Fields that no volume uses as a result are not loaded: their plugins and field maps are skipped.
   
   Examples: -no_field=target            (reset only the 'target' volume)
   -no_field="target, magnet"  (reset both volumes)
   -no_field=all               (reset every field, including the global field)
```
