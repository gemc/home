---
layout: default
title: Custom Digitization Plugins
order: 36
description: Write a GDynamic digitization plugin to process hits with custom electronics models
permalink: /documentation/sensitivity/gplugins/
---

# Custom Digitization Plugins

When the built-in digitizations (`flux`, `dosimeter`, `particle_counter`, `gPhotonDetector`) are not
enough, you can write a **GDynamic digitization plugin**: a shared library (`.gplugin`) that GEMC loads
at run time and calls for every hit in a sensitive volume.

A plugin can implement any electronics model — time-to-distance, charge sharing, TDC jitter,
calibration corrections, translation tables — while still benefiting from GEMC's hit collection,
threading, and output infrastructure.

<br/>

## Quickstart

**1. Assign the digitization name to a volume:**

```python
gvolume.digitization = "myplugin"
gvolume.set_identifier("sector", 1)
gvolume.set_identifier("layer",  2)
```

**2. Build the plugin shared library** (see [Build](#build) below) as `myplugin.gplugin`.

**3. Put it on the plugin search path:**

```sh
export GEMC_PLUGIN_PATH=/path/to/your/plugins
gemc mydetector.yaml
```

GEMC finds `myplugin.gplugin`, loads it, calls your `GDynamicDigitizationFactory` entry point, and
routes every hit in the sensitive volume to your plugin.

<br/>

## Plugin class

Derive from `GDynamicDigitization` and override the methods you need:

```cpp
// myplugin.h
#pragma once
#include <gemc/gdynamicDigitization/gdynamicdigitization.h>

class MyPlugin : public GDynamicDigitization {
public:
    explicit MyPlugin(const std::shared_ptr<GOptions>& g) : GDynamicDigitization(g) {}

    bool defineReadoutSpecsImpl() override;              // required
    bool loadConstantsImpl(int runno,
                           std::string const& var) override;   // optional
    bool loadTTImpl(int runno,
                    std::string const& var) override;          // optional

    [[nodiscard]] std::unique_ptr<GDigitizedData>
    digitizeHitImpl(GHit* ghit, size_t hitn) override;        // optional
};
```

<br/>

## Required entry point

Every plugin must export a factory function with **exactly** this signature so GEMC can instantiate it
through `dlsym`:

```cpp
// myplugin.cc
extern "C" GDynamicDigitization*
GDynamicDigitizationFactory(const std::shared_ptr<GOptions>& g) {
    return new MyPlugin(g);
}
```

<br/>

## Override reference

| Method | When to override |
|--------|-----------------|
| `defineReadoutSpecsImpl()` | Always — sets the electronics timing model |
| `loadConstantsImpl(runno, variation)` | Load calibration constants from CCDB or files |
| `loadTTImpl(runno, variation)` | Build the identity→electronics address translation table |
| `digitizeHitImpl(ghit, hitn)` | Produce digitized output from a hit |
| `processTouchableImpl(gtouchable, step)` | Re-bin hits by time cell (default implementation handles the standard case) |
| `decisionToSkipHit(energy)` | Apply an energy threshold before digitization |

<br/>

### defineReadoutSpecsImpl

This method is required. It sets the electronics time model and must populate `readoutSpecs`:

```cpp
bool MyPlugin::defineReadoutSpecsImpl() {
    double timeWindow    = 500;           // electronics integration window [ns]
    double gridStartTime = 0;             // time grid origin [ns]
    auto   hitBitSet     = HitBitSet("100000");
    double maxStep       = 1 * CLHEP::mm;

    readoutSpecs = std::make_shared<GReadoutSpecs>(
        timeWindow, gridStartTime, hitBitSet, maxStep, log);
    return true;
}
```

The `HitBitSet` controls which hit information is computed and stored. The six bits from left to right
enable: `showTrue`, `showID`, `showRaw`, `showDgt`, `showIntegrated`, `showFlux`.

<br/>

### digitizeHitImpl

`digitizeHitImpl` receives an accumulated `GHit` and returns a `GDigitizedData` record:

```cpp
std::unique_ptr<GDigitizedData>
MyPlugin::digitizeHitImpl(GHit* ghit, size_t hitn) {
    auto data = std::make_unique<GDigitizedData>(gopts, ghit);

    double edep     = ghit->getTotalEnergyDeposited();
    double adc_time = ghit->getAverageTime() * 1.1;  // example smearing

    data->includeVariable("adc",  edep * 1000.0);
    data->includeVariable("time", adc_time);

    return data;
}
```

Variables added with `includeVariable` appear in the output bank alongside the identifiers.

<br/>

## Plugin options

Plugins can declare their own GEMC options. When `myplugin` is listed under `gsystem` in a YAML file,
GEMC probes `myplugin.gplugin` for a `definePluginOptions` symbol **before** command-line and YAML
parsing begins. Options declared there appear in `gemc -h`, are saved to the configuration snapshot,
and can be set from the command line or YAML like any other option.

### Declaring options

Export a second entry point:

```cpp
extern "C" GOptions* definePluginOptions() {
    // Pass the logger tag to GOptions() to register it in the verbosity schema.
    auto* opts = new GOptions("myplugin");

    opts->defineOption(
        GVariable("myplugin_threshold", 50.0, "Hit energy threshold [eV]"),
        "Hits with total deposited energy below this value are discarded.\n"
        "Default: 50 eV."
    );
    return opts;
}
```

The `GOptions("myplugin")` constructor registers `myplugin` as a **verbosity key** (see
[Verbosity](#verbosity) below). Add any number of scalar options or switches with `defineOption` /
`defineSwitch`.

### Reading options in the plugin

Options are available through `gopts` (inherited from `GDynamicDigitization`) in any method called
after construction:

```cpp
bool MyPlugin::defineReadoutSpecsImpl() {
    double threshold = gopts->getScalarDouble("myplugin_threshold");
    // ...
}
```

### Setting options from YAML

```yaml
myplugin_threshold: 30.0

gsystem:
  - name: myplugin
    factory: sqlite
    variation: default
```

Or from the command line:

```sh
gemc mydetector.yaml -myplugin_threshold=30.0
```

<br/>

## Verbosity

Passing the plugin name to the `GOptions` constructor and using it as the logger channel gives the
plugin its own `verbosity.X` key, independent of the global `gdigitization` verbosity.

Use the plugin name as the logger channel in the class constructor:

```cpp
explicit MyPlugin(const std::shared_ptr<GOptions>& g) : GDynamicDigitization(g) {
    log = std::make_shared<GLogger>(g, "MyPlugin", "myplugin");
}
```

Then control verbosity per run:

```yaml
verbosity:
  - myplugin: 2
```

Or from the command line:

```sh
gemc mydetector.yaml -verbosity.myplugin=2
```

`verbosity.gdigitization` continues to control all other digitization plugins.

<br/>

## Plugin search path

GEMC searches for `<digitization_name>.gplugin` in this order:

1. Directories in `-plugin_path=<dir>:<dir>` (command line or YAML).
2. Directories in the `GEMC_PLUGIN_PATH` environment variable.
3. The current working directory.
4. The GEMC installation `lib/` directory.

The recommended production setup uses `pkg-config` to set the path automatically:

```sh
export PKG_CONFIG_PATH=/your/clas12/prefix/lib/pkgconfig:$PKG_CONFIG_PATH
export GEMC_PLUGIN_PATH=$(pkg-config --variable=plugindir clas12-systems)
gemc mydetector.yaml
```

<br/>

## Build

Plugins are built as shared libraries with the `.gplugin` suffix. With Meson, register the plugin in
your `plugin/meson.build`:

```meson
clas12_plugins += [{
    'name'                : 'myplugin',
    'sources'             : files('myplugin.cc'),
    'dependencies'        : [gemc_dep],
    'include_directories' : [include_directories('.')],
}]
```

The top-level `meson.build` turns every entry in `clas12_plugins` into an installed `.gplugin` shared
library.

<br/>

## Context sensitivity of `gemc -h`

Plugin options appear in `gemc -h` only when a YAML file that lists the plugin under `gsystem` is
also passed on the command line:

```sh
gemc mydetector.yaml -h      # shows myplugin_threshold and verbosity.myplugin
gemc -h                      # shows core options only; no plugin is loaded
```

This is expected: GEMC can only advertise the options of plugins it knows it will load.
