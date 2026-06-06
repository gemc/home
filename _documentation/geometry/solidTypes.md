---
layout: default
title: Native Geant4 Solid Types
description: Python builders for every supported Geant4 solid, with interactive 3-D previews
---

This page lists every supported Geant4 solid and its Python builder function.
The full Geant4 geometry guide is at the
[Geant4 User Guide](https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/Detector/Geometry/geomSolids.html).

Each solid is built inside a `GVolume` via one of the `make_*` methods described below.

---

<h2 id="G4Box">G4Box — Simple Box</h2>

```python
gvolume.make_box(dx, dy, dz, lunit='mm')
```

{% capture left_box %}
| Parameter | Description |
|-----------|-------------|
| `dx` | half-length in X |
| `dy` | half-length in Y |
| `dz` | half-length in Z |
| `lunit` | length unit (default: `mm`) |
{% endcapture %}

{% capture right_box %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aBox.jpg"
     alt="G4Box" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_box right_content=right_box %}

```python
gvolume.make_box(30, 20, 10)           # 30×20×10 mm half-lengths
gvolume.make_box(3, 2, 1, lunit='cm')  # same in cm
```

```shell
gemc-system-template -gv G4Box -gvp '30, 20, 10' -silent
```

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/documentation/solidTypes/G4Box.vtksz"
  title="Interactive 3-D view of G4Box"
  width="100%" height="400"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

---

<h2 id="G4Tubs">G4Tubs — Cylindrical Section or Tube</h2>

```python
gvolume.make_tube(rin, rout, length, phistart, phitotal, lunit1='mm', lunit2='deg')
```

{% capture left_tubs %}
| Parameter | Description |
|-----------|-------------|
| `rin` | inner radius |
| `rout` | outer radius |
| `length` | half-length in Z |
| `phistart` | starting φ angle |
| `phitotal` | total φ angle |
| `lunit1` | length unit (default: `mm`) |
| `lunit2` | angle unit (default: `deg`) |
{% endcapture %}

{% capture right_tubs %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTubs.jpg"
     alt="G4Tubs" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_tubs right_content=right_tubs %}

```python
gvolume.make_tube(10, 20, 30, 0, 360)    # full tube
gvolume.make_tube(0, 15, 25, 0, 270)     # three-quarter open cylinder
```

```shell
gemc-system-template -gv G4Tubs -gvp '10, 20, 30, 0, 360' -silent
```

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/documentation/solidTypes/G4Tubs.vtksz"
  title="Interactive 3-D view of G4Tubs"
  width="100%" height="400"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

---

<h2 id="G4Cons">G4Cons — Cone or Conical Section</h2>

```python
gvolume.make_cons(rin1, rout1, rin2, rout2, length, phi_start, phi_total,
                  lunit1='mm', lunit2='deg')
```

{% capture left_cons %}
| Parameter | Description |
|-----------|-------------|
| `rin1` | inner radius at −dz |
| `rout1` | outer radius at −dz |
| `rin2` | inner radius at +dz |
| `rout2` | outer radius at +dz |
| `length` | half-length in Z |
| `phi_start` | starting φ angle |
| `phi_total` | total φ angle |
{% endcapture %}

{% capture right_cons %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aCons.jpg"
     alt="G4Cons" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_cons right_content=right_cons %}

```python
gvolume.make_cons(5, 15, 15, 25, 30, 0, 270)   # hollow truncated cone, 270°
gvolume.make_cons(0, 10, 0, 20, 40, 0, 360)     # solid cone, full rotation
```

```shell
gemc-system-template -gv G4Cons -gvp '5, 15, 15, 25, 30, 0, 270' -silent
```

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/documentation/solidTypes/G4Cons.vtksz"
  title="Interactive 3-D view of G4Cons"
  width="100%" height="400"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

---

<h2 id="G4Trd">G4Trd — Trapezoid</h2>

```python
gvolume.make_trapezoid(dx1, dx2, dy1, dy2, z, lunit='mm')
```

{% capture left_trd %}
| Parameter | Description |
|-----------|-------------|
| `dx1` | half-length X at −dz |
| `dx2` | half-length X at +dz |
| `dy1` | half-length Y at −dz |
| `dy2` | half-length Y at +dz |
| `z` | half-length in Z |
| `lunit` | length unit (default: `mm`) |
{% endcapture %}

{% capture right_trd %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrd.jpg"
     alt="G4Trd" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_trd right_content=right_trd %}

```python
gvolume.make_trapezoid(20, 10, 15, 8, 25)
```

```shell
gemc-system-template -gv G4Trd -gvp '20, 10, 15, 8, 25' -silent
```

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/documentation/solidTypes/G4Trd.vtksz"
  title="Interactive 3-D view of G4Trd"
  width="100%" height="400"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

---

<h2 id="G4Trap">G4Trap — General Trapezoid</h2>

Three builder functions map to the three Geant4 G4Trap constructors.

### 11-parameter general trapezoid

```python
gvolume.make_general_trapezoid(pDz, pTheta, pPhi,
                                pDy1, pDx1, pDx2, pAlp1,
                                pDy2, pDx3, pDx4, pAlp2,
                                lunit1='mm', lunit2='deg')
```

{% capture left_trapg %}
| Parameter | Description |
|-----------|-------------|
| `pDz` | half-length in Z |
| `pTheta` | polar angle of axis joining face centres |
| `pPhi` | azimuthal angle of that axis |
| `pDy1` | half-length Y at −pDz |
| `pDx1` | half-length X at small Y of −pDz face |
| `pDx2` | half-length X at large Y of −pDz face |
| `pAlp1` | tilt of −pDz face from Y axis |
| `pDy2` | half-length Y at +pDz |
| `pDx3` | half-length X at small Y of +pDz face |
| `pDx4` | half-length X at large Y of +pDz face |
| `pAlp2` | tilt of +pDz face from Y axis |
{% endcapture %}

{% capture right_trapg %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/wTrap.jpg"
     alt="G4Trap general" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_trapg right_content=right_trapg %}

```python
gvolume.make_general_trapezoid(25, 5, 10, 12, 15, 10, 8, 10, 12, 8, 5)
```

```shell
gemc-system-template -gv G4TrapG -gvp '25, 5, 10, 12, 15, 10, 8, 10, 12, 8, 5' -silent
```

### 4-parameter right-angular wedge

```python
gvolume.make_trap_from_right_angular_wedges(pz, py, px, pltx, unit='mm')
```

{% capture left_trapraw %}
| Parameter | Description |
|-----------|-------------|
| `pz` | length along Z |
| `py` | length along Y |
| `px` | length along X at the wider side |
| `pltx` | length along X at the narrower side (`pltx` ≤ `px`) |
| `unit` | length unit (default: `mm`) |
{% endcapture %}

{% capture right_trapraw %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrap.jpg"
     alt="G4Trap right-angular wedge" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_trapraw right_content=right_trapraw %}

```shell
gemc-system-template -gv G4TrapRAW -gvp '30, 40, 50, 20' -silent
```

### 8-vertex form (24 parameters)

```python
gvolume.make_trap_from_vertices(v1x, v1y, v1z, v2x, v2y, v2z,
                                 v3x, v3y, v3z, v4x, v4y, v4z,
                                 v5x, v5y, v5z, v6x, v6y, v6z,
                                 v7x, v7y, v7z, v8x, v8y, v8z, lunit1='mm')
```

{% capture left_trap8 %}
| Vertices | Description |
|----------|-------------|
| `v1, v2` | edge at small Y of −z face |
| `v3, v4` | edge at large Y of −z face |
| `v5, v6` | edge at small Y of +z face |
| `v7, v8` | edge at large Y of +z face |
{% endcapture %}

{% capture right_trap8 %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aTrap.jpg"
     alt="G4Trap 8-vertex" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_trap8 right_content=right_trap8 %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/documentation/solidTypes/G4Trap.vtksz"
  title="Interactive 3-D view of G4Trap"
  width="100%" height="400"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

---

<h2 id="G4Sphere">G4Sphere — Sphere or Spherical Shell Section</h2>

```python
gvolume.make_sphere(rmin, rmax, sphi, dphi, stheta, dtheta,
                    lunit1='mm', lunit2='deg')
```

{% capture left_sphere %}
| Parameter | Description |
|-----------|-------------|
| `rmin` | inner radius |
| `rmax` | outer radius |
| `sphi` | starting φ angle |
| `dphi` | delta φ angle |
| `stheta` | starting θ angle |
| `dtheta` | delta θ angle |
{% endcapture %}

{% capture right_sphere %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aSphere.jpg"
     alt="G4Sphere" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_sphere right_content=right_sphere %}

```python
gvolume.make_sphere(10, 20, 0, 270, 10, 120)   # partial shell
gvolume.make_sphere(0, 15, 0, 360, 0, 180)     # full solid sphere
```

```shell
gemc-system-template -gv G4Sphere -gvp '10, 20, 0, 270, 10, 120' -silent
```

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/documentation/solidTypes/G4Sphere.vtksz"
  title="Interactive 3-D view of G4Sphere"
  width="100%" height="400"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

---

<h2 id="G4Polycone">G4Polycone — Polycone</h2>

```python
gvolume.make_polycone(phiStart, phiTotal, zplane, iradius, oradius,
                      lunit1='mm', lunit2='deg')
```

{% capture left_pcone %}
| Parameter | Description |
|-----------|-------------|
| `phiStart` | starting φ angle |
| `phiTotal` | total φ angle |
| `zplane` | list of Z coordinates of cross-section planes |
| `iradius` | list of inner radii at each Z plane |
| `oradius` | list of outer radii at each Z plane |
{% endcapture %}

{% capture right_pcone %}
<img src="https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/_images/aBREPSolidPCone.jpg"
     alt="G4Polycone" style="max-width:100%; max-height:220px; object-fit:contain;" />
{% endcapture %}

{% include two_col_md.html left="1fr" right="220px" left_content=left_pcone right_content=right_pcone %}

```python
zplane  = [-30, -10,  10,  30]
iradius = [  0,  10,  10,   0]
oradius = [ 15,  20,  20,  15]
gvolume.make_polycone(0, 360, zplane, iradius, oradius)
```

```shell
gemc-system-template -gv G4Polycone -gvp '0, 360, -30, -10, 10, 30, 0, 10, 10, 0, 15, 20, 20, 15' -silent
```

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/documentation/solidTypes/G4Polycone.vtksz"
  title="Interactive 3-D view of G4Polycone"
  width="100%" height="400"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>
