---
layout: default
title: JSON Output
order: 53
description: Structured JSON output for web tools and streaming pipelines
permalink: /documentation/output/json/
---

# JSON Output

The `json` format writes simulation data as a single JSON document per file. Depending on the
stream type, the top-level object holds either an `events` array or a `frames` array.

<br/>

## Configuration

```yaml
gstreamer:
  - format: json
    filename: myrun
```

Produces one `.json` file per worker thread:

```
myrun_t0.json   myrun_t1.json   ...
```

<br/>

## Document structure — event type

Each element of the `events` array represents one complete event:

```json
{
  "events": [
    {
      "event": 0,
      "timestamp": "2024-01-01T00:00:00",
      "thread": 0,
      "generated": {
        "generated": [
          {"pid": 11, "px": 0.0, "py": 0.0, "pz": 4000.0}
        ]
      },
      "true_info": {
        "dc": [
          {"pid": 11, "tid": 1, "trackE": 3998.2, "avgx": 12.4, "avgy": -3.1, "avgz": 310.0}
        ]
      },
      "digitized": {
        "dc": [
          {"sector": 1, "layer": 3, "wire": 42, "doca": 0.132, "time": 287.4}
        ]
      }
    }
  ]
}
```

<br/>

## Document structure — stream type

Frame records appear under a `frames` array:

```json
{
  "frames": [
    {
      "frame_id": 0,
      "timestamp_sec": 1234567890,
      "timestamp_nsec": 0,
      "payload": [1024, 2048, 4096]
    }
  ]
}
```

<br/>

## Reading with Python

```python
import json

with open("myrun_t0.json") as f:
    data = json.load(f)

for event in data["events"]:
    hits = event.get("digitized", {}).get("dc", [])
    for hit in hits:
        print(hit["wire"], hit["doca"])
```

<br/>

## Notes

- The plugin performs lightweight JSON escaping internally and has no external JSON dependency.
- String values in hit variables are escaped; numeric values are written as-is.
- The top-level structure (`events` or `frames`) is determined by the first publish call
  the plugin receives. Both types cannot appear in the same file.
- For large runs the resulting files can be large; use [`root`](/home/documentation/output/root)
  or [`csv`](/home/documentation/output/csv) for production analysis.
