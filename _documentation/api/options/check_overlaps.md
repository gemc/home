---
layout: default
title: 'GEMC option: check_overlaps'
---

# `check_overlaps`

Type: `option`

Description: check overlaps

Generated from:

```sh
gemc help check_overlaps
```

```text
-check_overlaps=<value> ....: check overlaps


   Check for overlaps at physical volume construction.
   Possible values are:
   - 0 (default): no check.
   - 1: enable the G4PVPlacement surface overlap check (pSurfChk) at volume placement.
   - 2: use the geant4 overlap validator with the default number of points on the surface
   - Any N greater than 100: use the geant4 overlap validator with N points on the surface
   
   Example: -check_overlaps=1
```
