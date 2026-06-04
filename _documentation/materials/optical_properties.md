---
layout: default
title: Optical Properties
order: 25
description: Create optical properties for mirrors and materials
---

# Optical Properties

Optical properties are attached to a `GMaterial` instance.
They enable Geant4 to simulate Cherenkov radiation, scintillation, Rayleigh scattering,
and photon boundary interactions (reflection, refraction, absorption).

Several energy-dependent quantities can be defined:

<br/>

## photonEnergy — [required]

`photonEnergy` is the energy axis for all other optical properties. It must be set whenever
any optical field is used:

```python
mat.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV"
```

Values are space-separated strings with Geant4 units (`*eV`, `*keV`, `*MeV`).
Values must be in **strictly increasing order** — Geant4 interpolates between them and
will produce undefined behaviour if the energy axis is unsorted.

To convert from photon wavelength to energy:

```
E (eV) = 1240 / λ (nm)
```

For example, 400 nm (blue) ≈ 3.1 eV; 700 nm (red) ≈ 1.77 eV.

<br/>

## Index of refraction

Set `indexOfRefraction` to enable Cherenkov radiation and optical photon refraction at boundaries.

```python
mat.photonEnergy      = "2.0*eV 3.0*eV 4.0*eV 5.0*eV"
mat.indexOfRefraction = "1.458 1.466 1.476 1.490"
```

Maps to the Geant4 property %%RINDEX%%.

See the [Cherenkov example](/home/examples/optical/cherenkov) for a complete setup using three gas
radiators with different refractive indices.

<br/>

## Optical materials in variations

When a detector uses geometry variations, declare every optical material that may be used by any
variation in every variation. This includes materials that are not assigned to a volume in the current
variation.

For example, the Cherenkov example has three radiator materials: %%lowIndexRadiator%%,
%%mediumIndexRadiator%%, and %%highIndexRadiator%%. Each variation publishes all three material
definitions, then assigns the radiator volume to the material selected by that variation.

This keeps the Geant4 optical material tables complete when the setup tab reloads geometry or changes
the selected variation before a run. It is especially important for Cherenkov tracking, where
%%G4Cerenkov%% uses the material optical-property tables during stepping.

<br/>

## Absorption length

`absorptionLength` controls how far optical photons travel before being absorbed.
Values carry length units (`*m`, `*cm`, `*mm`):

```python
mat.absorptionLength = "3*m 3*m 3*m 3*m"
```

Maps to the Geant4 property %%ABSLENGTH%%

<br/>

## Scintillation properties

Scintillators emit optical photons when charged particles deposit energy. Geant4 models two emission
time components: fast (prompt) and slow (delayed).

### Energy-dependent fields

| Field | Geant4 key                  | Description |
|-------|-----------------------------|-------------|
| `fastcomponent` | %%SCINTILLATIONCOMPONENT1%% | Relative emission spectrum of the fast component |
| `slowcomponent` | %%SCINTILLATIONCOMPONENT2%% | Relative emission spectrum of the slow component |

```python
mat.photonEnergy  = "2.0*eV 2.5*eV 3.0*eV 3.5*eV 4.0*eV"
mat.fastcomponent = "1.0 0.9 0.8 0.7 0.6"
mat.slowcomponent = "0.5 0.4 0.3 0.2 0.1"
```

Values are relative (not absolute); Geant4 normalises them internally.

### Scalar fields

| Field                | Geant4 key                     | Unit        | Description                                                                                                                     |
|----------------------|--------------------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------|
| `scintillationyield` | %%SCINTILLATIONYIELD%%         | photons/MeV | Mean light yield per deposited MeV                                                                                              |
| `resolutionscale`    | %%RESOLUTIONSCALE%%            | —           | Width of the photon-count distribution: values < 1 give sub-Poisson (Fano factor); values > 1 model impurity-broadened crystals |
| `fasttimeconstant`   | %%SCINTILLATIONTIMECONSTANT1%% | ns          | Decay time constant of the fast component                                                                                       |
| `slowtimeconstant`   | %%SCINTILLATIONTIMECONSTANT2%% | ns          | Decay time constant of the slow component                                                                                       |
| `yieldratio`         | %%SCINTILLATIONYIELD1%%        | —           | Fraction of total yield emitted by the fast component (0–1)                                                                     |
| `birksConstant`      | —                              | mm/MeV      | Birks quenching parameter (see note below)                                                                                      |

> [!NOTE]
> Scalar properties set to **0** are silently skipped — Geant4's `AddConstProperty` is not called.
> Use a small non-zero value if you intentionally want to set a property to zero.

> [!NOTE]
> `birksConstant` is applied via `G4Material::GetIonisation()->SetBirksConstant()`, not through
> the optical properties table. It quenches the scintillation yield for high-dE/dx particles
> (Birks' law).

<br/>

### Complete NaI-like scintillator

```python
scint = GMaterial("my_scintillator")
scint.density = 3.67
scint.addNAtoms("Na", 1)
scint.addNAtoms("I",  1)
scint.photonEnergy       = "2.0*eV 2.5*eV 3.0*eV 3.5*eV 4.0*eV"
scint.fastcomponent      = "1.0 0.9 0.8 0.7 0.6"
scint.slowcomponent      = "0.5 0.4 0.3 0.2 0.1"
scint.scintillationyield = 1000
scint.resolutionscale    = 1.0
scint.fasttimeconstant   = 6
scint.slowtimeconstant   = 88
scint.yieldratio         = 0.8
scint.birksConstant      = 0.00152
scint.publish(cfg)
```

<br/>

## Reflectivity and efficiency

These properties model the behaviour of optical photons at a **dielectric–metal boundary**
(e.g. a mirror or a PMT photocathode). At such a boundary there is no refraction; the photon is
either reflected or absorbed with `efficiency`.

| Field          | Geant4 key     | Description                                                                                           |
|----------------|----------------|-------------------------------------------------------------------------------------------------------|
| `reflectivity` | %%REFLECTIVITY%% | Fraction of photons reflected                                                                         |
| `efficiency`   | %%EFFICIENCY%%   | Absorption probability for photons that are not reflected; models quantum efficiency for photosensors |

```python
mat.reflectivity = "0.85 0.87 0.90 0.88 0.85"
mat.efficiency   = "0.20 0.22 0.25 0.23 0.20"
```

These properties are most useful when the material is assigned to an optical surface
(`G4OpticalSurface`) defined in the geometry. For bulk material, `absorptionLength` is more
appropriate.

<br/>

## Rayleigh scattering

`rayleigh` defines the Rayleigh scattering attenuation length as a function of photon energy.
Values carry length units:

```python
mat.rayleigh = "50*cm 45*cm 40*cm 35*cm 30*cm"
```

Maps to the Geant4 property %%RAYLEIGH%%

<br/>


## Physics list requirement

Optical photon tracking requires an optical physics constructor. Add `G4OpticalPhysics` to the
physics list in the YAML file:

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

{% include notes/physics-list-note.md %}

<br/>

## Simulation

{% include figure.html
src="assets/images/examples/materials/geometry.png"
alt="Gemc simulation showing scintillation and Cherenkov radiation"
caption="Gemc simulation of the five-tube materials example with G4OpticalPhysics enabled. Proton tracks (straight lines) traverse all five tubes along the z-axis. The fourth tube (NaI-like scintillator) emits an isotropic fan of optical photons through scintillation when the proton deposits energy. The fifth tube (SiO₂ glass with index of refraction ≈ 1.46–1.49) produces the characteristic narrow Cherenkov cone, whose opening angle depends on the particle velocity relative to the phase velocity of light in the medium."
%}

<br/>

## Working examples

- [Materials example](/home/examples/basic/materials) — scintillation and index-of-refraction definitions side by side
- [Cherenkov example](/home/examples/optical/cherenkov) — full optical simulation with three gas radiators
