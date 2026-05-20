---
layout: default
title: Materials
order: 20
description: Create materials
---

# Materials

GEMC supports four ways to assign a material to a volume: referencing a Geant4 built-in,
referencing a GEMC pre-built special material, composing by atom count, or composing by
fractional mass. Optical properties can be attached to any custom material.

All custom materials are created with the `GMaterial` class.

```python
from gmaterial import GMaterial
```

<br/>

## Geant4 built-in materials

The [Geant4 NIST Material Database](https://geant4.web.cern.ch/documentation/dev/bfad_html/ForApplicationDevelopers/Appendix/materialNames.html)
provides several pre-defined materials. Assign the name directly to `gvolume` — no
`GMaterial` object is needed:

```python
gvolume.material = "G4_C"        # graphite
gvolume.material = "G4_AIR"
gvolume.material = "G4_WATER"
gvolume.material = "G4_lH2"      # liquid hydrogen
gvolume.material = "G4_Pb"
gvolume.material = "G4_Cu"
gvolume.material = "G4_Si"
gvolume.material = "G4_PLASTIC_SC_VINYLTOLUENE"
```

<br/>

## GEMC pre-built special materials

GEMC defines a small set of isotopically pure materials that are not in the NIST database.
These are built automatically at startup and can be used like any Geant4 material:

| Name | Formula | Density (g/cm³) | Temperature | Notes |
|------|---------|-----------------|-------------|-------|
| `HydrogenGas` | H | 0.00275 | 50 K | Pure protium gas |
| `DeuteriumGas` | D₂ | 0.000452 | 294 K | Deuterium gas at room temperature |
| `LD2` | D₂ | 0.169 | 22 K | Liquid deuterium |
| `ND3` | ND₃ | 1.007 | 1 K | Frozen ammonia (deuterated) |
| `Helium3Gas` | ³He | 1.65×10⁻⁴ | 294 K | Helium-3 gas at room temperature |
| `H3Gas` | T₂ | 0.0034 | 40 K | Tritium gas |

```python
gvolume.material = "LD2"         # liquid deuterium target
gvolume.material = "Helium3Gas"  # He-3 detector
gvolume.material = "ND3"         # polarized ammonia target
```

<br/>

## Custom materials

All custom materials share these mandatory fields:

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Unique name used in `gvolume.material` |
| `density` | float | Density in g/cm³ |
| composition | set by method | Set via `addNAtoms` or `addMaterialWithFractionalMass` |

The optional `description` field is for documentation only.
The two composition methods are mutually exclusive: using both on the same instance exits with an error.

<br/>

### By molecular composition

Use `addNAtoms(element, n)` to build a material from chemical elements. Element symbols must match
Geant4 NIST element names (single capital letter or capital + lowercase: `"H"`, `"He"`, `"Na"`, `"Pb"`).
The total atom count across all calls must be greater than 1.

```python
water = GMaterial("custom_water")
water.description = "Water (H2O)"
water.density = 1.0
water.addNAtoms("H", 2)
water.addNAtoms("O", 1)
water.publish(cfg)
```

```python
quartz = GMaterial("SiO2")
quartz.density = 2.65
quartz.addNAtoms("Si", 1)
quartz.addNAtoms("O",  2)
quartz.publish(cfg)
```

```python
nai = GMaterial("NaI_crystal")
nai.density = 3.67
nai.addNAtoms("Na", 1)
nai.addNAtoms("I",  1)
nai.publish(cfg)
```

<br/>

### By fractional mass

Use `addMaterialWithFractionalMass(material, fraction)` to blend existing materials by weight.
The fractions must sum to exactly 1.0 (checked at publish time with a relative tolerance of 1×10⁻⁶).

```python
mixture = GMaterial("air_water_mixture")
mixture.description = "80% air / 20% water by mass"
mixture.density = 0.9601
mixture.addMaterialWithFractionalMass("G4_AIR",   0.80)
mixture.addMaterialWithFractionalMass("G4_WATER", 0.20)
mixture.publish(cfg)
```

Component names may be Geant4 built-ins (`G4_*`), GEMC pre-built specials, or the names of custom
materials that have already been published.

```python
# mix a custom material with a Geant4 built-in
scint_mix = GMaterial("plastic_scintillator")
scint_mix.density = 1.032
scint_mix.addMaterialWithFractionalMass("G4_POLYSTYRENE", 0.975)
scint_mix.addMaterialWithFractionalMass("G4_NAPHTHALENE", 0.025)
scint_mix.publish(cfg)
```

<br/>

## Validation

`publish(cfg)` calls `check_validity()` before writing, which will exit with an error if:

- `density` was not set
- no composition method was called
- `addNAtoms` total atom count is ≤ 1
- `addMaterialWithFractionalMass` fractions do not sum to 1.0

<br/>

## Working example

The [Materials example](/home/examples/basic/materials) exercises definition methods and applies optical properties
in a single geometry: five tubes along the z-axis, each using a different material type.

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/materials/material.vtksz"
  title="Interactive VTK.js view of the materials example geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

{% include figure.html
src="assets/images/examples/materials/geometry.png"
alt="Five tubes, each using a different material definition"
caption="Five tubes along the z-axis, each using a different material definition. From left to right: graphite (G4_C Geant4 built-in, red), water composed by atom count (H₂O, green), an 80/20 air–water mixture by fractional mass (blue), a NaI-like scintillator with optical properties (indigo), and SiO₂ glass with an index of refraction enabling Cherenkov radiation (salmon)."
%}
