---
layout: default
title: 'GEMC option: g4decoration'
---

# `g4decoration`

Type: `option`

Description: Adds optional Geant4 scene decorations

Generated from:

```sh
gemc help g4decoration
```

```text
-g4decoration=<sequence> ...: Adds optional Geant4 scene decorations

   • scale: add a simple scale lineDefault value: false
   • scaleLength: scale lengthDefault value: 10.000000
   • scaleUnit: scale length unitDefault value: mm
   • scaleDirection: scale direction: x, y, or zDefault value: z
   • scaleColor: scale color as 'r g b' or a named colorDefault value: 0.9 0.9 0.9
   • axes: add simple XYZ axesDefault value: false
   • eventID: add event ID text at end of eventDefault value: false
   • date: add a date stampDefault value: false
   • logo2D: add the 2D Geant4 logoDefault value: false
   • logo: add the 3D Geant4 logoDefault value: false
   • frame: add a frame around the viewDefault value: false
   • frameColor: frame colorDefault value: red
   • frameLineWidth: frame line widthDefault value: 2.000000


   Adds optional Geant4 scene decorations.
   
   Example: -g4decoration="[{scale: true, axes: true, eventID: true, date: true, logo2D: true, logo: true, frame: true}]"
```
