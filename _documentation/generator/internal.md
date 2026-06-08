---
layout: default
title: Internal Generator Options
order: 31
description: GEMC gparticle and gparticlefile generator options
---

# Internal Generator

The internal GEMC generator is configured with two cumulative options.

%%gparticle%% defines inline particle sources. Each entry adds one particle (or a group of
identical copies) to every event. Multiple entries can be combined in the same list.

%%gparticlefile%% loads event records from a file. The built-in reader supports the
[LUND format](lund_format).

When both options are present, every generated event receives all particles from %%gparticle%%
**plus** all particles from the matching event record in each %%gparticlefile%% source.

Both options can be set from the YAML steering card or the command line:

```yaml
# YAML steering card
gparticle:
  - name: e-
    p: 2300*MeV
    theta: 23*deg
```

```shell
# equivalent command-line form
gemc -gparticle="[{name: e-, p: 2300*MeV, theta: 23*deg}]"
```

<br/>

## %%gparticle%%

### Unit convention

All kinematic values accept an explicit Geant4 unit attached with `*`, for example
`4*GeV`, `23*deg`, `0.4*rad`, `-10*cm`, `1.5*mm`. This is the recommended form.

If a plain number without a unit is given, GEMC falls back to the field default and
logs a warning:

| Field group | Default unit |
|-------------|-------------|
| Momentum (`p`, `delta_p`) | `MeV` |
| Angles (`theta`, `delta_theta`, `phi`, `delta_phi`) | `deg` |
| Vertex (`vx`, `vy`, `vz`, `delta_vx`, `delta_vy`, `delta_vz`) | `cm` |

### Fields

%%name%% and %%p%% are required. All other fields are optional.

| Field | Default | Description |
|-------|---------|-------------|
| %%name%% | required | Geant4 particle name, e.g. %%e-%%, %%proton%%, %%gamma%%, %%pi+%% |
| %%p%% | required | Nominal momentum magnitude with unit, e.g. `4*GeV` or `4000*MeV` |
| %%multiplicity%% | %%1%% | Number of copies generated per event; each copy is independently randomized |
| %%delta_p%% | %%0*MeV%% | Momentum spread around %%p%% |
| %%randomMomentumModel%% | %%uniform%% | %%uniform%%: flat in %%[p - delta_p, p + delta_p]%%; %%gaussian%%: Gaussian with sigma %%delta_p%% |
| %%theta%% | %%0*deg%% | Nominal polar angle (from the z-axis), e.g. `23*deg` or `0.4*rad` |
| %%delta_theta%% | %%0*deg%% | Polar-angle spread around %%theta%% |
| %%randomThetaModel%% | %%uniform%% | %%uniform%%: flat in %%[theta - delta_theta, theta + delta_theta]%%; %%gaussian%%: Gaussian sigma %%delta_theta%%; %%cosine%%: cos(theta) uniform, with rejection sampling within the window (see note below) |
| %%phi%% | %%0*deg%% | Nominal azimuthal angle |
| %%delta_phi%% | %%0*deg%% | Azimuthal-angle spread. **Always applied with the uniform model**; there is no %%randomPhiModel%% |
| %%vx%% | %%0*cm%% | Nominal vertex x |
| %%vy%% | %%0*cm%% | Nominal vertex y |
| %%vz%% | %%0*cm%% | Nominal vertex z |
| %%delta_vx%% | %%0*cm%% | Vertex x spread |
| %%delta_vy%% | %%0*cm%% | Vertex y spread |
| %%delta_vz%% | %%0*cm%% | Vertex z spread |
| %%randomVertexModel%% | %%uniform%% | %%uniform%%: each component flat in %%[v - delta_v, v + delta_v]%%; %%gaussian%%: Gaussian sigma per component; %%sphere%%: uniform sampling within a spherical volume (see note below) |

> [!NOTE]
> **cosine theta model**: samples theta such that cos(theta) is uniform using rejection sampling
> within %%[theta - delta_theta, theta + delta_theta]%%. For narrow windows the acceptance rate
> can be low. This model is most efficient when %%delta_theta%% covers a large fraction of
> the full range %%[0, 180 deg]%%.

> [!NOTE]
> **sphere vertex model**: generates vertices uniformly within a spherical volume centered on
> the nominal vertex. Set %%delta_vx%%, %%delta_vy%%, and %%delta_vz%% all equal to the desired sphere
> radius. Using different values for the three components changes the effective sampling sphere
> size.

<br/>

### Examples

**One 2.3 GeV electron at 23°**

```yaml
gparticle:
  - name: e-
    p: 2.3*GeV
    theta: 23*deg
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex01_theta_basic.png"
alt="theta distribution for one electron at 23 degrees"
caption="Polar angle (θ) of the generated-tracked bank in radians. The spike at θ ≈ 0.4 rad (≈ 23°) confirms a fixed-angle source."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv theta --kind csv --bins 50 --linear-y
```

<br/>

**Theta spread of 0.2 rad**

```yaml
gparticle:
  - name: e-
    p: 2.3*GeV
    theta: 0.4*rad
    delta_theta: 0.2*rad
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex02_theta_rad_spread.png"
alt="theta distribution for radian spread example"
caption="Flat θ distribution in the window [0.2, 0.6] rad produced by uniform smearing with delta_theta = 0.2 rad."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv theta --kind csv --bins 50 --linear-y
```

<br/>

**10 protons per event, uniform in φ**

```yaml
gparticle:
  - name: proton
    multiplicity: 10
    p: 1200*MeV
    theta: 14*deg
    delta_phi: 180*deg
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex03_phi_uniform.png"
alt="phi distribution for ten protons with uniform phi"
caption="Flat φ distribution across the full 2π range. phi is always smeared uniformly; no model option is needed."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv phi --kind csv --bins 50 --linear-y
```

<br/>

**Momentum spread — uniform**

```yaml
gparticle:
  - name: e-
    p: 2300*MeV
    delta_p: 100*MeV
    randomMomentumModel: uniform
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex04_p_uniform.png"
alt="momentum distribution for uniform smearing"
caption="Flat momentum distribution in [2200, 2400] MeV produced by uniform smearing with delta_p = 100 MeV."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv p --kind csv --bins 50 --linear-y
```

<br/>

**Momentum spread — Gaussian**

```yaml
gparticle:
  - name: e-
    p: 2300*MeV
    delta_p: 100*MeV
    randomMomentumModel: gaussian
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex05_p_gaussian.png"
alt="momentum distribution for Gaussian smearing"
caption="Gaussian momentum distribution centred at 2300 MeV with sigma = 100 MeV."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv p --kind csv --bins 50 --linear-y
```

<br/>

**Cosine theta sampling**

```yaml
gparticle:
  - name: e-
    p: 2300*MeV
    theta: 23*deg
    delta_theta: 5*deg
    randomThetaModel: cosine
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex06_theta_cosine.png"
alt="theta distribution for cosine theta sampling"
caption="cos(θ)-uniform sampling within [18°, 28°]. The rising density toward larger θ is the sin(θ) weighting that makes solid angle uniform."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv theta --kind csv --bins 50 --linear-y
```

<br/>

**Azimuthal-angle spread**

```yaml
gparticle:
  - name: e-
    p: 2300*MeV
    phi: 45*deg
    delta_phi: 20*deg
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex07_phi_spread.png"
alt="phi distribution for azimuthal angle smearing"
caption="Flat φ distribution in [25°, 65°] (≈ [0.44, 1.13] rad). phi is always spread uniformly."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv phi --kind csv --bins 50 --linear-y
```

<br/>

**Fixed vertex position**

```yaml
gparticle:
  - name: e-
    p: 2300*MeV
    vx: 0*cm
    vy: 0*cm
    vz: -10*cm
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex08_vz_fixed.png"
alt="vertex-z distribution for a fixed source vertex"
caption="All events originate at vz = −100 mm (−10 cm). GEMC stores vertex positions in mm internally."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv vz --kind csv --bins 50 --linear-y
```

<br/>

**Vertex z spread — uniform**

```yaml
gparticle:
  - name: e-
    p: 2300*MeV
    vz: 0*cm
    delta_vz: 2*cm
    randomVertexModel: uniform
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex09_vz_uniform.png"
alt="vertex-z distribution for uniform z-vertex smearing"
caption="Flat vz distribution in [−20, +20] mm (±2 cm) produced by uniform vertex smearing."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv vz --kind csv --bins 50 --linear-y
```

<br/>

**Vertex spread — Gaussian**

```yaml
gparticle:
  - name: e-
    p: 2300*MeV
    delta_vx: 1*mm
    delta_vy: 1*mm
    delta_vz: 5*mm
    randomVertexModel: gaussian
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex10_vz_gaussian.png"
alt="vertex-z distribution for Gaussian vertex smearing"
caption="Gaussian vz distribution with sigma = 5 mm centred at z = 0."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv vz --kind csv --bins 50 --linear-y
```

<br/>

**Multiple particle definitions**

Each entry is an independent source; all contribute to every event.
Here one electron (fixed angle) and two protons (smeared angle) are generated per event:

```yaml
gparticle:
  - name: e-
    p: 2300*MeV
    theta: 23*deg
  - name: proton
    multiplicity: 2
    p: 1200*MeV
    theta: 14*deg
    delta_theta: 10*deg
```

{% include figure.html
src="assets/images/documentation/generatorDocs/internal/ex11_theta_combined.png"
alt="theta distribution for combined electron and proton sources"
caption="Two populations: a spike at θ ≈ 0.4 rad (one electron at 23°) and a broad flat band from two protons smeared around 14°."
width="70%"
%}

Analyzer command:

```shell
gemc-analyzer generated_tracked.csv theta --kind csv --bins 50 --linear-y
```

<br/>

## `gparticlefile`

`gparticlefile` loads particle definitions from a file. Each entry specifies a format
and a filename:

| Field | Description |
|-------|-------------|
| `format` | File format reader name. The built-in reader is `lund` (case-insensitive). |
| `filename` | Path to the input file containing event records. |

```yaml
gparticlefile:
  - format: lund
    filename: events.lund
```

Event records are matched by index: file event 0 is used for GEMC event 0, file event 1 for
GEMC event 1, and so on. In multi-threaded mode Geant4 distributes event IDs to worker threads;
each file event is still assigned to exactly one GEMC event.

Multiple sources can be combined — events from all files are merged by index:

```yaml
gparticlefile:
  - format: lund
    filename: beam_background.lund
  - format: lund
    filename: signal.lund
```

See the [LUND format documentation](lund_format) for the file structure, column definitions, and unit conventions.
