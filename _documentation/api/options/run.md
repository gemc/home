---
layout: default
title: 'GEMC option: run'
---

# `run`

Type: `option`

Description: event run number

Generated from:

```sh
gemc help run
```

```text
-run=<value> ...............: event run number


   Run number assigned to the generated events; it is also the key looked up in the
   -run_weights file. This is distinct from -runno, which selects the geometry/conditions
   variation from the database, and from the Geant4 run id g4runno, set automatically.
   
   Example: -run=12
```
