---
layout: default
title: 'GEMC option: g4text'
---

# `g4text`

Type: `option`

Description: Insert texts in the current scene

Generated from:

```sh
gemc help g4text
```

```text
-g4text=<sequence> .........: Insert texts in the current scene

   • text: string with the text to be displayedDefault value: NODFLT
   • color: color of the textDefault value: black
   • kind: text kind: 2D or 3DDefault value: 2D
   • layout: optional text layout, for example rightDefault value: null
   • x: x position of the textDefault value: 0
   • y: y position of the textDefault value: 0
   • z: z position of the textDefault value: -1234.500000
   • unit: unit for 3D text positionsDefault value: cm
   • size: size of the textDefault value: 24.000000
   • dx: 3D text x offsetDefault value: 4.000000
   • dy: 3D text y offsetDefault value: 4.000000


   Adds 2D or 3D text to the current scene.
   
   Example to add two texts:
   
   -g4text="[{kind: 2D, text: hello, x: 0.9, y: -0.9, layout: right}, {kind: 3D, text: Shape1, x: 0, y: 6, z: -4}]"
```
