---
layout: default
title: 'GEMC option: gsystem'
---

# `gsystem`

Type: `option`

Description: defines the group of volumes in a system

Generated from:

```sh
gemc help gsystem
```

```text
-gsystem=<sequence> ........: defines the group of volumes in a system

   • name: system name (mandatory). For ascii factories, it may include the path to the fileDefault value: NODFLT
   • factory: factory name.Default value: sqlite
   • variation: geometry variationDefault value: default
   • annotations: optional system annotations. Examples: "mats_only" Default value: null
   • digitization: optional digitization plugin name when it differs from the system name (shared plugin, e.g. "ecal" for the EC and PCAL systems)Default value: null


   A system definition includes the geometry location, factory and variation
   
   Possible factories are:
   - ascii
   - sqlite
   - mysql
   - CAD
   Example: -gsystem="[{name: b1}]"
```
