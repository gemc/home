---
layout: roadmap
title: "Roadmap to GEMC 0.4"
date: 2026-06-17
categories: [roadmap]
tags: [generator, cherenkov, jupyter, screenshot]
milestones:
  - repo: src
    number: 3
  - repo: pygemc
    number: 2
  - repo: clas12-systems
    number: 2
---

New features, improvements, and issue resolutions planned for the next release.

Included are the milestones for [pygemc](https://github.com/gemc/pygemc) 
and [clas12-systems](https://github.com/gemc/clas12-systems).

See also the [Project Roadmap](https://github.com/orgs/gemc/projects/1/views/4).


{% for milestone in page.milestones %}
{% include github_milestone.html repo=milestone.repo milestone=milestone.number %}
{% endfor %}
