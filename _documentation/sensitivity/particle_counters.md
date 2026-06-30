---
layout: default
title: Particle Counters
order: 34
description: Use particle_counter for pid counting
permalink: /documentation/sensitivity/particle_counters/
---

# Particle Counters

The `particle_counter` digitization records particle passage using %%pid%% as the secondary
discriminator. Unlike `flux`, it does not distinguish particles that have the same %%pid%% in the
same sensitive element.

```python
gvolume.digitization = "particle_counter"
gvolume.set_identifier("counter", 1)
```

<br/>

## Hit grouping

`particle_counter` groups steps by detector identity and %%pid%%. Steps from particles with the
same %%pid%% in the same sensitive element are accumulated together.

<br/>

## Digitized variables

The output includes the user-defined identifiers plus:

| Variable | Meaning |
|----------|---------|
| `hitn` | Sequential hit number in the detector collection |
| `totEdep` | Total energy deposited by the particle group |
| `time` | Average hit time |
| `pid` | %%pid%% |
| `tid` | Geant4 track id associated with the hit |
| `totalE` | Track total energy |

<br/>

## Notes

`particle_counter` is event-level. ASCII and CSV output streamers write one file per thread.

Use `flux` instead when track id, rather than %%pid%%, should distinguish hits in the same
sensitive element.
