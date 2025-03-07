---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
# See https://github.com/jekyll/minima#readme

layout: default

description:  "{::nomarkdown} GEMC utilizes databases to dynamically create Geant4 
simulation objects. 
<br/>
Systems can be created without requiring code recompilation and without C++ or Geant4 knowledge,
<br/><br/>
<div style=\"text-align: center;\">
    <img src=\"assets/images/gemcArchitecture.png\" style=\"width: 80%;\" />
</div>
{:/}"

arc_caption: "Typical gemc usage: detectors are loaded from various databases sources.
Particles are transported through materials by Geant4, hits are collected and digitized, and output(s) are created."

api:  "Geant4 volumes are built using the python API.
An example geometry: a flux scintillator paddle collects hits from protons impinging on a liquid hydrogen target"
api_caption:  "The [above snippet](https://gist.github.com/maureeungaro/8e8616b388d65df0c8168a6b205f0c43) is 
the only code needed to build the geometry and record all tracks hitting the paddle."

variations: "<br/><br/><br/> A detector can be re-used in multiple experiments, 
with configuration changes such as components shifts, changes of materials, addition or removal of certain volumes.<br/><br/>
GEMC can manage these changes by using `variations`. This has the advantages:<br/>
{::nomarkdown}<li>Seamless organization of multiple versions of a detector</li>
<li>Easiness to select the desired configuration</li><br/>
In the YAML steering card the two variations of clas12CD are loaded by specifying the variation name: <br/><br/> 
<font size=\"4\"> { \"system\": \"clas12CD\", \"variation\": \"nominal\" } <br/>  { \"system\": \"clas12CD\", \"variation\": \"targetShift\" }</font>
{:/}"

var_caption: "In the above animation two variations of the CLAS12 Central Detector (*clas12CD*) are shown. 
The geometries are identical except for the position of the target. <br/>"

---

![gemcLogo]

<br/>

**GEMC** (**GE**ant **M**onte-**C**arlo) leverages databases to simulate,
using [Geant4](https://geant4.web.cern.ch), detector responses, including geometry, materials, optical elements, 
digitization, and measurements like particle fluxes and doses.
Key features include:<br/>

- ASCII, SQLite, GDML, CAD databases
- Python API
- Support for geometry variations and run numbers to adapt to different simulation setups
- Signal digitization tools, such as flux and dosimeter
- Plugin mechanisms to extend functionality, including custom event generators and digitization
- Emulation of hardware electronics
- Built-in ASCII and [ROOT](https://root.cern) output formats

<br/>

| Database and simulations |             
|--------------------------|
| {{ page.description }}   |
| *{{ page.arc_caption }}* |

<br/><br/>

| Python API        |                          |
|-------------------|--------------------------|
| ![gemcExamplePic] | ![gemcCodeExample]       |
| {{ page.api }}    | *{{ page.api_caption }}* |

<br/><br/>

| Geometry Variations      |                       |
|--------------------------|-----------------------|
| ![clas12v]               | {{ page.variations }} |
| *{{ page.var_caption }}* | {{ page.v6 }}         |

<br/><br/>


---

<br/>

Continuous Integration (CI) is used to test the code and ensure that the simulation is working as expected.

[![Almalinux Build](https://github.com/gemc/src/actions/workflows/build_gemc_almalinux.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/build_gemc_almalinux.yml)
[![Fedora Build](https://github.com/gemc/src/actions/workflows/build_gemc_fedora.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/build_gemc_fedora.yml)
[![Ubuntu Build](https://github.com/gemc/src/actions/workflows/build_gemc_ubuntu.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/build_gemc_ubuntu.yml)[![Doxygen](https://github.com/gemc/src/actions/workflows/doxygen.yaml/badge.svg)](https://github.com/gemc/src/actions/workflows/doxygen.yaml)
[![Sanitize](https://github.com/gemc/src/actions/workflows/sanitize.yaml/badge.svg)](https://github.com/gemc/src/actions/workflows/sanitize.yaml)
[![Nightly Dev Release](https://github.com/gemc/src/actions/workflows/dev_release.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/dev_release.yml)


[gemcCodeExample]: assets/images/pythonAPI.png

[gemcExamplePic]: assets/images/pythonAPIGeo.png

[clas12v]: assets/images/clas12v.gif

[gemcLogo]: assets/images/gemcLogo.png