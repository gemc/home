---
layout: default
title: Photon Detectors
order: 34
description: Use gPhotonDetector for optical-photon sensitivity
permalink: /documentation/sensitivity/photon_detectors/
---

# Photon Detectors

The `gPhotonDetector` digitization is a flux-like detector for optical photons. It records only
Geant4 optical photons and is the recommended sensitivity for Cherenkov photon collection surfaces.

```python
gvolume.digitization = "gPhotonDetector"
gvolume.set_identifier("detector", 1)
```

<br/>

## Hit grouping

`gPhotonDetector` groups optical-photon steps by detector identity and Geant4 track id, matching the
track-based grouping used by `flux`.

Non-optical particles are skipped.

<br/>

## Digitized variables

The output includes the user-defined identifiers plus the same variables as `flux`:

| Variable | Meaning |
|----------|---------|
| `hitn` | Sequential hit number in the detector collection |
| `totEdep` | Total energy deposited by the optical photon, usually zero |
| `time` | Average hit time |
| `pid` | %%pid%%; optical photons are written as `-22` |
| `tid` | Geant4 track id |
| `E` | Optical-photon total energy |

<br/>

## Notes

`gPhotonDetector` is event-level. ASCII and CSV output streamers write one file per thread.

Optical photons usually deposit zero energy. `gPhotonDetector` records them even when `totEdep` is
zero, so `recordZeroEdep` is not required.

Examples: [Cherenkov](/home/examples/optical/cherenkov).
