---
layout: post
title: "Upcoming in GEMC 0.2"
date: 2026-05-13
categories: news
tags: [release, generator, examples, pyvista]
progress:
  - label: "Flux example"
    value: 70
  - label: "Materials example "
    value: 35
  - label: "Pyvista example "
    value: 0
  - label: "Add Analyzer Scripts"
    value: 0
  - label: "Enviroment script upon installation"
    value: 0
---

Roadmap to the next GEMC release.

{% include github_milestone.html milestone=1 %}

## Features progress

{% for item in page.progress %}
  {% include progress-item.html label=item.label value=item.value %}
{% endfor %}

<br/>

