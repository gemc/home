---
layout: default
title: Dosimeter
order: 32
description: Use the dosimeter digitization for integrated dose
permalink: /documentation/sensitivity/dosimeter/
---

# Dosimeter

The `dosimeter` digitization accumulates deposited energy and dose for a sensitive volume. It is
intended for detector regions where the run-integrated response matters more than individual tracks.

```python
gvolume.digitization = "dosimeter"
gvolume.set_identifier("mydosimeter", 1)
```

<br/>

## Hit grouping

`dosimeter` groups by detector identity only. Once the identifiers match, contributions are accumulated
for the same sensitive element.

<br/>

## Digitized variables

The output includes the user-defined identifiers plus:

| Variable | Meaning |
|----------|---------|
| `etot` | Total deposited energy in MeV |
| `dose` | Dose in picogray |

The dose is computed from the deposited energy and the mass of the sensitive volume:

$$
\mathrm{dose} = \frac{\mathrm{etot}}{\mathrm{mass}}
$$

<br/>

## Notes

`dosimeter` is run-level. Output streamers write an integrated result for the run rather than one
event-level hit bank per thread.

Example: [B1](/home/examples/basic/b1).
