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
   • x: x position of the textDefault value: 0
   • y: y position of the textDefault value: 0
   • z: z position of the textDefault value: -1234.500000
   • size: size of the textDefault value: 24.000000


   If the z coordinate is specified, the text is considered 2D.
   
   Example to add two texts:
   
   -g4text="[{text: hello, x: -100}, {text: there, x: 100}]"
```
