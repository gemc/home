---
layout: default
title: Writing an Output Plugin
order: 57
description: Write a GStreamer output plugin to serialize GEMC events into a custom format
permalink: /documentation/output/gplugin/
---

# Writing an Output Plugin

When the built-in formats are not enough, you can write a **GStreamer output plugin**: a shared
library (`.gplugin`) that GEMC loads at run time and calls for every event, run, or frame record.

A plugin can implement any serialization strategy — binary databases, custom binary formats,
network sockets, third-party libraries — while still benefiting from GEMC's event buffering,
threading, and plugin search infrastructure.

<br/>

## Quickstart

**1. Add the format name to your YAML:**

```yaml
gstreamer:
  - format: myfmt
    filename: myrun
```

**2. Build the plugin shared library** (see [Build](#build) below) as `gstreamer_myfmt_plugin.gplugin`.

**3. Put it on the plugin search path:**

```sh
export GEMC_PLUGIN_PATH=/path/to/your/plugins
gemc mydetector.yaml
```

GEMC loads `gstreamer_myfmt_plugin.gplugin`, calls your `GStreamerFactory` entry point, and
routes every event to your plugin.

<br/>

## Plugin class

Derive from `GStreamer` and override the hooks you need:

```cpp
// myfmt.h
#pragma once
#include <gemc/gstreamer/gstreamer.h>
#include <fstream>

class MyFmtPlugin : public GStreamer {
public:
    explicit MyFmtPlugin(const std::shared_ptr<GOptions>& g) : GStreamer(g) {}

protected:
    bool openConnection()    override;
    bool closeConnectionImpl() override;

    bool startEventImpl(const std::shared_ptr<GEventDataCollection>&) override;
    bool endEventImpl  (const std::shared_ptr<GEventDataCollection>&) override;

    bool publishEventHeaderImpl(const std::unique_ptr<GEventHeader>&) override;
    bool publishEventTrueInfoDataImpl(
        const std::string&, const std::vector<const GTrueInfoData*>&) override;
    bool publishEventDigitizedDataImpl(
        const std::string&, const std::vector<const GDigitizedData*>&) override;
    bool publishEventGeneratedParticlesImpl(
        const std::string&, const GGeneratedParticleBank&) override;

private:
    std::ofstream ofile;
    [[nodiscard]] std::string filename() const override {
        return gstreamer_definitions.rootname + ".myfmt";
    }
};
```

<br/>

## Required entry point

Every plugin must export a factory function with **exactly** this signature:

```cpp
// myfmt.cc
extern "C" GStreamer* GStreamerFactory(const std::shared_ptr<GOptions>& g) {
    return new MyFmtPlugin(g);
}
```

GEMC resolves this symbol via `dlsym` when it loads the plugin.

<br/>

## Hook reference

| Hook | Called when |
|------|-------------|
| `openConnection()` | Plugin is initialized; open the output file or connection |
| `closeConnectionImpl()` | Simulation ends; close and flush |
| `startEventImpl(event_data)` | Start of each event — use for event delimiters |
| `endEventImpl(event_data)` | End of each event — flush buffered event data |
| `publishEventHeaderImpl(header)` | Event header available (number, timestamp, thread id) |
| `publishEventTrueInfoDataImpl(name, hits)` | True Geant4 hits for one detector |
| `publishEventDigitizedDataImpl(name, hits)` | Digitized hits for one detector |
| `publishEventGeneratedParticlesImpl(bank, particles)` | Generated-particle bank (`generated` or `generated_tracked`) |
| `startRunImpl(run_data)` | Start of a run-level collection |
| `endRunImpl(run_data)` | End of a run-level collection |
| `publishRunHeaderImpl(header)` | Run header |
| `publishRunDigitizedDataImpl(name, hits)` | Run-level digitized hits for one detector |
| `startStreamImpl(frame_data)` | Start of a frame record (stream type) |
| `endStreamImpl(frame_data)` | End of a frame record |
| `publishFrameHeaderImpl(header)` | Frame header |
| `publishPayloadImpl(payload)` | Frame payload words |

All hooks return `bool`; return `true` on success.

Hooks you do not override default to a no-op that returns `false`; override only what your format needs.

<br/>

## Accessing hit data

Inside `publishEventDigitizedDataImpl`, iterate the hit vector:

```cpp
bool MyFmtPlugin::publishEventDigitizedDataImpl(
    const std::string& detectorName,
    const std::vector<const GDigitizedData*>& digitizedData)
{
    for (const auto* hit : digitizedData) {
        // Identifiers (sector, layer, wire, …) are doubles in GDigitizedData.
        // Numeric variables set by the digitization plugin are also doubles.
        auto vars = hit->getDigitizedData();  // map<string, double>
        for (const auto& [key, val] : vars) {
            ofile << detectorName << "  " << key << "  " << val << "\n";
        }
    }
    return true;
}
```

For true-information hits:

```cpp
bool MyFmtPlugin::publishEventTrueInfoDataImpl(
    const std::string& detectorName,
    const std::vector<const GTrueInfoData*>& trueInfoData)
{
    for (const auto* hit : trueInfoData) {
        auto vars = hit->getTrueInfoData();   // map<string, double>
        // ...
    }
    return true;
}
```

<br/>

## Plugin options

Export a `definePluginOptions` symbol to register custom options and a verbosity domain.
This symbol is probed **before** any factory is instantiated, so options and verbosity
keys are available from the start.

```cpp
extern "C" GOptions* definePluginOptions() {
    auto* opts = new GOptions("myfmt");  // registers "myfmt" as a verbosity key

    opts->defineOption(
        GVariable("myfmt_compress", false, "Enable compression"),
        "Write the output file with zlib compression. Default: false."
    );
    return opts;
}
```

### Reading options in the plugin

```cpp
explicit MyFmtPlugin(const std::shared_ptr<GOptions>& g) : GStreamer(g) {
    log  = std::make_shared<GLogger>(g, "MyFmtPlugin", "myfmt");
    compress = g->getScalarBool("myfmt_compress");
}
```

### Setting options from YAML

```yaml
myfmt_compress: true

gstreamer:
  - format: myfmt
    filename: myrun
```

<br/>

## Verbosity

When `definePluginOptions` returns `new GOptions("myfmt")`, the `myfmt` key is registered as a
verbosity domain. Set it in YAML:

```yaml
verbosity:
  - myfmt: 1    # info-level messages
  # myfmt: 2   # per-event detail
```

Use `log->info(1, ...)` / `log->info(2, ...)` in your plugin to emit at those levels.

<br/>

## Build

Plugins are built as shared libraries with the `.gplugin` suffix. The naming convention is:

```
gstreamer_<format>_plugin.gplugin
```

With Meson, add an entry to `clas12_plugins` (or your own build file):

```meson
clas12_plugins += [{
    'name'    : 'gstreamer_myfmt_plugin',
    'sources' : files('myfmt.cc'),
    'dependencies'        : [gemc_dep],
    'include_directories' : [include_directories('.')],
}]
```

The top-level `meson.build` turns every entry into an installed `.gplugin` shared library.

<br/>

## Threading model

GEMC instantiates one plugin object per worker thread. Each instance calls `openConnection()`
independently and writes to its own file (the base class appends `_t<tid>` to the filename
automatically). Never share file handles or mutable state across instances.

<br/>

## Plugin search path

GEMC searches for `gstreamer_<format>_plugin.gplugin` in this order:

1. Directories in `-plugin_path=<dir>:<dir>` (command line or YAML).
2. Directories in the `GEMC_PLUGIN_PATH` environment variable.
3. The current working directory.
4. The GEMC installation `lib/` directory.

```sh
export GEMC_PLUGIN_PATH=/your/build/dir
gemc mydetector.yaml
```

<br/>

## Context sensitivity of `gemc -h`

Plugin options appear in `gemc -h` only when a YAML file that declares the plugin format under
`gstreamer` is also passed on the command line:

```sh
gemc mydetector.yaml -h   # shows myfmt_compress and verbosity.myfmt
gemc -h                   # shows core options only
```

This is expected: GEMC can only advertise the options of plugins it knows it will load.
