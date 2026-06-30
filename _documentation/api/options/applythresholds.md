---
layout: default
title: 'GEMC option: applyThresholds'
---

# `applyThresholds`

Type: `option`

Description: systems that reject hits below threshold

Generated from:

```sh
gemc help applyThresholds
```

```text
-applyThresholds=<value> ...: systems that reject hits below threshold


   List of digitization system names whose hits below the per-channel threshold are
   rejected. Use "all" for every system. Default: not set (no thresholds applied).
   
   Example: -applyThresholds="ftof, ctof"
```
