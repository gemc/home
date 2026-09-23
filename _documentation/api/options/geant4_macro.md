---
layout: default
title: 'GEMC option: geant4_macro'
---

# `geant4_macro`

Type: `option`

Description: execute a Geant4 macro text file at startup

Generated from:

```sh
gemc help geant4_macro
```

```text
-geant4_macro=<value> ......: execute a Geant4 macro text file at startup


   Example: -geant4_macro=run.mac (or geant4_macro: run.mac in YAML).
   Executed after GEMC initialization and visualization setup, before the GUI or terminal session.
   Relative paths use the current working directory. Geant4 macro syntax and nested macros apply.
   In batch mode the macro controls event generation with /run/beamOn; -n and -run_weights do not
   dispatch extra events. Detector conditions use -run. Without this option, normal runs apply.
   A missing file or a failed macro command terminates GEMC with a nonzero exit status.
```
