---
layout: default
title: 'GEMC option: ganalysis'
---

# `ganalysis`

Type: `option`

Description: prepare GUI Analyzer plots

Generated from:

```sh
gemc help ganalysis
```

```text
-ganalysis=<sequence> ......: prepare GUI Analyzer plots

   • position: plot position: top_left, top_right, bottom_left, or bottom_rightDefault value: NODFLT
   • run: run number; -1 selects the first available runDefault value: -1
   • plugin: runtime sensitive-detector/plugin nameDefault value: 
   • source: variable source: true or digitizedDefault value: true
   • dimension: histogram dimension: 1d or 2dDefault value: 1d
   • x: X variable name to validate after beamOnDefault value: 
   • y: Y variable name for a 2D histogramDefault value: 
   • bins: number of bins per axisDefault value: 100
   • x_min_auto: derive the X minimum from samplesDefault value: true
   • x_max_auto: derive the X maximum from samplesDefault value: true
   • y_min_auto: derive the Y minimum from samplesDefault value: true
   • y_max_auto: derive the Y maximum from samplesDefault value: true
   • x_min: fixed X minimum when x_min_auto is falseDefault value: 0.000000
   • x_max: fixed X maximum when x_max_auto is falseDefault value: 1.000000
   • y_min: fixed Y minimum when y_min_auto is falseDefault value: 0.000000
   • y_max: fixed Y maximum when y_max_auto is falseDefault value: 1.000000
   • title: plot title; empty uses an automatic titleDefault value: 
   • style: 2D rendering style: heatmap or boxesDefault value: heatmap
   • scale: 1D Y scale or 2D Z scale: linear or logarithmicDefault value: linear


   Prepare Analyzer plots before the GUI starts. Variable names remain red until a
   beamOn run validates them against runtime data. Example:
   ganalysis_plots: 4
   ganalysis_accumulate: true
   ganalysis:
   - position: top_left
   run: 11
   plugin: flux
   source: true
   dimension: 2d
   x: avg_x
   y: avg_y
   bins: 100
   style: heatmap
   scale: logarithmic
```
