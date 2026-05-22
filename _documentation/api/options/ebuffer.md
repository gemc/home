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


   Define output formats and filenames. It can be used to select event or stream outputs.
   The file extension is added automatically based on the format.
   
   Supported formats:
   
   - jlabsro
   - root
   - ascii
   - csv
   - json
   
   Output types:
   
   - event: write events
   - stream: write frame time snapshots
   
   Example that defines two gstreamer outputs:
   
   -gstreamer="[{format: root, filename: out}, {format: csv, filename: out}]"
   
   The produced files structure depends on the accumulation method used:
   
   - event-based digitization (like flux) will have one file for every thread, with "_t<thread>" appended to the filename
   - run-based digitization (like dosimeter) will have one file only
```
