---
layout: default
title: HIPO Output
order: 56
description: CLAS12 HIPO4 bank output for the Jefferson Lab CLAS12 analysis chain
permalink: /documentation/output/hipo/
---

# HIPO Output

The `hipo` format writes standard CLAS12 HIPO4 banks. It is the native output format
for the CLAS12 experiment at Jefferson Lab and is directly readable by
[coatjava](https://github.com/JeffersonLab/clas12-offline-software) and
[hipo4](https://github.com/gavalian/hipo) tools.

Unlike the built-in formats, HIPO is delivered as a separate plugin that is part of the
[clas12-systems](https://github.com/gemc/clas12-systems) repository, not the GEMC core.

<br/>

## Installation

The plugin is built and installed with the clas12-systems package. Once installed, point
`GEMC_PLUGIN_PATH` to its location:

```sh
export GEMC_PLUGIN_PATH=/path/to/clas12-systems/install/lib
gemc mydetector.yaml
```

Or declare the path in your YAML:

```yaml
plugin_path: /path/to/clas12-systems/install/lib
```

<br/>

## Configuration

```yaml
gstreamer:
  - format: hipo
    filename: myrun
```

Produces one `.hipo` file per worker thread:

```
myrun_t0.hipo   myrun_t1.hipo   myrun_t2.hipo   ...
```

<br/>

## Banks written

Each event writes the following standard CLAS12 banks:

| Bank | Content |
|------|---------|
| `RUN::config` | Run number, event number, timestamp |
| `MC::True` | True Geant4 hit information for all fired detectors |
| `MC::Particle` | Generated particles (full bank) |
| `MC::Event` | LUND-style event header |
| `<DET>::adc` / `<DET>::tdc` | Detector digitized ADC or TDC banks |

The detector banks follow the standard CLAS12 bank definitions from
`clas12-offline-software/etc/bankdefs/hipo4`.

<br/>

## Supported detectors

The plugin maps GEMC detector names to CLAS12 detector IDs and writes the appropriate ADC/TDC
banks for each. Supported detectors include: BMT, BST, CND, CTOF, DC, ECAL, FMT, FT_CAL,
FT_HODO, FT_TRK, FTOF, HTCC, LTCC, RICH, RTPC, BAND, URWT, ATOF, AHDC, RECOIL, MUCAL,
MUVT, MURT, MURH, and the generic FLUX detector.

<br/>

## Verbosity

The plugin registers its own verbosity domain. Set it in YAML or on the command line:

```yaml
verbosity:
  - hipo: 1     # file open/close messages
  # hipo: 2     # per-event bank details
```

```sh
gemc mydetector.yaml -verbosity.hipo=2
```

Because `definePluginOptions()` is called during startup, the `hipo` domain must be
visible to GEMC before option parsing — this happens automatically when `GEMC_PLUGIN_PATH`
or `plugin_path` is set and the plugin file is found.

<br/>

## Reading HIPO files

With the [hipo4](https://github.com/gavalian/hipo) C++ library:

```cpp
hipo::reader reader;
reader.open("myrun_t0.hipo");
hipo::dictionary factory;
reader.readDictionary(factory);

hipo::bank dc_tdc(factory.getSchema("DC::tdc"));
hipo::event event;

while (reader.next()) {
    reader.read(event);
    event.getStructure(dc_tdc);
    for (int i = 0; i < dc_tdc.getRows(); ++i) {
        int sector = dc_tdc.getInt("sector", i);
        int wire   = dc_tdc.getInt("component", i);
        int tdc    = dc_tdc.getInt("TDC", i);
        printf("sector %d  wire %d  tdc %d\n", sector, wire, tdc);
    }
}
```

With coatjava (Java / Groovy):

```groovy
def reader = new HipoDataSource()
reader.open("myrun_t0.hipo")
while (reader.hasEvent()) {
    def event = reader.getNextEvent()
    def dc    = event.getBank("DC::tdc")
    for (int i = 0; i < dc.rows(); i++) {
        println dc.getInt("sector", i)
    }
}
```
