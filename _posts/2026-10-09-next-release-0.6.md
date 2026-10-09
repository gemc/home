---
layout: roadmap
title: "Roadmap to GEMC 0.6"
date: 2026-10-09
categories: [roadmap]
tags: [physics, geometry, scoring, clas12]
milestones:
  - repo: src
    number: 5
  - repo: clas12-systems
    number: 4
---

This roadmap tracks the new features, improvements, and issue resolutions planned for GEMC 0.6.

Upcoming with the next release.

It also includes the milestone for [clas12-systems](https://github.com/gemc/clas12-systems) 0.4.

Highlights include physics-list selection, original track ID information, scoring, time-dependent geometry
evolution, and the remaining Geant4 solids. The CLAS12 roadmap continues the detector import with the RICH
and beamline, including shielding and downstream components.

See also the [Project Roadmap](https://github.com/orgs/gemc/projects/1/views/4).

{% for milestone in page.milestones %}
{% include github_milestone.html repo=milestone.repo milestone=milestone.number %}
{% endfor %}
