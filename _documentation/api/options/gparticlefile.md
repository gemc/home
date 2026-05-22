---
layout: default
title: 'GEMC option: gparticlefile'
---

# `gparticlefile`

Type: `option`

Description: define generator particles from file(s)

Generated from:

```sh
gemc help gparticlefile
```

```text
-gparticlefile=<sequence> ..: define generator particles from file(s)

   • format: Particle file format, for example "lund"Default value: NODFLT
   • filename: Input filename containing particle definitionsDefault value: NODFLT


   Adds particles to the event generator from particle-definition files.
   The option is cumulative and each entry selects a reader by format and filename.
   
   Built-in formats:
   - lund
   Formats are case-insensitive. Additional formats can be provided by dynamic plugins named gparticle_<format>_plugin.gplugin exporting GParticleReaderFactory.
   
   Example:
   -gparticlefile="[{format: lund, filename: a.lund}]"
```
