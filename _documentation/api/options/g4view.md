---
layout: default
title: 'GEMC option: g4view'
---

# `g4view`

Type: `option`

Description: Defines the geant4 viewer properties

Generated from:

```sh
gemc help g4view
```

```text
-g4view=<sequence> .........: Defines the geant4 viewer properties

   • driver: Geant4 visualization driver. Use TOOLSSG_OFFSCREEN in batch mode. Default value: TOOLSSG_QT_GLES
   • dimension: Geant4 viewer dimensionDefault value: 800x800
   • position: Geant4 viewer positionDefault value: -400+100
   • segsPerCircle: Number of segments per circleDefault value: 50


   Defines the Geant4 viewer properties:
   - screen dimensions
   - screen position
   - resolution in terms of segments per circle
   
   Examples:
   
   -g4view="[{dimension: 1200x1000}]"
   -g4view="[{driver: OGL, dimension: 1100x800, position: +200+100, segsPerCircle: 100}]"
   -g4view="[{driver: TOOLSSG_OFFSCREEN, segsPerCircle: 200}]" takes a screenshot at the end of each run
```
