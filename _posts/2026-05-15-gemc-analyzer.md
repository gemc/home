---
layout: post
title: "GEMC Analyzer is available"
date: 2026-05-15
categories: [news]
tags: [analyzer, output, csv, root, plotting, jupyter]
---

GEMC now includes `analyzer`, a small Python package for reading GEMC output files and plotting variables by name.

The first implementation focuses on CSV and ROOT output from %%gstreamer%%. It can read digitized and true information tables, flatten ROOT detector trees into `pandas` data frames, and make quick histograms from either Python, Jupyter, or the command line.

# What it does

- Reads GEMC CSV output such as `b2_t0_digitized.csv` and `b2_t0_true_info.csv`
- Reads GEMC ROOT output such as `b2_t0.root`
- Returns data as `DataFrame` objects for inspection and analysis
- Plots variables by name, for example %%totEdep%%
- Supports detector selection for ROOT detector trees
- Provides a dependency-free SVG histogram helper for minimal systems

Upcoming in the next release:

- Reads GEMC generated-particle output such as `b2_t0_generated_tracked.csv`
- Plots the generated particle kinematics `p`, `theta`, and `phi`, resolving them automatically even under
  the default data stream
- Lists the plottable quantities of a file when run without a variable name

# Documentation

See the [Analyzer documentation]({{ "/documentation/analyzer/" | relative_url }}) for dependencies, Python examples, command-line examples, Jupyter usage, CSV and ROOT output details, and B2 example commands.
