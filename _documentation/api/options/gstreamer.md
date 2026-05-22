---
layout: default
title: 'GEMC option: gstreamer'
---

# `gstreamer`

Type: `option`

Description: define a gstreamer output

Generated from:

```sh
gemc help gstreamer
```

```text
-gstreamer=<sequence> ......: define a gstreamer output

   • filename: name of output file. Default value: NODFLT
   • format: format of output file. Default value: NODFLT
   • type: type of output fileDefault value: event


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
