---
layout: default
title: JLAB SRO Output
order: 55
description: Jefferson Lab streaming readout binary frame format
permalink: /documentation/output/jlabsro/
---

# JLAB SRO Output

The `jlabsro` format writes packed binary frame records in the Jefferson Lab Streaming
Readout (SRO) format. It is used when GEMC simulates time-ordered frame snapshots rather
than individual events.

<br/>

## Configuration

```yaml
gstreamer:
  - format: jlabsro
    filename: myrun
    type: stream
```

The `type: stream` sub-key is required; this format only supports frame-stream output.

Produces one `.ev` file per plugin instance:

```
myrun.ev
```

<br/>

## Frame record structure

Each frame record is a contiguous binary block consisting of:

1. A packed `DataFrameHeader` (56 bytes):

   | Field | Type | Description |
   |-------|------|-------------|
   | `source_id` | uint32 | Source identifier |
   | `total_length` | uint32 | Total frame length in bytes |
   | `payload_length` | uint32 | Payload length in bytes |
   | `compressed_length` | uint32 | Compressed length (0 = uncompressed) |
   | `magic` | uint32 | Format magic number |
   | `format_version` | uint32 | Format version |
   | `flags` | uint32 | Status flags |
   | `record_counter` | uint64 | Frame sequence number |
   | `ts_sec` | uint64 | Timestamp seconds |
   | `ts_nsec` | uint64 | Timestamp nanoseconds |

2. The frame payload: the integral payload words from the active sensitive detectors.

All fields are written in the byte order native to the host platform.

<br/>

## When to use JLAB SRO

Use this format when:

- Simulating the JLab streaming readout DAQ pipeline.
- The downstream software expects `.ev` binary frames produced by JLab SRO hardware.
- Your digitization plugin produces `GIntegralPayload` objects via a stream-mode sensitive detector.

For standard event-based simulation, use [`csv`](/home/documentation/output/csv),
[`root`](/home/documentation/output/root), or [`hipo`](/home/documentation/output/hipo) instead.
