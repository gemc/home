---
layout: default
title: Output
order: 50
description: Overview of GEMC output formats and how to configure gstreamer outputs
permalink: /documentation/output/
---

# Output

GEMC writes simulation data through **gstreamer** plugins. Each plugin serializes the event,
run, and frame data produced during a simulation run into a specific file format.

One or more outputs are configured with the `gstreamer` YAML key:

```yaml
gstreamer:
  - format: csv
    filename: myrun
  - format: root
    filename: myrun
```

Multiple entries are allowed; GEMC instantiates all configured plugins in parallel.

<br/>

## Built-in formats

| Format | Type token | Extension | Best for |
|--------|-----------|-----------|----------|
| [ASCII](/home/documentation/output/ascii) | `ascii` | `.txt` | Inspection, debugging |
| [CSV](/home/documentation/output/csv) | `csv` | `.csv` | Python / pandas analysis |
| [JSON](/home/documentation/output/json) | `json` | `.json` | Web tools, streaming pipelines |
| [ROOT](/home/documentation/output/root) | `root` | `.root` | HEP analysis with ROOT TTrees |
| [JLAB SRO](/home/documentation/output/jlabsro) | `jlabsro` | `.ev` | Jefferson Lab streaming readout frames |
| [HIPO](/home/documentation/output/hipo) | `hipo` | `.hipo` | CLAS12 analysis with standard banks |

HIPO is a separately installed plugin specific to the CLAS12 detector suite. The remaining
formats are bundled with GEMC.

<br/>

## Output types

The `type` sub-key selects what the plugin writes:

| Type | Content |
|------|---------|
| `event` (default) | per-event hits: headers, true info, digitized data, generated particles |
| `stream` | per-frame time-snapshot payloads |

```yaml
gstreamer:
  - format: root
    filename: myrun
    type: event       # default
  - format: jlabsro
    filename: myrun
    type: stream      # frame snapshots
```

<br/>

## Threading and file naming

Event-based outputs (such as `flux` or custom plugins) produce **one file per worker thread**.
The thread index is appended to the filename automatically:

```
myrun_t0.root   myrun_t1.root   myrun_t2.root   ...
```

Run-based outputs (such as `dosimeter`) accumulate across the full run and produce a
**single file per streamer**:

```
myrun.root
```

The number of threads is controlled by `nthreads`. A value of `0` (the default) uses one thread
per available core.

<br/>

## Event buffer

Each streamer instance accumulates events in memory and flushes them to disk in batches.
The default batch size is 100 events. Adjust it with `ebuffer`:

```yaml
ebuffer: 50
```

Smaller values reduce peak memory use at the cost of more frequent I/O.

<br/>

## Writing a custom plugin

When the built-in formats are not enough, you can ship your own output plugin as a `.gplugin`
shared library. See [Writing an output plugin](/home/documentation/output/gplugin) for a
step-by-step guide.
