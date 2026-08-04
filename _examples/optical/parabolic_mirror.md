---
layout: default
title: "Parabolic Mirror"
---

# Parabolic Mirror Example
<hr style="height:4px;border:0;background:#4a90e2;">

This example builds a telescope-like optical mirror from two Geant4 `G4Paraboloid`
solids. A parallel bundle of optical photons enters an optical vacuum volume,
reflects from the inner surface of the mirror shell, and is collected by a small
%%gPhotonDetector%% panel near the nominal focus.

<br/>

## Quickstart

Copy the example to your current directory, create the geometry, and run one event:

```shell
cp -r $GEMC_HOME/examples/optical/parabolic_mirror .
cd parabolic_mirror
./parabolic_mirror.py
gemc parabolic_mirror.yaml -n=1
```

<br/>

## Geometry

The mirror is a thin boolean shell. The geometry script defines two construction
operands:

* %%outer_dish%% - the outside `G4Paraboloid`;
* %%inner_dish%% - a slightly smaller `G4Paraboloid` that defines the empty cavity.

Both operands are published with %%exist%% set to %%0%%. They are not placed as detector
volumes, but their solids remain available to the final boolean operation:

```python
mirror = GVolume("parabolic_dish")
mirror.mother = "optical_space"
mirror.solidsOpr = "outer_dish - inner_dish"
mirror.set_position(0, 0, mirror_z)
mirror.set_rotation(180, 0, 0)
mirror.material = "G4_Al"
mirror.mirror = "parabolic_reflector"
mirror.publish(cfg)
```

`G4Paraboloid` requires the radius at %%-dz%% to be smaller than the radius at
%%+dz%%. The final shell is rotated 180 degrees around x so the open side faces the
incoming photons.

Interactive viewer:

{% assign parabolic_mirror_vtk = "/assets/images/examples/parabolic_mirror/parabolic_mirror.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ parabolic_mirror_vtk }}"
  title="Interactive VTK.js view of the parabolic mirror geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="assets/images/examples/parabolic_mirror/gemc_view.png"
caption="Parabolic mirror simulation with 1 generated optical-photon event."
%}

<br/>

## Mirror Surface

The mirror coating is a `GMirror` skin surface attached to the final boolean shell:

```python
reflector = GMirror("parabolic_reflector")
reflector.type = "dielectric_metal"
reflector.finish = "polished"
reflector.model = "unified"
reflector.border = "SkinSurface"
reflector.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV 6.0*eV"
reflector.reflectivity = "0.95 0.95 0.95 0.95 0.95"
reflector.publish(cfg)
```

```python
mirror.mirror = "parabolic_reflector"
```

See the [Mirrors documentation](/home/documentation/optical/mirrors) for the mirror
surface fields.

<br/>

## Photon Detector

The detector is placed near the nominal focal point and uses %%gPhotonDetector%%:

```python
detector = GVolume("focus_detector")
detector.make_tube(0, 60, 1, 0, 360)
detector.set_position(0, 0, focus_z)
detector.material = "opticalVacuum"
detector.digitization = "gPhotonDetector"
detector.set_identifier("panel", 1)
detector.publish(cfg)
```

The steering card enables optical physics and launches optical photons into the
mirror aperture:

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics

gparticle:
  - name: opticalphoton
    multiplicity: 200
    p: 3*eV
    vz: -42*cm
    delta_vx: 17*cm
    delta_vy: 17*cm
```

Geant4 may warn that generated optical photons have zero polarization and assign a
random polarization. That warning is expected for this simple source.
