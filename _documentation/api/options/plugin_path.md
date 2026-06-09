---
layout: default
title: 'GEMC option: plugin_path'
---

# `plugin_path`

Type: `option`

Description: colon-separated list of directories to search for .gplugin files

Generated from:

```sh
gemc help plugin_path
```

```text
-plugin_path=<value> .......: colon-separated list of directories to search for .gplugin files


   Additional directories searched for GEMC plugin libraries (*.gplugin) before the
   current working directory and the system library path (LD_LIBRARY_PATH / DYLD_LIBRARY_PATH).
   Example: -plugin_path=/opt/clas12/lib:/usr/local/gemc/plugins
```
