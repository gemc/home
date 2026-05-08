---
layout: post
title: "Upcoming in GEMC 0.2"
date: 2026-05-07
categories: news
tags: [release, generator, examples, pyvista]
progress:
  - label: "Jupyter support"
    value: 60
  - label: "Flux example"
    value: 25
  - label: "Materials example "
    value: 35
  - label: "Pyvista examples "
    value: 25
  - label: "LUND support for generator"
    value: 0
---

Several GEMC features are currently under active development Jupyter support, LUND format for
particles generators and more examples. 

<br/>

## Feature progress

{% for item in page.progress %}
  {% include progress-item.html label=item.label value=item.value %}
{% endfor %}