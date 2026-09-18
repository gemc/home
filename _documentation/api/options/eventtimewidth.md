---
layout: default
title: 'GEMC option: eventTimeWidth'
---

# `eventTimeWidth`

Type: `option`

Description: Time assigned to each consecutive generated event

Generated from:

```sh
gemc help eventTimeWidth
```

```text
-eventTimeWidth=<value> ....: Time assigned to each consecutive generated event


   Continuous event timeline spacing. Consecutive event IDs begin one eventTimeWidth apart. The default 0*ns leaves the timeline disabled; consumers that require continuous time must configure it.
```
