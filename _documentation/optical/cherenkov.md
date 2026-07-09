---
layout: default
title: Cherenkov
order: 25
description: Configure materials and physics for Cherenkov radiation
---

# Cherenkov

Cherenkov radiation appears when a charged particle moves through a material faster than light
propagates through that material. In GEMC, this requires three pieces:

* a material with an optical %%RINDEX%% table;
* a physics list that includes `G4OpticalPhysics`;
* a detector response, usually `gPhotonDetector`, to record optical photons.

<br/>

## Material setup

The material must define `photonEnergy` and `indexOfRefraction` with the same number of entries:

```python
radiator = GMaterial("radiatorGas")
radiator.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV"
radiator.indexOfRefraction = "1.0010 1.0011 1.0012 1.0013"
radiator.absorptionLength = "100*m 100*m 100*m 100*m"
radiator.publish(cfg)
```

The `photonEnergy` values are the interpolation axis for every optical table. Keep them strictly
increasing and use the same number of values in every table attached to the material.

<br/>

## Physics list

Optical photons are produced only when the physics list includes `G4OpticalPhysics`:

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

{% include notes/physics-list-note.md %}

<br/>

## Photon detectors

Use `gPhotonDetector` on collection panels when the goal is to count optical photons rather than
energy deposition:

```python
panel.digitization = "gPhotonDetector"
panel.set_identifier("detector", 1)
```

`gPhotonDetector` records optical photons even when their energy deposition is zero, so
%%recordZeroEdep%% is not required for this workflow.

<br/>

## Example

The [Cherenkov example](/home/examples/optical/cherenkov) compares three radiator indices. A larger
index of refraction produces a wider cone and a different hit pattern on the photon detector.

<div class="gallery-grid">

<figure class="figure figure--center">
  <img src="/home/assets/images/examples/cherenkov/low_index_radiator.png" alt="low index radiator">
  <figcaption>lowIndexRadiator geometry</figcaption>
</figure>

<figure class="figure figure--center">
  <img src="/home/assets/images/examples/cherenkov/medium_index_radiator.png" alt="medium index radiator">
  <figcaption>mediumIndexRadiator geometry</figcaption>
</figure>

<figure class="figure figure--center">
  <img src="/home/assets/images/examples/cherenkov/high_index_radiator.png" alt="high index radiator">
  <figcaption>highIndexRadiator geometry</figcaption>
</figure>

<figure class="figure figure--center">
  <img src="/home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png" alt="low index y vs x">
  <figcaption>lowIndexRadiator y vs x</figcaption>
</figure>

<figure class="figure figure--center">
  <img src="/home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png" alt="medium y vs x">
  <figcaption>mediumIndexRadiator y vs x</figcaption>
</figure>

<figure class="figure figure--center">
  <img src="/home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png" alt="high index y vs x">
  <figcaption>highIndexRadiator y vs x</figcaption>
</figure>

</div>

<p class="image-caption">
  Left: <span class="gstring">lowIndexRadiator</span>, center:
  <span class="gstring">mediumIndexRadiator</span>, right:
  <span class="gstring">highIndexRadiator</span>.
</p>

<br/>

## Related pages

- [Optical Properties](/home/documentation/optical/optical_properties)
- [Photon Detectors](/home/documentation/sensitivity/photon_detectors)
- [Mirrors](/home/documentation/optical/mirrors)
