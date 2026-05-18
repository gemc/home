---
layout: default
title: Internal Generator Options
order: 31
description: GEMC gparticle and gparticlefile generator options
---

The internal GEMC generator is configured with the cumulative `gparticle` option.
Each `gparticle` entry defines one particle source that contributes to every event.
Multiple entries can be supplied in the same list.

File-backed event generators are configured with the cumulative `gparticlefile` option.
Each `gparticlefile` entry loads event records from a file format reader, for example the
built-in LUND reader.

If both options are present, every generated event receives:

1. all particles from `gparticle`;
2. all particles from the matching event record in each `gparticlefile` source.

## `gparticle`

The `gparticle` option is a list of particle definitions:

```bash
gemc -gparticle="[{name: e-, p: 2300, theta: 23.0}]"
```

The minimal required fields are:

| Field | Meaning |
| --- | --- |
| `name` | Geant4 particle name, for example `e-`, `proton`, `gamma`, `pi+`. |
| `p` | Nominal momentum. The value is interpreted with `punit`. |

All available fields are:

| Field | Default | Meaning |
| --- | --- | --- |
| `name` | required | Geant4 particle name. |
| `multiplicity` | `1` | Number of copies generated for this particle entry in each event. |
| `p` | required | Nominal momentum. |
| `delta_p` | `0` | Momentum spread around `p`. |
| `punit` | `MeV` | Unit for `p` and `delta_p`, for example `MeV` or `GeV`. |
| `randomMomentumModel` | `uniform` | Momentum smearing model. Use `uniform` for a flat range or `gaussian` to interpret `delta_p` as sigma. |
| `theta` | `0` | Nominal polar angle. |
| `delta_theta` | `0` | Polar-angle spread around `theta`. |
| `randomThetaModel` | `uniform` | Polar-angle smearing model. Use `uniform`, `gaussian`, or `cosine` to sample uniformly in cos(theta). |
| `phi` | `0` | Nominal azimuthal angle. |
| `delta_phi` | `0` | Azimuthal-angle spread around `phi`. |
| `aunit` | `deg` | Unit for angles, for example `deg` or `rad`. |
| `vx` | `0` | Nominal vertex x position. |
| `vy` | `0` | Nominal vertex y position. |
| `vz` | `0` | Nominal vertex z position. |
| `delta_vx` | `0` | Vertex x spread around `vx`. |
| `delta_vy` | `0` | Vertex y spread around `vy`. |
| `delta_vz` | `0` | Vertex z spread around `vz`. |
| `vunit` | `cm` | Unit for vertex positions and spreads. |
| `randomVertexModel` | `uniform` | Vertex smearing model. Use `uniform`, `gaussian`, or `sphere`. |

### Examples

Generate one 2.3 GeV electron at 23 degrees in every event:

```bash
gemc -gparticle="[{name: e-, p: 2300, theta: 23.0}]"
```

Use explicit units:

```bash
gemc -gparticle="[{name: e-, p: 2.3, punit: GeV, theta: 0.4, aunit: rad}]"
```

Generate three identical protons in every event:

```bash
gemc -gparticle="[{name: proton, multiplicity: 3, p: 1200, theta: 14.0}]"
```

Smear the momentum uniformly by plus or minus 100 MeV:

```bash
gemc -gparticle="[{name: e-, p: 2300, delta_p: 100, randomMomentumModel: uniform}]"
```

Smear the momentum with a Gaussian sigma of 100 MeV:

```bash
gemc -gparticle="[{name: e-, p: 2300, delta_p: 100, randomMomentumModel: gaussian}]"
```

Smear the polar angle uniformly by plus or minus 5 degrees:

```bash
gemc -gparticle="[{name: e-, p: 2300, theta: 23.0, delta_theta: 5.0}]"
```

Sample the polar angle uniformly in cos(theta):

```bash
gemc -gparticle="[{name: e-, p: 2300, theta: 23.0, delta_theta: 5.0, randomThetaModel: cosine}]"
```

Smear the azimuthal angle by plus or minus 20 degrees:

```bash
gemc -gparticle="[{name: e-, p: 2300, phi: 45.0, delta_phi: 20.0}]"
```

Place the source at a fixed vertex:

```bash
gemc -gparticle="[{name: e-, p: 2300, vx: 0.0, vy: 0.0, vz: -10.0, vunit: cm}]"
```

Smear only the z vertex by plus or minus 2 cm:

```bash
gemc -gparticle="[{name: e-, p: 2300, vz: 0.0, delta_vz: 2.0, vunit: cm, randomVertexModel: uniform}]"
```

Smear the vertex with Gaussian sigmas of 1 mm in x and y, and 5 mm in z:

```bash
gemc -gparticle="[{name: e-, p: 2300, delta_vx: 1.0, delta_vy: 1.0, delta_vz: 5.0, vunit: mm, randomVertexModel: gaussian}]"
```

Combine multiple particle definitions:

```bash
gemc -gparticle="[
  {name: e-, p: 2300, theta: 23.0},
  {name: proton, multiplicity: 2, p: 1200, theta: 14.0, delta_theta: 10.0}
]"
```

## `gparticlefile`

The `gparticlefile` option is a list of file sources. Each item has two fields:

| Field | Meaning |
| --- | --- |
| `format` | File format reader name. The built-in reader is `lund`. The value is case-insensitive, so `lund`, `Lund`, and `LUND` are equivalent. |
| `filename` | Input file containing event particle definitions. |

Example:

```bash
gemc -gparticlefile="[{format: lund, filename: events.lund}]"
```

Combine inline particles with a LUND file. The electron is generated in every event, and
the matching event record from `events.lund` is added to that same GEMC event:

```bash
gemc \
  -gparticle="[{name: e-, p: 2300, theta: 23.0}]" \
  -gparticlefile="[{format: LUND, filename: events.lund}]"
```

Use more than one file source:

```bash
gemc -gparticlefile="[
  {format: lund, filename: beam_background.lund},
  {format: lund, filename: signal.lund}
]"
```

For multiple file sources, event records are merged by event index: event 0 from every
source contributes to GEMC event 0, event 1 from every source contributes to GEMC event 1,
and so on.

## Adding Another File Format

GEMC uses a particle-reader factory for file-backed generator formats.

The built-in `lund` reader is registered statically. Additional formats can be provided by
dynamic plugins named:

```text
gparticle_<format>_plugin.gplugin
```

The plugin must export:

```text
GParticleReaderFactory
```

For example, a format named `hepmc` would be loaded from:

```text
gparticle_hepmc_plugin.gplugin
```

and used as:

```bash
gemc -gparticlefile="[{format: hepmc, filename: events.hepmc}]"
```
