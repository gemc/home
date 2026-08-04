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

This roadmap tracks the new features, improvements, and issue resolutions for GEMC 0.4.

Included are the milestones for [pygemc](https://github.com/gemc/pygemc) 
and [clas12-systems](https://github.com/gemc/clas12-systems).

Highlights include the post-digitization threshold and efficiency policy API in GEMC core: plugins can
cache deterministic transient `GDigitizedData` values, apply detector-intrinsic policies after
digitization, and keep efficiency random draws inside `apply_efficiency_impl`. The CLAS12 DC, ECAL/PCAL,
and FTOF plugins use this split so `digitize_hit.cc` builds detector observables while dedicated
`apply_thresholds.cc` / `apply_efficiency.cc` files own the policy decisions.

See also the [Project Roadmap](https://github.com/orgs/gemc/projects/1/views/4).


{% for milestone in page.milestones %}
{% include github_milestone.html repo=milestone.repo milestone=milestone.number %}
{% endfor %}
