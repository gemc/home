---
layout: roadmap
title: "Roadmap to GEMC 0.5"
date: 2026-08-17
categories: [roadmap]
tags: [geometry, geant4, clas12]
milestones:
  - repo: src
    number: 4
  - repo: clas12-systems
    number: 3
---

This roadmap tracks the new features, improvements, and issue resolutions planned for GEMC 0.5.

It also includes the milestone for [clas12-systems](https://github.com/gemc/clas12-systems).

Highlights include time-dependent geometry evolution, original track ID information, support for running
Geant4 macros, physics-list selection, and the remaining Geant4 solids. The CLAS12 roadmap continues the
detector import with the beamline, HTCC, RICH, and Forward Tracker.

See also the [Project Roadmap](https://github.com/orgs/gemc/projects/1/views/4).

{% for milestone in page.milestones %}
{% include github_milestone.html repo=milestone.repo milestone=milestone.number %}
{% endfor %}
