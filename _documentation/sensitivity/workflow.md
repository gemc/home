---
layout: default
title: Digitization Workflow
order: 31
description: How GEMC turns Geant4 steps into digitized hits and Monte-Carlo truth
permalink: /documentation/sensitivity/workflow/
---

# Digitization Workflow

Every sensitive volume names a **digitization routine** through its `digitization` field. The routine is a
`GDynamicDigitization` object — one of the [built-in routines](/home/documentation/sensitivity) or a
[custom plugin](/home/documentation/sensitivity/gplugins) — that GEMC drives through a fixed lifecycle, from
the first Geant4 step in the volume all the way to the output file.

The diagram below shows the full path and the routine methods that run at each stage. Methods drawn in blue
are the ones you override in a plugin; gray boxes are GEMC core actions; green boxes are the data products.

{% include figure.html
src="assets/images/documentation/digitization_workflow.svg"
alt="GEMC digitization workflow: construction, begin of run, stepping, end of event, and output"
caption="The digitization lifecycle. Each sensitive volume's routine is configured once, primed at every run,
called for every step, and harvested at the end of each event."
%}

<br/>

## The pipeline at a glance

| Phase | When it runs | Routine methods |
|-------|--------------|-----------------|
| Construction  | Once per worker thread, while the geometry is built | `defineReadoutSpecs()` |
| Begin of run  | Each time the run number changes | `loadConstants()`, `loadTT()` |
| Stepping      | Every Geant4 step inside a sensitive volume | `decisionToSkipHit()`, `processTouchable()` |
| End of event  | Once per event, for every accumulated hit | `digitizeHit()`, `apply_thresholds()` / `apply_efficiency()`, `collectTrueInformation()` |
| Output        | Per event, or once at the end of the run | streamer publication, `normalize()` |

<br/>

## Construction — once per worker thread

While `GDetectorConstruction` builds the geometry, each named routine is instantiated once per worker
thread: the built-in routines directly, a custom routine by loading its `.gplugin` shared library. GEMC then
calls **`defineReadoutSpecs()`** on it.

`defineReadoutSpecs()` declares the electronics readout model: the integration `timeWindow`, the time-grid
origin, the `HitBitSet` that selects which hit information is computed, and the `maxStep` used inside the
volume. It is the one method every routine must implement.

<br/>

## Begin of run — when the run number changes

At the start of a run, and again whenever the run number changes, the `EventDispenser` primes each routine
for that run:

- **`loadConstants(run, variation)`** loads the run- and variation-dependent calibration constants (from
  CCDB, SQLite, or files). Default: a no-op.
- **`loadTT(run, variation)`** builds the translation table that maps a hit identity to its electronics
  address. Default: a no-op.

If the run number does not change between events, this phase is skipped — the constants and tables stay
loaded.

<br/>

## Stepping — every step in a sensitive volume

For each Geant4 step deposited in a sensitive volume, `GSensitiveDetector::ProcessHits` calls the routine:

1. **`decisionToSkipHit(edep)`** can drop the step early — by default a zero-energy step, unless
   `recordZeroEdep` is set — before any hit is created.
2. **`processTouchable()`** turns the stepping touchable into one or more **touchables**. The default returns
   the touchable unchanged (one hit per sensitive element); routines override it to split the energy across
   neighbours (charge sharing), re-bin by time cell, or otherwise reshape the readout.

Each resulting touchable is matched against the event's hit collection: a new touchable creates a `GHit`,
while a touchable that already has a hit accumulates the step into it with `addHitInfos()`. A `GHit`
therefore gathers **every step** a track takes through the same readout element across the whole event.

<br/>

## End of event — once per hit

At `GEventAction::EndOfEventAction`, each accumulated `GHit` is finalized. The routine produces up to two
records per hit:

- **`digitizeHit()`** → a `GDigitizedData` bank: the detector response (for example `adc`, `time`) produced
  by the routine's electronics model. This is the "measured" output. After it runs, GEMC applies the
  optional threshold and efficiency rejection (see below), which may **drop** the digitized bank.
- **`collectTrueInformation()`** → a `GTrueInfoData` bank: the Monte-Carlo truth for the hit, such as
  %%pid%%, %%tid%%, %%mtid%%, energy, and position (it also computes the hit averages, via
  `calculateInfos()`). With `-save_original_track`, it also carries the primary track's %%otid%%, %%opid%%,
  and momentum (%%opx%%, %%opy%%, %%opz%%).

Which banks are written is governed by the `HitBitSet` set in `defineReadoutSpecs()`.

### Threshold and efficiency rejection

The per-channel **threshold** and detector **efficiency** are applied on the digitized path, **after**
`digitizeHit()` has produced the bank, not during stepping. GEMC calls two routine hooks in turn:

- **`apply_thresholds()`** drops the hit when it is below the channel threshold.
- **`apply_efficiency()`** drops the hit when a uniform random draw exceeds the channel efficiency.

Each is a thin wrapper that returns *keep the hit* unless its system is enrolled, and otherwise delegates to
the plugin override — **`apply_thresholds_impl()`** / **`apply_efficiency_impl()`** — where the detector
computes the actual comparison. Both are **off by default** and enabled per system with the
`-applyThresholds` and `-applyInefficiencies` options (each a list of system names, or `all`), resolved once
at construction. The earlier stepping-level `decisionToSkipHit()` is a separate, simpler filter that only
discards zero-energy steps.

### Rejected hits and `also_reject_true_info`

When either hook rejects a hit, no `GDigitizedData` is written. By default the hit's `GTrueInfoData` is
dropped as well, so a rejected hit leaves no trace in the output. The **`-also_reject_true_info`** option
(default `true`) controls this: set `-also_reject_true_info=false` to keep the true information for **every**
Geant4 hit, even those with no digitized counterpart — useful when you need the Monte-Carlo truth regardless
of the electronics response.

<br/>

## Output — per event or end of run

The collection mode of the routine decides when its data leaves the worker:

- **Event mode** (`flux`, `particle_counter`, `gPhotonDetector`, most plugins) publishes the digitized and
  true-info banks at the end of each event to the per-thread streamers (ASCII, CSV, ROOT, JSON) — one file
  per worker thread.
- **Run mode** (`dosimeter`) accumulates across the whole run and, at the end, calls **`normalize()`** on the
  routine before writing a single integrated output file.

<br/>

## See also

- [Sensitivity overview](/home/documentation/sensitivity) — assigning a digitization to a volume.
- [Custom digitization plugins](/home/documentation/sensitivity/gplugins) — implementing each method above in
  your own `.gplugin`.
