---
layout: default
title: Documentation
permalink: /documentation/
---

Start with **Quickstart** if you are new to GEMC. Use **Installation** from the top navigation when
you need a local executable, then return here for task-oriented reference pages.

The documentation is organized by workflow:

- **API**: first run, Python visualization, analysis tools, and command-line options.
- **GUI**: Geant4 display setup and annotations.
- **Geometry**: detector volumes, materials, CAD imports, mirrors, and reusable structures.
- **Sensitivity**: built-in detector responses and custom digitization plugins.
- **Fields**: multipole magnetic fields and plugin-backed field maps.
- **Generator**: internal particle generation and LUND input files.
- **Output**: file formats, streamer configuration, and custom output plugins.

{% include directory.html data=site.data.documentation columns=5 section_breaks=4 link_target="_self" %}
