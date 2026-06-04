---
layout: default
title: Flux
order: 31
description: Use the flux digitization for track-passage detectors
permalink: /documentation/sensitivity/flux/
---

# Flux

The `flux` digitization records track passage through a sensitive volume. It is useful for planes,
chambers, counters, and other detectors where each track crossing a detector element should create
one digitized hit.

```python
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
```

<br/>

## Hit grouping

`flux` groups steps by detector identity and Geant4 track id. All steps from the same track in the
same sensitive element are accumulated into one hit. Different tracks in the same element produce
separate hits.

<br/>

## Digitized variables

The output includes the user-defined identifiers plus:

| Variable | Meaning |
|----------|---------|
| `hitn` | Sequential hit number in the detector collection |
| `totEdep` | Total energy deposited by the track in the sensitive element |
| `time` | Average hit time |
| `pid` | %%pid%% |
| `tid` | Geant4 track id |
| `E` | Track total energy |

<br/>

## Notes

`flux` is event-level. ASCII and CSV output streamers write one file per thread.

By default, zero-energy steps are skipped. Enable `recordZeroEdep` only when you intentionally need
ordinary zero-energy steps in `flux` output.

Examples: [Simple flux](/home/examples/basic/simple_flux), [B2](/home/examples/basic/b2).
