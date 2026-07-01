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

<br/>

## Digitization hooks

A digitization routine is a set of overridable **hooks** that GEMC calls across the hit lifecycle: it is
configured once, primed when the run number changes, called for every Geant4 step, and harvested at the end
of each event — where `digitizeHit` builds the measured bank, the optional `apply_thresholds` /
`apply_efficiency` hooks reject hits, and `collectTrueInformation` writes the Monte-Carlo truth. Run-mode
routines add a final `normalize`.

{% include figure.html
src="assets/images/documentation/digitization_hooks.svg"
alt="GEMC digitization plugin hooks grouped by lifecycle phase"
caption="The digitization hooks, grouped by lifecycle phase. The amber apply_thresholds / apply_efficiency
hooks reject a digitized hit and are off by default."
%}

See the [Digitization Workflow](/home/documentation/sensitivity/workflow) for when each hook runs and how
the data flows, and [Custom digitization plugins](/home/documentation/sensitivity/gplugins) for
implementing them in a `.gplugin`.

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
