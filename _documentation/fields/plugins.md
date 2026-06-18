---
layout: default
title: Field Plugins
order: 42
description: Supply a magnetic field from a shared-library plugin with the generic gfields key
permalink: /documentation/fields/plugins/
---

# Field Plugins

*Upcoming in the next release.*

When a field cannot be expressed as an ideal [multipole](/home/documentation/fields/multipoles) —
for example a measured field map, or any custom model — a **field plugin** supplies it. The generic
`gfields` YAML key names the field, selects a plugin by `type`, and forwards every other key to that
plugin verbatim. No change to GEMC is needed to add a new field type.

```yaml
gfields:
  - name: myfield
    type: mytype
    some_parameter: 1.5
    another_parameter: "30*cm"
```

<br/>

## How a type selects a plugin

The `type` value is turned into a shared-library name following the convention

```
gfield<type>Factory
```

so `type: mytype` loads `gfieldmytypeFactory.gplugin`. GEMC finds it on the plugin search path
(see [search path](#plugin-search-path)), `dlopen`s it, and calls its `GFieldFactory` entry point.

<br/>

## The `gfields` keys

Only two keys are mandatory; two more configure the Geant4 integration. **Every other scalar key is
forwarded to the plugin** as a string (units preserved), so the plugin alone decides which
parameters it understands.

| Key | Default | Meaning |
|-----|---------|---------|
| `name` | *(required)* | Unique field name used by the field registry |
| `type` | *(required)* | Selects the plugin shared library `gfield<type>Factory` |
| `integration_stepper` | `G4DormandPrince745` | Geant4 stepper class name |
| `minimum_step` | `1.0*mm` | Minimum step for the `G4ChordFinder` |
| *(anything else)* | — | Passed straight to the plugin as a string parameter |

Because extra keys pass through untouched, the same `gfields` parser serves every present and
future field plugin.

<br/>

## Writing a field plugin

A plugin is a shared library that derives from `GField` and exports a C factory function.

### Plugin class

```cpp
// myfield.h
#pragma once
#include <gemc/gfields/gfield.h>

class MyField : public GField {
public:
    explicit MyField(const std::shared_ptr<GOptions>& g) : GField(g) {}

    // Required: return B at the lab-frame point pos = {x, y, z}.
    void GetFieldValue(const double pos[3], G4double* bfield) const override;

    // Optional: parse and cache parameters once before stepping begins.
    void load_field_definitions(GFieldDefinition gfd) override;
};
```

### Required entry point

Every plugin must export this exact symbol so GEMC can instantiate it through `dlsym`:

```cpp
// myfield.cc
extern "C" GField* GFieldFactory(const std::shared_ptr<GOptions>& g) {
    return static_cast<GField*>(new MyField(g));
}
```

### Reading parameters

`load_field_definitions` receives a `GFieldDefinition` whose `field_parameters` map holds every
forwarded key as a string. Two base-class helpers parse the common cases (both honor unit
expressions such as `30*cm`):

```cpp
void MyField::load_field_definitions(GFieldDefinition gfd) {
    gfield_definitions = gfd;                          // keep a copy

    int    poles    = get_field_parameter_int("some_count");
    double distance = get_field_parameter_double("another_parameter");  // "30*cm" → mm
}
```

`GetFieldValue` then fills `bfield[0..2]` with `Bx, By, Bz` in Geant4 units. Multiply your stored
values by the matching CLHEP unit (`CLHEP::tesla`, `CLHEP::kilogauss`, …) so the result is unit-correct.

<br/>

## Build

Field plugins build exactly like other GEMC plugins — a shared library with the `.gplugin` suffix.
With Meson, register the plugin in your `meson.build`:

```meson
clas12_plugins += [{
    'name'                : 'gfieldmytypeFactory',
    'sources'             : files('myfield.cc'),
    'dependencies'        : [gemc_dep],
    'include_directories' : [include_directories('.')],
}]
```

The `name` must match the `gfield<type>Factory` convention so the `type` key resolves to this
library.

<br/>

## Plugin search path

GEMC searches for `<plugin_name>.gplugin` in this order:

1. Directories in `-plugin_path=<dir>:<dir>` (command line or YAML).
2. Directories in the `GEMC_PLUGIN_PATH` environment variable.
3. The current working directory.
4. The GEMC installation `lib/` directory.

The recommended production setup discovers the path with `pkg-config`:

```sh
export GEMC_PLUGIN_PATH=$(pkg-config --variable=plugindir clas12-systems)
gemc mydetector.yaml
```

<br/>

## Querying a field

Both field routes can be inspected without running a simulation. These options evaluate **every
configured field** at the requested points, print the result, and exit.

### A single point

```sh
gemc mydetector.yaml -fieldAt="10*cm 0*mm 2*m"
```

The value is three coordinate expressions with units, separated by spaces. Each line of output
reports the field name, the point, and `B`:

```
# field query results
field=myfield source=fieldAt x=10 cm y=0 fm z=2 m Bx=... By=... Bz=... |B|=... tesla
```

### Many points from a file

```sh
gemc mydetector.yaml -fieldMapPoints=field_points.txt
```

Each non-empty, non-comment line holds three coordinate expressions; coordinates may be separated
by spaces or commas, and `#` starts a comment:

```
# x y z field-query points
0*cm  0*cm  0*cm
10*cm, 0*cm, 0*cm
```

Both options may be combined; the single point is queried first, then the file points.
