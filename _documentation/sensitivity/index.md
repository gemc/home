---
layout: default
title: Sensitivity
order: 30
description: Assign detector sensitivity and choose a built-in digitization
permalink: /documentation/sensitivity/
---

# Sensitivity

In GEMC, a volume becomes sensitive when its `digitization` field is set. The value is the name
of the digitization routine that will receive Geant4 steps from that volume and turn them into
digitized output.

```python
gvolume.digitization = "flux"
gvolume.set_identifier("sector", 1)
gvolume.set_identifier("layer", 2)
```

The identifier fields define the detector element address written to output. Use enough identifiers
to distinguish the sensitive elements you want to analyze, such as sector, layer, paddle, or channel.

For the full lifecycle of a routine — what each method does and when it runs — see the
[Digitization Workflow](/home/documentation/sensitivity/workflow).

<br/>

## Built-in digitizations

| Digitization | Collection | Main use |
|--------------|------------|----------|
| [`flux`](/home/documentation/sensitivity/flux) | event | Track passage and hit-level observables |
| [`dosimeter`](/home/documentation/sensitivity/dosimeter) | run | Integrated deposited energy and dose |
| [`particle_counter`](/home/documentation/sensitivity/particle_counters) | event | Per-%%pid%% counting |
| [`gPhotonDetector`](/home/documentation/sensitivity/photon_detectors) | event | Optical-photon detectors |
| [Custom plugin](/home/documentation/sensitivity/gplugins) | any | User-defined electronics model via `.gplugin` |

<br/>

## Output behavior

Event-level digitizations write one output file per thread for ASCII and CSV streamers. Run-level
digitizations write one integrated output file.

The `recordZeroEdep` option controls whether ordinary zero-energy steps are recorded. Optical photons
usually deposit zero energy in detector volumes; `gPhotonDetector` handles this case directly and does
not require `recordZeroEdep`.

<br/>

## Choosing a sensitivity

Use `flux` when you want one hit per track in each sensitive element.

Use `dosimeter` when the detector should accumulate energy deposition and dose across the run.

Use `particle_counter` when hits in the same sensitive element should be grouped by %%pid%% rather than by track id.

Use `gPhotonDetector` for Cherenkov and other optical examples where only optical photons should be
recorded.

Write a [custom plugin](/home/documentation/sensitivity/gplugins) when you need a detector-specific
electronics model such as time-to-distance conversion, charge sharing, TDC jitter, or calibration
corrections loaded from a database.
