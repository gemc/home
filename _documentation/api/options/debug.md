---
layout: default
title: 'GEMC option: debug'
---

# `debug`

Type: `option`

Description: Sets the debug level for various classes

Generated from:

```sh
gemc help debug
```

```text
-debug=<sequence> ..........: Sets the debug level for various classes

   • gemc: gemc verbosity level or debug switchDefault value: 0
   • dbselect: dbselect verbosity level or debug switchDefault value: 0
   • gdetector: gdetector verbosity level or debug switchDefault value: 0
   • gvolume: gvolume verbosity level or debug switchDefault value: 0
   • gmaterial: gmaterial verbosity level or debug switchDefault value: 0
   • gsystem: gsystem verbosity level or debug switchDefault value: 0
   • gworld: gworld verbosity level or debug switchDefault value: 0
   • gsfactory: gsfactory verbosity level or debug switchDefault value: 0
   • plugins: plugins verbosity level or debug switchDefault value: 0
   • g4system: g4system verbosity level or debug switchDefault value: 0
   • g4sfactory: g4sfactory verbosity level or debug switchDefault value: 0
   • gdigitization: gdigitization verbosity level or debug switchDefault value: 0
   • gevent_data: gevent_data verbosity level or debug switchDefault value: 0
   • event_header: event_header verbosity level or debug switchDefault value: 0
   • true_data: true_data verbosity level or debug switchDefault value: 0
   • digitized_data: digitized_data verbosity level or debug switchDefault value: 0
   • gtouchable: gtouchable verbosity level or debug switchDefault value: 0
   • grun_data: grun_data verbosity level or debug switchDefault value: 0
   • run_header: run_header verbosity level or debug switchDefault value: 0
   • gtranslationtable: gtranslationtable verbosity level or debug switchDefault value: 0
   • gsd: gsd verbosity level or debug switchDefault value: 0
   • gstreamer: gstreamer verbosity level or debug switchDefault value: 0
   • gsplash: gsplash verbosity level or debug switchDefault value: 0
   • gphysics: gphysics verbosity level or debug switchDefault value: 0
   • gaction: gaction verbosity level or debug switchDefault value: 0
   • geventaction: geventaction verbosity level or debug switchDefault value: 0
   • grunaction: grunaction verbosity level or debug switchDefault value: 0
   • generator: generator verbosity level or debug switchDefault value: 0
   • grun: grun verbosity level or debug switchDefault value: 0
   • gparticle: gparticle verbosity level or debug switchDefault value: 0
   • eventdispenser: eventdispenser verbosity level or debug switchDefault value: 0
   • g4display: g4display verbosity level or debug switchDefault value: 0
   • g4scene: g4scene verbosity level or debug switchDefault value: 0
   • g4dialog: g4dialog verbosity level or debug switchDefault value: 0
   • gfield: gfield verbosity level or debug switchDefault value: 0
   • gmagneto: gmagneto verbosity level or debug switchDefault value: 0
   • gboard: gboard verbosity level or debug switchDefault value: 0
   • gtree: gtree verbosity level or debug switchDefault value: 0


   Debug information Types:
   
   - false: (default): do not print debug information
   - true: print debug information
   Example: -debug="[{gemc: true}]"
   
   The YAML value can include multiple logger keys.
```
