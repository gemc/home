---
layout: default
title: ASCII Output
order: 51
description: Human-readable text output format for inspection and debugging
permalink: /documentation/output/ascii/
---

# ASCII Output

The `ascii` format writes simulation data as structured plain text. It is intended for
inspection and debugging: every bank boundary, header field, and hit variable appears on
its own labeled line.

<br/>

## Configuration

```yaml
gstreamer:
  - format: ascii
    filename: myrun
```

Produces one `.txt` file per worker thread:

```
myrun_t0.txt   myrun_t1.txt   myrun_t2.txt   ...
```

Run-level outputs (such as `dosimeter`) produce a single file:

```
myrun.txt
```

<br/>

## File structure

The file follows the event publish sequence. A typical event record looks like:

```text
--- Event 0 ---
  Event header: event 0 timestamp 2024-01-01T00:00:00 thread 0
  --- generated bank ---
    pid: 11  px: 0  py: 0  pz: 4000
  --- true info: dc ---
    pid: 11  tid: 1  trackE: 3998.2  avgx: 12.4  avgy: -3.1  avgz: 310.0  ...
  --- digitized: dc ---
    sector: 1  layer: 3  wire: 42  doca: 0.132  time: 287.4
--- End event 0 ---
```

Run-level records are emitted once at the end of the run:

```text
--- Run 11 ---
  --- run digitized: dosimeter ---
    region: 1  edep: 1.24e-04  dose: 8.71e-11
--- End run 11 ---
```

Frame records (stream type) are written in a similar bracketed style showing the frame header
followed by the integral payload values.

<br/>

## When to use ASCII

- Quick visual checks of geometry, identifiers, and digitization variables.
- Verifying that a new plugin produces the expected variables before switching to a binary format.
- Teaching and documentation: the format is self-describing and requires no reader tool.

For analysis workflows, prefer [`csv`](/home/documentation/output/csv) or
[`root`](/home/documentation/output/root) which are more compact and directly loadable.
