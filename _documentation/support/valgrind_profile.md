---
layout: default
title: Profiling
order: 110
description: Valgrind callgrind profiling — per-category and per-routine cycle metrics, and how to read them.
permalink: /documentation/support/valgrind_profile/
---

# Profiling

The **Valgrind Profile** workflow runs representative examples under Valgrind's
[`callgrind`](https://valgrind.org/docs/manual/cl-manual.html) tool and publishes a per-category and a
per-routine cost table, plus the raw profiles for interactive exploration. It is a scheduled (weekly) and
manually dispatchable workflow, not a per-push check, because `callgrind` is roughly 50× slower than a native
run.

Each job profiles one workload single-threaded, from freshly generated geometry, with:

```shell
valgrind --tool=callgrind --cache-sim=yes --branch-sim=yes \
         --dump-instr=yes --collect-jumps=yes gemc <card> -n <events> -nthreads 1
```

Cache and branch simulation are enabled so the cost can be reported as **CEst** (cycle estimation), the same
derived metric `qcachegrind` shows:

```text
CEst = Ir + 10 × (L1 misses) + 100 × (last-level misses)
```

where `Ir` is instruction reads. CEst is a deterministic CPU-cost proxy, not wall-clock time.

<br/>

## What the summary reports

Every job writes two tables into its run summary.

**Time per category (inclusive).** The inclusive cost of each category's entry function — its own cost plus
everything it calls. Digitization, streaming-readout, and field categories are *discovered* from the profile
(every `::digitizeHit`, `::stream_hit`, and field `GetFieldValue`), so a detector or plugin added elsewhere
appears on its own row automatically.

| Category | Entry symbol(s) | CEst (Mcycles) | % of run |
|----------|-----------------|---------------:|---------:|
| Track swimming (field propagation) | `G4PropagatorInField::ComputeStep` | … | … |
| Hit collection (sensitive detector) | `GSensitiveDetector::ProcessHits` | … | … |
| Digitization: … | `…::digitizeHit` | … | … |
| Output writing | `GStreamer::publishEventData` | … | … |

Categories use *inclusive* cost and can overlap or nest (field evaluation is part of track swimming), so the
percentages are not meant to add up to 100%.

**Top 10 routines by self time.** The hottest individual routines ranked by *self* cost — the time the CPU
spends directly in each routine, excluding its callees. This is the classic hotspot view.

| # | Routine | CEst (Mcycles) | % of run |
|---|---------|---------------:|---------:|
| 1 | `…` | … | … |

<br/>

## Reading a profile with qcachegrind

The raw `callgrind.out.<name>` files are attached to each run as artifacts and are best explored
interactively with **qcachegrind** (Qt) or **kcachegrind** (KDE). The profiles are dumped with
`--dump-instr=yes` and `--collect-jumps=yes`, so per-source-line and per-instruction annotation and the
jump/branch arrows are available.

1. **Install a viewer.** macOS: `brew install qcachegrind` (`brew install graphviz` enables call graphs).
   Debian/Ubuntu: `apt-get install kcachegrind graphviz`. Fedora/AlmaLinux: `dnf install kcachegrind graphviz`.
2. **Download and unzip** the artifact and open it: `qcachegrind callgrind.out.<name>` (or File → Open).
3. **Pick the cost type** in the toolbar dropdown. Because the runs enable cache and branch simulation,
   **`CEst`** is available and matches the tables above; `Ir` is the simpler default. Each row shows `Incl.`
   (self + callees) and `Self` costs; toggle `%` (Relative) and `Cycle Detection` as needed.
4. **Find hotspots** in the left **Flat Profile**: sort by `Self` for the routines doing the work, or by
   `Incl.` for whole call subtrees (a detector's digitization, field swimming, hit collection).
5. **Split by detector or library** with **Grouping → Source File / Class / ELF Object**: each detector's
   digitization class, and the GEMC, Geant4, and CLHEP costs, aggregate into their own rows.
6. **Drill into source** with the **Source** and **Machine Code** tabs for per-line cost, and use the
   **Callers** / **Callees** / **Call Graph** (needs graphviz) panels to follow the call structure.

For a non-interactive summary without a GUI, `callgrind_annotate callgrind.out.<name>` prints the top
functions and, with `--auto=yes`, annotated source.
