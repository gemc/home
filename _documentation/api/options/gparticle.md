---
layout: default
title: 'GEMC option: gparticle'
---

# `gparticle`

Type: `option`

Description: define the generator particle(s)

Generated from:

```sh
gemc help gparticle
```

```text
-gparticle=<sequence> ......: define the generator particle(s)

   • name: Particle name (mandatory), for example "proton"Default value: NODFLT
   • multiplicity: How many copies of this particle will be generated in each eventDefault value: 1
   • p: Particle momentumDefault value: NODFLT
   • delta_p: Particle momentum range, centered on p.Default value: 0
   • punit: Geant4 unit for the particle momentum. Default value: MeV
   • randomMomentumModel: Momentum randomization. 'gaussian' (use deltas as sigmas)Default value: uniform
   • theta: Particle polar angle. Default value: 0
   • delta_theta: Particle polar angle range, centered on theta. Default value: 0
   • randomThetaModel: Distribute cos(theta) or theta. 'cosine': cos(theta) is uniform. 'uniform': theta is uniformDefault value: uniform
   • phi: Particle azimuthal angle. Default value: 0
   • delta_phi: Particle azimuthal angle range, centered on phi. Default value: 0
   • aunit: Geant4 unit for the particle angles.  Default value: deg
   • vx: Particle vertex x component. Default value: 0
   • vy: Particle vertex y component. Default value: 0
   • vz: Particle vertex z component. Default value: 0
   • delta_vx: Particle vertex range of the x component. Default value: 0
   • delta_vy: Particle vertex range of the y component. Default value: 0
   • delta_vz: Particle vertex range of the z component. Default value: 0
   • vunit: Unit for the particle vertex. Default value: cm
   • randomVertexModel: Vertex randomization. Default: 'uniform'. Alternative: 'gaussian' (use deltas as sigmas), 'sphere'Default value: uniform


   Adds a particle to the event generator.
   The particle is generated with a fixed or randomized momentum, angles, and vertex.
   
   Examples:
   - 5 GeV electron along z:
   -gparticle="[{name: e-, p: 5000}]"
   
   - one electron and two protons, with the protons spread in theta:
   
   -gparticle="[{name: e-, p: 2300, theta: 23.0}, {name: proton, multiplicity: 2, p: 1200, theta: 14.0, delta_theta: 10}]"
```
