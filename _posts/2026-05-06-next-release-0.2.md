---
layout: post
title: "Upcoming in GEMC 0.2"
date: 2026-05-07
categories: news
tags: [release, generator, examples, pyvista]
progress:
  - label: "Jupyter support"
    value: 100
  - label: "Flux example"
    value: 25
  - label: "Materials example "
    value: 35
  - label: "Pyvista examples "
    value: 25
  - label: "LUND support for generator"
    value: 0
  - label: "Analyzer Scripts"
    value: 0
  - label: "gemc.sh enviroment upon installation"
    value: 0
---

Several GEMC features are currently under active development: Jupyter support, LUND format for
particle generators, more examples, and bug fixes.

<br/>

## Feature progress

{% for item in page.progress %}
  {% include progress-item.html label=item.label value=item.value %}
{% endfor %}

<br/>

## Issues to be addressed:

- [ ] [#80: add batch screenshot](https://github.com/gemc/src/issues/80)
- [ ] [#81: Cherenkov bug](https://github.com/gemc/src/issues/81)