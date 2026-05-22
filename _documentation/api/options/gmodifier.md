---
layout: default
title: 'GEMC option: gmodifier'
---

# `gmodifier`

Type: `option`

Description: modify volume existence or placement

Generated from:

```sh
gemc help gmodifier
```

```text
-gmodifier=<sequence> ......: modify volume existence or placement

   • name: volume name (mandatory)Default value: NODFLT
   • shift: volume shift added to existing positionDefault value: noModifier
   • tilt: volume tilt added to existing rotationDefault value: noModifier
   • isPresent: If set to false, remove the volume from the worldDefault value: true


   The volume modifier can shift, tilt, or delete a volume from the gworld
   
   Example: -gmodifier="[{name: targetCell, tilt: '0*deg, 0*deg, -10*deg'}]"
```
