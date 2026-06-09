---
layout: default
title: CSV Output
order: 52
description: Comma-separated output suitable for pandas, numpy, and spreadsheet tools
permalink: /documentation/output/csv/
---

# CSV Output

The `csv` format writes simulation data into flat comma-separated files, one row per hit.
It is well-suited for analysis with Python (pandas, numpy), R, or any spreadsheet tool.

<br/>

## Configuration

```yaml
gstreamer:
  - format: csv
    filename: myrun
```

<br/>

## Files produced

Each streamer instance writes four separate files. With two threads the output looks like:

```
myrun_t0_true_info.csv          myrun_t1_true_info.csv
myrun_t0_digitized.csv          myrun_t1_digitized.csv
myrun_t0_generated.csv          myrun_t1_generated.csv
myrun_t0_generated_tracked.csv  myrun_t1_generated_tracked.csv
```

Run-level outputs (such as `dosimeter`) produce a single set of files without the `_tN` suffix.

| File suffix | Content |
|-------------|---------|
| `_true_info.csv` | Geant4 true-hit information (one row per step per detector) |
| `_digitized.csv` | Digitized hit output from the assigned digitization routine |
| `_generated.csv` | All configured/generated particles, including LUND rows not propagated by Geant4 |
| `_generated_tracked.csv` | Only particles that were propagated by Geant4 |

<br/>

## Column layout

The first row of each file is a header. Subsequent rows contain one flattened hit.

**True-info columns:**

```
event,timestamp,thread,detector,<variable>,<variable>,...
```

**Digitized columns:**

```
event,timestamp,thread,detector,<identifier>,<identifier>,...,<variable>,<variable>,...
```

The exact variable columns depend on the detector's digitization plugin. The first row of each file
is written when the first event with data arrives; the column set is fixed at that point.

<br/>

## Reading with pandas

```python
import pandas as pd

df = pd.read_csv("myrun_t0_digitized.csv")
print(df.head())

# all threads combined
import glob
frames = [pd.read_csv(f) for f in glob.glob("myrun_t*_digitized.csv")]
df_all = pd.concat(frames, ignore_index=True)
```

<br/>

## Notes

- Files are written in text mode; values are not quoted unless they contain a comma.
- The column schema is inferred from the first hit in each file. If two threads see different
  detectors first, their column sets may differ — use the header row rather than column positions.
- For large runs with many threads, consider merging thread files after the run or switching
  to [`root`](/home/documentation/output/root) for indexed access.
