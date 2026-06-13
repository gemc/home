---
layout: default
title: Options
category: api
---

# GEMC Options

GEMC options can be set from the command line, from one or more YAML files, or
from both. Use YAML files for configurations you want to keep, and use
command-line options for short run-time changes.

For the generated list of every option and switch, see the
[Options Reference](/home/documentation/api/options_reference).

## Basic Usage

Pass YAML files as plain arguments and command-line options as `-name=value`:

```sh
gemc config.yaml -n=1000 -runno=11
```

Scalar options use the same name in YAML:

```yaml
n: 1000
runno: 11
phys_list: FTFP_BERT
```

Equivalent command line:

```sh
gemc -n=1000 -runno=11 -phys_list=FTFP_BERT
```

Structured options use YAML lists of maps:

```yaml
gparticle:
  - name: e-
    p: 5*GeV
```

Equivalent command line:

```sh
gemc -gparticle="[{name: e-, p: 5*GeV}]"
```

Quote structured command-line values so the shell does not split the YAML-like
payload.

## Precedence

GEMC resolves options in this order:

1. Built-in defaults.
2. YAML files, in the order they appear on the command line.
3. Command-line options.

Later values overwrite earlier values. For example:

```sh
gemc base.yaml production.yaml -n=5000 -runno=17
```

In this command, `production.yaml` can overwrite values from `base.yaml`, and
`-n=5000 -runno=17` overwrite both YAML files.

Each run writes the resolved configuration to:

```text
<executable>.<conf_yaml>.yaml
```

The default %%conf_yaml%% value is %%saved_configuration%%, so a `gemc` run normally
writes:

```text
gemc.saved_configuration.yaml
```

Set another snapshot name with:

```sh
gemc config.yaml -conf_yaml=run17
```

## Switches

Switches are boolean flags enabled by their presence:

```sh
gemc config.yaml -gui
gemc config.yaml -recordZeroEdep
```

In YAML, a switch key enables that switch:

```yaml
gui: true
recordZeroEdep: true
```

Use command-line switches for temporary toggles. Current switch parsing treats
the presence of a switch key in YAML as enabled, so omit the key when you do not
want the switch.

## Structured Options

Many GEMC options are structured YAML lists. Each list item is a map.

```yaml
gstreamer:
  - format: root
    filename: out
  - format: csv
    filename: out
```

Equivalent command line:

```sh
gemc -gstreamer="[{format: root, filename: out}, {format: csv, filename: out}]"
```

Some structured options require mandatory keys. Optional keys are filled from
defaults. For example, %%gparticle%% requires %%name%% and %%p%%; fields such as
%%theta%%, %%phi%%, %%multiplicity%%, and units have defaults.

## Dot Notation

Dot notation is intended for verbosity settings:

```sh
gemc config.yaml -verbosity.gemc=1
```

YAML equivalent:

```yaml
verbosity:
  - gemc: 1
```

For other structured options, prefer setting the full YAML list in a YAML file
or as a quoted command-line value.

## Help

Print all available options for the executable:

```sh
gemc -h
```

Print detailed help for one option:

```sh
gemc help gparticle
gemc help gsystem
gemc help gstreamer
```

Search every option and switch whose name or description contains a value. The
match is case-insensitive and matches anywhere in the name or description:

```sh
gemc search particle
gemc search stream
gemc search overlap
```

Each match is printed with its detailed help, so `search` is a quick way to
discover related options without scanning the full reference. Use
`gemc help <value>` afterwards for the detailed help of a single option.

The generated [Options Reference](/home/documentation/api/options_reference)
contains links to the detailed help output for every option and switch.

## Examples

### Basic Run

```yaml
n: 1000
runno: 11
nthreads: 4
phys_list: FTFP_BERT
verbosity:
  - gemc: 1
```

Equivalent command line:

```sh
gemc -n=1000 -runno=11 -nthreads=4 -phys_list=FTFP_BERT -verbosity.gemc=1
```

### Particle Generator

```yaml
gparticle:
  - name: e-
    p: 5*GeV
```

Equivalent command line:

```sh
gemc -gparticle="[{name: e-, p: 5*GeV}]"
```

### Geometry System

```yaml
sql: gemc.db
experiment: examples
runno: 1
gsystem:
  - name: b1
    factory: sqlite
    variation: default
```

Equivalent command line:

```sh
gemc -sql=gemc.db -experiment=examples -runno=1 \
  -gsystem="[{name: b1, factory: sqlite, variation: default}]"
```

### Output Streams

```yaml
gstreamer:
  - format: root
    filename: out
  - format: csv
    filename: out
```

Equivalent command line:

```sh
gemc -gstreamer="[{format: root, filename: out}, {format: csv, filename: out}]"
```

### Visualization

```yaml
g4view:
  - driver: TOOLSSG_OFFSCREEN
  - segsPerCircle: 200
g4camera:
  - phi: -10*deg
  - theta: 250*deg
g4light:
  - phi: 160*deg
  - theta: 120*deg
```

Equivalent command line:

```sh
gemc -g4view="[{driver: TOOLSSG_OFFSCREEN, segsPerCircle: 200}]" \
  -g4camera="[{phi: -10*deg, theta: 250*deg}]" \
  -g4light="[{phi: 160*deg, theta: 120*deg}]"
```

### Command Line Overrides YAML

Given this file:

```yaml
n: 1000
runno: 1
gparticle:
  - name: e-
    p: 1*GeV
```

This command runs 10,000 events with run number 22 and leaves the particle
definition from YAML unchanged:

```sh
gemc run.yaml -n=10000 -runno=22
```

This command replaces the %%gparticle%% list from YAML:

```sh
gemc run.yaml -gparticle="[{name: proton, p: 1200*MeV, theta: 14*deg}]"
```
