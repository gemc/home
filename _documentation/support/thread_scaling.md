---
layout: default
title: Thread Scaling
order: 100
description: Multithread benchmarking of GEMC — the local threading suite and the scaling sweep.
permalink: /documentation/support/thread_scaling/
---

# Thread Scaling

GEMC runs its event loop across worker threads. The **Thread Scaling** workflow measures how run time,
event rate, speedup, and parallel efficiency change with the number of workers, so regressions in
multithreaded performance are caught automatically.

On pull requests a short thread-scaling sweep of representative `basic` and `optical` examples runs.
Weekly and versioned-release runs repeat full sweeps across hosted runners. Each workflow artifact contains
the complete CSV, JSON, and SVG reports plus a plotted `summary_<cpu>_<os>_<arch>_<ncores>cores.md` report.

<br/>

## Local threading tests

Developers can run the local multithreading and race-focused `meson` suite. It detects the CPUs available
to the process, creates one sequential test for every thread count from one through that maximum, and can be
repeated to vary worker scheduling:

```shell
meson test -C build --suite threading --repeat 10 --print-errorlogs
```

<br/>

## Running a scaling sweep

To run the standard 20,000-event scintillator scaling sweep, make sure `gemc`, Git, Node.js 24 or newer, and
Python 3 are available, then run:

```shell
bin/scaling.sh
```

For example, select a 50,000-event workload, cap the sweep at 32 threads, and override `ThreadScale`'s
measurement defaults with:

```shell
bin/scaling.sh --workload 50000 --max-threads 32 -- --runs 8 --warmup-runs 2 --summary-plots rate
```

By default, the script compares no output with ROOT output. Use `--without-output` to run only the
no-output case, without producing the comparison series. Use `--gemc-options` to append GEMC arguments to
every measured invocation. For example, this transport-focused run disables output, digitization, and
true-information construction:

```shell
bin/scaling.sh \
  --without-output \
  --gemc-options '-no_digitized=all -no_true_info=all' \
  --workload 100000 \
  --max-threads 64 \
  --output-dir thread-scaling-transport
```

<br/>

## Report output and options

The script clones the current `ThreadScale` development branch into a temporary directory and retains the
full report in `thread-scaling/`. Its Markdown report is named from the CPU model, OS and release,
architecture, and physical core count, for example
`summary_amd-epyc-9354-32-core-processor_linux-5-14_x64_64cores.md`. The core count falls back to CPUs
visible to the benchmark when physical topology is unavailable.

Set `THREADSCALE_REF` to test another branch or tag. Neither `thread-scaling/` nor `thread-scaling.parts/`
may already exist. The `{workload}` command placeholder ensures the simulated event count is the same value
used to calculate the reported rate. The powers-of-two sweep ends at the maximum number of CPUs visible to
the process unless `--max-threads` sets a cap. Options after `--` are passed to `test_scaling` after the
defaults, so they can override runs, warmups, duration, thread selection, strategy, replicas, and plot
selection. Run `bin/scaling.sh --help` for the wrapper options.
