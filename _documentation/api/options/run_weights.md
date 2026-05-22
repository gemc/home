---
layout: default
title: 'GEMC option: run_weights'
---

# `run_weights`

Type: `option`

Description: File with run number and weights

Generated from:

```sh
gemc help run_weights
```

```text
-run_weights=<value> .......: File with run number and weights


   Text file with run number and their weights.
   
   The text file must have two columns: run# and weight. The weight represents the ratio of events desired for a run number.
   For example a "weights.txt" file that contains:
   
   11 0.1
   12 0.7
   13 0.2
   
   will simulate 10% of events with run number 11 conditions, 70% for run 12 and 20% for run 13.
```
