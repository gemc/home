---
layout: default
title: 'GEMC option: log_every'
---

# `log_every`

Type: `option`

Description: log module: print event progress and average rate every N events per thread

Generated from:

```sh
gemc help log_every
```

```text
-log_every=<value> .........: log module: print event progress and average rate every N events per thread


   Print a progress log line every N events, with the average event rate.
   
   The value is a string of the form N or N-NTH, where N is the log module:
   N     : every worker thread prints 'Starting event n. <k> in thread <tid>.
   Average rate: <r> events / second' every time it has processed a multiple
   of N events. <k> is that thread's own 1-based event count (not the global
   Geant4 event id), and <r> is that thread's average rate.
   N-NTH : as above, but only the worker thread with id NTH prints. NTH must be
   in the range [0, nthreads-1].
   
   Examples: -log_every=100 (all threads, every 100 events)
   -log_every=100-2 (only thread 2, every 100 events)
```
