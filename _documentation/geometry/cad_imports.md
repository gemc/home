---
layout: default
title: Cad Imports
description: use python to create volumes based on geant4 solids
---

Cad Imports: coming soon

Preparing a mesh for import? Heavy or non-watertight CAD meshes can be simplified and repaired for Geant4
with the [Cure Mesh](/home/documentation/api/cure_mesh) utility (`gemc-cure-mesh`), which decimates, welds,
closes holes, and re-orients facets so the tessellated solid loads fast and without warnings.

## Sensitive CAD volumes and detector dimensions

A CAD volume is imported from a mesh (`.stl` / `.ply`), so it has no native Geant4 solid and therefore no
constructor dimensions. For native solids (`G4Box`, `G4Tubs`, ...) GEMC exposes those dimensions to the
digitization stage — a hit-process plugin can read them back through `GHit::getDetectorDimensions()`. For a
CAD volume that list is intentionally **empty**: the mesh has no width/height/radius to report.

This matters when a CAD volume is made sensitive (it is assigned a `digitization`). Such a volume still
carries its full identity (the `gidentity` string, e.g. `sector: 1`), and hits are collected normally, but a
digitization plugin must not rely on `getDetectorDimensions()` for CAD hits — it will receive an empty
vector. Derive any per-element geometry the plugin needs from the identity or from the mesh itself instead.