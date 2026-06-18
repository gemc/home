---
layout: default
title: 'GEMC option: fieldMapPoints'
---

# `fieldMapPoints`

Type: `option`

Description: ASCII file of x y z points for field queries

Generated from:

```sh
gemc help fieldMapPoints
```

```text
-fieldMapPoints=<value> ....: ASCII file of x y z points for field queries


   Evaluate all configured electromagnetic fields at coordinates listed in an ASCII file.
   
   Each non-empty, non-comment line must contain three coordinate expressions with units.
   Coordinates may be separated by spaces or commas. Lines beginning with # are ignored.
   
   Example: -fieldMapPoints=points.txt
```
