---
layout: default
title: ROOT Output
order: 54
description: ROOT TTree output for HEP analysis workflows
permalink: /documentation/output/root/
---

# ROOT Output

The `root` format writes simulation data into [ROOT](https://root.cern.ch) `TTree` objects
stored in a single `TFile` per plugin instance. Trees are created lazily on the first hit
seen for each detector, so only detectors that actually fired appear in the output.

<br/>

## Configuration

```yaml
gstreamer:
  - format: root
    filename: myrun
```

Produces one `.root` file per worker thread:

```
myrun_t0.root   myrun_t1.root   myrun_t2.root   ...
```

Run-level outputs (such as `dosimeter`) produce a single file:

```
myrun.root
```

<br/>

## Tree layout

Each file contains the following trees:

| Tree name | Content |
|-----------|---------|
| `event_header` | One entry per event: event number, timestamp, thread id |
| `run_header` | One entry per run: run number |
| `<detector>_true_info` | One entry per hit: Geant4 true-information variables |
| `<detector>_digitized` | One entry per hit: digitized output variables and identifiers |
| `generated` | One entry per generated particle (all configured particles) |
| `generated_tracked` | One entry per particle propagated by Geant4 |

The `<detector>` prefix matches the name used in the Python geometry definition (e.g. `dc`,
`ctof`, `ft_cal`). Trees for detectors that produced no hits are not created.

<br/>

## Reading with ROOT

```cpp
TFile* f = TFile::Open("myrun_t0.root");
TTree* t = (TTree*)f->Get("dc_digitized");

Double_t doca;
Int_t    sector, layer, wire;
t->SetBranchAddress("doca",   &doca);
t->SetBranchAddress("sector", &sector);
t->SetBranchAddress("layer",  &layer);
t->SetBranchAddress("wire",   &wire);

for (Long64_t i = 0; i < t->GetEntries(); ++i) {
    t->GetEntry(i);
    printf("sector %d  layer %d  wire %d  doca %.4f\n", sector, layer, wire, doca);
}
```

<br/>

## Reading with uproot (Python)

```python
import uproot

with uproot.open("myrun_t0.root") as f:
    tree = f["dc_digitized"]
    df = tree.arrays(library="pd")
    print(df.head())
```

<br/>

## Merging thread files

Thread files can be merged with ROOT's `hadd` utility:

```sh
hadd myrun_merged.root myrun_t*.root
```

<br/>

## Notes

- ROOT thread safety is enabled at library load time; one instance per worker thread is the
  intended usage.
- The branch schema for each tree is fixed by the first hit seen for that detector. All
  subsequent hits must provide the same variables.
- The ROOT plugin requires ROOT to be present at GEMC build time. If ROOT is not found,
  the plugin is excluded from the build.
