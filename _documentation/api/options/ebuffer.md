---
layout: default
title: 'GEMC option: ebuffer'
---

# `ebuffer`

Type: `option`

Description: number of events kept in memory before flushing them to the filestream

Generated from:

```sh
gemc help ebuffer
```

```text
-ebuffer=<value> ...........: number of events kept in memory before flushing them to the filestream


   Number of events each streamer keeps in memory before flushing them to the
   output file. Larger values reduce I/O frequency at the cost of more memory.
   
   Example: -ebuffer=100
```
