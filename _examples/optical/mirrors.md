---
layout: default
title: "Mirrors"
---

# Mirrors Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

*Upcoming in the next release.*

This example showcases the GEMC optical surfaces ("mirrors"). Three identical 1 GeV electrons
cross a low-index gas radiator, each aimed at the center of one reflector plate. The Cherenkov
photons stay in a narrow forward cone around each electron and land on that electron's plate.
Each plate demonstrates a different mirror definition:

* %%polished_metal%% - `dielectric_metal` / `polished` / `unified` skin surface with an
  explicit reflectivity table: a typical metal-coated mirror;
* %%rough_metal%% - the same skin surface with a `ground` finish: the reflection goes into a
  specular lobe (%%specularlobe%% = 1) whose blur is set by %%sigmaAlpha%%;
* %%semi_transparent%% - a half-silvered mirror defined as a **border surface** between the
  radiator and its plate: 60% of the photons are reflected, 30% are transmitted through the
  plate (%%transmittance%%), and 10% are absorbed.

Each plate reflects its photons back onto its own upstream photon detector panel (using the
%%gPhotonDetector%% digitization and drawn in its mirror's color), so the panels see identical
conditions and only the reflection differs. A fourth panel counts the transmitted photons
after they cross a large gap behind the semi-transparent plate. Typical relative photon counts
(flat panel = 1):

| Panel | Surface | Relative count |
|---|---|---|
| flat (gold) | polished, R = 0.90 | 1.00 |
| rough (tomato) | specular lobe, sigmaAlpha = 0.03 | about 0.99 (blurred image, slight leak) |
| semi (blue) | reflected, R = 0.60 | about 0.69 (= 0.60 / 0.90) |
| behind (blue) | transmitted, T = 0.30 | about 0.37 (= 0.30 / 0.90) |

<br/>

## Quickstart

Copy the example to your current directory.
To create the geometry, run 10 events, and produce CSV output files:

```shell
cp -r $GEMC_HOME/examples/optical/mirrors .
cd mirrors
./mirrors.py
gemc mirrors.yaml -n=10
```

<br/>

## Geometry

The geometry is defined in `mirrors.py`. The world volume %%root%% contains a 1 m^3 gas radiator
(%%radiatorGas%%, a demonstration gas with refractive index about 1.001). Inside the radiator:

* three thin plates at mid-radiator: two aluminum plates carrying the skin mirrors, and the
  semi-transparent plate - made of radiator gas so that transmitted photons continue
  undisturbed - targeted by the %%semi_transparent%% border surface;
* three upstream photon detector panels, each aligned with one plate and drawn in its mirror's
  color, collecting the photons reflected by that plate;
* a long transmission gap behind the semi-transparent plate, filled with an optical vacuum
  (refractive index 1) so the electron radiates no Cherenkov light in the gap and the
  transmitted photons can be seen crossing it;
* a fourth panel at the end of the gap, collecting the transmitted photons.

Interactive viewer:

{% assign mirrors_vtk = "/assets/images/examples/mirrors/mirrors.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ mirrors_vtk }}"
  title="Interactive VTK.js view of the mirrors geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="assets/images/examples/mirrors/gemc_view.png"
caption="Mirrors simulation with 1 generated event."
%}

<br/>

## Mirror definitions

Each mirror is a `GMirror` published alongside the geometry:

```python
polished = GMirror("polished_metal")
polished.type = "dielectric_metal"
polished.finish = "polished"
polished.model = "unified"
polished.border = "SkinSurface"
polished.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV 6.0*eV"
polished.reflectivity = "0.90 0.90 0.89 0.88 0.87"
polished.publish(cfg)
```

and volumes reference them by name:

```python
plate.mirror = "polished_metal"
```

See the [Mirrors documentation](/home/documentation/optical/mirrors) for the complete field
reference.

<br/>

## Physics

The steering card enables optical physics:

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

Running the example prints the surfaces created by GEMC:

```text
G4World: created optical surface <mirrors/polished_metal> type <dielectric_metal>,
finish <polished>, model <unified>
G4World: created 3 optical surfaces, attached to 2 skin and 1 border logical surfaces
```


## Plotting with the GEMC Analyzer

Run GEMC with 10 events first. The default YAML file writes the analyzer CSV streams.

```shell
gemc mirrors.yaml -n=10
```

### Per-panel y vs x

The plots below split the optical-photon hit positions by %%panel%%. The back transmitted panel
is shown as its own plot, not merged into the semi-transparent reflected-panel plot. The count
shown on each image is the number of rows selected from the true-information stream.

| | |
|:---:|:---:|
| ![flat panel y vs x][mirrors-flat-panel-yvsx] | ![rough panel y vs x][mirrors-rough-panel-yvsx] |
| flat reflected panel<br>counts = 2,339 | rough reflected panel<br>counts = 2,347 |
| ![semi panel y vs x][mirrors-semi-panel-yvsx] | ![back panel y vs x][mirrors-back-panel-yvsx] |
| semi-transparent reflected panel<br>counts = 1,650 | back transmitted panel<br>counts = 877 |

[mirrors-flat-panel-yvsx]: /home/assets/images/examples/mirrors/flat_panel_y_vs_x.png
[mirrors-rough-panel-yvsx]: /home/assets/images/examples/mirrors/rough_panel_y_vs_x.png
[mirrors-semi-panel-yvsx]: /home/assets/images/examples/mirrors/semi_panel_y_vs_x.png
[mirrors-back-panel-yvsx]: /home/assets/images/examples/mirrors/back_panel_y_vs_x.png
