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

   • name: Particle name (mandatory), e.g. "proton" or "e-"Default value: NODFLT
   • multiplicity: How many copies of this particle will be generated in each eventDefault value: 1
   • p: Particle momentum with unit, e.g. "4*GeV" or "4000*MeV". Plain number falls back to MeV.Default value: NODFLT
   • delta_p: Particle momentum spread, centered on p (same unit convention as p).Default value: 0*MeV
   • randomMomentumModel: Momentum randomization. 'gaussian' uses deltas as sigmas.Default value: uniform
   • theta: Particle polar angle, e.g. "23*deg" or "0.4*rad". Plain number falls back to deg.Default value: 0*deg
   • delta_theta: Particle polar angle spread, centered on theta.Default value: 0*deg
   • randomThetaModel: Distribute cos(theta) or theta. 'cosine': cos(theta) is uniform. 'uniform': theta is uniform.Default value: uniform
   • phi: Particle azimuthal angle, e.g. "90*deg". Plain number falls back to deg.Default value: 0*deg
   • delta_phi: Particle azimuthal angle spread, centered on phi.Default value: 0*deg
   • vx: Particle vertex x component, e.g. "1*mm". Plain number falls back to cm.Default value: 0*cm
   • vy: Particle vertex y component.Default value: 0*cm
   • vz: Particle vertex z component.Default value: 0*cm
   • delta_vx: Particle vertex spread in x.Default value: 0*cm
   • delta_vy: Particle vertex spread in y.Default value: 0*cm
   • delta_vz: Particle vertex spread in z.Default value: 0*cm
   • randomVertexModel: Vertex randomization. 'uniform': flat. 'gaussian': deltas are sigmas. 'sphere': uniform in sphere.Default value: uniform


   Adds a particle to the event generator.
   Kinematic values accept an explicit Geant4 unit (e.g. '4*GeV', '23*deg', '1*mm').
   A plain number without a unit falls back to the field default: MeV for momentum,
   deg for angles, cm for vertex coordinates. A warning is logged in that case.
   Examples:
   - 5 GeV electron along z:
   -gparticle="[{name: e-, p: 5*GeV}]"
   - one electron and two protons spread in theta:
   -gparticle="[{name: e-, p: 2300*MeV, theta: 23*deg},
   {name: proton, multiplicity: 2, p: 1200*MeV, theta: 14*deg, delta_theta: 10*deg}]"
```
