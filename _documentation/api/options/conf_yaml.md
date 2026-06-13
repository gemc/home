---
layout: default
title: 'GEMC option: conf_yaml'
---

# `conf_yaml`

Type: `option`

Description: infix for the YAML file that records the resolved options

Generated from:

```sh
gemc help conf_yaml
```

```text
-conf_yaml=<value> .........: infix for the YAML file that records the resolved options


   On exit the resolved configuration is written to <executable>.<conf_yaml>.yaml,
   so the default value produces, for example, gemc.saved_configuration.yaml.
   
   Example: -conf_yaml=run12   ->   saves to gemc.run12.yaml
```
