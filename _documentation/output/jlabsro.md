---
layout: default
title: FT-Cal / JLAB Output
order: 55
description: FT-Cal streaming configuration and the preserved Jefferson Lab binary frame layout
permalink: /documentation/output/jlabsro/
---

# FT-Cal / JLAB Output

**Upcoming in the next release.** JLAB SRO encoding lives in the `clas12-systems` implementation selected
with %%format: sro%% and %%implementation: ft_cal%%. GEMC's former %%format: jlabsro%% selection is rejected
by the new framework. This page retains its URL for existing links.

The [Streaming Readout Plugins guide](/home/documentation/sro/plugins/) explains activation, event timing,
worker-to-crate delivery, translation tables, implementation contracts, and user choices.

## Configure FT-Cal

With current GEMC and rebuilt CLAS12 plugins, run from `clas12-systems` in the usual FT environment:

```sh
gemc geometry_src/ft/ft.yaml -n=10000 \
  -gstreamer='[{format: sro, filename: ftcal_sro, implementation: ft_cal}]' \
  -eventTimeWidth='10*ns'
```

This replaces the FT card's normal CSV/HIPO output selection. SRO is disabled without an explicit %%sro%%
entry; setting %%eventTimeWidth%% alone does not enable it. The width above is an example, not a measured
beam parameter. For the general syntax of
[separate overrides and combined output](/home/documentation/sro/plugins/#optional-separate-configuration-card),
the plugin guide uses the random-ADC example. Use %%implementation: ft_cal%% and an FT output basename when
applying that pattern here.

Each active crate writes %%ftcal_sro_r<resolved_run>_crate<crate>.ev%%. Files combine all workers and contain
completed occupied 65,536 ns frames. Empty frames are omitted; incomplete tails are discarded, including on
interruption. Reusing the basename/run/crate overwrites the earlier file.

## Payload and translation

`IntegralPayload` derives from `GSROData` and owns crate, slot, channel, charge, and frame-relative time.
The detector worker obtains the electronics address from %%loadTTImpl%%'s `GTranslationTable`, with
%%{ix, iy}%% identity. The framework envelope carries absolute run time for sorting. Slot/channel values
are retained even though the translation entry uses %%ComparisonMode::crate%% for frame-source identity.

The integral contains calibrated charge saturated to 13 bits and signal time quantized to 4 ns ticks.
Separate hits/events remain separate integrals; overlap merging and dead time are not implemented yet.
For response details and the enforced time bound, see
[FT-Cal implementation](/home/documentation/sro/plugins/#ft-cal-implementation-and-current-scope).

## File preamble and frame header

The file begins with two 32-bit words, %%0xC0DA2019%% and %%0xC0DA0001%%, written once even when the first
occupied frame has an index greater than zero. Each subsequent frame has a **52-byte header** followed by
its payload. The preserved wire layout is:

| Field | Type | Value / meaning |
|---|---|---|
| %%source_id%% | uint32 | 0; crate identification is in the slot marker. |
| %%total_length%% | uint32 | Payload bytes + 52 - 4, retaining the legacy convention. |
| %%payload_length%% | uint32 | Payload byte count. |
| %%compressed_length%% | uint32 | Same payload byte count; no compression. |
| %%magic%% | uint32 | 0xC0DA2019. |
| %%format_version%% | uint32 | 257. |
| %%flags%% | uint32 | 0. |
| %%record_counter%% | uint64 | Frame index + 1. |
| %%ts_sec%% | uint64 | Frame-end time: whole seconds. |
| %%ts_nsec%% | uint64 | Frame-end time: remaining nanoseconds. |

Each 32-bit word is explicitly little-endian. The three 64-bit fields store the high 32-bit word before
the low word, matching the legacy half-word swap on little-endian hosts. This is not native struct dumping.
The timestamp is the frame's end in simulation ns, equivalent to %%record_counter * 65536%%; it is not a
wall-clock timestamp. Omitted empty frames can produce gaps in record counters.

## Frame payload

The payload begins with %%0x80000000%% and a 16-word slot directory. Each directory word is:

```text
(word_count << 16) | offset
```

Counts and offsets are in 32-bit words. Offset is measured from the start of the payload. For occupied
slots, the count includes the slot marker; empty slots retain an offset and have a zero count.

Each occupied slot starts with:

```text
0x80008000 | (crate << 8) | slot
```

The marker uses the owning collector's crate. Integral words follow it:

```text
charge | (channel << 13) | ((time / 4) << 17)
```

%%time%% is relative to the frame, in [0, 65536) ns. The supported ranges are crate 0–255, slot/channel 0–15,
and charge 0–8191. Slot directory counts and offsets must fit 16 bits. The crate processor rejects more
than 65,500 samples in a frame; it does not split an oversized frame into extra records. Unsupported
addresses and invalid payloads fail explicitly. Write and close failures are reported through GEMC's
SRO failure path.

## DAQ definitions and setup

The active
[`daq` definitions](https://github.com/gemc/clas12-systems/tree/main/geometry_src/sro/daq)
retain the original named header explicitly:

```cpp
#pragma pack(push, 1)
struct DataFrameHeader
{
    uint32_t source_id;
    uint32_t total_length;
    uint32_t payload_length;
    uint32_t compressed_length;
    uint32_t magic;
    uint32_t format_version;
    uint32_t flags;
    uint64_t record_counter;
    uint64_t ts_sec;
    uint64_t ts_nsec;
};
#pragma pack(pop)
```

Compile-time size and offset assertions protect the 52-byte layout. %%setup_frame_header%% fills the named
fields in host order; %%encode_header%% serializes them in the preserved wire order. %%HeaderSettings%%
lets the implementation set source ID, magic, version, and flags through %%create_crate%%. Default values
retain the current output. These are C++ setup facilities, not new run-card options.

When DAQ supplies a changed definition, document its source and update the active declaration, layout
assertions, setup, serializer, and byte fixtures together. Changing a C++ struct alone does not automatically
change the serialized format correctly.

The original DAQ note describes a seven-bit rocid and five-bit slot, while the retired GEMC writer uses an
eight-bit crate range and 16-slot directory. The current port retains its existing ranges; use above crate
127 and interpretation of the directory still require DAQ-reader validation. The DAQ documentation records
this discrepancy; no extended payload or tracker-specific SRO word has been inferred.

## Source, compatibility, and tests

The implementation lives in
[`geometry_src/sro`](https://github.com/gemc/clas12-systems/tree/main/geometry_src/sro), with worker timing
and translation under
[`ft_cal`](https://github.com/gemc/clas12-systems/tree/main/geometry_src/ft/plugin/ft_cal).
The required declarations and setup were ported from GEMC's old JLAB SRO backend. The
[`DAQ README`](https://github.com/gemc/clas12-systems/blob/main/geometry_src/sro/daq/README.md)
records its Git revision, the original DAQ document locations, and the FT port decisions. The obsolete
streamer, translator copy, and empty FT stubs have been removed; the active implementation is maintained
in `clas12-systems`. GEMC supplies the generic SRO infrastructure.

Local binary fixtures check word layout, byte order, bounds, exact frame boundaries, interrupted tails,
and output-open failures. The full FT-Cal test uses synthetic local CCDB assignments and independently
decodes the worker-produced files with one and four simulation workers. Compatibility with production
JLAB readers and real FT-Cal CCDB assignments still needs validation.

Run the `clas12-systems` SRO test suite from its matching build environment:

```sh
meson test -C build --suite sro --print-errorlogs
```
